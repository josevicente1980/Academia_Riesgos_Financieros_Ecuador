from pathlib import Path
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from modules.data_factory import (
    generar_cartera,
    generar_liquidez,
    generar_eventos_operativos,
)
from modules.calculations import (
    formato_dinero,
    nivel_riesgo,
    var_historico,
    var_parametrico,
)

st.set_page_config(
    page_title="Academia de Riesgos Financieros | Ecuador",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .stApp {background: linear-gradient(180deg, #f6f8fb 0%, #eef3f8 100%);}
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071b33 0%, #0b315a 100%);
    }
    [data-testid="stSidebar"] * {color: #ffffff;}
    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 20px;
        background: linear-gradient(110deg, #071b33 0%, #0b5cad 72%, #18a0a8 100%);
        color: white;
        box-shadow: 0 12px 30px rgba(0,0,0,.14);
        margin-bottom: 1.25rem;
    }
    .hero h1 {margin: 0; font-size: 2.05rem;}
    .hero p {margin: .45rem 0 0 0; opacity: .93; font-size: 1.03rem;}
    .section-title {
        font-size: 1.28rem; font-weight: 750; color: #102a43;
        margin: .55rem 0 .8rem 0;
    }
    .info-card {
        background: white; border: 1px solid #d9e2ec; padding: 1rem 1.1rem;
        border-radius: 16px; box-shadow: 0 6px 18px rgba(16,42,67,.06);
        min-height: 125px;
    }
    .info-card h4 {margin: 0 0 .35rem 0; color: #0b5cad;}
    .tag {
        display: inline-block; padding: .23rem .55rem; border-radius: 999px;
        background: #d9f2f2; color: #07575b; font-size: .78rem; font-weight: 700;
        margin-right: .3rem;
        margin-top: .35rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.95);
        border: 1px solid #d9e2ec;
        padding: .75rem 1rem;
        border-radius: 15px;
        box-shadow: 0 5px 14px rgba(16,42,67,.05);
    }
    .disclaimer {
        padding: .8rem 1rem; border-radius: 12px; background: #fff8e1;
        border-left: 5px solid #f2b134; color: #5d4700;
    }
    .formula {
        background:#0d2238; color:#e9f2ff; padding:1rem 1.2rem;
        border-radius:14px; font-family:monospace; font-size:1rem;
    }
    .teaching-card {
        background: linear-gradient(180deg, #ffffff 0%, #f7fbff 100%);
        border: 1px solid #d8e4f2; border-radius: 18px;
        padding: 1rem 1.1rem; box-shadow: 0 8px 22px rgba(16,42,67,.05);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

MODULES = [
    "Inicio ejecutivo",
    "Riesgo de crédito",
    "Pérdida esperada",
    "Riesgo de liquidez",
    "Riesgo de mercado",
    "Riesgo operativo",
    "Pruebas de estrés",
    "Laboratorio de datos",
    "Marco ecuatoriano",
]


def hero(titulo, subtitulo):
    st.markdown(
        f'<div class="hero"><h1>{titulo}</h1><p>{subtitulo}</p></div>',
        unsafe_allow_html=True,
    )


def lesson_card(titulo, descripcion, bullets):
    st.markdown(
        f"""
        <div class="teaching-card">
            <h4 style="margin:0 0 .35rem 0; color:#0b5cad;">{titulo}</h4>
            <p style="margin:0 0 .6rem 0; color:#1e3a5f;">{descripcion}</p>
            {''.join(f'<span class="tag">{b}</span>' for b in bullets)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_learning_path():
    st.markdown("### 🧭 Ruta didáctica")
    st.caption("Recorrido sugerido para comprender el riesgo en tres pasos")
    steps = [
        ("1. Reconocer", "Identifica la fuente del riesgo, su actividad y su materialidad."),
        ("2. Medir", "Usa indicadores, modelos, límites y escenarios para cuantificar el impacto."),
        ("3. Actuar", "Además del número, define controles, comunicación y respuesta institucional."),
    ]
    for title, description in steps:
        st.markdown(f"- **{title}**: {description}")


def render_preguntas_clave(questions):
    for q in questions:
        with st.expander(q["title"]):
            st.write(q["body"])

@st.cache_data
def load_demo():
    return generar_cartera()

@st.cache_data
def load_liquidity():
    return generar_liquidez()

@st.cache_data
def load_operational():
    return generar_eventos_operativos()

cartera_demo = load_demo()

with st.sidebar:
    st.markdown("## 🏦 Academia de Riesgos")
    st.caption("Bancos y cooperativas del Ecuador")
    pagina = st.radio("Módulos", MODULES, label_visibility="collapsed")
    st.markdown("---")
    render_learning_path()
    st.markdown("---")
    institucion = st.selectbox(
        "Enfoque institucional",
        ["Banco privado", "Banco público", "Cooperativa segmento 1", 
         "Cooperativa segmento 2", "Cooperativa segmentos 3–5"],
    )
    st.caption("El enfoque modifica únicamente la narrativa educativa; no sustituye parámetros regulatorios.")
    st.markdown("---")
    st.caption("Versión educativa 1.1 · Datos sintéticos")

def download_excel(df, nombre):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Resultados")
    st.download_button(
        "⬇️ Descargar resultados en Excel",
        data=output.getvalue(),
        file_name=nombre,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

if pagina == "Inicio ejecutivo":
    hero(
        "Gestión Integral de Riesgos Financieros",
        f"Entorno interactivo de formación para {institucion.lower()} · Ecuador",
    )
    st.markdown(
        '<div class="disclaimer"><b>Uso educativo:</b> todos los datos y umbrales son '
        'simulados. La aplicación no constituye asesoría, calificación oficial ni reporte regulatorio.</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.info("Este panel funciona como una hoja de ruta. Primero enseña la exposición, luego la medición y finalmente la toma de decisiones institucionales.")
    saldo = cartera_demo["saldo"].sum()
    mora = cartera_demo.loc[cartera_demo["dias_mora"] > 30, "saldo"].sum() / saldo
    pe = cartera_demo["perdida_esperada"].sum()
    cobertura_demo = 1.18
    liquidez_inmediata = 0.214

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Cartera analizada", formato_dinero(saldo))
    c2.metric("Morosidad > 30 días", f"{mora:.2%}", delta="-0.32 pp")
    c3.metric("Pérdida esperada", formato_dinero(pe))
    c4.metric("Cobertura simulada", f"{cobertura_demo:.0%}")
    c5.metric("Liquidez inmediata", f"{liquidez_inmediata:.1%}")

    st.markdown('<div class="section-title">Mapa integral de riesgos</div>', unsafe_allow_html=True)
    mapa = pd.DataFrame({
        "Riesgo": ["Crédito", "Liquidez", "Mercado", "Operativo", "LA/FT", "Tecnológico"],
        "Exposición": [4.0, 3.1, 2.4, 3.4, 2.8, 3.7],
        "Calidad de gestión": [3.4, 3.8, 3.6, 2.9, 3.7, 3.0],
        "Tendencia": ["Estable", "Mejora", "Estable", "Atención", "Estable", "Atención"],
    })
    fig = px.scatter(
        mapa, x="Calidad de gestión", y="Exposición", size="Exposición",
        color="Tendencia", text="Riesgo", size_max=45,
        range_x=[1,5], range_y=[1,5],
        labels={"Exposición":"Nivel de exposición", "Calidad de gestión":"Calidad de controles"},
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(height=430, legend_title_text="Tendencia")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ¿Cómo leer esta pantalla?")
    render_preguntas_clave([
        {
            "title": "¿Qué significa este mapa de riesgos?",
            "body": "Muestra la relación entre la calidad de controles de la institución y el nivel de exposición. Un punto más alto en exposición no necesariamente es un problema si la gestión es sólida y la tendencia es controlada.",
        },
        {
            "title": "¿Qué debería hacer un comité al verlo?",
            "body": "Priorizar áreas con mayor exposición y menor calidad de gestión, asignar responsables, definir límites y pedir información adicional si el riesgo no está entendido.",
        },
    ])

    a, b, c = st.columns(3)
    with a:
        lesson_card(
            "1. Identificar",
            "Reconocer fuentes, procesos, productos, clientes y eventos que generan exposición.",
            ["Inventario", "Taxonomía", "Materialidad"],
        )
    with b:
        lesson_card(
            "2. Medir y controlar",
            "Aplicar indicadores, modelos, límites, alertas y controles coherentes con la realidad del negocio.",
            ["Modelos", "Límites", "Alertas"],
        )
    with c:
        lesson_card(
            "3. Monitorear y comunicar",
            "Presentar resultados al comité, directorio o consejo con trazabilidad y acciones definidas.",
            ["KRI", "Gobierno", "Trazabilidad"],
        )

elif pagina == "Riesgo de crédito":
    hero("Riesgo de crédito", "Score, probabilidad de incumplimiento, discriminación y segmentación de cartera")
    st.markdown('<div class="formula">Modelo didáctico: PD = P(incumplimiento en los próximos 12 meses | características del cliente)</div>', unsafe_allow_html=True)
    st.write("")
    st.success("Objetivo didáctico: aprender a distinguir entre una buena cartera, clientes más frágiles y qué tan útil es un score en la toma de decisiones.")
    render_preguntas_clave([
        {
            "title": "¿Qué enseñan las métricas de esta pantalla?",
            "body": "La cartera se organiza por segmentos. El score y la PD ayudan a ver qué clientes tienen más probabilidades de incumplir, y la matriz ayuda a ubicar dónde está el mayor riesgo relativo.",
        },
        {
            "title": "¿Qué mensaje debe quedar en una reunión de crédito?",
            "body": "El riesgo no se observa solo en el volumen, sino en la calidad de la estructura, la calidad del cliente y la capacidad del proceso para identificar deterioro temprano.",
        },
    ])

    segmento = st.multiselect(
        "Segmentos de cartera",
        sorted(cartera_demo["segmento"].unique()),
        default=sorted(cartera_demo["segmento"].unique()),
    )
    df = cartera_demo[cartera_demo["segmento"].isin(segmento)].copy()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Operaciones", f"{len(df):,}")
    col2.metric("Score promedio", f"{df['score'].mean():.0f}")
    col3.metric("PD promedio", f"{df['pd_12m'].mean():.2%}")
    col4.metric("Incumplimiento observado", f"{df['incumplimiento'].mean():.2%}")

    tab1, tab2, tab3 = st.tabs(["Distribución", "Modelo logístico", "Simulador individual"])
    with tab1:
        left, right = st.columns(2)
        fig = px.histogram(df, x="score", color="segmento", nbins=35, barmode="overlay")
        fig.update_layout(height=400)
        left.plotly_chart(fig, use_container_width=True)
        resumen = df.groupby("segmento", as_index=False).agg(
            operaciones=("id_credito", "count"),
            saldo=("saldo", "sum"),
            pd_promedio=("pd_12m", "mean"),
            mora=("incumplimiento", "mean"),
        )
        fig2 = px.scatter(
            resumen, x="pd_promedio", y="mora", size="saldo", color="segmento",
            hover_data=["operaciones"], labels={"pd_promedio":"PD promedio", "mora":"Incumplimiento observado"}
        )
        fig2.update_layout(height=400)
        right.plotly_chart(fig2, use_container_width=True)
        st.dataframe(resumen.style.format({"saldo":"${:,.0f}", "pd_promedio":"{:.2%}", "mora":"{:.2%}"}), use_container_width=True)

    with tab2:
        features = ["score", "deuda_ingreso", "dias_mora", "ingreso_mensual", "antiguedad_meses"]
        X = df[features]
        y = df["incumplimiento"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=12, stratify=y
        )
        model = Pipeline([
            ("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ])
        model.fit(X_train, y_train)
        pred = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, pred)
        umbral = st.slider("Umbral de clasificación", 0.05, 0.70, 0.30, 0.01)
        cls = (pred >= umbral).astype(int)
        cm = confusion_matrix(y_test, cls)
        fpr, tpr, _ = roc_curve(y_test, pred)

        m1, m2, m3 = st.columns(3)
        m1.metric("AUC / ROC", f"{auc:.3f}")
        m2.metric("Sensibilidad", f"{cm[1,1] / max(1, cm[1].sum()):.1%}")
        m3.metric("Especificidad", f"{cm[0,0] / max(1, cm[0].sum()):.1%}")

        left, right = st.columns(2)
        roc_fig = go.Figure()
        roc_fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="Modelo"))
        roc_fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Azar", line=dict(dash="dash")))
        roc_fig.update_layout(title="Curva ROC", xaxis_title="1 - Especificidad", yaxis_title="Sensibilidad", height=400)
        left.plotly_chart(roc_fig, use_container_width=True)
        cm_df = pd.DataFrame(cm, index=["Real: no incumple", "Real: incumple"], columns=["Predice: no", "Predice: sí"])
        heat = px.imshow(cm_df, text_auto=True, aspect="auto", title="Matriz de confusión")
        heat.update_layout(height=400)
        right.plotly_chart(heat, use_container_width=True)
        st.info("Una mayor AUC indica mejor capacidad de ordenar clientes de menor a mayor riesgo. Antes de usar un modelo real deben revisarse estabilidad, sesgo, calibración, explicabilidad y validación independiente.")

    with tab3:
        c1, c2, c3 = st.columns(3)
        score = c1.slider("Score", 300, 900, 650)
        dti = c2.slider("Deuda / ingreso", 0.0, 1.0, 0.38, 0.01)
        mora_dias = c3.slider("Días de mora", 0, 180, 10)
        c4, c5 = st.columns(2)
        ingreso = c4.number_input("Ingreso mensual", 450.0, 30000.0, 1500.0, 50.0)
        antig = c5.slider("Antigüedad como cliente (meses)", 1, 240, 36)
        z = -7.0 + 0.011*(650-score) + 2.0*dti + 0.018*mora_dias - 0.000035*ingreso
        pd_ind = float(np.clip(1/(1+np.exp(-z)), .002, .75))
        n1, n2 = st.columns([1,2])
        n1.metric("PD estimada a 12 meses", f"{pd_ind:.2%}")
        n2.success(f"Nivel didáctico: **{nivel_riesgo(pd_ind)}**. La decisión crediticia real no debe basarse únicamente en esta estimación.")

elif pagina == "Pérdida esperada":
    hero("Pérdida esperada", "Cuantificación didáctica mediante PD, LGD y EAD")
    st.markdown('<div class="formula">Pérdida esperada (EL) = PD × LGD × EAD</div>', unsafe_allow_html=True)
    st.write("")
    st.info("La fórmula enseña que el riesgo no depende solo de la probabilidad de impago: también importa la pérdida ante incumplimiento y la exposición al momento del evento.")
    render_preguntas_clave([
        {
            "title": "¿Qué cambia cuando sube el multiplicador de PD?",
            "body": "Aumenta la probabilidad de que el cliente incumpla; por tanto, la pérdida esperada se eleva si se mantiene el resto de factores constantes.",
        },
        {
            "title": "¿Por qué LGD y EAD son importantes?",
            "body": "El LGD indica cuánto se pierde si el cliente incumple; el EAD mide la exposición efectiva. Dos carteras con la misma PD pueden tener pérdidas muy diferentes si una tiene exposiciones más grandes o recuperaciones peores.",
        },
    ])
    df = cartera_demo.copy()
    c1, c2, c3 = st.columns(3)
    mult_pd = c1.slider("Multiplicador de PD", 0.5, 3.0, 1.0, 0.1)
    mult_lgd = c2.slider("Multiplicador de LGD", 0.7, 1.8, 1.0, 0.1)
    mult_ead = c3.slider("Multiplicador de EAD", 0.8, 1.3, 1.0, 0.05)
    df["pd_escenario"] = (df["pd_12m"] * mult_pd).clip(upper=1)
    df["lgd_escenario"] = (df["lgd"] * mult_lgd).clip(upper=1)
    df["ead_escenario"] = df["ead"] * mult_ead
    df["el_escenario"] = df["pd_escenario"] * df["lgd_escenario"] * df["ead_escenario"]

    base = df["perdida_esperada"].sum()
    estres = df["el_escenario"].sum()
    a,b,c,d = st.columns(4)
    a.metric("EL base", formato_dinero(base))
    b.metric("EL escenario", formato_dinero(estres), delta=f"{(estres/base-1):.1%}")
    c.metric("EL / cartera", f"{estres/df['saldo'].sum():.2%}")
    d.metric("Exposición EAD", formato_dinero(df["ead_escenario"].sum()))

    resumen = df.groupby("segmento", as_index=False).agg(
        EAD=("ead_escenario","sum"),
        PD=("pd_escenario","mean"),
        LGD=("lgd_escenario","mean"),
        EL=("el_escenario","sum"),
    )
    fig = px.bar(resumen, x="segmento", y="EL", color="PD", text_auto=".3s",
                 labels={"EL":"Pérdida esperada", "PD":"PD promedio"})
    fig.update_layout(height=430)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(resumen.style.format({"EAD":"${:,.0f}", "PD":"{:.2%}", "LGD":"{:.2%}", "EL":"${:,.0f}"}), use_container_width=True)
    download_excel(resumen, "perdida_esperada_escenario.xlsx")

elif pagina == "Riesgo de liquidez":
    hero("Riesgo de liquidez", "Brechas contractuales, concentración de fondeo y escenarios de salida de depósitos")
    st.warning("La liquidez no se mide solo con el saldo disponible: también importa el momento en que vencen los pasivos, la estabilidad de los depósitos y la rapidez con la que se pueden convertir activos en efectivo.")
    base = load_liquidity()
    salida = st.slider("Salida extraordinaria de pasivos de corto plazo", 0, 40, 10, 1) / 100
    liquidos = st.number_input("Activos líquidos disponibles", 1_000_000.0, 200_000_000.0, 58_000_000.0, 1_000_000.0)
    df = base.copy()
    df["pasivos_escenario"] = df["pasivos"]
    df.loc[df.index[:2], "pasivos_escenario"] *= (1 + salida)
    df["brecha_escenario"] = df["activos"] - df["pasivos_escenario"]
    df["acumulada_escenario"] = df["brecha_escenario"].cumsum()
    necesidad_30 = max(0, -df.loc[:1, "brecha_escenario"].sum())
    cobertura = liquidos / necesidad_30 if necesidad_30 else np.inf

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Brecha 1–7 días", formato_dinero(df.loc[0,"brecha_escenario"]))
    c2.metric("Brecha acumulada 30 días", formato_dinero(df.loc[:1,"brecha_escenario"].sum()))
    c3.metric("Necesidad de liquidez", formato_dinero(necesidad_30))
    c4.metric("Cobertura con líquidos", "Sin déficit" if np.isinf(cobertura) else f"{cobertura:.1f}x")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["banda"], y=df["activos"], name="Activos"))
    fig.add_trace(go.Bar(x=df["banda"], y=-df["pasivos_escenario"], name="Pasivos"))
    fig.add_trace(go.Scatter(x=df["banda"], y=df["acumulada_escenario"], name="Brecha acumulada", mode="lines+markers", yaxis="y2"))
    fig.update_layout(
        barmode="relative", height=460, title="Brechas de liquidez por bandas",
        yaxis_title="Flujos", yaxis2=dict(title="Brecha acumulada", overlaying="y", side="right"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("La enseñanza debe complementar las brechas con concentración de depositantes, estabilidad de fuentes, activos líquidos, planes de contingencia, límites y pruebas de tensión.")
    download_excel(df, "brechas_liquidez.xlsx")

elif pagina == "Riesgo de mercado":
    hero("Riesgo de mercado", "Valor en Riesgo, volatilidad y sensibilidad del valor económico ante tasas")
    st.success("En esta pantalla la idea central es entender que una pérdida esperada por volatilidad no sustituye la realidad de un escenario extremo; la cola de distribución también importa.")
    rng = np.random.default_rng(15)
    fechas = pd.date_range("2024-01-01", periods=520, freq="B")
    retornos = pd.Series(rng.normal(0.00015, 0.0075, len(fechas)), index=fechas)
    exposicion = st.number_input("Exposición del portafolio", 100_000.0, 500_000_000.0, 25_000_000.0, 500_000.0)
    confianza = st.select_slider("Nivel de confianza", options=[0.90,0.95,0.975,0.99], value=0.95, format_func=lambda x: f"{x:.1%}")
    horizonte = st.slider("Horizonte (días)", 1, 20, 1)
    vh = var_historico(retornos, confianza, exposicion) * np.sqrt(horizonte)
    vp = var_parametrico(retornos, confianza, exposicion) * np.sqrt(horizonte)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("VaR histórico", formato_dinero(vh))
    c2.metric("VaR paramétrico", formato_dinero(vp))
    c3.metric("Volatilidad diaria", f"{retornos.std():.2%}")
    c4.metric("Horizonte", f"{horizonte} día(s)")

    precios = exposicion * (1 + retornos).cumprod()
    fig = px.line(x=precios.index, y=precios.values, labels={"x":"Fecha","y":"Valor simulado"}, title="Evolución simulada del portafolio")
    fig.update_layout(height=410)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Sensibilidad a tasas de interés")
    c1,c2,c3 = st.columns(3)
    duracion = c1.slider("Duración modificada", 0.1, 8.0, 2.8, 0.1)
    choque_pb = c2.slider("Choque de tasa (puntos básicos)", -500, 500, 200, 25)
    convexidad = c3.slider("Convexidad", 0.0, 30.0, 8.0, 0.5)
    dy = choque_pb / 10000
    cambio_pct = -duracion * dy + 0.5 * convexidad * dy**2
    cambio_valor = exposicion * cambio_pct
    st.metric("Variación aproximada del valor económico", formato_dinero(cambio_valor), delta=f"{cambio_pct:.2%}")
    st.warning("El VaR no representa la pérdida máxima posible. Debe complementarse con backtesting, límites, análisis de colas y escenarios extremos.")

elif pagina == "Riesgo operativo":
    hero("Riesgo operativo", "Eventos, pérdidas, controles y matriz de criticidad")
    st.info("Aquí se observa una diferencia clave: un evento puede ser raro, pero si tiene alta severidad y un control débil, puede volverse material para la organización.")
    df = load_operational()
    proceso = st.multiselect("Procesos", sorted(df["proceso"].unique()), default=sorted(df["proceso"].unique()))
    df = df[df["proceso"].isin(proceso)].copy()
    df["riesgo_inherente"] = df["probabilidad"] * df["impacto"]
    factor = df["control_efectivo"].map({"Sí":0.35, "Parcial":0.65, "No":1.0})
    df["riesgo_residual"] = df["riesgo_inherente"] * factor

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Eventos", f"{len(df):,}")
    c2.metric("Pérdida acumulada", formato_dinero(df["perdida"].sum()))
    c3.metric("Pérdida promedio", formato_dinero(df["perdida"].mean()))
    c4.metric("Controles no efectivos", f"{(df['control_efectivo']=='No').mean():.1%}")

    matriz = df.groupby(["probabilidad","impacto"], as_index=False).agg(
        eventos=("tipo_evento","count"), perdida=("perdida","sum")
    )
    fig = px.scatter(
        matriz, x="probabilidad", y="impacto", size="perdida", color="eventos",
        text="eventos", size_max=55, range_x=[0.5,5.5], range_y=[0.5,5.5],
        title="Matriz de riesgo inherente",
    )
    fig.update_layout(height=440)
    st.plotly_chart(fig, use_container_width=True)

    top = df.groupby("tipo_evento", as_index=False).agg(
        eventos=("tipo_evento","count"), perdida=("perdida","sum"),
        riesgo_residual=("riesgo_residual","mean")
    ).sort_values("perdida", ascending=False)
    st.dataframe(top.style.format({"perdida":"${:,.0f}", "riesgo_residual":"{:.2f}"}), use_container_width=True)
    download_excel(df, "eventos_riesgo_operativo.xlsx")

elif pagina == "Pruebas de estrés":
    hero("Pruebas de estrés integradas", "Impacto de choques macrofinancieros simulados sobre pérdidas, liquidez y solvencia")
    st.markdown("Ajuste los choques y observe cómo se transmite el riesgo.")
    st.warning("La educación del estrés no consiste sólo en aumentar el choque; se trata de analizar la transmisión desde la economía hasta el patrimonio y la liquidez de la entidad.")
    c1,c2,c3 = st.columns(3)
    desempleo = c1.slider("Aumento del desempleo (pp)", 0.0, 8.0, 2.0, 0.5)
    caida_pib = c2.slider("Caída del PIB (%)", 0.0, 12.0, 3.0, 0.5)
    retiro = c3.slider("Retiro de depósitos (%)", 0.0, 35.0, 12.0, 1.0)
    c4,c5 = st.columns(2)
    alza_tasas = c4.slider("Aumento de tasas (pb)", 0, 600, 200, 25)
    perdida_operativa = c5.slider("Choque operativo extraordinario (USD)", 0, 10_000_000, 1_000_000, 250_000)

    df = cartera_demo.copy()
    factor_pd = 1 + desempleo*0.12 + caida_pib*0.08
    pd_stress = (df["pd_12m"] * factor_pd).clip(upper=1)
    lgd_stress = (df["lgd"] * (1 + caida_pib*0.018)).clip(upper=1)
    el_base = df["perdida_esperada"].sum()
    el_stress = (pd_stress * lgd_stress * df["ead"]).sum()
    perdida_mercado = 25_000_000 * 2.8 * (alza_tasas/10000)
    salida_depositos = 360_000_000 * retiro/100
    liquidez_disponible = 72_000_000
    deficit_liquidez = max(0, salida_depositos-liquidez_disponible)
    patrimonio = 64_000_000
    impacto_total = (el_stress-el_base) + perdida_mercado + perdida_operativa
    patrimonio_post = patrimonio-impacto_total
    activos_ponderados = 510_000_000
    solvencia = patrimonio_post/activos_ponderados

    a,b,c,d = st.columns(4)
    a.metric("EL bajo estrés", formato_dinero(el_stress), delta=f"{el_stress/el_base-1:.1%}")
    b.metric("Pérdida de mercado", formato_dinero(perdida_mercado))
    c.metric("Déficit de liquidez", formato_dinero(deficit_liquidez))
    d.metric("Solvencia simulada", f"{solvencia:.2%}", delta=f"{solvencia-patrimonio/activos_ponderados:.2%}")

    puente = pd.DataFrame({
        "Componente":["Patrimonio inicial","Incremento pérdida crédito","Pérdida mercado","Evento operativo","Patrimonio final"],
        "Valor":[patrimonio, -(el_stress-el_base), -perdida_mercado, -perdida_operativa, patrimonio_post],
        "Medida":["absolute","relative","relative","relative","total"],
    })
    fig = go.Figure(go.Waterfall(
        x=puente["Componente"], y=puente["Valor"], measure=puente["Medida"],
        text=[formato_dinero(v) for v in puente["Valor"]], textposition="outside"
    ))
    fig.update_layout(title="Transmisión del escenario al patrimonio", height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.error("Resultado didáctico. Una prueba institucional debe definir escenarios plausibles pero severos, horizonte, supuestos, canales de transmisión, capacidad de respuesta y acciones del plan de contingencia.")

elif pagina == "Laboratorio de datos":
    hero("Laboratorio de datos", "Cargue una cartera propia anonimizada o utilice la base demostrativa")
    st.warning("No cargue nombres, cédulas, cuentas, teléfonos, direcciones ni datos personales. Use información anonimizada y autorizada.")
    st.info("Aquí se practica el principio de análisis reproducible: primero revisar calidad, luego visualizar y finalmente preparar el dato para métricas o modelos.")
    archivo = st.file_uploader("Archivo CSV o Excel", type=["csv","xlsx"])
    if archivo:
        try:
            if archivo.name.lower().endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)
            st.success(f"Archivo cargado: {len(df):,} filas y {len(df.columns)} columnas.")
        except Exception as e:
            st.error(f"No fue posible leer el archivo: {e}")
            df = cartera_demo.copy()
    else:
        df = cartera_demo.copy()
        st.info("Se está utilizando la cartera sintética incluida.")

    st.dataframe(df.head(200), use_container_width=True)
    st.markdown("### Perfil de calidad")
    calidad = pd.DataFrame({
        "variable": df.columns,
        "tipo": [str(t) for t in df.dtypes],
        "nulos": df.isna().sum().values,
        "nulos_pct": (df.isna().mean()*100).round(2).values,
        "unicos": df.nunique(dropna=True).values,
    })
    st.dataframe(calidad, use_container_width=True)
    numeric = df.select_dtypes(include=np.number)
    if not numeric.empty:
        variable = st.selectbox("Variable numérica para explorar", numeric.columns)
        fig = px.histogram(df, x=variable, nbins=40, marginal="box")
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
    download_excel(calidad, "reporte_calidad_datos.xlsx")

elif pagina == "Marco ecuatoriano":
    hero("Marco institucional ecuatoriano", "Orientación para ubicar los modelos dentro de la gestión y supervisión")
    st.info("La práctica no termina en una métrica. Un buen análisis hace conexión entre modelos, gobierno, protección de datos y responsabilidades de la autoridad institucional.")
    st.markdown("""
### Dos ámbitos de supervisión

**Bancos y entidades de los sectores financieros público y privado:** su marco de
control comprende la gestión integral y la administración de riesgos de crédito,
mercado, liquidez, operativo y otros riesgos relacionados.

**Cooperativas de ahorro y crédito y mutualistas:** están sujetas al marco del
sector financiero popular y solidario, con normas, resoluciones y guías emitidas
por los organismos competentes y con requerimientos diferenciados según su
naturaleza y segmento.

### Gobierno mínimo que debe enseñarse junto al modelo

1. Responsabilidades del directorio o consejo, alta gerencia, comité y unidad de riesgos.
2. Políticas, apetito, límites, metodologías, fuentes de datos y documentación.
3. Validación independiente, control interno, auditoría y trazabilidad.
4. Alertas tempranas, planes de acción, contingencia y comunicación.
5. Protección de datos, seguridad de la información y continuidad del negocio.

### Referencias oficiales para consulta

- Superintendencia de Bancos: Codificación de Normas, Libro I, gestión y administración de riesgos.
- Superintendencia de Economía Popular y Solidaria: resoluciones y estadísticas del SFPS.
- Junta de Política y Regulación Financiera y Registro Oficial: resoluciones vigentes.

> Revise siempre la versión vigente antes de convertir un ejemplo educativo en
> una política, límite, metodología o reporte institucional.
""")
    glosario = pd.DataFrame({
        "Término":["PD","LGD","EAD","EL","VaR","KRI","Backtesting","Stress testing","Riesgo inherente","Riesgo residual"],
        "Definición":[
            "Probabilidad de incumplimiento.",
            "Pérdida dado el incumplimiento.",
            "Exposición al momento del incumplimiento.",
            "Pérdida esperada: PD × LGD × EAD.",
            "Estimación de pérdida para un horizonte y nivel de confianza.",
            "Indicador clave de riesgo.",
            "Comparación de resultados del modelo con observaciones reales.",
            "Evaluación bajo escenarios adversos severos pero plausibles.",
            "Riesgo antes de considerar controles.",
            "Riesgo que permanece después de aplicar controles.",
        ]
    })
    st.dataframe(glosario, hide_index=True, use_container_width=True)
