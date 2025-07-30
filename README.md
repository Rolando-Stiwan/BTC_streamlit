# 📈 Predicción de Señales de Trading para Bitcoin (BTC)

Este proyecto es una aplicación web construida con **Streamlit** que predice señales de trading **BUY** / **SELL** para el precio de Bitcoin (BTC). Utiliza una red neuronal LSTM entrenada previamente, datos históricos financieros, indicadores técnicos y correlaciones con el índice **S&P 500**.

---

## 🚀 Funcionalidades

- Consulta automática de precios históricos de **BTC** y **S&P 500** desde `yfinance`.
- Cálculo de indicadores técnicos: `SMA`, `RSI`, `MACD`.
- Predicción de señales **BUY / SELL** usando un modelo LSTM desplegado vía API.
- Interfaz web interactiva con visualización de gráficos y tablas.

---

## 🧠 Modelo de Predicción

El modelo LSTM fue entrenado previamente sobre una ventana deslizante de precios BTC, y expone una API REST que devuelve la señal de trading para los últimos datos.

---

## 📦 Requisitos

Instala los requisitos usando:

```bash
pip install -r requirements.txt

🤝 Créditos
Desarrollado por Rolando Stiwan — Científico de Datos con enfoque en finanzas cuantitativas, deep learning y riesgo.

⚠️ Disclaimer
Este proyecto es educativo y no constituye asesoría financiera. Invertir en criptomonedas conlleva riesgos.