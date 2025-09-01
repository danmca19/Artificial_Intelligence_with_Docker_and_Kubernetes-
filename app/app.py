# Imports
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Carregar o modelo
model = joblib.load("model.pkl")

# Configuração da página do Streamlit
st.set_page_config(page_title="AI Deployment Project", page_icon="🤖", layout="wide")

# Barra lateral com instruções
st.sidebar.header("📘 Instructions")
st.sidebar.info("""
This application predicts whether an **industrial machine** requires maintenance.  

➡️ Enter the machine's parameters below and click **Predict**.
""")

# Título principal
st.markdown("<h1 style='text-align: center;'>🛠 Industrial Maintenance Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>AI-driven predictive maintenance for smarter operations</h4>", unsafe_allow_html=True)

# Campos para entrada dos dados
st.subheader("🔧 Machine Parameters")
col1, col2 = st.columns(2)

with col1:
    temperatura = st.number_input("🌡 Temperature (°C)", value=25.0)
    pressao = st.number_input("⏲ Pressure (bar)", value=1.0)
    horas_operacao = st.number_input("⏳ Operating Hours", value=100.0)

with col2:
    vibracao = st.number_input("📈 Vibration (mm/s)", value=0.5)
    ruido = st.number_input("🔊 Noise Level (dB)", value=60.0)

# Botão de previsão
if st.button("🚀 Predict", use_container_width=True):

    input_array = np.array([[temperatura, pressao, horas_operacao, vibracao, ruido]])
    prediction = model.predict(input_array)
    prediction_proba = model.predict_proba(input_array)[0]

    # Resultado
    st.subheader("📌 Prediction Result")
    if prediction[0] == 1:
        st.error("⚠️ **Maintenance Required!**")
        status = "Maintenance Required"
    else:
        st.success("✅ **Machine Operating Normally. No Maintenance Needed.**")
        status = "Machine OK"

    # Probabilidades
    st.subheader("📊 Probability by Class")

    # Gráfico de barras
    fig, ax = plt.subplots()
    classes = ["Machine OK", "Maintenance Required"]
    ax.barh(classes, prediction_proba, color=["green", "red"])
    ax.set_xlim(0, 1)
    ax.set_xlabel("Probability")
    for i, v in enumerate(prediction_proba):
        ax.text(v + 0.01, i, f"{v*100:.1f}%", va="center")
    st.pyplot(fig)

    # Gráfico estilo velocímetro
    st.subheader("🎯 Maintenance Risk Gauge")
    gauge_value = prediction_proba[1] * 100
    st.progress(int(gauge_value))
    st.write(f"**Risk of Maintenance Need:** {gauge_value:.2f}%")

    # 📋 Tabela resumo
    st.subheader("📋 Input Summary & Prediction")
    data = {
        "Temperature (°C)": [temperatura],
        "Pressure (bar)": [pressao],
        "Operating Hours": [horas_operacao],
        "Vibration (mm/s)": [vibracao],
        "Noise (dB)": [ruido],
        "Predicted Status": [status],
        "Probability (Maintenance)": [f"{prediction_proba[1]*100:.2f}%"],
    }
    df = pd.DataFrame(data)
    st.table(df)
