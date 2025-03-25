import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
sales_data = {
    'top1': pd.read_csv('data/sales/top1_item_sales_h1_2025.csv'),
    'top2': pd.read_csv('data/sales/top2_item_sales_h1_2025.csv'),
    'top3': pd.read_csv('data/sales/top3_item_sales_h1_2025.csv'),
    'top4': pd.read_csv('data/sales/top4_item_sales_h1_2025.csv'),
    'top5': pd.read_csv('data/sales/top5_item_sales_h1_2025.csv'),
}

stocks_data = {
    'top1': pd.read_csv('data/stocks/top1_item_stocks_h1_2025.csv'),
    'top2': pd.read_csv('data/stocks/top2_item_stocks_h1_2025.csv'),
    'top3': pd.read_csv('data/stocks/top3_item_stocks_h1_2025.csv'),
    'top4': pd.read_csv('data/stocks/top4_item_stocks_h1_2025.csv'),
    'top5': pd.read_csv('data/stocks/top5_item_stocks_h1_2025.csv'),
}

item_names = {
    'top1': 'Стиральная машина LG F-2M5HS6S (store_id: jsySHiRm8fJNrz6IubJskA==)',
    'top2': 'Чайник Tefal KI-700830 (store_id: gPKQGw4P74wR5sEfXKoQ9g==)',
    'top3': 'AirPods with Charging Case MV7N2RU/A (store_id: mFgAGZmZFE4R4zMCL19vIg==)',
    'top4': 'AirPods with Charging Case MV7N2RU/A (store_id: jsySHiRm8fJNrz6IubJskA==)',
    'top5': 'EarPods with Lightning Connector MMTN2ZMA (store_id: jsySHiRm8fJNrz6IubJskA==)'
}

st.set_page_config(layout="wide")
st.title('📦 AIRBA Technodom: Stock-Out Optimization Dashboard')

# Select top item
selected_top = st.selectbox("Выберите товар:", options=list(item_names.keys()), format_func=lambda x: item_names[x])

# Merge sales and stocks
sales_df = sales_data[selected_top].rename(columns={"Quantity": "Sales"})
stocks_df = stocks_data[selected_top].rename(columns={"Quantity": "Stocks"})

merged = pd.merge(sales_df, stocks_df, on=["Дата", "store_id", "item_id"], how="inner")
merged["Дата"] = pd.to_datetime(merged["Дата"])
merged = merged.sort_values("Дата")
merged["Delta"] = merged["Stocks"] - merged["Sales"]

# Plotly line chart with highlighting
fig = px.line(merged, x="Дата", y=["Sales", "Stocks"],
              labels={"value": "Количество", "variable": "Показатель"},
              title=f"Прогноз продаж и остатков — {item_names[selected_top]}")

# Add coloring for critical delta areas
merged["critical"] = merged["Delta"] < 0
critical_df = merged[merged["critical"] == True]

fig.add_scatter(x=critical_df["Дата"], y=critical_df["Stocks"],
                mode="markers", marker=dict(color="red", size=8),
                name="Stock < Sales (Δ < 0)")

st.plotly_chart(fig, use_container_width=True)

# Show Delta(t) values
with st.expander("📉 Показать расчёт дисбаланса Δ(t)"):
    st.latex(r"\Delta(t) = \text{Stocks}(t + \tau) - \text{Sales}(t)")
    st.latex(r"\text{Цель:} \quad \min_{\tau} \, \mathbb{E}[|\Delta(t)|]")
    st.dataframe(merged[["Дата", "Sales", "Stocks", "Delta"]].round(2))