
#proyecto simulador de ahorros

#importar librerias
import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt

st.title("💰 Simulador de Ahorro e Inversión")
st.markdown("""
Simula el crecimiento de tu capital mensual considerando ahorro e inversión.
""")

with st.sidebar:
    ingreso_mensual = st.number_input("💵 Ingreso mensual (DOP)", min_value=0, value=70000)
    gasto_mensual = st.number_input("💸 Gasto mensual (DOP)", min_value=0, value=50000)
    tasa_interes = st.slider("📈 Tasa de interés anual esperada (%)", 0.0, 20.0, 8.0)
    years = st.slider("⏳ Número de años", 1, 30, 5)

capital = []
ahorro_mensual = ingreso_mensual - gasto_mensual
meses = years * 12
interes_mensual = (1 + tasa_interes / 100) ** (1/12) - 1
monto = 0

for mes in range(1, meses + 1):
    monto = monto * (1 + interes_mensual) + ahorro_mensual
    capital.append(monto)

df = pd.DataFrame({
    "Mes": list(range(1, meses + 1)),
    "Capital acumulado": capital
})

st.line_chart(df.set_index("Mes"))
st.write(f"💼 Capital acumulado al final de {years} años: {capital[-1]:,.2f} DOP")


