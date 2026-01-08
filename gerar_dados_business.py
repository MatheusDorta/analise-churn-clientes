import pandas as pd
import random
from datetime import datetime, timedelta

# Configurações
qtd_registros = 500
cidades = ['São Paulo', 'Londrina', 'Toledo']
status_opcoes = ['Ativo', 'Cancelado']
motivos_cancelamento = ['Preço', 'Concorrência', 'Mau Atendimento', 'Mudança de Endereço', 'Financeiro']

dados = []

# Data inicial simulada (jan/2023 até hoje)
start_date = datetime(2023, 1, 1)

for i in range(1, qtd_registros + 1):
    # 1. Escolha aleatória de cidade (peso maior para SP, como no seu caso real)
    cidade = random.choices(cidades, weights=[60, 20, 20], k=1)[0]
    
    # 2. Valor do contrato (varia um pouco)
    valor = round(random.uniform(500.00, 2500.00), 2)
    
    # 3. Datas
    dias_aleatorios = random.randint(0, 1000)
    data_inicio = start_date + timedelta(days=dias_aleatorios)
    
    # 4. Status e Churn
    # Vamos dizer que 20% dos clientes cancelaram
    status = random.choices(status_opcoes, weights=[80, 20], k=1)[0]
    
    data_fim = None
    motivo = None
    
    if status == 'Cancelado':
        # Cancelou entre 1 e 12 meses depois de entrar
        dias_ativo = random.randint(30, 365)
        data_fim = data_inicio + timedelta(days=dias_ativo)
        # Se a data de fim for no futuro, ajusta para hoje (não pode cancelar no futuro)
        if data_fim > datetime.now():
            data_fim = datetime.now()
            
        motivo = random.choice(motivos_cancelamento)
    
    dados.append({
        'ID_Contrato': i,
        'Cidade': cidade,
        'Valor_Mensal': valor,
        'Data_Inicio': data_inicio.strftime('%Y-%m-%d'),
        'Data_Fim': data_fim.strftime('%Y-%m-%d') if data_fim else None,
        'Status': status,
        'Motivo_Cancelamento': motivo
    })

# Criar DataFrame e Salvar
df = pd.DataFrame(dados)
df.to_csv('dados_contratos.csv', index=False, encoding='utf-8')

print(f"Arquivo 'dados_contratos.csv' gerado com {qtd_registros} linhas!")
print(df.head())