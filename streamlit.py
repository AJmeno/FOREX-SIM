import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import ta

# Set page configuration
st.set_page_config(page_title="Forex Trading Simulator", layout="wide")

# Fetch forex data
def fetch_forex_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty or data.isnull().values.any():
            st.warning("Data has missing values. Handling missing data may be required.")
        return data
    except (ValueError, yf.exceptions.YahooFinanceError) as e:
        st.error(f"Error fetching data: {e}")
        return None

# Calculate PnL for a single trade
def calculate_pnl(initial_balance, trade_size, entry_price, exit_price, leverage):
    margin = trade_size / leverage
    pnl = (exit_price - entry_price) * trade_size * leverage
    return pnl

# Implement dollar cost averaging
def dollar_cost_average(initial_balance, trade_size, entry_prices, leverage):
    balance = initial_balance
    total_trade_size = 0
    avg_entry_price = 0
    prices = []
    avg_prices = []

    for price in entry_prices:
        exit_price = price * 1.01  # Assume a 1% profit
        pnl = calculate_pnl(balance, trade_size, price, exit_price, leverage)
        balance += pnl
        total_trade_size += trade_size
        avg_entry_price = (avg_entry_price * (total_trade_size - trade_size) + price * trade_size) / total_trade_size
        prices.append(price)
        avg_prices.append(avg_entry_price)

    margin = total_trade_size / leverage
    return balance, avg_entry_price, margin, prices, avg_prices

# Streamlit app
st.title("Forex Trading Simulator")

# Validate user inputs
start_date = st.date_input("Start Date", value=pd.Timestamp("2022-01-01"))
end_date = st.date_input("End Date", value=pd.Timestamp("2023-01-01"))
if start_date >= end_date:
    st.error("Start date must be before end date.")
    return

initial_balance = st.number_input("Initial Balance (USD)", min_value=1000.0, step=100.0, value=10000.0)
if initial_balance <= 0:
    st.error("Initial balance must be a positive number.")
    return

trade_size = st.number_input("Trade Size (EUR)", min_value=1000.0, step=100.0, value=5000.0)
if trade_size <= 0:
    st.error("Trade size must be a positive number.")
    return

leverage = st.number_input("Leverage", min_value=1.0, max_value=50.0, step=1.0, value=50.0)
if leverage < 1 or leverage > 50:
    st.error("Leverage must be between 1 and 50.")
    return

num_trades = st.number_input("Number of Trades", min_value=1, step=1, value=5)

# Fetch and display forex data
forex_pair = st.selectbox("Select Forex Pair", ["USD/EUR", "USD/JPY", "EUR/JPY"])
forex_data = fetch_forex_data(forex_pair, start_date, end_date)
if forex_data is not None:
    st.subheader(f"{forex_pair} Price")
    st.line_chart(forex_data["Close"])

# Simulate trades
entry_prices = []
for i in range(num_trades):
    entry_price = st.number_input(f"Entry Price {i+1}", min_value=1.0, step=0.0001, value=1.1000)
    if entry_price <= 0:
        st.error(f"Entry price {i+1} must be a positive number.")
        return
    entry_prices.append(entry_price)

if len(set(entry_prices)) == 1:
    st.warning("All entry prices are the same. Dollar cost averaging may not be effective.")

if st.button("Simulate Trades"):
    final_balance, avg_entry_price, margin, prices, avg_prices = dollar_cost_average(initial_balance, trade_size, entry_prices, leverage)
    pnl = final_balance - initial_balance
    st.write(f"Final Balance: ${final_balance:.2f}")
    st.write(f"Profit/Loss: ${pnl:.2f}")
    st.write(f"Average Entry Price: {avg_entry_price:.4f}")
    st.write(f"Margin Used: ${margin:.2f}")

    # Plot the average entry price and current price over time
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(prices, label="Current Price")
    ax.plot(avg_prices, label="Average Entry Price")
    ax.set_xlabel("Trade Number")
    ax.set_ylabel("Price")
    ax.set_title("Dollar Cost Averaging")
    ax.legend()
    st.pyplot(fig)
