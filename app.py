import streamlit as st
import pandas as pd
import requests

# --- PAGE SETTINGS ---
st.set_page_config(page_title="JuliaOS Investor Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>JuliaOS Investor Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- SUPABASE CONFIG ---
SUPABASE_URL = "https://znfwwcxskreqpuuenrxo.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpuZnd3Y3hza3JlcXB1dWVucnhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1NzkxNzUsImV4cCI6MjA2MTE1NTE3NX0.HeMRepQ8nwHyGDjJFl8kH7jnUsUFFHa-diKy37Mk_Co"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"
}

# --- FETCH DATA ---
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/current_holdings?select=investor_name,current_balance,presale_retention,token_mint,investor_id",
    headers=headers
)

if response.status_code != 200:
    st.error("Failed to fetch data from Supabase.")
    st.stop()

holdings = pd.DataFrame(response.json())

# Presale amounts tablosunu çek
response2 = requests.get(
    f"{SUPABASE_URL}/rest/v1/presale_amounts?select=investor_id,presale_amount",
    headers=headers
)

if response2.status_code != 200:
    st.error("Failed to fetch presale data from Supabase.")
    st.stop()

presale = pd.DataFrame(response2.json())

# --- MERGE BOTH DATASETS ---
df = holdings.merge(presale, on="investor_id", how="left")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Investors", len(df))
col2.metric("Total Held Tokens", f"{df['current_balance'].sum():,.2f}")
col3.metric("Avg. Retention", f"{df['presale_retention'].mean():.2f}%")

st.markdown("---")

# --- TABLE ---
df = df.rename(columns={
    "investor_name": "Investor",
    "presale_amount": "Presale Amount",
    "current_balance": "Current Balance",
    "presale_retention": "Presale Retention (%)"
})

df = df.sort_values(by="Presale Retention (%)", ascending=False)

st.subheader("Token Holding Overview")

st.dataframe(
    df[["Investor", "Presale Amount", "Current Balance", "Presale Retention (%)"]].style.format({
        "Presale Amount": "{:,.2f}",
        "Current Balance": "{:,.2f}",
        "Presale Retention (%)": "{:.2f}"
    }).background_gradient(subset="Presale Retention (%)", cmap="YlGn")
)


