import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime


# App Configuration
st.set_page_config(page_title="Stock Price App", layout="wide")

# Title and Description
st.title("📈 Stock Price Web Application")
st.markdown("""
This application allows you to visualize the stock price data for various companies.
You can select a company ticker, date range, and choose the type of chart you'd like to see.
""")

# Sidebar for User Inputs
st.sidebar.header("User Input Parameters")

def get_user_input():
    ticker = st.sidebar.text_input("Ticker Symbol", "AAPL").upper()
    start_date = st.sidebar.date_input("Start Date", datetime(2022, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime.today())
    chart_type = st.sidebar.selectbox("Chart Type", ("Line", "Candlestick", "OHLC"))
    return ticker, start_date, end_date, chart_type

ticker, start_date, end_date, chart_type = get_user_input()

# Fetching Data
@st.cache_data
def fetch_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Loading data...")
data = fetch_data(ticker, start_date, end_date)
data_load_state.text("Loading data...done!")

# Display Data
st.subheader(f"Raw Data for {ticker}")
st.write(data.tail())


# Plotting Data

st.subheader(f"{ticker} Price Chart")

if chart_type == "Line":
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close'))
    fig.update_layout(title=f"{ticker} Closing Price Over Time",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)")
elif chart_type == "Candlestick":
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title=f"{ticker} Candlestick Chart",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)")
elif chart_type == "OHLC":
    fig = go.Figure(data=[go.Ohlc(x=data['Date'],
                                  open=data['Open'],
                                  high=data['High'],
                                  low=data['Low'],
                                  close=data['Close'])])
    fig.update_layout(title=f"{ticker} OHLC Chart",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)")
else:
    st.error("Unsupported chart type selected.")

st.plotly_chart(fig, use_container_width=True)


# Additional Insights

st.subheader("Additional Metrics")

# Calculate Moving Averages
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

# Display Moving Averages
st.write(data[['Date', 'Close', 'MA20', 'MA50']].tail())

# Plot Moving Averages
fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close'))
fig_ma.add_trace(go.Scatter(x=data['Date'], y=data['MA20'], mode='lines', name='MA 20'))
fig_ma.add_trace(go.Scatter(x=data['Date'], y=data['MA50'], mode='lines', name='MA 50'))
fig_ma.update_layout(title=f"{ticker} Closing Price with Moving Averages",
                     xaxis_title="Date",
                     yaxis_title="Price (USD)")
st.plotly_chart(fig_ma, use_container_width=True)
