import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

############################################### PAGE SETUP ###########################################
# 1. Title
st.title("Annual Return Stock Tracker")

# 2. Header
st.header("Do you want to beat the S&P500 Index?")

# 3. Subheader
st.subheader("This is a Subheader")

# 4. Text
st.text("Streamlit makes it easy to create web apps for data science.")

# 5. Selectbox
symbls = pd.read_csv('info_0_250.csv')
annual_returns = pd.read_csv('annual_returns.csv')
symbols = symbls['symbol'].unique()

# Select Box. 
select_symbol = st.selectbox("Choose a stock for analysis:", symbols)
 
# Displays
website = symbls.loc[symbls['symbol'] == select_symbol, 'website'].values[0]
sector = symbls.loc[symbls['symbol'] == select_symbol, 'sector'].values[0]
summary = symbls.loc[symbls['symbol'] == select_symbol, 'longBusinessSummary'].values[0]


#Display Slect Box. 
st.write(f"You selected: {select_symbol}")
st.write(f'Sector: {sector}')
st.markdown(f'Information: {summary}')
st.write("Check out their website [link](%s)" % website) # Difference between markdown and write. 

############################################### Tab 1 ###########################################

st.subheader("Chart")
def annual_return_plot(annual_returns, stock=select_symbol):
    # Filter the DataFrame for both the selected symbol (stock) and SP500
    symbols_to_plot = annual_returns[annual_returns["symbol"].isin([stock, 'SP500'])]
    
    # If no data is found for the selected stock or SP500, print a warning and exit the function
    if symbols_to_plot.empty:
        print(f"⚠️ No data available for {stock} or SP500.")
        return
    
    # Pivot the DataFrame to structure it for plotting: 
    # Index will be the 'year', columns will be the 'symbol', and values will be the 'annual_return'
    df_pivot = symbols_to_plot.pivot(index="year", columns="symbol", values="annual_return")
    
    # Define custom colors: SP500 will always be red, and the selected stock will be blue
    colors = {'SP500': '#FF0000', stock: '#0000FF'}

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot the annual return data for the selected symbol and SP500 over the years
    for i, symbol in enumerate(df_pivot.columns):
        plt.plot(df_pivot.index, df_pivot[symbol], marker='o', label=symbol, color=colors[symbol])

    # Title and labels for the plot
    plt.title(f"Annual Return Comparison: {stock} vs SP500", fontsize=14, fontweight='bold', color="#5F9EA0")
    plt.xlabel("Year", fontsize=12, fontweight='bold', color="#1E90FF")
    plt.ylabel("Annual Return (%)", fontsize=12, fontweight='bold', color="#4682B4")
    plt.legend(title="Symbol", title_fontsize=12, fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Show the plot
    st.pyplot(plt.gcf())

# Automatically update the chart when a different symbol is selected
if select_symbol:
    annual_return_plot(annual_returns, stock=select_symbol)

# 8. Button
if st.button("Click Me"):
    st.write("Button clicked!")

