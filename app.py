import streamlit as st
import pandas as pd
import requests

# --- CONFIG ---
st.set_page_config(page_title="Investor Dashboard", layout="wide")
st.title("Investor Dashboard")

# --- SUPABASE CONFIG ---
SUPABASE_URL = "https://znfwwcxskreqpuuenrxo.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpuZnd3Y3hza3JlcXB1dWVucnhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1NzkxNzUsImV4cCI6MjA2MTE1NTE3NX0.HeMRepQ8nwHyGDjJFl8kH7jnUsUFFHa-diKy37Mk_Co"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"
}

# --- DATA FETCH ---
response = requests.get(
    f"{SUPABASE_URL}/rest/v1/current_holdings?select=investor_name,current_balance,presale_retention",
    headers=headers
)

if response.status_code != 200:
    st.error("Failed to fetch data from Supabase.")
    st.stop()

data = response.json()
df = pd.DataFrame(data)

# --- UI ---
st.subheader("Presale Token Holding Overview")

st.dataframe(df.rename(columns={
    "investor_name": "Investor",
    "current_balance": "Current Balance",
    "presale_retention": "Presale Retention (%)"
}).style.format({
    "Current Balance": "{:.2f}",
    "Presale Retention (%)": "{:.2f}"
}))

