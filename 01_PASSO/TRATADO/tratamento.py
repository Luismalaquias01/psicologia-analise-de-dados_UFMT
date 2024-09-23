import pandas as pd

# Função para garantir que o arquivo seja lido corretamente
def carregar_arquivo(filepath):
    try:
        # Carregar o arquivo CSV
        df = pd.read_csv(filepath, delimiter=',', encoding='utf-8', engine='python')
        print(f"Arquivo '{filepath}' carregado com sucesso. Total de linhas: {len(df)}")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{filepath}': {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Função para remover duplicatas de emails
def remover_duplicados_email(df, email_column):
    if email_column in df.columns:
        # Remover duplicatas com base na coluna de email, mantendo apenas a primeira ocorrência
        df_sem_duplicatas = df.drop_duplicates(subset=[email_column], keep='first')
        print(f"Total de linhas após remoção de duplicatas: {len(df_sem_duplicatas)}")
        return df_sem_duplicatas
    else:
        print(f"Coluna '{email_column}' não encontrada no arquivo. Nenhuma duplicata foi removida.")
        return df

# Função para sobrescrever o arquivo CSV com os dados sem duplicatas
def salvar_csv(df, filepath):
    df.to_csv(filepath, index=False)
    print(f"Arquivo '{filepath}' atualizado com sucesso (duplicatas removidas).")

# Lista de arquivos a serem processados
arquivos = ['Banco_de_dados_aceitaram.csv', 
            'Banco_de_dados_nao_aceitaram.csv', 
            'Banco_de_dados_nao_responderam.csv', 
            'Banco_de_dados_responderam_sem_estar_no_cadastro.csv']

# Nome da coluna de email
email_column = 'Endereço de Email'  # Substitua pelo nome exato da coluna de email nos arquivos

# Processar cada arquivo da lista
for arquivo in arquivos:
    print(f"Processando o arquivo: {arquivo}")
    
    # Carregar o arquivo CSV
    dados_df = carregar_arquivo(arquivo)
    
    # Remover duplicatas de emails, se a coluna existir
    dados_sem_duplicatas = remover_duplicados_email(dados_df, email_column)
    
    # Sobrescrever o arquivo original com os dados sem duplicatas
    salvar_csv(dados_sem_duplicatas, arquivo)

print("Todos os arquivos foram processados.")
