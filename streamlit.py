import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

def calculate_profit_loss(entries, exit_price):
    total_cost = 0
    total_units = 0
    
    for entry in entries:
        entry_price, units = entry
        total_cost += entry_price * units
        total_units += units
    
    average_price = total_cost / total_units
    profit_loss = (exit_price - average_price) * total_units
    
    return profit_loss, average_price

def plot_eur_usd_chart():
    # Fetch EUR/USD data from Yahoo Finance
    eur_usd = yf.download("EURUSD=X", start="2023-01-01", end="2024-04-07")
    
    # Create the chart
    fig = go.Figure(data=[go.Candlestick(
        x=eur_usd.index,
        open=eur_usd['Open'],
        high=eur_usd['High'],
        low=eur_usd['Low'],
        close=eur_usd['Close']
    )])
    
    fig.update_layout(
        title="EUR/USD Forex Pair",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    
    return fig

def main():
    st.title("Currency Pair Profit/Loss Calculator")
    
    # Display the EUR/USD chart
    st.plotly_chart(plot_eur_usd_chart(), use_container_width=True)
    
    entries = []
    
    st.subheader("Entry Points")
    num_entries = st.number_input("Number of Entry Points", min_value=1, value=1)
    for i in range(num_entries):
        entry_price = st.number_input(f"Entry Price {i+1}", value=0.0, step=0.00001, format="%.5f")
        units = st.number_input(f"Units {i+1}", min_value=0, value=0, step=1)
        entries.append((entry_price, units))
    
    exit_price = st.number_input("Exit Price", value=0.0, step=0.00001)
    
    if st.button("Add Entry Point"):
        entry_price = st.number_input("New Entry Price", value=0.0, step=0.00001, format="%.5f")
        units = st.number_input("New Units", min_value=0, value=0, step=1)
        entries.append((entry_price, units))
        
    if st.button("Calculate"):
        if entries:
            profit_loss, average_price = calculate_profit_loss(entries, exit_price)
            st.write(f"Total Profit/Loss: {profit_loss:.5f}")
            st.write(f"Average Entry Price: {average_price:.5f}")
        else:
            st.write("Please input at least one entry point.")

if __name__ == "__main__":
    main()
