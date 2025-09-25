# proyecto simulador de ahorros

# importar librerías
import streamlit as st
import pandas as pd

st.image("logo.png", width=160)
st.title("💰 Simulador de Ahorro e Inversión")
st.markdown("""
Simula el crecimiento de tu capital mensual considerando ahorro e inversión.
""")

with st.sidebar:
    nombre = st.text_input("👤 Ingresa tu nombre", value="", placeholder="Ej. Andrés")
    ingreso_mensual = st.number_input("💵 Ingreso mensual (DOP)", min_value=0, value=70000, step=1000)
    gasto_mensual   = st.number_input("💸 Gasto mensual (DOP)",   min_value=0, value=50000, step=1000)
    tasa_interes    = st.slider("📈 Tasa de interés anual esperada (%)",
                                min_value=0.0, max_value=30.0, value=10.0, step=0.1)
    years           = st.slider("⏳ Número de años", min_value=1, max_value=30, value=5, step=1)

# Validación: nombre obligatorio antes de continuar
if not nombre.strip():
    st.info("👋 Escribe tu nombre en la barra lateral para ver la simulación.")
    st.stop()

# Cálculos
ahorro_mensual = ingreso_mensual - gasto_mensual
meses = years * 12

# Interés mensual efectivo a partir de la tasa anual (dividir entre 100 SOLO una vez)
interes_mensual = (1 + tasa_interes / 100) ** (1/12) - 1

monto = 0.0
capital = []
for mes in range(1, meses + 1):
    # capital del mes anterior crece por interés y se suma el ahorro de ese mes
    monto = monto * (1 + interes_mensual) + ahorro_mensual
    capital.append(monto)

df = pd.DataFrame({
    "Mes": list(range(1, meses + 1)),
    "Capital acumulado (DOP)": capital
})

# Mensajes útiles
if ahorro_mensual <= 0:
    st.warning("⚠️ Tus gastos son mayores o iguales a tus ingresos. La proyección podría estancarse o decrecer.")

st.markdown(
    f"**{nombre}**, tu proyección final a **{years} año{'s' if years>1 else ''}** "
    f"es de **{monto:,.2f} DOP** con una **tasa anual de {tasa_interes:.2f}%**."
)

# Gráfico
st.line_chart(df, x="Mes", y="Capital acumulado (DOP)")

# Resumen final
st.write(f"💼 Capital acumulado al final de {years} año{'s' if years>1 else ''}: **{capital[-1]:,.2f} DOP**")
