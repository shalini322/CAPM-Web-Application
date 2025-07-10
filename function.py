import plotly.express as px
import numpy as np

# function to create an interactive line plot
# that takes a DataFrame with a 'Date' column and multiple stock price columns

def interactive_plot(df):
    # Create an empty Plotly line figure
    fig = px.line()
    
    # Loop through all stock columns (skip the first column, which is 'Date')
    for i in df.columns[1:]:
        # Add each stock's time series as a separate line in the plot
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    
    # Customize the layout of the plot (size, margins, legend position)
    fig.update_layout(
        width=450,  # Width of the chart
        margin=dict(l=20, r=20, t=50, b=20),  # Set margins (left, right, top, bottom)
        legend=dict(
            orientation="h",  # horizontal legend
            yanchor="bottom", y=1.02,         # place the legend slightly above the plot
            xanchor="right", x=1              # align the legend to the right
        )
    )
    
    # Return the final figure to be shown in Streamlit
    return fig


def normalize_prices(df):
    df_copy = df.copy()
    # Loop through each stock column (skip 'Date' which is at index 0)
    for i in df_copy.columns[1:]:
        # Divide every value in the column by the first value in that column
        # This makes the first value = 1, and everything else relative to that
        df_copy[i] = df_copy[i] / df_copy[i][0]
    
    # Return the modified DataFrame with normalized values
    return df_copy


# function to calculate daily returns
def daily_returns(df):
    # Create a copy of the original DataFrame to avoid modifying it
    df_ret = df.copy()
    
    # Loop through each column except the first one (which is 'Date')
    for i in df.columns[1:]:
        # Calculate daily percentage change for each column
        # .pct_change() gives (today - yesterday) / yesterday
        # .fillna(0) fills the first row which will have NaN
        # Multiply by 100 to convert from decimal to percent
        df_ret[i] = df_ret[i].pct_change().fillna(0) * 100

    # Return the modified DataFrame with daily returns
    return df_ret


# function to calculate the beta of a stock

# stock return = alpha + (beta × market return) + error
# Predicted_Stock_Return = α + β × Market_Return
# error = Actual_Stock_Return - Predicted_Stock_Return
# Where:
# - alpha is the intercept (performance unexplained by the market)
# - beta is the slope (sensitivity to market)
# - error is the random noise or unexplained part

def calculate_beta(stock_daily_returns, stock):
    
    # Calculate the expected annual return of the market (rm)
    
    # This column contains the percentage change in the S&P 500 for each trading day
    daily_market_returns = stock_daily_returns['sp500']

    # Calculate the average daily return of the market
    average_daily_market_return = daily_market_returns.mean()

    # Multiply by 252 (number of trading days in a year) to annualize it. This gives the expected annual return of the market
    rm = average_daily_market_return * 252
    
    # x = Independent variable → market returns (S&P 500)
    x = daily_market_returns
    
    # y = Dependent variable → returns of the selected stock
    y = stock_daily_returns[stock]
    
    b, a = np.polyfit(x, y, deg=1)
    return b, a


# Beta (β) measures how much a stock's return changes in response to market movements.
# It tells us how volatile the stock is compared to the overall market (like the S&P 500).
# Interpretation:
# - β = 1   → Stock moves exactly like the market.
# - β > 1   → Stock is more volatile (amplifies market movements).
# - β < 1   → Stock is less volatile (moves less than the market).
# - β = 0   → Stock is not affected by the market (e.g., cash, gold).
# - β < 0   → Stock moves in the opposite direction of the market (rare case).

# Alpha (α) measures the stock's performance independent of the market.
# It tells us whether the stock has overperformed or underperformed relative to what CAPM predicts.
# Interpretation:
# - α > 0   → Stock outperformed the market (gave extra return).
# - α < 0   → Stock underperformed (did worse than expected).
# - α = 0   → Stock performed exactly as the model predicted (neutral).

