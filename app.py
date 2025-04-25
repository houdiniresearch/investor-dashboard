import streamlit as st
import pandas as pd
import requests

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Investor Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>Investor Dashboard</h1>", unsafe_allow_html=True)
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
    f"{SUPABASE_URL}/rest/v1/current_holdings?select=investor_name,current_balance,presale_retention",
    headers=headers
)

if response.status_code != 200:
    st.error("Failed to fetch data from Supabase.")
    st.stop()

data = response.json()
df = pd.DataFrame(data)

# --- METRICS SECTION ---
total_investors = len(df)
avg_retention = df["presale_retention"].mean()
total_tokens = df["current_balance"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Investors", total_investors)
col2.metric("Total Held Tokens", f"{total_tokens:,.2f}")
col3.metric("Average Retention", f"{avg_retention:.2f}%")

st.markdown("---")

# --- TABLE ---
st.subheader("Presale Token Holding Overview")

styled_df = df.rename(columns={
    "investor_name": "Investor",
    "current_balance": "Current Balance",
    "presale_retention": "Presale Retention (%)"
}).sort_values(by="Presale Retention (%)", ascending=False)

st.dataframe(
    styled_df.style.format({
        "Current Balance": "{:,.2f}",
        "Presale Retention (%)": "{:.2f}"
    }).background_gradient(subset="Presale Retention (%)", cmap="YlGn")
)

