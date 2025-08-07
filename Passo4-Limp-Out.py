import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Iniciando a Etapa de Limpeza de Outliers")
print("="*60)

try:
    df = pd.read_csv('icarros_preprocessado.csv', sep=';')
    print("Arquivo 'icarros_preprocessado.csv' carregado com sucesso.\n")
except FileNotFoundError:
    print("ERRO: Arquivo 'icarros_preprocessado.csv' não encontrado.")
    exit()

print("--- Tratando outliers da coluna 'km' ---")
km_max_antes = df['km'].max()
print(f"Quilometragem máxima ANTES da limpeza: {km_max_antes:,.0f} Km")

limiar_km = 1000000
registros_antes = len(df)

df_limpo = df[df['km'] < limiar_km].copy()

registros_depois = len(df_limpo)
print(f"Registros removidos com km > {limiar_km:,.0f} Km: {registros_antes - registros_depois}")

km_max_depois = df_limpo['km'].max()
print(f"Quilometragem máxima DEPOIS da limpeza: {km_max_depois:,.0f} Km")
print("="*60)

print("\n--- Gerando a visualização dos dados limpos ---")
sns.set_style("whitegrid")
plt.figure(figsize=(12, 7))
sns.histplot(df_limpo['km'].dropna(), bins=50, kde=True, color='green')
plt.title('Distribuição da Quilometragem (Após Limpeza)', fontsize=16, weight='bold')
plt.xlabel('Quilometragem (Km)', fontsize=12)
plt.ylabel('Frequência', fontsize=12)
plt.ticklabel_format(style='plain', axis='x')
plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
km_hist_limpo_path = 'histograma_km_limpo.png'
plt.savefig(km_hist_limpo_path)

print(f"Novo histograma salvo como: '{km_hist_limpo_path}'")
print("="*60)

print("\n--- Salvando o arquivo final e limpo ---")
nome_arquivo_final = 'icarros_final_limpo.csv'
df_limpo.to_csv(nome_arquivo_final, index=False, sep=';', encoding='utf-8-sig')
print(f"Arquivo final e limpo foi salvo com sucesso como: '{nome_arquivo_final}'")
print("="*60)