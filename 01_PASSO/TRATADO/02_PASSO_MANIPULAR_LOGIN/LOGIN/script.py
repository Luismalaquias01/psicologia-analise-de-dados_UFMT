import pandas as pd

# Função para carregar os arquivos CSV
def carregar_arquivo(filepath):
    try:
        df = pd.read_csv(filepath, delimiter= ',', encoding= 'utf-8', engine= 'python')
        print(f"O arquivo '{filepath}' foi carregado com sucesso e possui o total de: {len(df)} linhas!")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo {filepath}: {e}")
        return pd.DataFrame()

# Função para verificar se o DataFrame está vazio e tratar erro
def verificar_erro_leitura(df, filename):
    if df.empty:
        print(f"Erro, o arquivo '{filename}' não foi carregado corretamente.")
        exit()

# Carregar os arquivos
banco_de_dados_df = carregar_arquivo('Banco_de_dados_aceitaram.csv')
log1500_df = carregar_arquivo('logs_1500.csv')
log1501_df = carregar_arquivo('logs_1501.csv')
log1502_df = carregar_arquivo('logs_1502.csv')
log1503_df = carregar_arquivo('logs_1503.csv')

# Verificar se os arquivos foram carregados corretamente
verificar_erro_leitura(banco_de_dados_df, 'Banco_de_dados_aceitaram.csv')
verificar_erro_leitura(log1500_df, 'logs_1500.csv')
verificar_erro_leitura(log1501_df, 'logs_1501.csv')
verificar_erro_leitura(log1502_df, 'logs_1502.csv')
verificar_erro_leitura(log1503_df, 'logs_1503.csv')

# Limpeza dos nomes (remover espaços e converter para minúsculas)
banco_de_dados_df['Nome'] = banco_de_dados_df['Nome'].str.strip().str.lower()

# Função para comparar e filtrar os logs com base no banco de dados de aceitos
def filtrar_log_por_aceitos(log_df, banco_de_dados_df):
    log_df['Nome completo'] = log_df['Nome completo'].str.strip().str.lower()
    log_df['Usuário afetado'] = log_df['Usuário afetado'].str.strip().str.lower()

    # Filtrar as linhas onde o nome ou o usuário afetado está no banco de dados
    log_filtrado = log_df[log_df['Nome completo'].isin(banco_de_dados_df['Nome']) |
                          log_df['Usuário afetado'].isin(banco_de_dados_df['Nome'])]
    return log_filtrado

# Filtrar cada log
log1500_filtrado = filtrar_log_por_aceitos(log1500_df, banco_de_dados_df)
log1501_filtrado = filtrar_log_por_aceitos(log1501_df, banco_de_dados_df)
log1502_filtrado = filtrar_log_por_aceitos(log1502_df, banco_de_dados_df)
log1503_filtrado = filtrar_log_por_aceitos(log1503_df, banco_de_dados_df)

# Contar quantas linhas foram removidas de cada log
linhas_removidas_1500 = len(log1500_df) - len(log1500_filtrado)
linhas_removidas_1501 = len(log1501_df) - len(log1501_filtrado)
linhas_removidas_1502 = len(log1502_df) - len(log1502_filtrado)
linhas_removidas_1503 = len(log1503_df) - len(log1503_filtrado)

# Exibir o total de linhas removidas de cada log
print(f"Total de linhas removidas no log 1500: {linhas_removidas_1500}")
print(f"Total de linhas removidas no log 1501: {linhas_removidas_1501}")
print(f"Total de linhas removidas no log 1502: {linhas_removidas_1502}")
print(f"Total de linhas removidas no log 1503: {linhas_removidas_1503}")

# Salvar os logs filtrados
log1500_filtrado.to_csv('logs_1500_filtrado.csv', index=False)
log1501_filtrado.to_csv('logs_1501_filtrado.csv', index=False)
log1502_filtrado.to_csv('logs_1502_filtrado.csv', index=False)
log1503_filtrado.to_csv('logs_1503_filtrado.csv', index=False)

print("Arquivos filtrados gerados com sucesso.")
