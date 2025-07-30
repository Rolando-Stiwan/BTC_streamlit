import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
import matplotlib.dates as mdates

API_URL = "https://btc-6vq9.onrender.com/predict"

# --- Función para cargar datos históricos ---
@st.cache_data(ttl=3600)
def cargar_datos_btc(period='100d', interval='1d'):
    df = yf.download("BTC-USD", period=period, interval=interval)
    df = df[["Close"]].copy()
    df.reset_index(inplace=True)
    df.rename(columns={"Close": "Price", "Date": "Fecha"}, inplace=True)
    return df

# Datos sp500
@st.cache_data(ttl=3600)
def cargar_datos_sp500(period='100d', interval='1d'):
    df = yf.download("^GSPC", period=period, interval=interval)
    df = df[["Close"]].copy()
    df.reset_index(inplace=True)
    df.rename(columns={"Close": "Price", "Date": "Fecha"}, inplace=True)
    return df


# --- Función para calcular indicadores técnicos ---
def calcular_indicadores(df):
    df['SMA_5'] = df['Price'].rolling(window=5).mean()

    price_series = df['Price']
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.iloc[:, 0]
    rsi_indicator = RSIIndicator(price_series, window=14)
    df['RSI_14'] = rsi_indicator.rsi()

    macd = MACD(price_series)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    
    return df

# --- Función para obtener señales de la API ---
def obtener_senales(days):
    try:
        response = requests.get(API_URL, params={"days": days})
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                return None, data["error"]
            else:
                return data, None
        else:
            return None, f"Error al consultar API. Código: {response.status_code}"
    except Exception as e:
        return None, f"Error inesperado: {str(e)}"

# --- Función para mostrar tabla de señales ---
def mostrar_tabla_senales(df_signals):
    tabla_html = df_signals.to_html(index=False)
    html = f"""
    <div style="display: flex; justify-content: center; margin-top: 10px;">
        <div style="width: 300px; font-size: 22px;">
            {tabla_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- Función para graficar ---
def graficar(df_plot, signals):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True,
                                        gridspec_kw={'height_ratios': [3, 1, 1]})
    plt.subplots_adjust(hspace=0.05)
    
    # Precio + SMA 5
    ax1.plot(df_plot["Fecha"], df_plot["Price"], label="Precio BTC", color='black')
    ax1.plot(df_plot["Fecha"], df_plot["SMA_5"], label="SMA 5", color='blue', linestyle='--')
    ax1.set_title("Precio BTC con SMA 5")
    ax1.set_ylabel("USD")
    ax1.grid(True)
    ax1.legend()

    # RSI
    ax2.plot(df_plot["Fecha"], df_plot["RSI_14"], label="RSI 14", color='purple')
    ax2.axhline(70, color='red', linestyle='--', linewidth=1)
    ax2.axhline(30, color='green', linestyle='--', linewidth=1)
    ax2.set_ylim(0, 100)
    ax2.set_yticks([0, 30, 70, 100])
    ax2.set_ylabel("RSI")
    ax2.grid(True)
    ax2.legend()

    # MACD
    ax3.plot(df_plot["Fecha"], df_plot["MACD"], label="MACD", color='blue')
    ax3.plot(df_plot["Fecha"], df_plot["MACD_signal"], label="Señal MACD", color='orange', linestyle='--')
    ax3.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax3.set_ylabel("MACD")
    ax3.set_xlabel("Fecha")
    ax3.grid(True)
    ax3.legend()

    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    fig.autofmt_xdate()

    st.pyplot(fig)


    # --- Gráfico S&P 500 con indicadores ---
    df_sp = cargar_datos_sp500()
    df_sp = calcular_indicadores(df_sp)

    fig3, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    # Precio
    ax1.plot(df_sp["Fecha"], df_sp["Price"], label="S&P 500", color='green')
    ax1.set_title("S&P 500 - Precio")
    ax1.grid(True)

    # RSI
    ax2.plot(df_sp["Fecha"], df_sp["RSI_14"], label="RSI 14", color='purple')
    ax2.axhline(70, linestyle='--', color='red')
    ax2.axhline(30, linestyle='--', color='blue')
    ax2.set_title("RSI 14")
    ax2.grid(True)

    # MACD
    ax3.plot(df_sp["Fecha"], df_sp["MACD"], label="MACD", color='blue')
    ax3.plot(df_sp["Fecha"], df_sp["MACD_signal"], label="Signal", color='orange')
    ax3.set_title("MACD")
    ax3.legend()
    ax3.grid(True)

    fig3.tight_layout()

    st.pyplot(fig3)




# --- Función principal ---
def main():
    st.set_page_config(page_title="Predicción BTC", layout="wide")
    st.title("🔍 Predicción de Señales BTC")

    df_hist = cargar_datos_btc()
    df_hist = calcular_indicadores(df_hist)

    days = st.slider("Selecciona días a predecir (BUY/SELL)", min_value=1, max_value=7, value=3)

    if st.button("🔮 Predecir señales"):
        data, error = obtener_senales(days)
        if error:
            st.warning(error)
        else:
            st.success("✅ Predicción recibida correctamente.")
            current_price = data["current_price"]
            signals = data["signals"]

            st.markdown(f"### Precio actual BTC: **${current_price:,.2f}**")

            df_signals = pd.DataFrame({
                "Día": range(1, len(signals) + 1),
                "Señal": signals
            })

            st.markdown("### 🔁 Señales próximas")
            mostrar_tabla_senales(df_signals)

            st.markdown("### 📈 Precio histórico de BTC (últimos 100 días)")
            df_plot = df_hist.copy()
            graficar(df_plot, signals)

if __name__ == "__main__":
    main()