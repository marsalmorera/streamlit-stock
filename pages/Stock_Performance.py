import streamlit as st
import pandas as pd


############################################# PAGE SETUP ###########################################

st.title('Best Stock Performance')

############################################# DATA LOAD #############################################

annual_returns = pd.read_csv('plan_kaggle/annual_returns.csv')
extra = pd.read_csv('plan_yahoo/extrainfo.csv')
pivoted_df = annual_returns.pivot(index='symbol', columns='year', values='annual_return')

############################################# INFO DISPLAY #############################################

# Sidebar for year selection
year = st.selectbox("Select a year for annual return performance", [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]) 

# Sort by the selected year and get top 5
top_df = pivoted_df.sort_values(by=year, ascending=False).head(5)
top_df = top_df.reset_index()
top_df.columns.name = None
# Create a dictionary
name_dict = dict(zip(extra['symbol'], extra['shortName']))
top_df['shortName'] = top_df['symbol'].map(name_dict)
top_df = top_df.rename(columns={
    'symbol': 'Ticker',
    'shortName':'Company'
})

# Display the top 5 table
st.table(top_df[["Ticker",'Company', year]])