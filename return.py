import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import plotly.express as px
import plotly.graph_objects as go
import function

# Set up the Streamlit page configuration
st.set_page_config(
    page_title = 'CAPM',  # Title of the web page
    page_icon = 'chart_with_upwards_trend',  # Icon for the web page
    layout = 'wide'  # Use the wide layout for the app
)

# Display the main title of the app
st.title('Capital Asset Pricing Model (CAPM)')

# Section to get user input

# Create two columns for input widgets
col1, col2 = st.columns([1,1])

with col1 : 
    # Multiselect widget for users to choose 4 stocks to analyze
    stocks_list = st.multiselect(
        "Choose up to n number of stocks to analyze",
        (
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'MGM', 'NVDA', 'META',
            'NFLX', 'BRK-B', 'JPM', 'V', 'UNH', 'HD', 'PG', 'DIS'
        ),
        ['TSLA', 'AAPL', 'AMZN', 'GOOGL']  # Default selected stocks
    )

with col2 :
    # Number input widget for users to select number of years to analyze
    no_of_years = st.number_input(
        'Number of years to analyze',
        min_value=1,
        max_value=10
    )
    
# downloading data for SP500

try:
    # Get today's date as the end date for data download
    end = datetime.date.today()
    # Calculate the start date by subtracting the number of years selected by the user
    start = datetime.date(end.year - no_of_years, end.month, end.day)
    # Download S&P 500 index data from FRED between start and end dates
    SP500 = web.DataReader(['sp500'], 'fred', start, end) 
    
    # It uses the FRED database (Federal Reserve Economic Data) to download historical S&P 500 index values. ['sp500'] is the code used by FRED for S&P 500.
    # S&P500 is a stock market index that tracks the performance of the 500 largest publicly traded companies in the United States.
    # If it goes up, it usually means the economy or market is doing well.
    # We can use it in CAPM to see if your chosen stock is riskier or more stable than the market.

    # Create an empty DataFrame to store stock prices
    stocks_df = pd.DataFrame()

    # Loop through each selected stock and download its historical closing prices
    for stock in stocks_list:
        data = yf.download(stock, period=f'{no_of_years}y')
        stocks_df[f'{stock}'] = data['Close']
        
    #  Why use only Close?
    # 1. It reflects the true value of the stock at the end of the day.
    # 2. It’s consistent and less noisy than highs/lows.
    # 3. Most financial indicators (returns, trends, etc.) are based on closing prices    

    # Reset the index of the stock prices DataFrame so that the 'Date' becomes a normal column instead of the index
    stocks_df.reset_index(inplace=True)

    # Reset the index of the S&P 500 DataFrame so that its 'DATE' column becomes a regular column for merging
    SP500.reset_index(inplace=True)

    # Rename S&P 500 columns for clarity
    SP500.columns = ['Date', 'sp500'] 
    # When we fetch S&P 500 data using web.DataReader, The column is originally named sp500, but the index (the date) is not labeled.
    
    # Convert the 'Date' column to datetime format for merging
    stocks_df['Date'] = stocks_df["Date"].apply(lambda x: str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    # Merge stock prices and S&P 500 data on the 'Date' column
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # Create two columns in the Streamlit app for displaying data
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Dataframe head')
        # Show the first few rows of the merged DataFrame
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown('### Dataframe tail')
        # Show the last few rows of the merged DataFrame
        st.dataframe(stocks_df.tail(), use_container_width=True)

    # Create two columns for plotting
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Price of Stocks')
        # Plot the raw stock prices
        st.plotly_chart(function.interactive_plot(stocks_df))
    with col2:
        st.markdown('### Normalized Price of Stocks')
        # Plot the normalized stock prices for comparison
        st.plotly_chart(function.interactive_plot(function.normalize_prices(stocks_df)))
        
        # Normalization means:
        # Making all stock prices start from the same value (usually 1 or 100), so you can compare how much they have grown or dropped over time on the same scale.

        # Why is this useful in CAPM or portfolio analysis?
        # 1. Helps to visually compare relative performance.
        # 2. Makes it easier to spot which stock grew faster or fell more over the same period.
        # 3. Helps in choosing better-performing assets.
        

    # Calculate daily returns for each stock and the S&P 500
    stocks_daily_return = function.daily_returns(stocks_df)

    # Dictionaries to store beta and alpha values for each stock
    beta = {}
    alpha = {}

    # Calculate beta and alpha for each stock (excluding 'Date' and 'sp500' columns)
    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            # Calculate beta and alpha using the helper function
            b, a = function.calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    # Create a DataFrame to display beta values
    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    # Round beta values to 2 decimal places for display
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    with col1:
        st.markdown('### Beta Values')
        # Show the beta values for each stock
        st.dataframe(beta_df, use_container_width=True)
        

    # Set risk-free rate (rf) to 0 for simplicity
    rf = 0
    # Calculate the expected market return (rm) as the mean daily return of S&P 500 annualized (252 trading days)
    rm = stocks_daily_return['sp500'].mean() * 252

    # Create a DataFrame to store the calculated CAPM returns
    return_df = pd.DataFrame()
    return_value = []
    
    # Calculate expected return for each stock using the CAPM formula: E(Ri) = rf + beta_i * (rm - rf)
    for stock, value in beta.items():
        return_value.append(round(rf + value * (rm - rf), 2))
        # Expected Return = Risk-Free Rate + Beta * (Expected Market Return - Risk-Free Rate)
        
    # Assign stock names and their calculated returns to the DataFrame
    return_df['Stock'] = list(beta.keys())  # safer than using stocks_list directly
    return_df['Return Value'] = return_value

    with col2:
        st.markdown('### Calculated Returns using CAPM')
        # Show the calculated expected returns for each stock
        st.dataframe(return_df, use_container_width=True)
        
    # Sample equal weights if user doesn't input custom weights
    equal_weight = 1 / len(stocks_list)

    # Assign equal weights to each stock
    weights = {stock: equal_weight for stock in stocks_list}

    # Fill any missing values in return_df using forward fill, then backward fill as a fallback
    return_df = return_df.ffill().bfill()

    # Calculate portfolio return as weighted average of expected returns
    portfolio_return = sum(weights[stock] * (rf + beta[stock] * (rm - rf)) for stock in stocks_list)
    
        
    st.markdown("---")  # horizontal line separator
    st.markdown("## 📊 CAPM Results Summary")

    # Display a summary of the CAPM results
    with st.expander(" 📌 Key CAPM Metrics", expanded=True):
        # Calculate the annualized risk-free rate using 10-year US Treasury yield from FRED
        rf_data = web.DataReader('DGS10', 'fred', start, end)
        rf_data = rf_data.fillna(method='ffill')
        rf = rf_data['DGS10'].iloc[-1] / 100  # Convert percent to decimal

        st.markdown(f"""
        <div style="font-size: 2em; font-weight: bold; color: #2E86C1;">
            Risk-Free Rate (rf): <span style="color:#117A65; font-size:1.2em; font-weight:bold;">{round(rf * 100, 2)}%</span>
        </div>
        <div style="font-size: 2em; font-weight: bold; color: #2E86C1;">
            Expected Market Return (rm): <span style="color:#117A65; font-size:1.2em; font-weight:bold;">{round(rm * 100, 2)}%</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:1.7em; font-weight:bold; margin-top:20px;">Expected Returns for Selected Stocks:</div>', unsafe_allow_html=True)
        for stock, ret in zip(return_df['Stock'], return_df['Return Value']):
            st.markdown(
                f'<div style="font-size:1.5em; font-weight:bold; color:#884EA0;">{stock}: <span style="color:#117A65; font-size:1.2em; font-weight:bold;">{round(ret * 100, 2)}%</span></div>',
                unsafe_allow_html=True
            )
    # Plot Beta values
    beta_plot_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Beta': list(beta.values())
    })

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📉 Beta Values Plot")
    st.plotly_chart(px.bar(beta_plot_df, x='Stock', y='Beta', title='Beta Values by Stock', color='Stock'))

    # Plot Alpha values
    alpha_plot_df = pd.DataFrame({
        'Stock': list(alpha.keys()),
        'Alpha': list(alpha.values())
    })

    st.markdown("### 📈 Alpha Values Plot")
    st.plotly_chart(px.bar(alpha_plot_df, x='Stock', y='Alpha', title='Alpha Values by Stock', color='Stock'))
    
    st.markdown("### 📊 Portfolio vs Market Return")
    # Display expected market and portfolio return with larger font
    st.markdown(f"""
    <div style="font-size:2em; font-weight:bold; color:#2E86C1;">
        Expected Market Return (rm): <span style="color:#117A65; font-size:1.2em; font-weight:bold;">{round(rm*100, 2)}%</span>
    </div>
    <div style="font-size:2em; font-weight:bold; color:#2E86C1;">
        Expected Portfolio Return: <span style="color:#117A65; font-size:1.2em; font-weight:bold;">{round(portfolio_return*100, 2)}%</span>
    </div>
    """, unsafe_allow_html=True)

    # Visual plot: Portfolio vs Market Return
    
    # Line plot: Expected Return vs Stock Tickers, with Market Return in red
    fig = go.Figure()
    # Expected Return (blue)
    fig.add_trace(
        go.Scatter(
            x=return_df['Stock'],
            y=[ret * 100 for ret in return_df['Return Value']],
            mode='lines+markers',
            name='Expected Return',
            line=dict(color='#2E86C1', width=3),
            marker=dict(size=10)
        )
    )
    # Market Return (red, horizontal line)
    fig.add_trace(
        go.Scatter(
            x=return_df['Stock'],
            y=[rm * 100] * len(return_df['Stock']),
            mode='lines',
            name='Market Return',
            line=dict(color='red', width=2, dash='dash')
        )
    )
    fig.update_layout(
        title='Expected Return by Stock (CAPM)',
        xaxis_title='Stock Ticker',
        yaxis_title='Expected Return (%)',
        width=1200,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    # Center the plot using Streamlit columns
    center_col1, center_col2, center_col3 = st.columns([1,2,1])
    with center_col2:
        st.plotly_chart(fig, use_container_width=False)


except :
    # If any error occurs (e.g., invalid input), display a message to the user
    st.write("Please enter valid inputs.")
    
    

