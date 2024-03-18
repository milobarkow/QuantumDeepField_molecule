import pandas as pd
import numpy as np
import shutil

def combine_smiles(file_paths):
    dic = {}
    for file in file_paths:
        with open(file) as f:
            for line in f:
                code, smile = line.strip().split('\t')
                n = int(code[code.rfind('_') + 1:])
                dic[code] = {'n' : n, 'smile' : smile }

    return dic

def get_new_data(path='DataEcoDF_RER_wMidpoints.xlsx'):
    df = pd.read_excel(path)
    return df

def get_val_from_code(code, smiles_key, excell_data):
    h1 = 'Climate Change (kg CO2-eq)'
    h2 = 'Ecosystem Quality (PDF*m2*yr)'
    h3 = 'Human Health (DALY)'
    h4 = 'Resources (MJ primary)'
    headers = [h1, h2, h3, h4]
    smile = smiles_key[code]['smile']
    ret = []
    if smile in list(excell_data['SMILES']):
        for header in headers:
            val = str(excell_data[excell_data['SMILES'] == smile][header].values)
            val = val.replace('[', '').replace(']', '')
            ret.append(val)
    return ret

def replace_data(path_to_copy, name):
    with open(f'{path_to_copy}/{name}') as f:
        chunks = [x for x in f.readlines()]

    good_chunk = False
    chunk = []
    with open(name, 'w') as f:
        code = ''
        for i, line in enumerate(chunks):
            if line[0] == 'd':
                code = line.strip()
                good_chunk = smiles_key[code]['smile'] in list(excell_data['SMILES'])
                if good_chunk:
                    chunk.append(line)
            elif line[0] == '-' and good_chunk:
                new_val = get_val_from_code(code, smiles_key, excell_data) 
                if (len(new_val) > 0 and 'nan' not in new_val):
                    chunk.append(' '.join(new_val) + '\n')
                    for l in chunk:
                        f.write(l)
                    chunk.clear()
            elif good_chunk:
                chunk.append(line)

if __name__ == '__main__':
    smiles_key = combine_smiles()
    excell_data = get_new_data()

    copy_from = '../QM9under14atoms_atomizationenergy_eV'

    replace_data(copy_from, 'test.txt')
    replace_data(copy_from, 'train.txt')
    replace_data(copy_from, 'val.txt')





