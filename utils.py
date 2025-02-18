import pandas as pd 

def load_prices ():
    prices_df = pd.read_csv('plan_yahoo/historical_prices_final.csv')
    prices_df.drop(columns='Unnamed: 0', inplace=True)
    prices_df['timestamps'] = pd.to_datetime(prices_df['timestamps']).dt.normalize()
    return prices_df

def load_average_return ():
    df = pd.read_csv('plan_kaggle/sp500_stocks.csv')
    sp = pd.read_csv('plan_kaggle/sp500_index.csv')

    # Cleaning columns with snake_case 
    df.columns = [col.lower().replace(" ", "_")for col in df.columns] 
    sp.columns = [col.lower().replace(" ", "_")for col in sp.columns]

    # Delete NaN.
    df.dropna(how='any', inplace=True)
    df.drop(columns=['high', 'low', 'open','close','volume'], inplace=True)

    # Change to datetime from stocks. 
    df['date'] = pd.to_datetime(df['date']) 
    sp['date'] = pd.to_datetime(sp['date'])

    sp['symbol'] = "SP500"
    
    sp.rename(columns={'s&p500':'price',}, inplace=True)
    df.rename(columns={'adj_close':'price',}, inplace=True)

    cols = ['date', 'symbol', 'price']
    sp = sp[cols]

    final_df = pd.concat([df, sp], axis=0)

    final_df['year'] = final_df['date'].dt.year
    final_df['month'] = final_df['date'].dt.month
    final_df['day'] = final_df['date'].dt.day

    final_df.drop(final_df[(final_df['year'] >= 2010) & (final_df['year'] <= 2013)].index, inplace=True)

    final_df.drop(columns=['date'], inplace=True)

    filtered_data = final_df[(final_df['year'] >= 2014) & (final_df['year'] <= 2024)]

    # Get the first and last adjusted close prices for each symbol
    first_last_prices = filtered_data.groupby('symbol').agg(
        first_price=('price', 'first'),
        last_price=('price', 'last')).reset_index()

    # Calculate the annual return from the first and last prices
    first_last_prices['average_return'] = (first_last_prices['last_price'] / first_last_prices['first_price']) - 1
    return first_last_prices