# SHP2小分子抑制剂筛选

----

## 环境
* python 3.12.9 
* DeepPurpose>=0.1.5 
* biopython>=1.85 
* numpy>=2.2.3 
* pandas>=2.2.3 
* openpyxl>=3.1.5

----

## 项目结构
- database
  - models
    - model_MPNN_CNN
    - model_mpnn_cnn_davis
- shp2_smi
  - DP.py
- environment.yml
- README.md
- requirements.txt

----

## conda环境创建
```bash
conda create -n smi python=3.12.9
```
```bash
conda activate smi
```

----

## 安装
### conda 安装
```bash
conda install -c conda-forge DeepPurpose==0.0.5 descriptastorus==2.7.0 pandas-flavor==0.6.0 biopython==1.85 numpy==2.2.3 pandas==2.2.3 openpyxl==3.1.5 -y
```
- 或者通过 environment.yml安装
```bash
conda env update -f environment.yml
```
### pip 安装
```bash
pip install DeepPurpose==0.1.5 descriptastorus==2.7.0 pandas-flavor==0.6.0 biopython==1.85 numpy==2.2.3 pandas==2.2.3 openpyxl==3.1.5
```
- 或者通过requirements.txt安装
```bash
pip install -r requirements.txt
```

----

## 运行
```bash
python shp2_smi/DP.py
```

