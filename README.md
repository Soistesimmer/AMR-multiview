# Multi-View Autoencoding Losses

### Data Processing

  - AMRdata-origin 是原数据处理文件
  - AMRdata-multiview 是改动后的文件


使用方法:
  - 设置 preprocess.py 中standford Corenlp的路径
  - 设置 preprocess.sh 中json文件（和原数据集文件）路径
  - 运行 preprocess.sh

### Training
    
- o2valk有baseline, biaffine, reconstructor, combine四个模型

使用方法：
  - 设置 preprocess.sh, train.sh, translate.sh 中的文件路径
  - 运行 preprocess.sh
  - 运行 train.sh
  - 运行 translate.sh
  - 结果默认在对应模型 workplace 目录下
