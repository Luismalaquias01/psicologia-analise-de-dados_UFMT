import pandas as pd

# Função para carregar os arquivos CSV
def carregar_arquivo(filepath):
    try:
        df = pd.read_csv(filepath, delimiter=',', encoding='utf-8', engine='python')
        print(f"O arquivo '{filepath}' foi carregado com sucesso e possui o total de: {len(df)} linhas!")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{filepath}': {e}")
        return pd.DataFrame()

# Função para verificar se o DataFrame está vazio e tratar erro
def verificar_erro_leitura(df, filename):
    if df.empty:
        print(f"Erro, o arquivo '{filename}' não foi carregado corretamente.")
        exit()

# Carregar os arquivos
banco_de_dados_df = carregar_arquivo('Banco_de_dados_aceitaram.csv')
notas1913_01_df = carregar_arquivo('NOTAS_1913_separated.csv')
notas1913_02_df = carregar_arquivo('NOTAS_1913_separated2.csv')
notas1914_01_df = carregar_arquivo('NOTAS_1914_separated.csv')
notas1914_02_df = carregar_arquivo('NOTAS_1914_separated2.csv')  # Corrigido para '.csv'

# Verificar se os arquivos foram carregados corretamente
verificar_erro_leitura(banco_de_dados_df, 'Banco_de_dados_aceitaram.csv')
verificar_erro_leitura(notas1913_01_df, 'NOTAS_1913_separated.csv')
verificar_erro_leitura(notas1913_02_df, 'NOTAS_1913_separated2.csv')
verificar_erro_leitura(notas1914_01_df, 'NOTAS_1914_separated.csv')
verificar_erro_leitura(notas1914_02_df, 'NOTAS_1914_separated2.csv')

# Limpeza dos nomes (remover espaços e converter para minúsculas)
banco_de_dados_df['Endereço de Email'] = banco_de_dados_df['Endereço de Email'].str.strip().str.lower()

# Função para comparar e filtrar as notas com base no banco de dados de aceitos
def filtrar_nota_por_aceitos(nota_df, banco_de_dados_df):
    nota_df['Endereço de email'] = nota_df['Endereço de email'].str.strip().str.lower()
    
    # Filtrar as linhas onde o email está no banco de dados
    nota_filtrado = nota_df[nota_df['Endereço de email'].isin(banco_de_dados_df['Endereço de Email'])]
    return nota_filtrado

# Filtrar cada log
notas1913_01_filtrado = filtrar_nota_por_aceitos(notas1913_01_df, banco_de_dados_df)
notas1913_02_filtrado = filtrar_nota_por_aceitos(notas1913_02_df, banco_de_dados_df)
notas1914_01_filtrado = filtrar_nota_por_aceitos(notas1914_01_df, banco_de_dados_df)
notas1914_02_filtrado = filtrar_nota_por_aceitos(notas1914_02_df, banco_de_dados_df)

# Contar quantas linhas foram removidas de cada log
linhas_removidas_1913_01 = len(notas1913_01_df) - len(notas1913_01_filtrado)
linhas_removidas_1913_02 = len(notas1913_02_df) - len(notas1913_02_filtrado)
linhas_removidas_1914_01 = len(notas1914_01_df) - len(notas1914_01_filtrado)
linhas_removidas_1914_02 = len(notas1914_02_df) - len(notas1914_02_filtrado)

# Exibir o total de linhas removidas de cada log
print(f"Total de linhas removidas no notas1913_01_df: {linhas_removidas_1913_01}")
print(f"Total de linhas removidas no notas1913_02_df: {linhas_removidas_1913_02}")
print(f"Total de linhas removidas no notas1914_01_df: {linhas_removidas_1914_01}")
print(f"Total de linhas removidas no notas1914_02_df: {linhas_removidas_1914_02}")

# Salvar os logs filtrados
notas1913_01_filtrado.to_csv('notas1913_01_filtrado.csv', index=False)
notas1913_02_filtrado.to_csv('notas1913_02_filtrado.csv', index=False)
notas1914_01_filtrado.to_csv('notas1914_01_filtrado.csv', index=False)
notas1914_02_filtrado.to_csv('notas1914_02_filtrado.csv', index=False)

print("Arquivos filtrados gerados com sucesso.")