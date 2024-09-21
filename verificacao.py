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

# Carregar os arquivos CSV
cadastro_df = carregar_arquivo('Novo_cadastro.csv')
pesquisa_df = carregar_arquivo('Formulario_pesquisa.csv')

# Verificar se os arquivos foram carregados corretamente e têm dados
if cadastro_df.empty:
    print("Erro: O arquivo de novo cadastro não foi carregado corretamente.")
    exit()
if pesquisa_df.empty:
    print("Erro: O arquivo de formulário não foi carregado corretamente.")
    exit()

# Limpar os emails: Remover espaços e converter para minúsculas
cadastro_df['Endereço de Email'] = cadastro_df['Endereço de Email'].str.strip().str.lower()
pesquisa_df['e-mail'] = pesquisa_df['e-mail'].str.strip().str.lower()

# Verificar se nome + email são duplicados no novo cadastro
duplicados_nome_email = cadastro_df[cadastro_df.duplicated(subset=['Nome', 'Endereço de Email'], keep=False)]
print(f"Total de duplicatas (nome + email) no novo cadastro: {len(duplicados_nome_email)}")

# Remover duplicatas com base em nome + email
cadastro_df_limpo = cadastro_df.drop_duplicates(subset=['Nome', 'Endereço de Email'], keep='first')
print(f"Total de pessoas no cadastro após remoção de duplicatas (nome + email): {len(cadastro_df_limpo)}")

# Fazer o merge (join) dos dados de acordo com o email, mantendo todas as pessoas do cadastro
merged_df = pd.merge(cadastro_df_limpo, pesquisa_df, left_on='Endereço de Email', right_on='e-mail', how='left')

# Criar a coluna "Aceite" para verificar se a pessoa aceitou participar, preencher com 'Não respondeu' onde estiver faltando
merged_df['Aceite'] = merged_df['Tendo em vista as informações apresentadas acima, eu: '].fillna('Não respondeu')

# 1. **Aceitaram**: Pessoas que aceitaram participar da pesquisa
aceitaram_df = merged_df[merged_df['Aceite'] == 'Aceito participar da pesquisa']

# 2. **Não aceitaram**: Pessoas que não aceitaram participar da pesquisa
nao_aceitaram_df = merged_df[merged_df['Aceite'] == 'Não aceito participar da pesquisa'].copy()

# 3. **Não responderam**: Pessoas do cadastro cujo email **não foi encontrado no formulário**
nao_responderam_df = merged_df[merged_df['e-mail'].isna()].copy()

# 4. **Responderam, mas não estão no cadastro**: Pessoas que responderam ao formulário, mas cujo email **não está no cadastro**
responderam_nao_encontrados_no_cadastro_df = pesquisa_df[~pesquisa_df['e-mail'].isin(cadastro_df_limpo['Endereço de Email'])]

# Estatísticas:
print(f'Total de pessoas no cadastro após remoção de duplicatas: {len(cadastro_df_limpo)}')
print(f'Total de pessoas que responderam ao formulário: {len(pesquisa_df)}')
print(f'Pessoas que aceitaram participar: {len(aceitaram_df)}')
print(f'Pessoas que não aceitaram: {len(nao_aceitaram_df)}')
print(f'Pessoas que não responderam ao formulário: {len(nao_responderam_df)}')
print(f'Pessoas que responderam mas não estão no cadastro: {len(responderam_nao_encontrados_no_cadastro_df)}')

# Salvar os quatro arquivos CSV
aceitaram_df.to_csv('Banco_de_dados_aceitaram.csv', index=False)
nao_aceitaram_df.to_csv('Banco_de_dados_nao_aceitaram.csv', index=False)
nao_responderam_df.to_csv('Banco_de_dados_nao_responderam.csv', index=False)
responderam_nao_encontrados_no_cadastro_df.to_csv('Banco_de_dados_responderam_sem_estar_no_cadastro.csv', index=False)

print("Arquivos gerados:")
print("1. Banco_de_dados_aceitaram.csv")
print("2. Banco_de_dados_nao_aceitaram.csv")
print("3. Banco_de_dados_nao_responderam.csv")
print("4. Banco_de_dados_responderam_sem_estar_no_cadastro.csv")
