import shap
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ─────────────────────────────────────────
# CARREGAMENTO E PREPARO DOS DADOS REAIS
# Fonte: AI4I 2020 Predictive Maintenance Dataset (UCI)
# ─────────────────────────────────────────
df_raw = pd.read_csv('ai4i2020.csv')

# Mapeamento pro contexto agrícola Sompo
df = pd.DataFrame()
df['equipamento']        = df_raw['Product ID']
df['tipo']               = df_raw['Type']  # L=Leve, M=Médio, H=Pesado
df['temp_ambiente_C']    = (df_raw['Air temperature [K]'] - 273.15).round(1)
df['temp_motor_C']       = (df_raw['Process temperature [K]'] - 273.15).round(1)
df['velocidade_rpm']     = df_raw['Rotational speed [rpm]']
df['torque_Nm']          = df_raw['Torque [Nm]']
df['horas_uso']          = df_raw['Tool wear [min]']
df['risco_alto']         = df_raw['Machine failure']

# Encode tipo (L/M/H → 0/1/2)
le = LabelEncoder()
df['tipo_enc'] = le.fit_transform(df['tipo'])

features = ['temp_ambiente_C', 'temp_motor_C', 'velocidade_rpm',
            'torque_Nm', 'horas_uso', 'tipo_enc']

nomes_features = {
    'temp_ambiente_C':  'Temperatura Ambiente',
    'temp_motor_C':     'Temperatura do Motor',
    'velocidade_rpm':   'Velocidade Operacional (RPM)',
    'torque_Nm':        'Torque do Eixo (Nm)',
    'horas_uso':        'Horas de Uso',
    'tipo_enc':         'Tipo de Equipamento'
}

# ─────────────────────────────────────────
# TREINAMENTO DO MODELO
# ─────────────────────────────────────────
X = df[features]
y = df['risco_alto']

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

df['score_risco'] = modelo.predict_proba(X)[:, 1]
df['score_pct']   = (df['score_risco'] * 100).round(1)

# ─────────────────────────────────────────
# SHAP — EXPLICABILIDADE
# ─────────────────────────────────────────
explainer   = shap.TreeExplainer(modelo)
shap_values = explainer.shap_values(X)
# Compatível com qualquer versão do SHAP
if isinstance(shap_values, list):
    shap_risco = shap_values[1]        # API antiga
elif shap_values.ndim == 3:
    shap_risco = shap_values[:, :, 1]  # API nova 3D
else:
    shap_risco = shap_values

def explicar_equipamento(idx):
    nome  = df.loc[idx, 'equipamento']
    score = df.loc[idx, 'score_pct']
    
    # Converte idx do DataFrame para posição no array SHAP
    pos = df.index.get_loc(idx)
    
    contribuicoes = sorted(
        zip(features, shap_risco[pos]),
        key=lambda x: abs(float(x[1])),
        reverse=True
    )
    total = sum(abs(float(v)) for _, v in contribuicoes[:3])
    
    print(f"\n  🔍 {nome} — Score de Risco: {score}%")
    print(f"  Top 3 fatores que explicam esse risco:")
    for feat, val in contribuicoes[:3]:
        pct     = round((abs(float(val)) / total) * 100, 1) if total > 0 else 0
        direcao = "↑ eleva" if float(val) > 0 else "↓ reduz"
        nome_f  = nomes_features.get(feat, feat)
        print(f"    • {nome_f}: {pct}% ({direcao} o risco)")
# ─────────────────────────────────────────
# MÓDULO 4 — FUNÇÃO PRINCIPAL DO MENU CLI
# ─────────────────────────────────────────
def opcao_4_dashboard_xai():
    print("\n" + "="*65)
    print("   SOMPO PREDICT — MÓDULO 4: DASHBOARD DE RISCO + XAI (SHAP)")
    print("="*65)

    # Pega os 10 equipamentos com maior score pra simular "frota monitorada"
    ranking = df[['equipamento', 'tipo', 'score_pct', 'risco_alto']].copy()
    ranking = ranking.sort_values('score_pct', ascending=False).head(10).reset_index(drop=True)
    ranking.index += 1
    ranking['Risco Crítico'] = ranking['risco_alto'].map({1: '🔴 SIM', 0: '🟢 NÃO'})
    ranking = ranking.rename(columns={
        'equipamento': 'Equipamento',
        'tipo':        'Tipo',
        'score_pct':   'Score Risco (%)'
    }).drop(columns=['risco_alto'])

    print("\n📊 RANKING DE RISCO DA FROTA (Top 10):\n")
    print(ranking.to_string())

    print("\n" + "-"*65)
    print("🔍 ANÁLISE SHAP — Equipamento com maior risco:\n")

    # Pega o idx real do equipamento com maior score
    idx_maior = df['score_risco'].idxmax()
    explicar_equipamento(idx_maior)

    print("\n" + "="*65)
    print("✅ Análise concluída. Fonte: UCI AI4I 2020 Predictive Maintenance")
    print("="*65 + "\n")

# Executa
opcao_4_dashboard_xai()