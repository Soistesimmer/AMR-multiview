# Multi-View Autoencoding Losses

This repository contains the code for our paper ["Structural Information Preserving for Graph-to-Text Generation"](https://)

The code is developed under Pytorch 1.0 Due to the compitibility reason of Pytorch, it may not be loaded by some lower version (such as 0.4.0).

## Data preprocessing 
The codes of data preprocessing could be found in folder [AMRdata-multiview](https://github.com/Soistesimmer/work-code-20190910/tree/master/AMRdata-multiview). Modify the PATH within [preprocess.sh](https://github.com/Soistesimmer/work-code-20190910/blob/master/AMRdata-multiview/preprocess.sh) and run ```sh preprocess.sh```

For every model, you need to run the preprocess.sh under its dir using the files generated above. Remember modifying the PATH first.

### Baseline 

Our baseline uses one of methods proposed by [Zhu et al.](https://github.com/Amazing-J/structural-transformer) named Feature-based. We follows the data preprocessing of (Zhu et al.) where concept sequences, label sequences and references are extracted from dataset. You could get more detailed descriptions from [README.md](https://github.com/Amazing-J/structural-transformer/blob/master/README.md) of their work.

### View 1: Triples Relations

For AMR-to-Text, We use node-to-word alignments dataset produced by the ISI aligner (Pourdamghani et al.).
```
# ::id bolt12_07_4800.1 ::amr-annotator SDL-AMR-09 ::preferred
# ::tok Establishing Models in Industrial Innovation
# ::alignments 0-1 1-1.1 2-1.1.1.r 3-1.1.1.1 4-1.1.1
(e / establish-01~e.0 
      :ARG1 (m / model~e.1 
            :mod~e.2 (i / innovate-01~e.4 
                  :ARG1 (i2 / industry~e.3))))
```
Take node 'model~e.1' as an example. It means this node is correspond with the word 'Models'(at position 1 if start from 0) in tok. Notice that we use toks as references in all experiments.

### View 2: Linearized Graphs

We use the depth-first traversal strategy as in [Konstas et al.](https://github.com/sinantie/NeuralAmr) to linearize AMR graphs to obtain reconstructed AMRs. We also try other methods, such as concept sequences same as the encoder inputs, and random graph linearization, where the order for picking children is random rather than following the left-to-right order at each stage of the depth-ﬁrst traversal procedure.


## Training 

First, modify the PATH within "train.sh". "data_prefix" is the preprocessing directory generated above. Note the prefix gq. For example "./workspace/data/gq". Finally, execute the corresponding script file, such as ```sh train.sh```.
> thanks to [@xdqkid](https://github.com/xdqkid), the [issue](https://github.com/Soistesimmer/AMR-multiview/issues/1) is corrected in [reconstructor_v2](https://github.com/Soistesimmer/AMR-multiview/tree/master/model/reconstructor_v2) directory. The mistake influences the hyperparameter β of view 2. According to the additional experiments below, 0.4 is best choice because linearized graph is always longer than the target sentence.

|0.3|  0.35   | 0.4  | 0.45 | 0.5 |
|  :----:  | :----:  |:---:|  :----:  | :----:  |
| 30.84  | 31.06 | 31.50 | 31.39 | 30.93 |

## Decoding 

You should change the PATH in the "translate.sh" accordingly, and then execute ```bash translate.sh```. 
