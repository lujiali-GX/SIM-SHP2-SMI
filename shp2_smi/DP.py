import os
from pathlib import Path

import pandas as pd
from DeepPurpose import DTI, utils
from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1

DRUG_ENCODING = 'MPNN'
TARGET_ENCODING = 'CNN'
CURRENT_DIR = os.getcwd()

def read_model():
    """读取药物-靶标亲和力预测模型
    """
    # model = DTI.model_pretrained(model='MPNN_CNN_BindingDB')
    # model =  DTI.model_pretrained(model = 'MPNN_CNN_DAVIS')
    Model = DTI.model_pretrained(path_dir=os.path.join(CURRENT_DIR, 'database/models/model_MPNN_CNN'))
    # Model = DTI.model_pretrained(path_dir=os.path.join(CURRENT_DIR, 'database/models/model_mpnn_cnn_davis'))
    return Model


def get_pdb_seq(pdb_file: str):
    """获取蛋白质PDB文件的sequence序列

    :param pdb_file: 蛋白质PDB文件

    :return: sequence序列
    """
    # 创建PDB解析器
    parser = PDBParser()
    pdb_id = os.path.splitext(os.path.basename(pdb_file))[0]
    # 解析PDB文件
    structure = parser.get_structure(pdb_id, pdb_file)

    # 提取氨基酸序列
    amino_acids = []
    for mod in structure:
        for chain in mod:
            for residue in chain:
                # 检查是否为标准氨基酸残基
                if residue.get_id()[0] == ' ':
                    amino_acids.append(residue.get_resname())

    # 将三字母代码转换为单字母代码
    return ''.join(seq1(aa) for aa in amino_acids)


def set_df(drugId_list, drug_list, target_list, label_list):
    """设置输入数据表格

    :param drugId_list: 药物唯一标识符列表
    :param drug_list: 药物列表
    :param target_list: 靶标列表
    :param label_list: 标签列表

    :return: DataFrame
    """

    # 创建DataFrame
    drug_df = pd.DataFrame({'SMILES': drug_list}, columns=['SMILES'])
    target_df = pd.DataFrame({'Target Sequence': target_list}, columns=['Target Sequence'])

    # 编码药物
    drug = utils.encode_drug(drug_df, DRUG_ENCODING)
    # print("drug:", drug)
    # 编码靶标蛋白
    target = utils.encode_protein(target_df, TARGET_ENCODING)

    df_data = pd.DataFrame(
        {
            "ID": drugId_list,
            'SMILES': drug["SMILES"],
            'drug_encoding': drug["drug_encoding"],
            'Target Sequence': target["Target Sequence"],
            'target_encoding': target["target_encoding"],
            'Label': label_list
        },
        columns=[
            "ID",
            'SMILES',
            'drug_encoding',
            'Target Sequence',
            'target_encoding',
            'Label'
        ])

    return df_data



if __name__ == '__main__':
    targetFile = os.path.join(CURRENT_DIR, "database/2shp.pdb")
    drugFile = os.path.join(CURRENT_DIR, "database/ASD_Release_201909_DR.txt")

    targetSeq = get_pdb_seq(targetFile)
    """靶标sequence序列"""
    drugDataframe = pd.read_csv(drugFile, sep='\t')
    """药物数据表"""
    model = read_model()
    """药物-靶标亲和力预测模型"""

    # =================== DRUG数据预处理 =============================
    # 去除SMILES为空的行
    drugDataframe = drugDataframe.dropna(subset=['tr_smiles'])
    # =================== DRUG数据预处理 =============================

    drugIdList = drugDataframe["drug_serial"].tolist()
    # 获取SMILES列表
    drugList = drugDataframe["tr_smiles"].tolist()
    # 获取靶标PDB序列
    targetList = [targetSeq] * len(drugList)
    # 获取标签列表
    labelList = [0] * len(drugList)

    # 设置输入数据表格
    dfData = set_df(drugIdList, drugList, targetList, labelList)

    # 使用模型预测
    pred = model.predict(df_data=dfData)
    print(f"预测亲和力值 (pKd):")
    # print(df_data.keys())
    for index, row in dfData.iterrows():
        print("{}: {}".format(row['ID'], pred[index]))

    print("len(drugDataframe) = {}".format(len(drugDataframe)))
    print("len(dfData) = {}".format(len(dfData)))

    drugDataframe["pKd"] = pred
    drugDataframe.to_excel(os.path.join(CURRENT_DIR, "database/预测结果.xlsx"), index=False, engine="openpyxl")
