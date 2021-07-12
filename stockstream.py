from yahooquery import Ticker
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
"""
# :chart_with_upwards_trend: Stock analyzer
Enter a stock ticker to visualize description, price and financial ratios.
"""

inp = st.text_input("Enter stock ticker:")
stock = Ticker(inp)

# ADD PRICE, COMPANY NAME AND OHLC CHART
if not inp:
    st.warning('No ticker entered')
    st.stop()
else:
    quote = stock.quotes[inp] 
    price = quote['regularMarketPrice']
    name = quote['longName']
    st.write(name, 
    'Last price:', price)

    hist = stock.history(start='1980-01-01')
    hist.reset_index(inplace=True)
    fig, ax = plt.subplots()
    ax = sns.lineplot(data=hist, x='date', y='close')
    ax.set_title(inp)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    st.pyplot(fig)


# Company info
my_expander1 = st.beta_expander('Company info')
with my_expander1: 
    summ = stock.summary_profile[inp]
    info = summ['longBusinessSummary']
    st.write(info)

# Balance sheet
balance = stock.balance_sheet(frequency='a', trailing=False)
income = stock.income_statement(trailing=False)
cashflow = stock.cash_flow(trailing=False)

my_expander2 = st.beta_expander("Financial statements", expanded=False)
with my_expander2:
    statement = st.radio(
        "Select financial statement",
        ('Balance sheet', 'Income statement', 'Cashflow statement'))
    
    if statement == 'Balance sheet':
        balance
    elif statement == 'Income statement':
        income
    elif statement == 'Cashflow statement':
        cashflow

my_expander3 = st.beta_expander("Financial ratios", expanded=False)
with my_expander3:
    ratio = st.radio(
        'Select financial ratio',
        ('Current ratio', 'Debt-to-Equity', 'Free Cash Flow', 'EPS', 'Total liabilities to Assets', 'Return on Equity')
    )

    if ratio == 'Current ratio':
        st.write('The current ratio is a liquidity ratio that measures a companys ability to pay short-term obligations or those due within one year. It tells investors and analysts how a company can maximize the current assets on its balance sheet to satisfy its current debt and other payables.')
        balance['Current_Ratio'] = balance['CurrentAssets']/balance['CurrentDebt'] 
        fig, ax = plt.subplots()
        ax = sns.lineplot(data=pd.DataFrame(balance), x='asOfDate', y='Current_Ratio')
        ax.set_title('Current Ratio')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        st.pyplot(fig)
    
    if ratio == 'Free Cash Flow':
        st.write('Free cash flow (FCF) represents the cash a company generates after accounting for cash outflows to support operations and maintain its capital assets. Unlike earnings or net income, free cash flow is a measure of profitability that excludes the non-cash expenses of the income statement and includes spending on equipment and assets as well as changes in working capital from the balance sheet.')
        cashflow['Free_cash_flow'] = cashflow['OperatingCashFlow'] - cashflow['CapitalExpenditure']
        fig, ax = plt.subplots()
        ax = sns.lineplot(data=pd.DataFrame(cashflow), x='asOfDate', y='Free_cash_flow')
        ax.set_title('Free Cash Flow')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        st.pyplot(fig)

    if ratio == 'Debt-to-Equity':
        st.write('The debt-to-equity (D/E) ratio is used to evaluate a companys financial leverage and is calculated by dividing a company’s total liabilities by its shareholder equity. It is a measure of the degree to which a company is financing its operations through debt versus wholly owned funds. More specifically, it reflects the ability of shareholder equity to cover all outstanding debts in the event of a business downturn.')
        balance['Debt_to_Equity'] = balance['TotalDebt']/balance['StockholdersEquity']
        fig, ax = plt.subplots()
        ax = sns.lineplot(data=pd.DataFrame(balance), x='asOfDate', y='Debt_to_Equity')
        ax.set_title('Debt to Equity Ratio')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        st.pyplot(fig)

    if ratio == 'EPS':
        st.write('Earnings per share (EPS) is calculated as a companys profit divided by the outstanding shares of its common stock. The resulting number serves as an indicator of a companys profitability. The higher a companys EPS, the more profitable it is considered to be.')
        fig, ax = plt.subplots()
        ax = sns.lineplot(data=pd.DataFrame(income), x='asOfDate', y='DilutedEPS')
        ax.set_title('Earning per share')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        st.pyplot(fig)
    
    if ratio == 'Total liabilities to Assets':
        st.write('The liabilities to assets (L/A) ratio is a solvency ratio that examines how much of a companys assets are made of liabilities. A L/A ratio of 20 percent means that 20 percent of the company are liabilities. A high liabilities to assets ratio can be negative; this indicates the shareholder equity is low and potential solvency issues. Rapidly expanding companies often have higher liabilities to assets ratio (quick expansion of debt and assets). Companies with low L/A ratios indicate a company with little to no liabilities. With some notable exceptions, this is normally a good sign of financial health for the company')
        balance['debt_pct_assets'] = balance['TotalDebt']/balance['TotalAssets']
        fig, ax = plt.subplots()
        ax = sns.lineplot(data=pd.DataFrame(balance), x='asOfDate', y='debt_pct_assets')
        ax.set_title('Total liabilities to Assets')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        st.pyplot(fig)
    
    if ratio == 'Return on Equity':
        st.write('Return on equity (ROE) is a measure of financial performance calculated by dividing net income by shareholders equity. Because shareholders equity is equal to a company’s assets minus its debt, ROE is considered the return on net assets. ROE is considered a measure of a corporations profitability in relation to stockholders’ equity.')
        income['ROE'] = income['NetIncome']/balance['StockholdersEquity']
        fig, ax = plt.subplots()
        ax = sns.lineplot(data=pd.DataFrame(income), x='asOfDate', y='ROE')
        ax.set_title('Return on Equity')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        st.pyplot(fig)
