import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_prices
from utils import load_average_return

############################################# PAGE SETUP ###########################################

# Set up the page
st.set_page_config(
    page_title="Stock Tracker",
    layout="centered", # or wide. Better centered. 
    page_icon="📈", 
    initial_sidebar_state="collapsed" # or expanded
)

############################################# DATA LOAD #############################################

symbls = pd.read_csv('plan_yahoo/info_0_500.csv')
annual_returns = pd.read_csv('plan_kaggle/annual_returns1.csv')
extra = pd.read_csv('plan_yahoo/extrainfo.csv')
symbols = symbls['symbol'].unique()
pivoted_df = annual_returns.pivot(index='symbol', columns='year', values='annual_return')
prices_df = load_prices()
average_df = load_average_return()

############################################# USER INPUTS ###########################################

# 1. Title
st.title("Annual Return Stock Tracker")

# 2. Subheader
st.subheader("Do you want to beat the S&P500 Index?")

# 3. Text 
st.markdown("""
This app allows you to compare the annual return of a stock from the S&P 500 index with the stock itself. 
You can select any stock from the S&P 500 and see how its performance compares to the overall index. 
This comparison can help you understand the stock's growth relative to the market and decide if it's outperforming the index!
""")

##################################### Info ###########################################

# 4 Select Box. 
select_symbol = st.selectbox("Choose a stock for analysis:", symbols)
 
 #################################### Info ############################################

name_symbol = extra.loc[extra['symbol'] == select_symbol, 'shortName'].values[0]
website = symbls.loc[symbls['symbol'] == select_symbol, 'website'].values[0]
sector = symbls.loc[symbls['symbol'] == select_symbol, 'sector'].values[0]
industry = symbls.loc[symbls['symbol'] == select_symbol, 'industry'].values[0]
summary = symbls.loc[symbls['symbol'] == select_symbol, 'longBusinessSummary'].values[0]
current_price = extra.loc[extra['symbol'] == select_symbol, 'regularMarketPrice'].values[0]
average_return = average_df.loc[average_df['symbol'] == select_symbol, 'average_return'].values[0]
average_return_SP500 = average_df.loc[average_df['symbol'] == "SP500", 'average_return'].values[0]

 ################################ METRIC CARDS ###########################################

return_difference = average_return - average_return_SP500

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Stock Price", f"{current_price}$")

with col2: 
    st.metric("10-Year Return", f"{average_return * 100:.2f}%",delta=f"{return_difference * 100:.2f}%")

with col3: 
    st.metric("SP500 10-Year Return", f"{average_return_SP500 * 100:.2f}%")


##################################### Display ###########################################
st.write("") 
#Display Slect Box. 
st.markdown(f'You have chosen **{name_symbol}**, a company in the **{sector}** sector, with **{industry}** as its primary industry.')

with st.expander("See Information"):
    st.markdown(f'Information: {summary}')
st.write("Check out their website [link](%s)" % website) # Difference between markdown and write. 

##################################### Tab 1 ###########################################

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
