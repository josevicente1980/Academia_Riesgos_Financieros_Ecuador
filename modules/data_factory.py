import numpy as np
import pandas as pd


def generar_cartera(n: int = 1800, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    segmentos = rng.choice(
        ["Consumo", "Microcrédito", "Productivo", "Vivienda", "Comercial"],
        size=n,
        p=[0.32, 0.25, 0.16, 0.17, 0.10],
    )
    provincias = rng.choice(
        ["Pichincha", "Guayas", "Azuay", "Loja", "Manabí", "El Oro",
         "Tungurahua", "Imbabura", "Los Ríos", "Chimborazo"],
        size=n,
    )
    ingreso = np.exp(rng.normal(7.7, 0.65, n)).clip(450, 18000)
    deuda_ingreso = rng.beta(2.2, 4.5, n).clip(0.02, 0.95)
    antiguedad = rng.integers(1, 181, n)
    dias_mora = rng.choice(
        [0, 5, 15, 30, 45, 60, 90, 120, 180],
        size=n,
        p=[0.56, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04, 0.035, 0.025],
    )
    monto = np.select(
        [
            segmentos == "Microcrédito",
            segmentos == "Consumo",
            segmentos == "Vivienda",
            segmentos == "Productivo",
        ],
        [
            rng.lognormal(8.1, 0.65, n),
            rng.lognormal(8.5, 0.65, n),
            rng.lognormal(10.5, 0.55, n),
            rng.lognormal(9.7, 0.75, n),
        ],
        default=rng.lognormal(10.0, 0.7, n),
    ).clip(500, 250000)

    score = (
        790
        - deuda_ingreso * 230
        - np.minimum(dias_mora, 120) * 1.35
        + np.log1p(ingreso) * 10
        + np.minimum(antiguedad, 120) * 0.18
        + rng.normal(0, 35, n)
    ).clip(300, 900)

    z = (
        -7.0
        + 0.011 * (650 - score)
        + 2.0 * deuda_ingreso
        + 0.018 * dias_mora
        - 0.000035 * ingreso
    )
    pd_12m = (1 / (1 + np.exp(-z))).clip(0.002, 0.75)
    lgd = np.where(segmentos == "Vivienda", 0.25, rng.uniform(0.35, 0.68, n))
    ead = monto * rng.uniform(0.72, 1.0, n)
    perdida_esperada = pd_12m * lgd * ead
    incumplimiento = rng.binomial(1, pd_12m)

    clasificacion = pd.cut(
        dias_mora,
        bins=[-1, 0, 30, 60, 90, 9999],
        labels=["Normal", "Vigilancia", "Deficiente", "Dudoso", "Pérdida"],
    )

    return pd.DataFrame({
        "id_credito": [f"EC-{i:06d}" for i in range(1, n + 1)],
        "segmento": segmentos,
        "provincia": provincias,
        "ingreso_mensual": ingreso.round(2),
        "deuda_ingreso": deuda_ingreso.round(4),
        "antiguedad_meses": antiguedad,
        "dias_mora": dias_mora,
        "saldo": monto.round(2),
        "score": score.round(0).astype(int),
        "pd_12m": pd_12m.round(5),
        "lgd": lgd.round(4),
        "ead": ead.round(2),
        "perdida_esperada": perdida_esperada.round(2),
        "incumplimiento": incumplimiento,
        "clasificacion": clasificacion.astype(str),
    })


def generar_liquidez(seed: int = 18) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    bandas = ["1–7 días", "8–30 días", "31–90 días", "91–180 días",
              "181–360 días", "Más de 360 días"]
    activos = np.array([22, 38, 54, 61, 83, 145], dtype=float) * 1_000_000
    pasivos = np.array([31, 49, 50, 57, 72, 112], dtype=float) * 1_000_000
    activos *= rng.uniform(0.94, 1.06, len(bandas))
    pasivos *= rng.uniform(0.94, 1.06, len(bandas))
    df = pd.DataFrame({"banda": bandas, "activos": activos, "pasivos": pasivos})
    df["brecha"] = df["activos"] - df["pasivos"]
    df["brecha_acumulada"] = df["brecha"].cumsum()
    return df


def generar_eventos_operativos(seed: int = 77) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    procesos = [
        "Crédito", "Caja", "Canales digitales", "Tesorería",
        "Cumplimiento", "Tecnología", "Contabilidad", "Atención al cliente"
    ]
    tipos = [
        "Fraude interno", "Fraude externo", "Falla tecnológica",
        "Error de proceso", "Daño a activos", "Prácticas laborales",
        "Clientes y productos"
    ]
    n = 180
    return pd.DataFrame({
        "fecha": pd.date_range("2025-01-01", periods=n, freq="2D"),
        "proceso": rng.choice(procesos, n),
        "tipo_evento": rng.choice(tipos, n),
        "probabilidad": rng.integers(1, 6, n),
        "impacto": rng.integers(1, 6, n),
        "perdida": rng.lognormal(7.4, 1.0, n).round(2),
        "control_efectivo": rng.choice(["Sí", "Parcial", "No"], n, p=[0.58, 0.30, 0.12]),
    })
