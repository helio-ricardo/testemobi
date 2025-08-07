import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

print("Iniciando o Passo 4: Teste de Hipóteses")
print("="*60)

try:
    df = pd.read_csv('icarros_final_limpo.csv', sep=';')
    print("Arquivo 'icarros_final_limpo.csv' carregado com sucesso.\n")
except FileNotFoundError:
    print("ERRO: Arquivo 'icarros_final_limpo.csv' não encontrado. Execute os passos anteriores primeiro.")
    exit()

print("--- Contagem de anúncios por estado (Top 5) ---")
print(df['estado'].value_counts().head())

estado_1 = 'SP'
estado_2 = 'PR'

precos_sp = df[df['estado'] == estado_1]['preco'].dropna()
precos_pr = df[df['estado'] == estado_2]['preco'].dropna()

print(f"\n--- Preparando dados para a comparação ---")
print(f"Número de anúncios válidos em {estado_1}: {len(precos_sp)}")
print(f"Preço médio em {estado_1}: R$ {precos_sp.mean():,.2f}")
print(f"Número de anúncios válidos em {estado_2}: {len(precos_pr)}")
print(f"Preço médio em {estado_2}: R$ {precos_pr.mean():,.2f}")
print("="*60)

print("\n--- Executando o Teste de Hipótese (Teste t) ---")
t_stat, p_value = ttest_ind(precos_sp, precos_pr, equal_var=False)

print(f"Estatística t: {t_stat:.4f}")
print(f"P-valor: {p_value:.4f}")

print("\n--- Interpretação do Resultado ---")
alpha = 0.05

if p_value < alpha:
    print(f"Como o p-valor ({p_value:.4f}) é menor que {alpha}, rejeitamos a Hipótese Nula.")
    print("Conclusão: Existe uma diferença estatisticamente significativa entre os preços médios dos carros em SP e PR.")
else:
    print(f"Como o p-valor ({p_value:.4f}) é maior que {alpha}, não podemos rejeitar a Hipótese Nula.")
    print("Conclusão: Não há evidências de uma diferença estatisticamente significativa entre os preços médios.")
print("="*60)

print("\n--- Gerando Visualização Comparativa (Boxplot) ---")
plt.figure(figsize=(12, 8))
sns.boxplot(
    x='estado',
    y='preco',
    data=df[df['estado'].isin([estado_1, estado_2])],
    palette='viridis'
)
plt.title(f'Comparação de Preços de Veículos: {estado_1} vs. {estado_2}', fontsize=16, weight='bold')
plt.xlabel('Estado', fontsize=12)
plt.ylabel('Preço (R$)', fontsize=12)
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda y, p: f"R$ {int(y):,}"))
plt.tight_layout()
boxplot_path = 'boxplot_preco_estados.png'
plt.savefig(boxplot_path)

print(f"Gráfico comparativo salvo como: '{boxplot_path}'")
print("="*60)