from employer import Employer
import pandas as pd
import re

def read_file_txt(file_path):
    employers = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            #verifico os espaços em branco, pois um employer comeca com 7 espacos em branco
            if line.startswith('       ') and not line.startswith('         '):  
                register = line[7:13].strip()
                name = line[17:48].strip()
                employer = Employer(register, name)
                employers.append(employer)
    return employers

def compare_with_csv(employers, csv_path):
    df = pd.read_csv(csv_path)

    # faço um dicionário onde a chave é register e o valor é o name
    employers_dict = {employer.register: employer.name for employer in employers}

    for i, row in df.iterrows():
        # vou remover a pontuação do register para comparar com o dicionário, mas sem alterar o csv
        register = re.sub(r'\D', '', str(row.iloc[0]))  

        if register in employers_dict:
            print(f'Register: {row.iloc[0]}, Found in CSV: True')
            # add o name do employer no df do csv
            df.at[i, 'NOME'] = employers_dict[register]
        else:
            print(f'Register: {row.iloc[0]}, Found in CSV: False')

    # salvo no csv os dados atualizados
    df.to_csv(csv_path, index=False)

def main():
    file_txt_path = 'files/Fm202308.TXT'
    employers = read_file_txt(file_txt_path)
    
    csv_path = 'files/temposcontribuicao-data_2023-09-22.csv'
    compare_with_csv(employers, csv_path)
    
if __name__ == "__main__":
    main()