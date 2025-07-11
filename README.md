# 📈 Capital Asset Pricing Model (CAPM) Web Application

This project is an interactive web app built with **Streamlit** that allows users to analyze and visualize the **Capital Asset Pricing Model (CAPM)** for selected stocks. It compares the expected return of a stock with the return of the **S&P 500 index**, using **Beta**, **Alpha**, and other key financial metrics.

---

**Watch Demo Video** 
- Link : https://drive.google.com/file/d/1GJhCbDi-Mwye-dfnT5L_YCF6xwohCo3U/view?usp=sharing
  
---

## 🚀 Features

- 🔍 Select up to **4 stocks** to analyze
- 📅 Choose a **time period** from 1 to 10 years
- 📉 Download historical data using **Yahoo Finance**
- 📊 Retrieve S&P 500 index from **FRED**
- 📈 Calculate:
  - **Daily returns**
  - **Beta (β)**: Stock's volatility vs. market
  - **Alpha (α)**: Stock-specific performance
  - **Expected Return** using **CAPM formula**
  - **Portfolio return vs. Market return**
- 📉 Plot normalized stock prices for easy comparison
- 📋 View dataframes, summary tables, and visual plots

---

## ⚙️ Tech Stack

| Tool/Library       | Purpose                         |
|--------------------|----------------------------------|
| `Streamlit`        | Web app UI                      |
| `yfinance`         | Download stock data             |
| `pandas_datareader`| Retrieve S&P 500 from FRED      |
| `pandas`           | Data manipulation               |
| `plotly.express`   | Interactive charts              |
| `numpy`            | Beta/Alpha regression           |
| `plotly.express(px)`    | High-level interactive visualizations         |
| `plotly.graph_objects(go)` | Fine-grained, customizable chart creation   |

---

## 🧠 How It Works

### 🧮 CAPM Formula
\[
E(R_i) = R_f + \beta_i (R_m - R_f)
\]

Where:
- \(E(R_i)\) = Expected return of stock
- \(R_f\) = Risk-free rate (e.g., US 10-year treasury yield)
- \(R_m\) = Expected market return (S&P 500)
- \(\beta_i\) = Stock’s sensitivity to market

---

## 🧠 How It Works

1. **User Input**:  
   - Select the stocks and number of years to analyze.
2. **Data Download & Preparation**:  
   - Fetch historical stock prices for the chosen stocks using `yfinance`.
   - Retrieve the S&P 500 index data from FRED.
   - Merge and clean the datasets by ensuring dates are compatible.
3. **Calculation of Returns and Metrics**:  
   - Compute daily percentage returns for each stock and the market.
   - Calculate **Beta** (via linear regression using `np.polyfit()`) and **Alpha**.
   - Compute the expected return using the CAPM formula:
     \[
     E(R_i) = R_f + \beta_i (R_m - R_f)
     \]
4. **Visualization**:  
   - Plot raw and normalized stock prices.
   - Display interactive bar charts for Beta and Alpha values.
   - Provide a summary section with key metrics (Risk-Free Rate, Expected Market Return).
5. **Portfolio vs. Market Comparison**:  
   - Calculate a weighted portfolio return and compare it with the market return.

---

## 🖼️ Conclusion

> This project served as a practical implementation of the Capital Asset Pricing Model (CAPM) and provided several key financial and technical insights:

## 🔍 Insights Gained

- 📊 **Market Risk Awareness**:  
  By calculating **Beta**, we identified which stocks were more or less volatile compared to the overall market.

- 💡 **Stock Selection**:  
  Through **Alpha**, we determined which stocks consistently outperformed or underperformed relative to their expected risk-adjusted return.

- 📈 **Performance Comparison**:  
  By normalizing stock prices, we could easily compare multiple stocks’ growth trends on a unified scale.

- 💼 **Portfolio Evaluation**:  
  We learned how to assess a group of stocks together as a portfolio and compare its performance against the broader market (**S&P 500**).

- 🧮 **CAPM Application**:  
  We applied the **Capital Asset Pricing Model (CAPM)** to estimate future returns — a fundamental concept in modern finance and investment decision-making.

---

## 🛠️ Skills & Concepts Learned

- ✅ **Data Collection**:
  - Automated retrieval of real-time stock and market data using **`yfinance`** and **`pandas_datareader`**

- ✅ **Data Preprocessing**:
  - Cleaned and merged stock and index data efficiently using **pandas**, including date alignment and missing value handling

- ✅ **Financial Computations**:
  - Calculated daily returns
  - Used **linear regression** (`np.polyfit`) to compute **Beta** and **Alpha**
  - Applied the **CAPM formula** to estimate expected returns

- ✅ **Visualization**:
  - Built interactive **line and bar charts** using **Plotly**
  - Displayed **side-by-side comparisons** of price and return metrics

- ✅ **Frontend Development**:
  - Developed an interactive, responsive **web app using Streamlit**

- ✅ **User Experience Enhancements**:
  - Implemented **input widgets**, **metric highlights**, and **expandable summaries** for a clean and user-friendly analysis experience

---
