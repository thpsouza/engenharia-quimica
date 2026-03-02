import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EngenhariaProcessos import Corrente
from EngenhariaProcessos.integracaoEnergetica import consumo_maximo_utilidades, consumo_minimo_utilidades
    
    
def exemplo_integracao_energetica():
    print("\n" + "=" * 70)
    print("EXEMPLO: ANÁLISE DE POSSIBILIDADE DE INTEGRAÇÃO ENERGÉTICA")
    print("=" * 70)
    
    # Definir correntes do processo
    correntes = [
        Corrente(WCp=5, To=60, Td=150),    # Corrente fria 1: 450 kW
        Corrente(WCp=7, To=100, Td=220),   # Corrente fria 2: 840 kW
        Corrente(WCp=10, To=180, Td=90),   # Corrente quente 1: -900 kW
        Corrente(WCp=2, To=250, Td=140)    # Corrente quente 2: -220 kW
    ]
    
    print("\nCorrentes do processo:")
    print("  Correntes FRIAS (requerem aquecimento):")
    for i, c in enumerate([c for c in correntes if not c.quente], 1):
        print(f"    F{i}: WCp = {c.WCp} kW/°C,  {c.To}°C → {c.Td}°C,  Q = {c.Q:.0f} kW")
    print("  Correntes QUENTES (requerem resfriamento):")
    for i, c in enumerate([c for c in correntes if c.quente], 1):
        print(f"    Q{i}: WCp = {c.WCp} kW/°C,  {c.To}°C → {c.Td}°C,  Q = {c.Q:.0f} kW")
    
    # Calcular consumo máximo
    cp_agua = 0.00116  # kWh/(kg·°C)
    dT_agua = 20       # °C
    dHvap_agua = 0.48  # kWh/kg
    
    (m_vap_max, m_agua_max),  (Q_vap_max, Q_agua_max) = consumo_maximo_utilidades(
        correntes, cp_agua, dT_agua, dHvap_agua
    )
    print(f"\nCONSUMO MÁXIMO (sem integração):")
    print(f"  Vapor de utilidade: {m_vap_max:.1f} kg/h ({Q_vap_max:.1f}kW)")
    print(f"  Água de refrigeração: {m_agua_max:.1f} kg/h ({Q_agua_max:.1f}kW)")
    
    # Calcular consumo mínimo com ΔT_min = 10°C
    vazoes, Q_min, intervalo, tabela = consumo_minimo_utilidades(correntes, cp_agua, dT_agua, dHvap_agua, dT_min=10)
    (m_vap_min, m_agua_min),  (Q_vap_min, Q_agua_min) = vazoes, Q_min
    print(f"\nCONSUMO MÍNIMO (com integração - ΔT_min = 10°C):")
    print(f"  Vapor de utilidade: {m_vap_min:.1f} kg/h ({Q_vap_min:.1f} kW)")
    print(f"  Água de refrigeração: {m_agua_min:.2f} kg/h ({Q_agua_min} kW)")
    
    # Calcular economia
    economia_agua = (Q_agua_max - Q_agua_min) / Q_agua_max * 100 if Q_agua_max > 0 else 0
    economia_vap = (Q_vap_max - Q_vap_min) / Q_vap_max * 100 if abs(Q_vap_max) > 0 else 0
    print(f"\nOPORTUNIDADE DE ECONOMIA:")
    print(f"  Vapor: {economia_vap:.1f}% (de {Q_vap_max:.1f} para {Q_vap_min:.1f} kW)")
    print(f"  Água: {economia_agua:.1f}% (de {Q_agua_max:.1f} para {Q_agua_min:.1f} kW)")
    
    
def imprimir_exemplos():
    """Executa e imprime todos os exemplos."""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  LIMITES DE INTEGRAÇÃO ENERGÉTICA - EXEMPLOS DE USO".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    # Executar exemplos
    exemplo_integracao_energetica()
    
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  FIM DOS EXEMPLOS".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70 + "\n")


def main():
    imprimir_exemplos()    


if __name__ == "__main__":
    main()