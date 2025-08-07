import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Iniciando a Etapa Opcional: Discretização e Normalização")
print("="*60)

try:
    df = pd.read_csv('icarros_final_limpo.csv', sep=';')
    print("Arquivo 'icarros_final_limpo.csv' carregado com sucesso.\n")
except FileNotFoundError:
    print("ERRO: Arquivo 'icarros_final_limpo.csv' não encontrado. Execute os passos anteriores primeiro.")
    exit()

print("--- 1. Aplicando Discretização na coluna 'preco' ---")

bins_preco = [0, 70000, 120000, float('inf')]
labels_preco = ['Popular', 'Intermediário', 'Premium']

df['faixa_preco'] = pd.cut(df['preco'], bins=bins_preco, labels=labels_preco, right=False)

print("Nova coluna 'faixa_preco' criada.")
print("Contagem de carros por faixa de preço:")
print(df['faixa_preco'].value_counts())
print("-" * 30)

print("\n--- 2. Aplicando Normalização nas colunas 'preco' e 'km' ---")

df['preco_norm'] = (df['preco'] - df['preco'].min()) / (df['preco'].max() - df['preco'].min())
df['km_norm'] = (df['km'] - df['km'].min()) / (df['km'].max() - df['km'].min())

print("Novas colunas 'preco_norm' e 'km_norm' criadas.")
print("-" * 30)

print("\n--- Visualizando o DataFrame transformado (primeiras linhas) ---")
print(df[['preco', 'faixa_preco', 'preco_norm', 'km', 'km_norm']].head())
print("="*60)

nome_arquivo_saida = 'icarros_com_features.csv'
df.to_csv(nome_arquivo_saida, index=False, sep=';', encoding='utf-8-sig')

print(f"\nArquivo com novas features salvo com sucesso como: '{nome_arquivo_saida}'")
print("="*60)

print("Gerando gráfico da nova categoria 'faixa_preco'...")
plt.figure(figsize=(10, 6))
sns.countplot(x='faixa_preco', data=df, palette='magma', order=labels_preco)
plt.title('Contagem de Veículos por Faixa de Preço', fontsize=16, weight='bold')
plt.xlabel('Faixa de Preço', fontsize=12)
plt.ylabel('Número de Veículos', fontsize=12)
plt.tight_layout()
countplot_path = 'countplot_faixa_preco.png'
plt.savefig(countplot_path)
print(f"Gráfico salvo como: '{countplot_path}'")