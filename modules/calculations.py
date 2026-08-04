import numpy as np
import pandas as pd


def formato_dinero(valor: float) -> str:
    if abs(valor) >= 1_000_000:
        return f"${valor / 1_000_000:,.2f} M"
    if abs(valor) >= 1_000:
        return f"${valor / 1_000:,.1f} mil"
    return f"${valor:,.2f}"


def nivel_riesgo(pd_value: float) -> str:
    if pd_value < 0.03:
        return "Bajo"
    if pd_value < 0.08:
        return "Moderado"
    if pd_value < 0.20:
        return "Alto"
    return "Crítico"


def var_historico(retornos: pd.Series, confianza: float, exposicion: float) -> float:
    perdida_percentil = -np.quantile(retornos.dropna(), 1 - confianza)
    return max(0.0, perdida_percentil * exposicion)


def var_parametrico(retornos: pd.Series, confianza: float, exposicion: float) -> float:
    z_map = {0.90: 1.2816, 0.95: 1.6449, 0.975: 1.9600, 0.99: 2.3263}
    z = z_map.get(confianza, 1.6449)
    return max(0.0, (z * retornos.std() - retornos.mean()) * exposicion)


def semaforo(valor: float, meta: float, inverso: bool = False) -> str:
    cumple = valor <= meta if inverso else valor >= meta
    return "🟢" if cumple else "🔴"
