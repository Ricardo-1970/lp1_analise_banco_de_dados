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
