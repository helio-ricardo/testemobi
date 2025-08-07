import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Iniciando o Passo 3: Análise Descritiva e Visualizações")
print("="*60)

try:
    df = pd.read_csv('icarros_preprocessado.csv', sep=';')
    print("Arquivo 'icarros_preprocessado.csv' carregado com sucesso.\n")
except FileNotFoundError:
    print("ERRO: Arquivo 'icarros_preprocessado.csv' não encontrado. Execute o passo anterior primeiro.")
    exit()

print("--- Estatísticas Descritivas para Preço e Quilometragem ---")
desc_stats = df[['preco', 'km']].describe()
print(desc_stats)
print("="*60)

print("\n--- Gerando Visualizações ---")

sns.set_style("whitegrid")

plt.figure(figsize=(12, 7))
sns.histplot(df['preco'].dropna(), bins=50, kde=True, color='navy')
plt.title('Distribuição dos Preços dos Veículos', fontsize=16, weight='bold')
plt.xlabel('Preço (R$)', fontsize=12)
plt.ylabel('Frequência (Nº de Veículos)', fontsize=12)
plt.ticklabel_format(style='plain', axis='x')
plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
preco_hist_path = 'histograma_precos.png'
plt.savefig(preco_hist_path)
print(f"Gráfico da distribuição de preços salvo como: '{preco_hist_path}'")

plt.figure(figsize=(12, 7))
sns.histplot(df['km'].dropna(), bins=50, kde=True, color='darkred')
plt.title('Distribuição da Quilometragem dos Veículos', fontsize=16, weight='bold')
plt.xlabel('Quilometragem (Km)', fontsize=12)
plt.ylabel('Frequência (Nº de Veículos)', fontsize=12)
plt.ticklabel_format(style='plain', axis='x')
plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
km_hist_path = 'histograma_km.png'
plt.savefig(km_hist_path)
print(f"Gráfico da distribuição de quilometragem salvo como: '{km_hist_path}'")

print("="*60)
print("Análise descritiva concluída.")