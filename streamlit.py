import streamlit as st

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

def main():
    st.title("Currency Pair Profit/Loss Calculator")
    
    entries = []
    
    st.subheader("Entry Points")
    num_entries = st.number_input("Number of Entry Points", min_value=1, value=1)
    for i in range(num_entries):
        entry_price = st.number_input(f"Entry Price {i+1}", value=0.0, step=0.0001)
        units = st.number_input(f"Units {i+1}", min_value=0, value=0, step=1)
        entries.append((entry_price, units))
    
    exit_price = st.number_input("Exit Price", value=0.0, step=0.0001)
    
    if st.button("Add Entry Point"):
        entry_price = st.number_input("New Entry Price", value=0.0, step=0.0001)
        units = st.number_input("New Units", min_value=0, value=0, step=1)
        entries.append((entry_price, units))
        
    if st.button("Calculate"):
        if entries:
            profit_loss, average_price = calculate_profit_loss(entries, exit_price)
            st.write(f"Total Profit/Loss: {profit_loss}")
            st.write(f"Average Entry Price: {average_price}")
        else:
            st.write("Please input at least one entry point.")

if __name__ == "__main__":
    main()
