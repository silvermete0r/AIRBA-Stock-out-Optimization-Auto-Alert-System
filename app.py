import streamlit as st
import pandas as pd

sales_top_1 = pd.read_csv('data/sales/top1_item_sales_h1_2025.csv')
sales_top_2 = pd.read_csv('data/sales/top2_item_sales_h1_2025.csv')
sales_top_3 = pd.read_csv('data/sales/top3_item_sales_h1_2025.csv')
sales_top_4 = pd.read_csv('data/sales/top4_item_sales_h1_2025.csv')
sales_top_5 = pd.read_csv('data/sales/top5_item_sales_h1_2025.csv')

stocks_top_1 = pd.read_csv('data/stocks/top1_item_stocks_h1_2025.csv')
stocks_top_2 = pd.read_csv('data/stocks/top2_item_stocks_h1_2025.csv')
stocks_top_3 = pd.read_csv('data/stocks/top3_item_stocks_h1_2025.csv')
stocks_top_4 = pd.read_csv('data/stocks/top4_item_stocks_h1_2025.csv')
stocks_top_5 = pd.read_csv('data/stocks/top5_item_stocks_h1_2025.csv')

st.title('Stock-out Optimization Auto-Alert System')
