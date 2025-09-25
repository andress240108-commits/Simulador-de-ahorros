import streamlit as st
import pandas as pd

# ===== Configuración de página =====
st.set_page_config(page_title="Simulador de Ahorro e Inversión",
                   page_icon="💰",
                   layout="centered",
                   initial_sidebar_state="expanded")  # cambia a "collapsed" si prefieres

# ===== Estado inicial =====
if "show_controls" not in st.session_state:
    st.session_state.show_controls = True
if "resultado" not in st.session_state:
    st.session_state.resultado = None  # guardará (df, monto, years, nombre, tasa)

# ===== Encabezado =====
st.image("logo.png", width=160)
st.title("💰 Simulador de Ahorro e Inversión")
st.markdown("Simula el crecimiento de tu capital mensual considerando ahorro e inversión.")

# ===== Sidebar (controles) =====
if st.session_state.show_controls:
    with st.sidebar:
        nombre = st.text_input("👤 Ingresa tu nombre", value="", placeholder="Ej. Andrés")
        ingreso_mensual = st.number_input("💵 Ingreso mensual (DOP)", min_value=0, value=70000, step=1000)
        gasto_mensual   = st.number_input("💸 Gasto mensual (DOP)",   min_value=0, value=50000, step=1000)

        # Ahorro preliminar = ingreso - gasto (base para el slider de "monto_ahorrado")
        ahorro_mensual_prelim = max(0, ingreso_mensual - gasto_mensual)

        # opciones de ahorro

        opciones_ahorro = list(range(0, int(ahorro_mensual_prelim)+1000, 1000))
        # El usuario puede decidir cuánto de su "ahorro preliminar" aporta realmente cada mes
        monto_ahorrado = st.select_slider(
            "🏦 Aporte mensual a inversión (DOP)",
            options=opciones_ahorro,
            value=ahorro_mensual_prelim if ahorro_mensual_prelim in opciones_ahorro else 0
    )
        

        tasa_interes = st.slider(
            "📈 Tasa de interés anual esperada (%)",
            min_value=0.0, max_value=30.0, value=10.0, step=0.1
        )
        years = st.slider("⏳ Número de años", min_value=1, max_value=30, value=5, step=1)

        # Botón Calcular
        calcular = st.button("🧮 Calcular", type="primary")

    # Validaciones y acción del botón
    if calcular:
        if not nombre.strip():
            st.info("👋 Escribe tu nombre en la barra lateral para calcular la simulación.")
            st.stop()

        # Cálculos
        meses = years * 12
        interes_mensual = (1 + tasa_interes / 100) ** (1/12) - 1

        monto = 0.0
        capital = []
        for _mes in range(1, meses + 1):
            monto = monto * (1 + interes_mensual) + monto_ahorrado
            capital.append(monto)

        df = pd.DataFrame({"Mes": list(range(1, meses + 1)),
                           "Capital acumulado (DOP)": capital})

        # Guardar resultado en sesión
        st.session_state.resultado = (df, monto, years, nombre, tasa_interes, monto_ahorrado)

        # "Ocultar" controles dejando el sidebar vacío
        st.session_state.show_controls = False
        st.rerun()

# ===== Mostrar resultados (cuando ya se calculó) =====
if st.session_state.resultado is not None and not st.session_state.show_controls:
    df, monto, years, nombre, tasa_interes, monto_ahorrado = st.session_state.resultado

    # Mensajes
    if monto_ahorrado == 0:
        st.warning("⚠️ Tu aporte mensual a inversión es 0. Aumenta el valor para ver crecimiento del capital.")

    st.markdown(
        f"**{nombre}**, aportando **{monto_ahorrado:,.0f} DOP/mes**, "
        f"tu proyección final a **{years} año{'s' if years>1 else ''}** "
        f"es de **{monto:,.2f} DOP** con una **tasa anual de {tasa_interes:.2f}%**."
    )

    st.line_chart(df, x="Mes", y="Capital acumulado (DOP)")
    st.write(f"💼 Capital acumulado al final de {years} año{'s' if years>1 else ''}: **{df['Capital acumulado (DOP)'].iloc[-1]:,.2f} DOP**")

    # Botón para volver a mostrar controles
    if st.button("🔧 Modificar parámetros"):
        st.session_state.show_controls = True
        st.rerun()
