import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# --- PAGE SETTINGS ---
st.set_page_config(page_title="JuliaOS Investor Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>JuliaOS Investor Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- SUPABASE CONFIG ---
SUPABASE_URL = "https://<YOUR-PROJECT-ID>.supabase.co"
API_KEY = "YOUR-ANON-KEY"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"
}

# --- FETCH current_holdings ---
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/current_holdings?select=investor_name,current_balance,presale_retention,token_mint,investor_id",
    headers=headers
)

if response.status_code != 200:
    st.error("Failed to fetch current_holdings from Supabase.")
    st.stop()

holdings = pd.DataFrame(response.json())

# --- FETCH presale_amounts ---
response2 = requests.get(
    f"{SUPABASE_URL}/rest/v1/presale_amounts?select=investor_id,presale_amount",
    headers=headers
)

if response2.status_code != 200:
    st.error("Failed to fetch presale_amounts from Supabase.")
    st.stop()

presale = pd.DataFrame(response2.json())
presale["presale_amount"] = pd.to_numeric(presale["presale_amount"], errors="coerce")

# --- MERGE DATA ---
df = holdings.merge(presale, on="investor_id", how="left")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Investors", len(df))
col2.metric("Total Held Tokens", f"{df['current_balance'].sum():,.2f}")
col3.metric("Avg. Retention", f"{df['presale_retention'].mean():.2f}%")

st.markdown("---")

# --- PIE CHART (Distribution) ---
st.subheader("Token Distribution Overview")
chart_data = pd.DataFrame({
    'Category': ['Presale Distributed', 'Currently Held'],
    'Amount': [df["presale_amount"].sum(), df["current_balance"].sum()]
})

fig, ax = plt.subplots()
ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

st.markdown("---")

# --- TABLE FORMAT ---
df = df.rename(columns={
    "investor_name": "Investor",
    "presale_amount": "Presale Amount",
    "current_balance": "Current Balance",
    "presale_retention": "Presale Retention (%)"
})
df = df.sort_values(by="Presale Retention (%)", ascending=False)

# --- TABLE DISPLAY ---
st.subheader("Presale Token Holding Breakdown")

st.dataframe(
    df[["Investor", "Presale Amount", "Current Balance", "Presale Retention (%)"]].style.format({
        "Presale Amount": "{:,.2f}",
        "Current Balance": "{:,.2f}",
        "Presale Retention (%)": "{:.2f}"
    }).background_gradient(subset="Presale Retention (%)", cmap="YlGn")
)



