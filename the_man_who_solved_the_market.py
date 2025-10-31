## Modeling Market Dynamics as Stochastic Processes on Curved Manifolds: A Quantitative Study
# This script is inspired by the concepts talked about in the book 'The Man Who Solved the Market' by Gregory Zuckerman
# and explores the modeling of market dynamics using stochastic processes on curved manifolds, inspired by the concept of holonomy.
# The goal is to provide a quantitative framework for understanding complex market behaviors through geometric and probabilistic lenses.

# Introduction
"""
This script explores the modeling of market dynamics using stochastic processes on curved manifolds, inspired by the concept of
holonomy.The goal is to provide a quantitative framework for understanding complex market behaviors through geometric and
probabilistic lenses.

First, we define the mathematical framework for a flat market model using Brownian Motion, which serves as a baseline.
We then extend this model to incorporate curvature, simulating a market influenced by geometric constraints.

The Brownian Motion model is defined on a flat manifold, representing a simplified market scenario
"""

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

## Download the historical data for SPY (S&P 500 ETF)
ticker = 'SPY'

# Download historical 2023 data for SPY from Yahoo Finance. Include last month of 2022 to allow a month of warm up period for the Rolling Sharpe Ratio to be calculated
data = yf.download(ticker, start='2022-12-01', end='2024-01-01')

# Get the closing prices
prices = data['Close'].values.flatten()

# Grab only 2023 dates, as only 2023 dates will be plotted
data_2023 = data.loc['2023-01-01':'2023-12-31']
prices_2023 = data_2023['Close'].values.flatten()  # This will now be ~252 trading days

# Calculate daily returns
daily_returns = np.diff(prices) / prices[:-1]

# Define the parameters for the Brownian Motion model
annual_mu = np.mean(daily_returns) * 252  # Annualized mean return
annual_sigma = np.std(daily_returns) * np.sqrt(252)  # Annualized volatility

# Simulate a Brownian Motion path
def simulate_brownian_motion(start_price, num_steps=252, mu=annual_mu, sigma=annual_sigma):
    dt = 1/252  # Daily time step

    # Initialize the price path
    price_path = np.zeros(num_steps)
    price_path[0] = start_price
    for i in range(1, num_steps):
        # Simulate the next price using the geometric Brownian motion formula
        price_path[i] = price_path[i-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal())
    return price_path

# Here’s what SPY might look like if price followed a simple flat stochastic process with constant drift and volatility
plt.plot(range(30, len(prices)),  prices[30:], label='Actual SPY Prices', color='black')

# Create a list to store all simulated brownian paths
all_brownian_paths = []

# Simulate multiple brownian market paths (100 paths)
for _ in range(100):
    path = simulate_brownian_motion(prices[0], num_steps=len(prices))
    all_brownian_paths.append(path)
    plt.plot(range(30, len(path)), path[30:], color='blue', alpha=0.2)

# Calculate the mean of all simulated brownian paths
flat_mean_paths = np.mean(np.array(all_brownian_paths), axis=0)
flat_eval_paths = flat_mean_paths[30:]  # Evaluate from day 252 onwards
plt.plot(range(30, len(flat_mean_paths)), flat_eval_paths, color='darkblue', linewidth=2, label='Mean Simulated Path')

# Final plot settings
plt.title('Actual SPY vs Simulated Flat Market SPY Prices')
plt.xlabel('Day')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

## Could earnings announcements, macro shifts, or other market events have been what pulled SPY’s path in a different geometric direction?
# This question leads us to consider how curvature might influence market dynamics.
# To explore curvature, we can simulate a market influenced by geometric constraints.
# I will curve the path by calculuating the Rolling Sharpe Ratio of the daily returns and using it to modify the drift of the stochastic process.
# This will create a path that is influenced by the market's historical performance, simulating a more realistic market behavior.
def simulate_curved_market_path(start_price, alpha, mu=annual_mu, sigma=annual_sigma, dt=1/252):

    # Calculate the rolling Sharpe ratio based on the daily returns (using a 30-day window)
    rolling_mean = pd.Series(daily_returns).rolling(window=30).mean()
    rolling_std = pd.Series(daily_returns).rolling(window=30).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
    # Shift by 1 and fillna(0) to align the Sharpe ratio with the end of the window *before* the current day
    rolling_sharpe = rolling_sharpe.shift(1).fillna(0).to_numpy()

    curved_path = np.zeros(len(prices)) # Initialize with the length of prices
    curved_path[0] = start_price

    # Iterate from the second day up to the length of prices - 1
    for i in range(1, len(prices)):
        # Use the rolling Sharpe ratio corresponding to the data up to day i-1.
        # This is at index i-1 in the shifted and filled rolling_sharpe array.
        # Ensure the index is within the bounds of rolling_sharpe.
        sharpe = rolling_sharpe[i-1] if i-1 < len(rolling_sharpe) else rolling_sharpe[-1]


        drift_modifier = 1 + alpha * sharpe
        modified_mu = mu * drift_modifier
        normal_curve_val = np.random.normal()

        # Simulate the next price using the geometric Brownian motion formula with curvature
        curved_path[i] = curved_path[i-1] * np.exp((modified_mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * normal_curve_val)
    return curved_path


# Plot the actual SPY prices and the simulated curved market paths
plt.plot(range(30, len(prices)), prices[30:], label='Actual SPY Prices', color='black')

# Create a list to store all simulated curved paths
all_curved_paths = []

# Simulate multiple curved market paths (100 paths where alpha = 0.9)
for _ in range(100):
    path = simulate_curved_market_path(prices[0], alpha=0.9)
    all_curved_paths.append(path)
    plt.plot(range(30, len(path)), path[30:], color='red', alpha=0.2)

# Calculate the mean of all simulated curved paths
curved_mean_paths = np.mean(np.array(all_curved_paths), axis=0)
curved_eval_paths = curved_mean_paths[30:]  # Evaluate from day 252 onwards
plt.plot(range(30, len(curved_mean_paths)), curved_eval_paths, color='darkred', linewidth=2, label='Mean Simulated Path')

# Final plot settings
plt.title('Actual SPY vs Simulated Curved Market SPY Prices')
plt.xlabel('Day')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()


# Now we will compare the correlation of the flat and curved models with the actual SPY prices
actual_prices_trimmed = prices_2023
flat_mean_trimmed = flat_mean_paths[30:30 + len(prices_2023)]
curved_mean_trimmed = curved_mean_paths[30:30 + len(prices_2023)]



# Determine the max number of aligned days available from index 30 onward
usable_len = min(len(prices_2023), len(flat_mean_paths) - 30, len(curved_mean_paths) - 30)

# Align all arrays to this same length
actual_prices_trimmed = prices_2023[:usable_len]
flat_mean_trimmed = flat_mean_paths[30:30 + usable_len]
curved_mean_trimmed = curved_mean_paths[30:30 + usable_len]

# Check they're equal in length
assert len(actual_prices_trimmed) == len(flat_mean_trimmed) == len(curved_mean_trimmed)


# Calculate Pearson correlation coefficients with actual SPY prices
corr_flat, _ = pearsonr(flat_mean_trimmed, actual_prices_trimmed)
corr_curved, _ = pearsonr(curved_mean_trimmed, actual_prices_trimmed)

# Calculate the percentage improvement in correlation
improvement_pct = 100 * (corr_curved - corr_flat) / abs(corr_flat)

# Output results
print(f"Flat model correlation: {corr_flat:.4f}")
print(f"Curved model correlation: {corr_curved:.4f}")
print(f"Curved model improved correlation by {improvement_pct:.2f}% over flat model.")

# Summarize the metrics
summary = {
    "Flat Correlation": float(round(corr_flat, 4)),
    "Curved Correlation": float(round(corr_curved, 4)),
    "Correlation Improvement (%)": float(round(improvement_pct, 2)),
    "Alpha Used": 0.9
}
print("\nSummary:", summary)

# Let's find which alpha value gives the best correlation on this simulated market path
best_alpha = None
best_corr = 0

# Iterate over a range of alpha values to find the best correlation
for alpha in np.arange(0.1, 1.01, 0.1):
    paths = [simulate_curved_market_path(prices[0], alpha=alpha) for _ in range(100)]
    curved_mean = np.mean(np.array(paths), axis=0)
    # Adjust slicing to match the length of prices_2023
    usable_len = min(len(curved_mean) - 30, len(prices_2023))
    curved_mean_eval = curved_mean[30:30 + usable_len]
    actual_eval = prices_2023[:usable_len]
    corr, _ = pearsonr(curved_mean_eval, actual_eval)
    if corr > best_corr:
        best_corr = corr
        best_alpha = alpha

# Print the alpha level that gives the best correlation
print(f"\nBest alpha: {best_alpha:.2f} → Correlation: {best_corr:.4f}")
