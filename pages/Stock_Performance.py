import streamlit as st
import pandas as pd
import altair as alt


########################################## PAGE SETUP ###########################################

st.title('Stock Performance')

########################################## DATA LOAD #############################################

annual_returns = pd.read_csv('plan_kaggle/annual_returns1.csv')
extra = pd.read_csv('plan_yahoo/extrainfo.csv')
annual_returns['annual_return'] = annual_returns['annual_return'].round(2) # Does not work. 
pivoted_df = annual_returns.pivot(index='symbol', columns='year', values='annual_return')

######################################  DISPLAY TOP 10 #############################################

st.markdown("""
Explore the top-performing and worst stocks based annual return and historical data. 
Select a year to view the top 5 best-performing and worst-performing stocks for that period. 
This allows you to analyze market trends and gain insights into stock performance over time.
""")

# Sidebar for year selection
year = st.selectbox("Select a year for annual return performance", [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]) 

#Title
st.subheader("Top 5 Stock Performance")

# Sort by the selected year and get top 10
top_df = pivoted_df.sort_values(by=year, ascending=False).head(5)
top_df = top_df.reset_index()
top_df.index = top_df.index + 1
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

###################################  WORSE 10  PERFORMANCE #############################################

#Title
st.subheader("Worst 5 Stock Performance")

# Sort by the selected year and get top 5
worst_df = pivoted_df.sort_values(by=year, ascending=True).head(5)
worst_df = worst_df.reset_index()
worst_df.index = worst_df.index + 1
worst_df.columns.name = None
# Create a dictionary
name_dict = dict(zip(extra['symbol'], extra['shortName']))
worst_df['shortName'] = worst_df['symbol'].map(name_dict)
worst_df = worst_df.rename(columns={
    'symbol': 'Ticker',
    'shortName':'Company'
})

# Display the top 5 table
st.table(worst_df[["Ticker",'Company', year]].round(2))


#############################################  TRIAL #############################################


### ✅ Create a combined dataframe for plotting
top_df["Category"] = "Top 5"
worst_df["Category"] = "Worst 5"

# Merge the top and worst dataframes
combined_df = pd.concat([top_df, worst_df])

# Rename the selected year column to "Annual Return" for clarity
combined_df = combined_df.rename(columns={year: "Annual Return"})
combined_df = combined_df.sort_values("Annual Return", ascending=True)

# 🔥 **Altair Bar Chart with Dynamic Colors**
chart = (
    alt.Chart(combined_df)
    .mark_bar()
    .encode(
        x=alt.X("Ticker:N", sort=combined_df["Annual Return"].tolist()),
        y="Annual Return:Q",
        color=alt.condition(
            alt.datum["Annual Return"] > 0,  
            alt.value("#1E90FF"),  # Blue for positive values
            alt.value("#FF6347"),  # Red for negative values
        ),
        tooltip=["Ticker", "Company", "Annual Return"]
    )
    .properties(title=f"Top & Worst 5 Stocks in {year}")
)

# Display the chart
st.altair_chart(chart, use_container_width=True)