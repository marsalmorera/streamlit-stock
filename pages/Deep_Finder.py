import streamlit as st
import pandas as pd
import altair as alt
from utils import load_prices


########################################## PAGE SETUP ###########################################

st.title('Deep Finder 2024')

########################################## DATA LOAD #############################################

annual_returns = pd.read_csv('plan_kaggle/annual_returns1.csv')
extra = pd.read_csv('plan_yahoo/extrainfo.csv')
annual_returns['annual_return'] = annual_returns['annual_return'].round(2) # Does not work. 
pivoted_df = annual_returns.pivot(index='symbol', columns='year', values='annual_return')
symbls = pd.read_csv('plan_yahoo/info_0_500.csv')
symbols = symbls['symbol'].unique()
prices_df = load_prices()

############################################# INFO DISPLAY #############################################


# Select stock(s) using the multiselect box
stock_selection = st.multiselect(
    "Choose your stocks for analysis:", 
    symbols, 
    default=['AAPL', 'MSFT']
)

# Filter the data based on the selected stock(s)
selected_df = pivoted_df[pivoted_df.index.isin(stock_selection)]

######################################  DISPLAY SELECTED STOCKS #############################################

# Sidebar for year selection (fixed to 2024)
year = 2024

# Title
# st.subheader(f"Deep Finder in {year}")

# Create a dictionary for company names
name_dict = dict(zip(extra['symbol'], extra['shortName']))

# Add short names to the selected dataframe
selected_df = selected_df.reset_index()
selected_df['shortName'] = selected_df['symbol'].map(name_dict)

# Rename columns
selected_df = selected_df.rename(columns={'symbol': 'Ticker', 'shortName': 'Company'})

####################################  CHART FOR SELECTED STOCKS ###########################################

# Create a new column for the annual return
selected_df['Annual Return'] = selected_df[year]
selected_df = selected_df.sort_values(by=year, ascending=False)
selected_df = selected_df.reset_index()
selected_df.index = selected_df.index + 1

st.write("")
# 🔥 **Altair Bar Chart with Dynamic Colors**
chart = (
    alt.Chart(selected_df)
    .mark_bar()
    .encode(
        x=alt.X("Ticker:N", sort=selected_df['Annual Return'].tolist()),
        y="Annual Return:Q",
        color=alt.condition(
            alt.datum["Annual Return"] > 0,  
            alt.value("#1E90FF"),  # Blue for positive values
            alt.value("#FF6347"),  # Red for negative values
        ),
        tooltip=["Ticker", "Company", "Annual Return"]
    )
    .properties(title=f"Stocks Performance in {year} (Annual Return %)")
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

# Display the selected stocks and their annual returns
st.table(selected_df[['Ticker', 'Company', year]])