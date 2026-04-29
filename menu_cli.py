# ============================================================
#   SOMPO PREDICT — MENU CLI INTEGRADO
#   Sprint 1 · Grupo T1 · FIAP x Sompo Seguros
# ============================================================

# Importa módulo do Rafael (já pronto)
from modulo_opcao4_xai import opcao_4_dashboard_xai

# Placeholders dos outros membros (serão substituídos quando eles entregarem)
def opcao_1_dados():
    print("\n[MÓDULO 1 — DADOS] Guilherme")
    print("  → Análise estatística + Isolation Forest")
    print("  ⏳ Em desenvolvimento...\n")

def opcao_2_cloud():
    print("\n[MÓDULO 2 — CLOUD + IA] Gustavo")
    print("  → Modelo ML na AWS + Flask API")
    print("  ⏳ Em desenvolvimento...\n")

def opcao_3_iot():
    print("\n[MÓDULO 3 — TELEMETRIA IoT] Anthony")
    print("  → Simulação ESP32 + leitura de sensores")
    print("  ⏳ Em desenvolvimento...\n")

def opcao_5_seguranca():
    print("\n[MÓDULO TRANSVERSAL — AUTH + AUDITORIA] Charles")
    print("  → Autenticação JWT + log de auditoria criptografado")
    print("  ⏳ Em desenvolvimento...\n")

# ────────────────────────────────────────
# MENU PRINCIPAL
# ────────────────────────────────────────
def exibir_menu():
    print("\n" + "="*60)
    print("   🌾 SOMPO PREDICT — Sistema de Risco Agrícola v1.0")
    print("   FIAP · Grupo T1 · Sprint 1")
    print("="*60)
    print("  [1] 📊 Análise de Dados e Anomalias     (Guilherme)")
    print("  [2] ☁️  Modelo IA na Nuvem               (Gustavo)")
    print("  [3] 📡 Telemetria IoT — Sensores ESP32  (Anthony)")
    print("  [4] 🎯 Dashboard de Risco + XAI (SHAP)  (Rafael)")
    print("  [5] 🔐 Segurança e Auditoria            (Charles)")
    print("  [0] 🚪 Sair")
    print("="*60)

def main():
    while True:
        exibir_menu()
        escolha = input("  Escolha uma opção: ").strip()

        if escolha == '1':
            opcao_1_dados()
        elif escolha == '2':
            opcao_2_cloud()
        elif escolha == '3':
            opcao_3_iot()
        elif escolha == '4':
            opcao_4_dashboard_xai()
        elif escolha == '5':
            opcao_5_seguranca()
        elif escolha == '0':
            print("\n  👋 Encerrando Sompo Predict. Até logo!\n")
            break
        else:
            print("\n  ⚠️  Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()