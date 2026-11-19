"""Cálculo reprodutível da análise SERS (sem bibliotecas externas)."""
import csv
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent
with (DIR / "premissas.json").open(encoding="utf-8") as arquivo:
    p = json.load(arquivo)

h = p["horas_uso_por_dia"]
dias_uso = p["dias_uso_por_mes"]
tarifa = p["tarifa_simulada_rs_por_kwh"]
e_base = p["potencia_media_base_w"] * h * dias_uso / 1000
e_eficiente = p["potencia_media_eficiente_w"] * h * dias_uso / 1000
e_poupada = e_base - e_eficiente
porcentagem_poupada = 100 * e_poupada / e_base
solar_total = (p["pv_potencia_kwp"] * p["pv_horas_sol_pleno_equivalentes_dia"]
               * p["pv_dias_por_mes"] * p["pv_fator_desempenho"])
solar_destinado_ao_notebook = min(e_base, solar_total)
economia_solar_maxima_rs = solar_destinado_ao_notebook * tarifa
investimento = p["pv_investimento_hipotetico_rs"]
retorno_meses_ideal = investimento / economia_solar_maxima_rs if economia_solar_maxima_rs > 0 else None

with (DIR / "comparacao.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["alternativa", "consumo_notebook_kwh_mes", "energia_solar_atribuida_kwh_mes",
                "custo_variavel_teorico_rs_mes", "investimento_inicial_hipotetico_rs", "nota"])
    w.writerow(["Base da rede", f"{e_base:.2f}", "0.00", f"{e_base * tarifa:.2f}", "0.00",
                "Cenário sem intervenções; custo ilustrativo"])
    w.writerow(["Eficiência energética", f"{e_eficiente:.2f}", "0.00", f"{e_eficiente * tarifa:.2f}",
                f"{p['custo_extra_eficiencia_rs']:.2f}", "Potência de 20 W é hipótese, não medição"])
    w.writerow(["Solar fotovoltaica", f"{e_base:.2f}", f"{solar_destinado_ao_notebook:.2f}",
                f"{max(0,e_base * tarifa - economia_solar_maxima_rs):.2f}", f"{investimento:.2f}",
                "Custo variável é apenas limite ideal; NÃO é a conta de luz real"])

print("ANÁLISE SERS - CENÁRIO HIPOTÉTICO")
print(f"Base: {e_base:.2f} kWh/mês | custo R$ {e_base * tarifa:.2f}")
print(f"Eficiência: {e_eficiente:.2f} kWh/mês | reduz {porcentagem_poupada:.1f}% | R$ {e_poupada * tarifa:.2f}/mês")
print(f"PV de 1 kWp (sistema inteiro): {solar_total:.1f} kWh/mês (projeção, não medida)")
print(f"Parcela máxima atribuível ao notebook: {solar_destinado_ao_notebook:.2f} kWh/mês")
print(f"PV: economia variável máxima hipotética no notebook = R$ {economia_solar_maxima_rs:.2f}/mês")
print(f"PV: retorno ideal considerando só o notebook = {retorno_meses_ideal / 12:.1f} anos (não é previsão real)")
print("Comparação gerada: analise/comparacao.csv")
