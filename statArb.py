import numpy as np
import pandas as pd
import yfinance as yf

# Define the tickers of the two stocks
stock1 = 'V'
stock2 = 'MA'

# Download the historical stock data
data = yf.download([stock1, stock2], start='2010-01-01', end='2022-03-20', group_by='ticker')

# Calculate the rolling correlation coefficient between the two stocks
window_size = 60
close_prices = pd.DataFrame()
for ticker in [stock1, stock2]:
    close_prices[ticker] = data[ticker]['Close']
corr = close_prices[stock1].rolling(window_size).corr(close_prices[stock2])

# Define the entry and exit thresholds
entry_threshold = 0.8
exit_threshold = 0.6

# Define the position size and stop loss
position_size = 10
stop_loss = 0.02

# Initialize the trading positions and account balance
position1 = 0
position2 = 0
balance = 0

# Iterate over the data and make trading decisions
for i in range(window_size, len(data)):
    # Check if the correlation coefficient is above the entry threshold
    if corr[i] > entry_threshold:
        # If so, short stock1 and buy stock2
        position1 = -position_size / data[stock1]['Close'][i]
        position2 = position_size / data[stock2]['Close'][i]
    # Check if the correlation coefficient is below the exit threshold
    elif corr[i] < exit_threshold:
        # If so, close the positions
        position1 = 0
        position2 = 0
    # Otherwise, maintain the current positions
    else:
        pass
    
    # Calculate the daily returns
    returns1 = position1 * (data[stock1]['Close'][i] - data[stock1]['Close'][i-1])
    returns2 = position2 * (data[stock2]['Close'][i] - data[stock2]['Close'][i-1])
    
    # Calculate the total daily returns
    total_returns = returns1 + returns2
    
    # Apply the stop loss
    if total_returns < -balance * stop_loss:
        total_returns = -balance * stop_loss
    
    # Update the account balance
    balance += total_returns
    
    # Print the total returns and account balance for the day
    print('Total Returns: ', total_returns)
    print('Account Balance: ', balance)
