import pandas as pd 

def load_prices ():
    prices_df = pd.read_csv('plan_yahoo/historical_prices_final.csv')
    prices_df.drop(columns='Unnamed: 0', inplace=True)
    prices_df['timestamps'] = pd.to_datetime(prices_df['timestamps']).dt.normalize()
    return prices_df