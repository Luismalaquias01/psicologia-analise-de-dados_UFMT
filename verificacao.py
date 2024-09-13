import pandas as pd

# Carregar os arquivos CSV
cadastro_df = pd.read_csv('Novo_cadastro.csv')
pesquisa_df = pd.read_csv('Formulario_pesquisa.csv')

# Limpar os emails: Remover espaços e converter para minúsculas
cadastro_df['Endereço de Email'] = cadastro_df['Endereço de Email'].str.strip().str.lower()
pesquisa_df['e-mail'] = pesquisa_df['e-mail'].str.strip().str.lower()

# Remover duplicatas, se houver
cadastro_df = cadastro_df.drop_duplicates(subset=['Endereço de Email'])
pesquisa_df = pesquisa_df.drop_duplicates(subset=['e-mail'])

# Fazer o merge (join) dos dados de acordo com o email
merged_df = pd.merge(cadastro_df, pesquisa_df, left_on='Endereço de Email', right_on='e-mail', how='left')

# Criar a coluna de "Aceite"
merged_df['Aceite'] = merged_df['Tendo em vista as informações apresentadas acima, eu: ']

# Para os não encontrados ou que não aceitaram, preencher a coluna 'Aceite' com 'Não aceito participar da pesquisa'
merged_df['Aceite'] = merged_df['Aceite'].fillna('Não aceito participar da pesquisa')

# Filtrar os dados de quem aceitou participar da pesquisa
participantes_df = merged_df[merged_df['Aceite'] == 'Aceito participar da pesquisa']

# Filtrar quem não foi encontrado ou não aceitou participar
nao_encontrados_df = merged_df[merged_df['Aceite'] == 'Não aceito participar da pesquisa']

# Salvar o novo banco de dados com os participantes e a coluna "Aceito participar da pesquisa"
participantes_df.to_csv('Banco_de_dados_participantes.csv', index=False)

# Salvar o banco de dados com as pessoas não encontradas ou que não aceitaram
nao_encontrados_df.to_csv('Nao_encontrados_ou_nao_aceitaram.csv', index=False)

print("Arquivos 'Banco_de_dados_participantes.csv' e 'Nao_encontrados_ou_nao_aceitaram.csv' foram gerados com a coluna 'Aceito participar da pesquisa'.")
