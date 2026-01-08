import pandas as pd
import os # Biblioteca para mexer com pastas do Windows
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÃO DE CAMINHO (A CORREÇÃO DO ERRO) ---
# Pega a pasta onde este script está salvo e procura o csv lá dentro
pasta_do_script = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(pasta_do_script, 'dados_contratos.csv')

print(f"Procurando arquivo em: {caminho_arquivo}")

try:
    df = pd.read_csv(caminho_arquivo)
    print("✅ Arquivo carregado com sucesso!\n")
except FileNotFoundError:
    print("❌ Erro: O arquivo 'dados_contratos.csv' não está na pasta 'Projeto de Dados'.")
    exit()

# --- 2. PRÉ-PROCESSAMENTO (PREPARAR OS DADOS PARA O ROBÔ) ---

# Criar uma cópia para trabalhar
df_ml = df.copy()

# A. Transformar texto em números (Encoder)
le_cidade = LabelEncoder()
df_ml['Cidade_Code'] = le_cidade.fit_transform(df_ml['Cidade'])
# Dica: O Encoder decora que SP=0, Toledo=1 (exemplo).

# B. Criar o Alvo (Target): 1 se Cancelou, 0 se Ativo
df_ml['Target'] = df_ml['Status'].apply(lambda x: 1 if x == 'Cancelado' else 0)

# C. Engenharia de Dados: Calcular "Dias de Casa"
# Converte colunas de texto para data
df_ml['Data_Inicio'] = pd.to_datetime(df_ml['Data_Inicio'])
# Se Data_Fim for vazia (cliente ativo), preenche com a data de hoje
df_ml['Data_Fim'] = pd.to_datetime(df_ml['Data_Fim']).fillna(pd.Timestamp.now())

# Calcula a diferença em dias
df_ml['Dias_De_Casa'] = (df_ml['Data_Fim'] - df_ml['Data_Inicio']).dt.days

# --- 3. TREINAMENTO DO MODELO ---

# X = Variáveis que explicam (Valor, Cidade, Tempo de Casa)
# y = A resposta (Cancelou ou não)
X = df_ml[['Valor_Mensal', 'Cidade_Code', 'Dias_De_Casa']]
y = df_ml['Target']

# Separar: 80% para o robô estudar, 20% para a prova final
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar a Árvore de Decisão
# max_depth=3 limita o tamanho para a árvore ficar fácil de ler no gráfico
modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo.fit(X_train, y_train)

# --- 4. AVALIAÇÃO E TESTE ---

# Ver se ele acertou a prova (Acurácia)
previsoes = modelo.predict(X_test)
acuracia = accuracy_score(y_test, previsoes)
print(f"🎯 Acurácia do Modelo: {acuracia*100:.2f}%")

# --- 5. SIMULAÇÃO REAL (PREVER UM NOVO CLIENTE) ---
print("-" * 30)
print("🤖 SIMULANDO UM NOVO CLIENTE:")

# Vamos inventar um cliente:
# Valor: R$ 2.500,00
# Cidade: Toledo (precisamos usar o código que o encoder criou para Toledo)
# Dias de Casa: 30 dias (Cliente novo)

# Descobrindo o código de Toledo
try:
    cod_toledo = le_cidade.transform(['Toledo'])[0]
except:
    cod_toledo = 0 # Se der erro, usa 0 como padrão

novo_cliente_dados = [[2500.00, cod_toledo, 30]] # [Valor, CodigoCidade, Dias]

# O robô faz a previsão
predicao = modelo.predict(novo_cliente_dados)
probabilidade = modelo.predict_proba(novo_cliente_dados) # Certeza dele

resultado = "VAI CANCELAR 🚨" if predicao[0] == 1 else "CLIENTE SEGURO ✅"
print(f"Perfil: R$ 2.500,00 | Toledo | 30 dias de casa")
print(f"Previsão: {resultado}")
print(f"Certeza do Robô: {probabilidade[0][predicao[0]]:.2f}%")

# --- 6. VISUALIZAR A ÁRVORE ---
print("\nAbrindo gráfico da árvore...")
plt.figure(figsize=(12, 8))
plot_tree(modelo, 
          feature_names=['Valor', 'Cidade', 'Dias'], 
          class_names=['Ativo', 'Cancelado'], 
          filled=True, 
          rounded=True)
plt.title("Árvore de Decisão - Churn")
plt.show()