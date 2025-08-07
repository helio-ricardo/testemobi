import pandas as pd
import numpy as np

print("Iniciando o Passo 2.1: Limpeza Inicial e Conversão de Tipos")
print("="*60)

try:
    df = pd.read_csv('salva-icarros.csv', sep=';', encoding='latin-1')
    print("Arquivo 'salva-icarros.csv' carregado com sucesso.")

except FileNotFoundError:
    print("ERRO: Arquivo 'salva-icarros.csv' não encontrado. Verifique se o nome e o local estão corretos.")
    exit()

print("\n--- Diagnóstico: Tipos de dados ANTES da limpeza ---")
df.info()

df.loc[:, 'preco_limpo'] = df['preco'].replace('ERRO', np.nan)
df.loc[:, 'preco_limpo'] = df['preco_limpo'].str.replace(r'[R$. ]', '', regex=True)
df.loc[:, 'preco_limpo'] = df['preco_limpo'].str.replace(',', '.', regex=False)
df.loc[:, 'preco_limpo'] = pd.to_numeric(df['preco_limpo'], errors='coerce')

df.loc[:, 'km_limpo'] = df['km'].str.replace(r'[Km. ]', '', regex=True)
df.loc[:, 'km_limpo'] = pd.to_numeric(df['km_limpo'], errors='coerce')

df['preco'] = df['preco_limpo']
df['km'] = df['km_limpo']
df = df.drop(columns=['preco_limpo', 'km_limpo'])

print("\n--- Diagnóstico: Tipos de dados DEPOIS da limpeza ---")
df.info()

nome_arquivo_saida = 'icarros_preprocessado.csv'
df.to_csv(nome_arquivo_saida, index=False, sep=';', encoding='utf-8-sig')

print("\n--- Conclusão da Etapa ---")
print(f"Arquivo pré-processado com sucesso e salvo como: '{nome_arquivo_saida}'")
print("="*60)