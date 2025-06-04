# 1. importe as bibliotecas necessárias no início do seu script ou notebook.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Bibliotecas importadas com sucesso!")

# 2.  Carregar Dados 

# Caminho onde está o arquivo com os dados
caminho_arquivo = '12 RP07 Análise de Dados com Python.xlsx'

try:
    df = pd.read_excel(caminho_arquivo)
    print(f"\nArquivo '{caminho_arquivo.split('/')[-1]}'carregado com sucesso em DataFrame!")

    # Exiba as primeiras linhas do DataFrame (.head) para uma primeira inspeção.
    print("\nPrimeiras 5 linhas do DataFrame:")
    print(df.head())

    # Exiba suas informações gerais (.info()) para uma primeira inspeção.
    print("\nInformações gerais do DataFrame:")
    df.info()

except FileNotFoundError:
    print(f"\ERRO: o arquivo não foi encontrada no caminho especificado: {caminho_arquivo}")
    print("Por favor, verifique se o caminho e o nome do arquivo estão corretos e se você montou seu google Colab (se aplicável).")
except Exception as e:
    print(f"\nOcorreu um erro ao carregar o arquivo: {e}") 

# Etapa 2:limpeza e pré-processamento de Dados
# Objetivo: tratar inconscistências e preparar os dados para análise.

print("\n" + "="*55)
print("Iniciando Etapa 2: limpeza e pré-processamento de Dados")
print("="*55)

# Antes de começar, vamos fazer uma cópia de DataFrame original para não alterar o DF da Etapa 1
df_limpo = df.copy()
print("\nCópia do DataFrame original criada para limpeza (df_limpo).")


# 1. Renomear colunas (opcional):
# Padronize nomes de colunas para facilitar o acesso (ex: remover espaços, caracteres especiais).
# Vamos inspecionar os nomes atuais para decidir o quê fazer.
print("\nNomes originais das colunas:")
print(df_limpo.columns.tolist())

# Exemplo de renomeação: converter para minúsculas e substituir espaços por underscores.
# Você pode ajustar esta lista conforme a necessidade real dos seus nomes de colunas.
novos_nomes_colunas = {col: col.replace(' ','_').replace('.','').lower()for col in df_limpo.columns}
df_limpo.rename(columns = novos_nomes_colunas, inplace = True)

print("\nNomes das colunas após renomeação (se houver):")
print(df_limpo.columns.tolist())

# 2. Verificar valores ausentes:
print("\nVerificcando valores ausentes no DataFrame")
valores_nulos = df_limpo.isnull().sum()
print(valores_nulos[valores_nulos > 0]) # Exibe apenas colunas com valores nulos.

for coluna in valores_nulos[valores_nulos > 0].index:
    if df_limpo[coluna].dtype == 'object': # Se for uma coluna de texto categórica.
        df_limpo[coluna].fillna('Desconhecido', inplace = True)
        print(f"Preenchido valores nulos na coluna '{coluna}'com 'Desconhecido.")
    elif pd.api.types.is_numeric_dtype(df_limpo[coluna]):
        df_limpo[coluna].fillna(0, inplace = True) # Preechendo com valor zero.    
        print(f"Preenchido valores nulos na coluna '{coluna}'com 0.")

    else:
        print(f"Coluna {coluna} possui nulos, mas não foi tratada automaticamente(necessita análise específica).")

print("\nValores ausentes após tratamento (se houver):")
print(df_limpo.isnull().sum()[df_limpo.isnull().sum() > 0])

# 3. Converter tipos de dados :
print("\nVerificando e convertendo tipod de dados: ")
print("Tipos de dados antes da conversão:")
print(df_limpo.info())

# 3.1 Converte colunas numéricas(ex: total, vendas, quantidade , desconto e lucro)
colunas_numericas_para_converter = ['total_vendas', 'quantidade', 'desconto','lucro']
for coluna in colunas_numericas_para_converter:
    if coluna in df_limpo.columns:
        # Ponto de atenção: a conversão de números pode exigir a substituição de vírgulas por pontos
        # antes de converter para float, e tratamento para caracteres não múmericos.
        # A coluna de desconto pode ter valores como 'S' ou vazios.
        if df_limpo[coluna].dtype == 'object': # Se a coluna for de objeto (string)
            # substitui vírgulas por pontos e tenta converter para numérico.
            # coerse erros como ('S' ou vazios) para NaN, que pode ser tratado depois.
            df_limpo[coluna] = df_limpo[coluna].astype(str).replace(',','.', regex = False)
            df_limpo[coluna] = pd.to_numeric(df_limpo[coluna], erros = 'coerse')
            # Após a conversão preenche NaNas criados por 'coerse' com '0'(ou outra estratégia)
            df_limpo[coluna].fillna(0, inplace=True)
            print(f"Coluna '{coluna}'convertida para numérico float e NaN/errors preenchidos com zero.")
        elif pd.api.types.is_numeric_dtype(df_limpo[coluna]) and df_limpo[coluna].dtype != 'float64':
            # Se já é numérico e não float(ex: int), assegura que é float para consistência
            df_limpo[coluna] = df_limpo[coluna].astype(float)
            print(f"Coluna '{coluna}'convertida para float.")

    else:
        print(f"Coluna '{coluna}'não encontrada no DataFrame para conversão numérica.")

# 3.2  Converter a coluna data_pedido para o tipo datetime.
coluna_data = 'data_pedido'# Adapte conforme o nome real da sua coluna de data.
if coluna_data in df_limpo.columns:
    df_limpo[coluna_data] = pd.to_datetime(df_limpo[coluna_data], errors='coerse')
    # Tratar possíveis NaNs criados por datas inválidas
    if df_limpo[coluna_data].isnull().sum()>0:
        print(f"Atenção: {df_limpo[coluna_data].isnull().sum()} valores inválidos na coluna '{coluna_data}' foram convertidos para 'Nat' (not a time). ")
        # você pode remover essas linhas pu preenchê - las com uma data padrão, dependendo da sua análise.
        # df_limpo.dropna(subset=[coluna_data], inplace=True). # Exemplo remover linhas com datas inválidas
    print(f"Coluna '{coluna_data}' convertida para o tipo datetime.")  
else:
    print(f"Aviso: coluna '{coluna_data}' não encontrada no DataFrame para conversão de data.")

print("\nTipos de dados após a conversão:")
print(df_limpo.info())

# 4. Tratar Duplicatas:
print("\nVerificando e tratando duplicatas:")
duplicatas = df_limpo.duplicated().sum()
if duplicatas > 0:
    print(f"Números de linhas duplicadas encontradas: {duplicatas}")
    df_limpo.drop_duplicates(inplace=True)
    print(f"Duplicatas removidas. Novo número de linhas: {len(df_limpo)}")
else:
    print("Nenhuma linha duplicada encontrada.")


print("\n" +"=" *56 )
print("Etapa 2: limpeza e pré-processamento de dados concluídos") 
print("=" *56) 

# Exiba as primeiras linhas do DataFrame após a limpeza para uma verificação final.
print("\nPrimeiras 5 linhas do dataFrame após a limpeza:")
print(df_limpo.head())