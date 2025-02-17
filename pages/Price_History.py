import streamlit as st
import pandas as pd
from utils import load_prices


############################################# PAGE SETUP ###########################################

st.title('Price History')

############################################# DATA LOAD #############################################

symbls = pd.read_csv('plan_yahoo/info_0_500.csv')
symbols = symbls['symbol'].unique()
prices_df = load_prices()

############################################# INFO DISPLAY #############################################

# Select a stock using the select box

stock_selection = st.multiselect("Choose a stock for analysis:", symbols, default=['AAPL', 'MSFT']) # Add more colors for display.

# Filter the dataframe based on the selected symbol
filtered_df = prices_df[prices_df['symbol'].isin(stock_selection)]

# Display the line chart of historical prices
st.line_chart(filtered_df.pivot(index='timestamps', columns='symbol', values='price'))

