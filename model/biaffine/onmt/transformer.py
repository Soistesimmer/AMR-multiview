"""
This file is for models creation, which consults options
and creates each encoder and decoder accordingly.
"""
import math
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.init import xavier_uniform_

import onmt.constants as Constants

from onmt.transformer_encoder import TransformerEncoder
from onmt.transformer_decoder import TransformerDecoder

from onmt.embeddings import Embeddings
from utils.misc import use_gpu
from utils.logging import logger
from inputters.dataset import load_fields_from_vocab


class NMTModel(nn.Module):
    def __init__(self, encoder, decoder, biaffine):
        super(NMTModel, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.biaffine = biaffine

    def forward(self, src, tgt, structure, mask, lengths):
        tgt = tgt[:-1]  # exclude last target from inputs
        _, memory_bank, lengths = self.encoder(src, structure, lengths)  # src: ......<EOS>
        self.decoder.init_state(src, memory_bank)
        dec_out, attns = self.decoder(tgt)
        if mask is not None:
            bi_out, label_out = self.biaffine(dec_out[1:], mask)
            return dec_out, attns, bi_out, label_out
        return dec_out, attns


class Biaffine(nn.Module):
    def __init__(self, in_size, dropout, out_size):
        super(Biaffine, self).__init__()
        self.in_size=in_size
        self.out_size=out_size
        self.head_mlp = nn.Sequential(nn.Linear(in_size, in_size), nn.Dropout(dropout), nn.ReLU(),
                                      nn.Linear(in_size, in_size))
        self.dep_mlp = nn.Sequential(nn.Linear(in_size, in_size), nn.Dropout(dropout), nn.ReLU(),
                                     nn.Linear(in_size, in_size))
        self.label_head_mlp = nn.Sequential(nn.Linear(in_size, in_size), nn.Dropout(dropout), nn.ReLU(),
                                            nn.Linear(in_size, in_size))
        self.label_dep_mlp = nn.Sequential(nn.Linear(in_size, in_size), nn.Dropout(dropout), nn.ReLU(),
                                           nn.Linear(in_size, in_size))
        self.U = nn.Parameter(torch.Tensor(in_size, in_size))
        self.W = nn.Parameter(torch.Tensor(2 * in_size))
        self.b = nn.Parameter(torch.Tensor(1))

        self.label_U = nn.Parameter(torch.Tensor(out_size, in_size, in_size))
        self.label_W_1 = nn.Parameter(torch.Tensor(in_size, out_size))
        self.label_W_2 = nn.Parameter(torch.Tensor(in_size, out_size))
        self.label_b = nn.Parameter(torch.Tensor(out_size))

        self.reset_parameters()
        self.gen_func = nn.LogSoftmax(dim=-1)

    def reset_parameters(self):
        bound = 1 / math.sqrt(self.in_size*2)
        nn.init.uniform_(self.W, -bound, bound)
        nn.init.constant_(self.b, 0.)
        nn.init.xavier_uniform_(self.U)
        nn.init.xavier_uniform_(self.label_W_1)
        nn.init.xavier_uniform_(self.label_W_2)
        nn.init.xavier_uniform_(self.label_U)
        nn.init.constant_(self.label_b, 0.)

    def bilinear_(self, head, dep):
        out=torch.zeros([head.size(0),head.size(1),head.size(1),self.out_size]).cuda()
        for k in range(self.label_U.shape[0]):
            x=torch.matmul(head,self.label_U[k])
            x=torch.matmul(x,dep.transpose(1,2))
            out[:,:,:,k]=x
        return out

    def linear_(self, head, dep):
        out=torch.zeros([head.size(1),head.size(0),head.size(1),self.out_size]).cuda()
        x=torch.matmul(head, self.label_W_1)
        y = torch.matmul(dep, self.label_W_2)
        batch_size = x.size(0)
        x=x.transpose(0,1)
        for k in range(x.size(0)):
            out[k]=x[k].view(batch_size,1,self.out_size)+y
        out=out.transpose(0,1)
        return out

    def forward(self, input, mask):
        input = input.transpose(0, 1)
        batch_size=input.size(0)
        seq_len=input.size(1)
        o_head = self.head_mlp(input)
        o_dep = self.dep_mlp(input)
        out = torch.matmul(o_head, self.U)
        out = torch.matmul(out, o_dep.transpose(1, 2))
        out_ = torch.matmul((torch.cat((o_head, o_dep), 2)), self.W).unsqueeze(2)
        out = out + out_ + self.b
        # out = F.log_softmax(out, 2)
        out = F.log_softmax(out, 2)
        out=out.view(batch_size,seq_len,seq_len,1)

        l_head = self.label_head_mlp(input)
        l_dep = self.label_dep_mlp(input)
        l_out = self.bilinear_(l_head, l_dep)
        l_out = l_out + self.linear_(l_head, l_dep)
        # l_out = torch.matmul(l_head, self.label_U)
        # l_out = torch.matmul(l_out, l_dep.transpose(1, 2))
        # l_out_ = torch.matmul((torch.cat((l_head, l_dep), 2)), self.label_W).unsqueeze(2)
        # l_out = l_out + l_out_ + self.label_b
        # l_out = torch.masked_select(l_out.reshape(batch_size, -1), mask.reshape(batch_size,-1))

        out=out[mask]
        out=out.sum()
        l_out = l_out[mask]
        l_out=self.gen_func(l_out)
        # tmp = mask.sum(2)
        # out = out.masked_fill(1 - mask, value=torch.tensor(0.))
        # out = out.sum(2)
        # count = tmp[tmp > 0].size(0)
        # tmp[tmp>0]=1
        # tmp=tmp.byte()
        # out=out.masked_select(tmp)
        # out=torch.log(out)
        # out = out.sum() / count
        # l_out = l_out.reshape(-1,self.out_size)
        # tmp=tmp.reshape(-1)
        # l_out=l_out[tmp,:]
        # l_out = self.gen_func(l_out)
        return out, l_out


def build_embeddings(opt, word_dict, for_encoder='src'):
    """
    Build an Embeddings instance.
    Args:
        opt: the option in current environment.
        word_dict(Vocab): words dictionary.
        feature_dicts([Vocab], optional): a list of feature dictionary.
        for_encoder(bool): build Embeddings for encoder or decoder?
    """
    if for_encoder == 'src':
        embedding_dim = opt.src_word_vec_size  # 512
    elif for_encoder == 'tgt':
        embedding_dim = opt.tgt_word_vec_size
    elif for_encoder == 'structure':
        embedding_dim = 64

    word_padding_idx = word_dict.stoi[Constants.PAD_WORD]
    num_word_embeddings = len(word_dict)

    if for_encoder == 'src' or for_encoder == 'tgt':

        return Embeddings(word_vec_size=embedding_dim,
                          position_encoding=opt.position_encoding,
                          dropout=opt.dropout,
                          word_padding_idx=word_padding_idx,
                          word_vocab_size=num_word_embeddings,
                          sparse=opt.optim == "sparseadam")
    elif for_encoder == 'structure':
        return Embeddings(word_vec_size=embedding_dim,
                          position_encoding=False,
                          dropout=opt.dropout,
                          word_padding_idx=word_padding_idx,
                          word_vocab_size=num_word_embeddings,
                          sparse=opt.optim == "sparseadam")


def build_encoder(opt, embeddings, structure_embeddings):
    """
    Various encoder dispatcher function.
    Args:
        opt: the option in current environment.
        embeddings (Embeddings): vocab embeddings for this encoder.
    """
    return TransformerEncoder(opt.enc_layers, opt.enc_rnn_size, opt.heads, opt.transformer_ff, opt.dropout, embeddings,
                              structure_embeddings)


def build_decoder(opt, embeddings):
    """
    Various decoder dispatcher function.
    Args:
        opt: the option in current environment.
        embeddings (Embeddings): vocab embeddings for this decoder.
    """
    return TransformerDecoder(opt.dec_layers, opt.dec_rnn_size, opt.heads, opt.transformer_ff, opt.dropout, embeddings)


def build_biaffine(opt, fields):
    return Biaffine(opt.dec_rnn_size, opt.dropout, len(fields["relation"].vocab))


def load_test_model(opt, dummy_opt, model_path=None):
    if model_path is None:
        model_path = opt.models[0]
    checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)

    fields = load_fields_from_vocab(checkpoint['vocab'])

    model_opt = checkpoint['opt']

    for arg in dummy_opt:
        if arg not in model_opt:
            model_opt.__dict__[arg] = dummy_opt[arg]
    model = build_base_model(model_opt, fields, use_gpu(opt), checkpoint)

    model.eval()
    model.generator.eval()
    return fields, model


def build_base_model(model_opt, fields, gpu, checkpoint=None):
    """
    Args:
        model_opt: the option loaded from checkpoint.
        fields: `Field` objects for the model.
        gpu(bool): whether to use gpu.
        checkpoint: the model gnerated by train phase, or a resumed snapshot
                    model from a stopped training.
    Returns:
        the NMTModel.
    """

    # for backward compatibility
    if model_opt.enc_rnn_size != model_opt.dec_rnn_size:
        raise AssertionError("""We do not support different encoder and
                         decoder rnn sizes for translation now.""")

    # Bulid_structure
    structure_dict = fields["structure"].vocab
    structure_embeddings = build_embeddings(model_opt, structure_dict, for_encoder='structure')

    # Build encoder.
    src_dict = fields["src"].vocab
    src_embeddings = build_embeddings(model_opt, src_dict, for_encoder='src')
    encoder = build_encoder(model_opt, src_embeddings, structure_embeddings)

    # Build decoder.
    tgt_dict = fields["tgt"].vocab
    tgt_embeddings = build_embeddings(model_opt, tgt_dict, for_encoder='tgt')

    # Share the embedding matrix - preprocess with share_vocab required.
    if model_opt.share_embeddings:
        # src/tgt vocab should be the same if `-share_vocab` is specified.
        if src_dict != tgt_dict:
            raise AssertionError('The `-share_vocab` should be set during '
                                 'preprocess if you use share_embeddings!')

        tgt_embeddings.word_lut.weight = src_embeddings.word_lut.weight
    # Build decoder.
    decoder = build_decoder(model_opt, tgt_embeddings)

    biaffine = build_biaffine(model_opt, fields)

    # Build NMTModel(= encoder + decoder).
    device = torch.device("cuda:0" if gpu else "cpu")
    model = NMTModel(encoder, decoder, biaffine)

    # Build Generator.
    gen_func = nn.LogSoftmax(dim=-1)
    generator = nn.Sequential(
        nn.Linear(model_opt.dec_rnn_size, len(fields["tgt"].vocab)),
        gen_func
    )
    if model_opt.share_decoder_embeddings:
        generator[0].weight = decoder.embeddings.word_lut.weight

    # Load the model states from checkpoint or initialize them.
    if checkpoint is not None:
        # This preserves backward-compat for models using customed layernorm
        def fix_key(s):
            s = re.sub(r'(.*)\.layer_norm((_\d+)?)\.b_2',
                       r'\1.layer_norm\2.bias', s)
            s = re.sub(r'(.*)\.layer_norm((_\d+)?)\.a_2',
                       r'\1.layer_norm\2.weight', s)
            return s

        checkpoint['model'] = \
            {fix_key(k): v for (k, v) in checkpoint['model'].items()}
        # end of patch for backward compatibility

        model.load_state_dict(checkpoint['model'], strict=False)
        generator.load_state_dict(checkpoint['generator'], strict=False)
    else:
        if model_opt.param_init != 0.0:
            for p in model.parameters():
                p.data.uniform_(-model_opt.param_init, model_opt.param_init)
            for p in generator.parameters():
                p.data.uniform_(-model_opt.param_init, model_opt.param_init)
            # for p in biaffine.generator.parameters():
            #     p.data.uniform_(-model_opt.param_init, model_opt.param_init)
        if model_opt.param_init_glorot:
            for p in model.parameters():
                if p.dim() > 1:
                    xavier_uniform_(p)
            for p in generator.parameters():
                if p.dim() > 1:
                    xavier_uniform_(p)
            # for p in biaffine.generator.parameters():
            #     if p.dim() > 1:
            #         xavier_uniform_(p)

        if hasattr(model.encoder, 'embeddings'):
            model.encoder.embeddings.load_pretrained_vectors(
                model_opt.pre_word_vecs_enc, model_opt.fix_word_vecs_enc)
        if hasattr(model.decoder, 'embeddings'):
            model.decoder.embeddings.load_pretrained_vectors(
                model_opt.pre_word_vecs_dec, model_opt.fix_word_vecs_dec)
    # pdb.set_trace()
    # Add generator to model (this registers it as parameter of model).
    model.generator = generator
    model.to(device)

    return model


def build_model(model_opt, opt, fields, checkpoint):
    """ Build the Model """
    logger.info('Building model...')
    model = build_base_model(model_opt, fields,
                             use_gpu(opt), checkpoint)
    logger.info(model)
    return model
