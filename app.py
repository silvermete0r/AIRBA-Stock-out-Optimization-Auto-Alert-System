import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json
from datetime import timedelta

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
    st.dataframe(merged[["Дата", "Sales", "Stocks", "Delta"]].round(2), use_container_width=True)

# Smart analysis per item
if st.button("🧠 Smart Analysis"):
    result_json = {}
    for key in item_names:
        df_sales = sales_data[key].rename(columns={"Quantity": "Sales"})
        df_stocks = stocks_data[key].rename(columns={"Quantity": "Stocks"})
        df = pd.merge(df_sales, df_stocks, on=["Дата", "store_id", "item_id"], how="inner")
        df["Дата"] = pd.to_datetime(df["Дата"])
        df = df.sort_values("Дата")
        df["Delta"] = df["Stocks"] - df["Sales"]

        high_risk = df[df["Delta"] < 0]
        medium_risk = df[(df["Delta"] >= 0) & (df["Delta"] <= 3)]

        def extract_periods(df_period):
            periods = []
            if df_period.empty:
                return periods
            df_period = df_period.sort_values("Дата")
            start = df_period.iloc[0]["Дата"]
            prev = start
            for i in range(1, len(df_period)):
                current = df_period.iloc[i]["Дата"]
                if current - prev > timedelta(days=1):
                    periods.append((start.date(), prev.date()))
                    start = current
                prev = current
            periods.append((start.date(), prev.date()))
            return periods

        if not high_risk.empty:
            risk = "высокий"
            high_periods = extract_periods(high_risk)
            desc = f"Обнаружены периоды, когда продажи превышают остатки: {high_periods}."
        elif not medium_risk.empty:
            risk = "средний"
            medium_periods = extract_periods(medium_risk)
            desc = f"Остатки близки к продажам (менее 3 ед.) в периоды: {medium_periods}."
        else:
            risk = "низкий"
            desc = "Запасы значительно превышают прогноз продаж. Рисков не обнаружено."

        result_json[item_names[key]] = {"риск": risk, "описание": desc}

    st.subheader("🧾 JSON-анализ")
    st.json(result_json, expanded=False)

    with st.spinner("🤖 AI-анализ в процессе..."):
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Проведи анализ на русском языке по следующему JSON, оцени товары с самыми высокими рисками и предложи варианты оптимизацию запасов с датами (когда примерно нужно их закупить), чтобы закупить необходимый товар в нужном количестве заранее. 
        Также сокращение маркетинговых затрат на уже популярные товары, с высокими продажами. Предложение маркетинговых стратегии для товаров у которых продажи нормальные, но можно сделать ещё лучше. Все это оформи четко и понятно в формате markdown.
        Сегодняшня дата: {pd.Timestamp.now().date()}
        Данные для анализа:
        {json.dumps(result_json, ensure_ascii=False, indent=2)}
        """
        response = model.generate_content(prompt)
        st.subheader("🤖 AI-анализ от Gemini")
        st.markdown(response.text)
