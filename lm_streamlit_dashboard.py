import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import io
from datetime import datetime

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide", page_icon="📊")

# --- Data Handling & Caching ---
@st.cache_data(ttl=300)
def load_data(uploaded_file=None, github_url=None):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    elif github_url:
        r = requests.get(github_url)
        df = pd.read_csv(io.StringIO(r.text))
    else:
        df = pd.DataFrame()
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

GITHUB_URL = "https://raw.githubusercontent.com/youruser/yourrepo/main/lm.csv"  # <-- update to your repo

# --- Sidebar: Upload, Refresh, Filters ---
st.sidebar.title("Dashboard Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
refresh = st.sidebar.button("🔄 Refresh Data")
if 'last_refresh' not in st.session_state or refresh:
    st.session_state['last_refresh'] = datetime.now()
st.sidebar.caption(f"Last refresh: {st.session_state['last_refresh'].strftime('%Y-%m-%d %H:%M:%S')}")
df = load_data(uploaded_file, github_url=GITHUB_URL)
if refresh:
    st.cache_data.clear()
    df = load_data(uploaded_file, github_url=GITHUB_URL)

# Sidebar Filters
if not df.empty:
    # Date
    if 'Date' in df.columns:
        min_date, max_date = df['Date'].min(), df['Date'].max()
        date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
        df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]
    # Product
    prod_col = st.sidebar.selectbox("Product Column", options=["None"] + list(df.columns))
    if prod_col != "None":
        prods = st.sidebar.multiselect("Product Filter", options=df[prod_col].dropna().unique())
        if prods:
            df = df[df[prod_col].isin(prods)]
    # Region
    region_col = st.sidebar.selectbox("Region Column", options=["None"] + list(df.columns))
    if region_col != "None":
        regs = st.sidebar.multiselect("Region Filter", options=df[region_col].dropna().unique())
        if regs:
            df = df[df[region_col].isin(regs)]
    # Custom columns
    custom_cols = st.sidebar.multiselect("Columns to Display", options=list(df.columns), default=list(df.columns))
    df = df[custom_cols]

# --- KPI Grid ---
def kpi_grid(df):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", f"${df['Sales'].sum():,.2f}" if 'Sales' in df.columns else "N/A")
    with col2:
        st.metric("Avg Order Value", f"${df['Sales'].mean():,.2f}" if 'Sales' in df.columns else "N/A")
    with col3:
        growth = (df['Sales'].pct_change().mean()*100) if 'Sales' in df.columns else 0
        st.metric("Growth %", f"{growth:.2f}%")
    with col4:
        st.metric("Orders", f"{len(df):,}")
kpi_grid(df)

# --- Tabs/Pages ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Home", "🔍 Data Preview", "📊 EDA", "📈 Trends", "💡 Insights"
])

with tab1:
    st.header("Welcome to the Executive BI Dashboard")
    st.write("Upload a CSV/Excel or auto-load the GitHub dataset. Use the sidebar to filter data.")
    st.write("This dashboard provides interactive EDA, trends, insights, and an AI assistant for your data.")

with tab2:
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)
    st.download_button("Export CSV", df.to_csv(index=False), "data.csv")
    # PDF export can be added with st.download_button and a PDF writer

with tab3:
    st.subheader("EDA")
    num_cols = df.select_dtypes(include='number').columns
    if not num_cols.empty:
        col = st.selectbox("Column for Histogram", num_cols)
        st.plotly_chart(px.histogram(df, x=col, nbins=30), use_container_width=True)
        x = st.selectbox("X for Scatter", num_cols)
        y = st.selectbox("Y for Scatter", num_cols, index=1)
        st.plotly_chart(px.scatter(df, x=x, y=y, hover_data=df.columns), use_container_width=True)
        st.plotly_chart(px.box(df, y=col), use_container_width=True)

with tab4:
    st.subheader("Trends")
    if 'Date' in df.columns and not df.empty:
        y_col = st.selectbox("Y Axis", df.select_dtypes(include='number').columns)
        fig = px.line(df, x='Date', y=y_col)
        st.plotly_chart(fig, use_container_width=True)
        # Moving average, forecast, and sliders can be added as needed

with tab5:
    st.subheader("Insights")
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
    st.write("**AI Summary:** (Optional: Integrate OpenAI for auto-insights)")
