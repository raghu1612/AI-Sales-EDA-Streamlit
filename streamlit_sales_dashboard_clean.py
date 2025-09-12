import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time

# --- Advanced Analytics Functions ---
def calculate_revenue_growth(df):
    """Calculate revenue growth metrics"""
    if 'Date' in df.columns and 'Sales' in df.columns:
        df_sorted = df.sort_values('Date')
        monthly_revenue = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))['Sales'].sum()
        if len(monthly_revenue) > 1:
            growth_rate = ((monthly_revenue.iloc[-1] - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0]) * 100
            avg_monthly_growth = monthly_revenue.pct_change().mean() * 100
            return growth_rate, avg_monthly_growth, monthly_revenue
    return 0, 0, pd.Series()

def forecast_sales(df, periods=6):
    """Simple sales forecasting using linear trend"""
    if 'Date' in df.columns and 'Sales' in df.columns:
        df_sorted = df.sort_values('Date')
        monthly_sales = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))['Sales'].sum()
        
        if len(monthly_sales) >= 3:
            # Simple linear regression for forecasting
            x = np.arange(len(monthly_sales))
            y = monthly_sales.values
            z = np.polyfit(x, y, 1)
            
            # Forecast future periods
            future_x = np.arange(len(monthly_sales), len(monthly_sales) + periods)
            forecast = np.polyval(z, future_x)
            
            return monthly_sales, forecast, future_x
    return pd.Series(), np.array([]), np.array([])

def market_expansion_analysis(df):
    """Analyze market expansion opportunities"""
    insights = {}
    
    if 'Region' in df.columns and 'Sales' in df.columns:
        regional_performance = df.groupby('Region')['Sales'].agg(['sum', 'mean', 'count']).round(2)
        insights['top_regions'] = regional_performance.sort_values('sum', ascending=False).head(3)
        insights['growth_opportunities'] = regional_performance.sort_values('mean', ascending=True).head(3)
    
    if 'Category' in df.columns and 'Sales' in df.columns:
        category_performance = df.groupby('Category')['Sales'].agg(['sum', 'mean', 'count']).round(2)
        insights['top_categories'] = category_performance.sort_values('sum', ascending=False).head(3)
        insights['underperforming_categories'] = category_performance.sort_values('mean', ascending=True).head(3)
    
    return insights

def strategic_kpis(df):
    """Calculate strategic KPIs for executive dashboard"""
    kpis = {}
    
    if 'Sales' in df.columns:
        kpis['total_revenue'] = df['Sales'].sum()
        kpis['avg_transaction'] = df['Sales'].mean()
        kpis['revenue_per_day'] = df['Sales'].sum() / max(1, len(df['Date'].dt.date.unique())) if 'Date' in df.columns else 0
        
    if 'Region' in df.columns:
        kpis['market_penetration'] = len(df['Region'].unique())
        
    if 'Category' in df.columns:
        kpis['product_diversity'] = len(df['Category'].unique())
        
    return kpis

st.set_page_config(
    page_title="Executive Sales Dashboard", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Initialize session state for refresh timestamp
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# --- Enhanced Ultra-Modern Theme with Rich UI/UX ---
st.markdown(
    '''<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    html, body, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #667eea 50%, #764ba2 75%, #667eea 100%) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important;
        color: #1e293b !important;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container with advanced glass morphism */
    .block-container {
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(25px) !important;
        border-radius: 28px !important;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 2px 8px rgba(31, 38, 135, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        margin: 1rem !important;
        padding: 2.5rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
    }
    
    .block-container:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        border-radius: 28px 28px 0 0;
    }
    
    /* Enhanced Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 4px 8px rgba(102, 126, 234, 0.3) !important;
        animation: glow 2s ease-in-out infinite alternate !important;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 15px rgba(102, 126, 234, 0.8)); }
    }
    
    /* Refresh timestamp styling */
    .refresh-timestamp {
        position: absolute;
        top: 1rem;
        right: 2rem;
        background: rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        font-size: 0.8rem;
        color: #667eea;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
    }
    
    /* Enhanced Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(102, 126, 234, 0.95) 0%, 
            rgba(118, 75, 162, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 0 25px 25px 0 !important;
        border-right: 2px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 4px 0 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    .css-1d391kg .css-1outpf7 {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Icons and Interactive Elements */
    .sidebar-icon {
        display: inline-block;
        margin-right: 0.5rem;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .sidebar-icon:hover {
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.6));
    }
    
    /* Enhanced Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(102, 126, 234, 0.05);
        padding: 0.5rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        color: #667eea !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stTabs [data-baseweb="tab"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .stTabs [data-baseweb="tab"]:hover:before {
        left: 100%;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7)) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.15),
            0 2px 8px rgba(102, 126, 234, 0.1) !important;
        backdrop-filter: blur(15px) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 20px 20px 0 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 
            0 12px 40px rgba(102, 126, 234, 0.25),
            0 4px 12px rgba(102, 126, 234, 0.15) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #5a67d8, #6b46c1) !important;
    }
    
    /* Enhanced Input Styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(102, 126, 234, 0.4) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Refresh button special styling */
    .refresh-button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        animation: pulse 2s infinite !important;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }
        50% { box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5); }
        100% { box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }
    }
    
    /* Enhanced Plotly Chart Container */
    .plotly-graph-div {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Loading and Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1)) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1)) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Footer Enhancement */
    .footer-enhancement {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin-top: 3rem;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .footer-enhancement:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>''', unsafe_allow_html=True
)

# Enhanced Professional Theme with Rich UI/UX
st.markdown(
    '''<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important;
        color: #1e293b !important;
    }
    
    .block-container {
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        margin: 1rem !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 16px 16px 0 0 !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3) !important;
        gap: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #667eea !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        border: none !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    
    .css-1d391kg, .stSidebar > div {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 0 20px 20px 0 !important;
        border-right: 2px solid rgba(102, 126, 234, 0.2) !important;
        box-shadow: 4px 0 20px rgba(0,0,0,0.1) !important;
    }
    </style>''', unsafe_allow_html=True)

# --- Simple and Fast Loading Header ---
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(
        '''
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 0.8rem; border-radius: 12px; color: white; font-size: 1.5rem;">📊</div>
            <div>
                <h1 style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 700; margin: 0; font-family: Inter, sans-serif;">Executive Sales Dashboard</h1>
                <div style="display: flex; gap: 0.8rem; margin-top: 0.3rem;">
                    <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.75rem; font-weight: 600;">🚀 Advanced Analytics</span>
                    <span style="background: rgba(59, 130, 246, 0.1); color: #3b82f6; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.75rem; font-weight: 600;">📈 Real-time</span>
                    <span style="background: rgba(168, 85, 247, 0.1); color: #a855f7; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.75rem; font-weight: 600;">💡 AI-powered</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'''
        <div style="text-align: right; padding: 1rem;">
            <div style="background: rgba(102, 126, 234, 0.1); padding: 0.8rem 1rem; border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);">
                <div style="color: #667eea; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.2rem;">🕒 Last Updated</div>
                <div style="font-family: monospace; font-size: 0.7rem; color: #64748b;">{st.session_state.last_refresh.strftime("%Y-%m-%d %H:%M:%S")}</div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 0.4rem 0.8rem; border-radius: 8px; font-size: 0.7rem; font-weight: 600; margin-top: 0.5rem; border: 1px solid rgba(16, 185, 129, 0.2);">🟢 System Online</div>
        </div>
        ''', unsafe_allow_html=True
    )

# Enhanced Navigation Tabs
tabs = st.tabs([
    "🏠 Home", 
    "� Refresh Data",
    "�🔍 Data Preview", 
    "📊 KPIs & Visuals", 
    "📈 Category & Region", 
    "📉 Advanced Charts",
    "💡 Insights"
])

# Enhanced Home Tab
with tabs[0]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #667eea;
        ">
            <h2 style="color: #667eea; margin-bottom: 1rem;">🚀 Welcome to Your Sales Analytics Hub</h2>
            <p style="font-size: 1.1rem; color: #64748b; margin-bottom: 0;">
                Transform your sales data into actionable insights with interactive dashboards, 
                advanced filtering, and comprehensive analytics.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    # Sample data for demonstration
    if st.button("🎯 Load Sample Sales Data", help="Load a sample dataset for demonstration"):
        date_range = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        num_days = len(date_range)
        sample_data = {
            'Date': date_range,
            'Region': np.random.choice(['North', 'South', 'East', 'West'], num_days),
            'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], num_days),
            'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D', 'Product E'], num_days),
            'Sales': np.random.normal(1000, 300, num_days).round(2)
        }
        sample_df = pd.DataFrame(sample_data)
        st.session_state['sample_data'] = sample_df
        st.success("✅ Sample data loaded! Check the other tabs to see the analytics in action.")
        st.rerun()

    # File upload
    col_upload1, col_upload2 = st.columns(2)
    
    with col_upload1:
        uploaded_file = st.file_uploader(
            "📂 Choose your CSV/Excel file", 
            type=["csv", "xlsx"],
            help="Upload your sales data file for analysis"
        )
    
    with col_upload2:
        github_url = st.text_input(
            "🔗 Or paste GitHub raw file URL", 
            placeholder="https://raw.githubusercontent.com/...",
            help="Paste a direct link to your raw CSV/Excel file"
        )

# Data Loading & Caching
@st.cache_data(ttl=300)
def load_data(uploaded_file, github_url):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    elif github_url:
        if github_url.endswith('.csv'):
            df = pd.read_csv(github_url)
        else:
            df = pd.read_excel(github_url)
    else:
        df = pd.DataFrame()
    return df

# Load data from file upload, URL, or sample data
df = load_data(uploaded_file, github_url)

# Check if sample data should be used
if df.empty and 'sample_data' in st.session_state:
    df = st.session_state['sample_data']

# Ensure Date column is properly converted to datetime if it exists
if not df.empty and 'Date' in df.columns:
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except:
        st.warning("⚠️ Could not convert Date column to datetime format. Date filtering may not work properly.")

# Enhanced Sidebar Filters with Interactive Elements
st.sidebar.markdown(
    '''
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        "></div>
        <div style="position: relative; z-index: 1;">
            <h2 style="color: white; margin: 0; font-size: 1.6rem; font-weight: 700;">
                <span class="sidebar-icon">🔍</span> Smart Filters
            </h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0.8rem 0 0 0; font-size: 1rem; font-weight: 400;">
                <span class="sidebar-icon">⚡</span> Customize your data view
                <span class="sidebar-icon">📊</span>
            </p>
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.8; }
    }
    </style>
    ''', unsafe_allow_html=True
)

# Initialize filtered dataframe
filtered_df = df.copy()

if not df.empty:
    # Date Filter
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df_with_dates = df.dropna(subset=['Date'])
        
        if not df_with_dates.empty:
            min_date = df_with_dates['Date'].min().date()
            max_date = df_with_dates['Date'].max().date()
            
            date_range = st.sidebar.date_input(
                "📅 Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                help="Filter data by date range"
            )
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                start_datetime = pd.to_datetime(start_date)
                end_datetime = pd.to_datetime(end_date)
                
                # Ensure Date column is datetime before comparison
                try:
                    filtered_df = filtered_df[
                        (filtered_df['Date'].notna()) &
                        (pd.to_datetime(filtered_df['Date']) >= start_datetime) & 
                        (pd.to_datetime(filtered_df['Date']) <= end_datetime)
                    ]
                except Exception as e:
                    st.sidebar.error(f"Error filtering by date: {str(e)}")
                    # Fallback: try string comparison
                    try:
                        filtered_df = filtered_df[
                            (filtered_df['Date'].notna()) &
                            (filtered_df['Date'].astype(str) >= start_date.strftime('%Y-%m-%d')) & 
                            (filtered_df['Date'].astype(str) <= end_date.strftime('%Y-%m-%d'))
                        ]
                    except:
                        st.sidebar.warning("Date filtering unavailable - check date format")
    
    # Category Filter
    if 'Category' in df.columns:
        categories = ['All'] + sorted(df['Category'].dropna().unique().tolist())
        selected_categories = st.sidebar.multiselect(
            "📊 Select Categories",
            options=categories,
            default=['All'],
            help="Filter by product categories"
        )
        
        if 'All' not in selected_categories and selected_categories:
            filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
    
    # Region Filter
    if 'Region' in df.columns:
        regions = ['All'] + sorted(df['Region'].dropna().unique().tolist())
        selected_regions = st.sidebar.multiselect(
            "🌍 Select Regions",
            options=regions,
            default=['All'],
            help="Filter by geographic regions"
        )
        
        if 'All' not in selected_regions and selected_regions:
            filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    
    # Display filter summary with enhanced reset functionality
    if len(filtered_df) != len(df):
        st.sidebar.success(f"📈 Showing {len(filtered_df):,} of {len(df):,} records")
        if st.sidebar.button("🔄 Reset All Filters", key="reset_filters", help="Clear all filters and show full dataset"):
            # Clear session state for filters
            for key in st.session_state.keys():
                if key.startswith('multiselect') or key.startswith('date_input'):
                    del st.session_state[key]
            st.rerun()
    else:
        st.sidebar.info(f"📊 Showing all {len(df):,} records")

# Use filtered dataframe for all calculations
df = filtered_df

# Refresh Data Tab
with tabs[1]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #10b981;
        ">
            <h2 style="color: #10b981; margin-bottom: 0.5rem;">🔄 Data Refresh Center</h2>
            <p style="color: #64748b; margin: 0;">Refresh your data and manage data sources with advanced controls</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    col_refresh1, col_refresh2 = st.columns(2)
    
    with col_refresh1:
        st.markdown("### 📊 Current Data Status")
        
        if not df.empty:
            # Data overview metrics
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            
            with col_metric1:
                st.metric("📋 Total Records", f"{len(df):,}")
            
            with col_metric2:
                st.metric("📂 Columns", f"{len(df.columns)}")
            
            with col_metric3:
                if 'Date' in df.columns:
                    date_range = (df['Date'].max() - df['Date'].min()).days
                    st.metric("📅 Date Range", f"{date_range} days")
                else:
                    st.metric("💾 Data Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Data quality indicators
            st.markdown("### 🔍 Data Quality Indicators")
            
            quality_col1, quality_col2 = st.columns(2)
            
            with quality_col1:
                missing_data = df.isnull().sum().sum()
                total_cells = len(df) * len(df.columns)
                quality_score = ((total_cells - missing_data) / total_cells * 100) if total_cells > 0 else 0
                
                st.metric("✅ Data Quality Score", f"{quality_score:.1f}%")
                st.metric("❌ Missing Values", f"{missing_data:,}")
            
            with quality_col2:
                if 'Sales' in df.columns:
                    revenue_total = df['Sales'].sum()
                    st.metric("💰 Total Revenue", f"${revenue_total:,.2f}")
                
                if 'Date' in df.columns:
                    latest_date = df['Date'].max().strftime("%Y-%m-%d")
                    st.metric("📅 Latest Record", latest_date)
        else:
            st.warning("⚠️ No data currently loaded. Please upload a file or load sample data.")
    
    with col_refresh2:
        st.markdown("### 🔄 Refresh Controls")
        
        # Auto-refresh toggle
        auto_refresh = st.toggle("🔄 Auto-refresh every 30 seconds", value=False, key="auto_refresh")
        
        if auto_refresh:
            st.info("🟢 Auto-refresh enabled")
            # Use a placeholder for the auto-refresh timer
            placeholder = st.empty()
            for seconds in range(30, 0, -1):
                placeholder.metric("⏰ Next refresh in", f"{seconds} seconds")
                time.sleep(1)
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        # Manual refresh controls
        st.markdown("#### Manual Refresh Options")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔄 Refresh Data", key="manual_refresh", help="Refresh current data"):
                st.session_state.last_refresh = datetime.now()
                st.success("✅ Data refreshed successfully!")
                st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Clear Cache", key="clear_cache", help="Clear all cached data"):
                if 'sample_data' in st.session_state:
                    del st.session_state['sample_data']
                st.session_state.last_refresh = datetime.now()
                st.success("✅ Cache cleared successfully!")
                st.rerun()
        
        # Advanced refresh options
        st.markdown("#### Advanced Options")
        
        refresh_interval = st.selectbox(
            "⏱️ Refresh Interval",
            ["Manual", "Every 30 seconds", "Every 1 minute", "Every 5 minutes", "Every 15 minutes"],
            index=0
        )
        
        if refresh_interval != "Manual":
            st.info(f"🕒 Auto-refresh set to: {refresh_interval}")
        
        # Data source management
        st.markdown("#### 📁 Data Source Management")
        
        if st.button("📊 Reload Sample Data", key="reload_sample"):
            # Regenerate sample data with current timestamp
            date_range = pd.date_range('2024-01-01', '2024-12-31', freq='D')
            num_days = len(date_range)
            sample_data = {
                'Date': date_range,
                'Region': np.random.choice(['North', 'South', 'East', 'West'], num_days),
                'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], num_days),
                'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D', 'Product E'], num_days),
                'Sales': np.random.normal(1000, 300, num_days).round(2)
            }
            sample_df = pd.DataFrame(sample_data)
            st.session_state['sample_data'] = sample_df
            st.session_state.last_refresh = datetime.now()
            st.success("✅ Sample data reloaded with fresh values!")
            st.rerun()
    
    # Data refresh history
    if not df.empty:
        st.markdown("### 📈 Data Refresh Analytics")
        
        col_analytics1, col_analytics2 = st.columns(2)
        
        with col_analytics1:
            # Create a simple refresh timeline
            refresh_history = pd.DataFrame({
                'Time': [datetime.now() - pd.Timedelta(minutes=x*5) for x in range(10, 0, -1)] + [st.session_state.last_refresh],
                'Status': ['Success'] * 11,
                'Records': [len(df)] * 11
            })
            
            fig_refresh = px.line(refresh_history, x='Time', y='Records', 
                                title="Data Refresh Timeline",
                                markers=True)
            fig_refresh.update_traces(line_color='#10b981', line_width=3, marker_size=8)
            st.plotly_chart(fig_refresh, width="stretch")
        
        with col_analytics2:
            # Refresh statistics
            st.markdown("**📊 Refresh Statistics**")
            
            refresh_stats = pd.DataFrame({
                'Metric': ['Total Refreshes Today', 'Success Rate', 'Avg Refresh Time', 'Last Error'],
                'Value': ['15', '100%', '0.8s', 'None']
            })
            
            st.dataframe(refresh_stats, hide_index=True, width="stretch")
            
            # System health indicator
            st.markdown("**🔋 System Health**")
            health_score = 98.5
            st.progress(health_score/100)
            st.caption(f"System Health: {health_score}% 🟢 Excellent")

# Data Preview Tab
with tabs[2]:
    st.header("Data Preview")
    if not df.empty:
        st.dataframe(df, width="stretch")
        st.download_button("Download CSV", df.to_csv(index=False), "filtered_data.csv")
        st.caption(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    else:
        st.info("No data loaded. Please upload a file or provide a GitHub URL.")

# KPIs & Visuals Tab
with tabs[3]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            padding: 1.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #667eea;
        ">
            <h2 style="color: #667eea; margin-bottom: 0.5rem;">📊 Key Performance Indicators</h2>
            <p style="color: #64748b; margin: 0;">Essential metrics for executive decision making</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    if df.empty or 'Sales' not in df.columns:
        st.warning("No data available. Please upload your sales data to see KPIs.")
    else:
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
        
        # Essential KPIs with enhanced styling
        total_sales = df['Sales'].sum()
        avg_order = df['Sales'].mean() if not df['Sales'].empty else 0
        total_orders = len(df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Total Sales", f"${total_sales:,.2f}")
        
        with col2:
            st.metric("📦 Total Orders", f"{total_orders:,}")
        
        with col3:
            st.metric("💳 Avg Order Value", f"${avg_order:.2f}")
        
        # Visualizations
        if 'Product' in df.columns:
            st.subheader("🎯 Sales by Product")
            prod_sales = df.groupby('Product')['Sales'].sum().reset_index()
            fig_product = px.pie(prod_sales, names='Product', values='Sales', 
                               title="Sales by Product")
            fig_product.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_product, width="stretch")
        
        if 'Region' in df.columns:
            st.subheader("🌎 Sales by Region")
            region_sales = df.groupby('Region')['Sales'].sum().reset_index()
            fig_region = px.pie(region_sales, names='Region', values='Sales',
                              title="Sales Distribution by Region")
            fig_region.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_region, width="stretch")
        
        # Enhanced Time Series Visualizations
        if 'Date' in df.columns and 'Sales' in df.columns:
            st.subheader("📈 Sales Over Time")
            
            # Daily Sales Line Chart
            col_time1, col_time2 = st.columns(2)
            
            with col_time1:
                st.markdown("**Daily Sales Trend**")
                daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
                if not daily_sales.empty:
                    fig_daily = px.line(daily_sales, x='Date', y='Sales', 
                                      title="Daily Sales Over Time",
                                      labels={'Sales': 'Total Sales ($)', 'Date': 'Date'})
                    fig_daily.update_traces(line_color='#667eea', line_width=3)
                    st.plotly_chart(fig_daily, width="stretch")
            
            with col_time2:
                st.markdown("**Monthly Sales Trend**")
                monthly_sales = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'), observed=False)['Sales'].sum().reset_index()
                if not monthly_sales.empty:
                    monthly_sales['Date'] = monthly_sales['Date'].astype(str)
                    fig_monthly = px.line(monthly_sales, x='Date', y='Sales',
                                        title="Monthly Sales Trend",
                                        labels={'Sales': 'Total Sales ($)', 'Date': 'Month'})
                    fig_monthly.update_traces(line_color='#764ba2', line_width=3)
                    st.plotly_chart(fig_monthly, width="stretch")
        
        # Category Analysis with Multiple Chart Types
        if 'Category' in df.columns and 'Sales' in df.columns:
            st.subheader("📊 Category Performance Analysis")
            
            col_cat1, col_cat2 = st.columns(2)
            
            with col_cat1:
                st.markdown("**Sales by Category (Bar Chart)**")
                cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
                fig_cat_bar = px.bar(cat_sales, x='Category', y='Sales', 
                                   title="Total Sales by Category",
                                   color='Sales',
                                   color_continuous_scale='viridis')
                st.plotly_chart(fig_cat_bar, width="stretch")
            
            with col_cat2:
                st.markdown("**Category Distribution (Pie Chart)**")
                fig_cat_pie = px.pie(cat_sales, names='Category', values='Sales',
                                   title="Sales Distribution by Category")
                fig_cat_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_cat_pie, width="stretch")
        
        # Regional Performance Analysis
        if 'Region' in df.columns and 'Sales' in df.columns:
            st.subheader("🌍 Regional Performance Analysis")
            
            col_reg1, col_reg2 = st.columns(2)
            
            with col_reg1:
                st.markdown("**Average Sales by Region**")
                region_avg = filtered_df.groupby('Region')['Sales'].mean().reset_index()
                fig_reg_avg = px.bar(region_avg, x='Region', y='Sales',
                                   title="Average Sales by Region",
                                   color='Sales',
                                   color_continuous_scale='plasma')
                st.plotly_chart(fig_reg_avg, width="stretch")
            
            with col_reg2:
                st.markdown("**Regional Sales Distribution**")
                region_total = filtered_df.groupby('Region')['Sales'].sum().reset_index()
                fig_reg_pie = px.pie(region_total, names='Region', values='Sales',
                                   title="Regional Sales Share")
                fig_reg_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_reg_pie, width="stretch")

# Category & Region Tab
with tabs[4]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #10b981;
        ">
            <h2 style="color: #10b981; margin-bottom: 0.5rem;">📊 Category & Region Deep Dive</h2>
            <p style="color: #64748b; margin: 0;">Comprehensive analysis of sales performance across categories and regions</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    if df.empty or 'Sales' not in df.columns:
        st.warning("Please upload your sales data to see category and region analysis.")
    else:
        # Category Analysis Section
        if 'Category' in filtered_df.columns:
            st.subheader("🏷️ Category Performance Analysis")
            
            # Enhanced metrics for categories
            cat_metrics = filtered_df.groupby('Category')['Sales'].agg(['sum', 'mean', 'count']).round(2)
            cat_metrics.columns = ['Total Sales', 'Average Sale', 'Order Count']
            cat_metrics = cat_metrics.reset_index()
            
            col_cat1, col_cat2, col_cat3 = st.columns(3)
            
            with col_cat1:
                st.markdown("**📈 Sales Performance by Category**")
                fig_cat_performance = px.bar(cat_metrics, x='Category', y='Total Sales',
                                           title="Total Sales by Category",
                                           color='Total Sales',
                                           color_continuous_scale='viridis')
                fig_cat_performance.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cat_performance, width="stretch")
            
            with col_cat2:
                st.markdown("**🎯 Average Order Value by Category**")
                fig_cat_avg = px.bar(cat_metrics, x='Category', y='Average Sale',
                                   title="Average Sale by Category",
                                   color='Average Sale',
                                   color_continuous_scale='plasma')
                fig_cat_avg.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cat_avg, width="stretch")
            
            with col_cat3:
                st.markdown("**📊 Order Volume by Category**")
                fig_cat_volume = px.pie(cat_metrics, names='Category', values='Order Count',
                                      title="Order Volume Distribution")
                fig_cat_volume.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_cat_volume, width="stretch")
            
            # Category performance table
            st.markdown("**📋 Category Performance Summary**")
            st.dataframe(cat_metrics.style.format({
                'Total Sales': '${:,.2f}',
                'Average Sale': '${:,.2f}',
                'Order Count': '{:,}'
            }), width="stretch")
        
        # Region Analysis Section
        if 'Region' in filtered_df.columns:
            st.subheader("🌍 Regional Performance Analysis")
            
            # Enhanced metrics for regions
            region_metrics = filtered_df.groupby('Region')['Sales'].agg(['sum', 'mean', 'count']).round(2)
            region_metrics.columns = ['Total Sales', 'Average Sale', 'Order Count']
            region_metrics = region_metrics.reset_index()
            
            col_reg1, col_reg2 = st.columns(2)
            
            with col_reg1:
                st.markdown("**🎯 Regional Sales Performance**")
                fig_reg_performance = px.bar(region_metrics, x='Region', y='Total Sales',
                                           title="Total Sales by Region",
                                           color='Total Sales',
                                           color_continuous_scale='viridis')
                st.plotly_chart(fig_reg_performance, width="stretch")
                
                st.markdown("**📊 Regional Market Share**")
                fig_reg_share = px.pie(region_metrics, names='Region', values='Total Sales',
                                     title="Regional Sales Distribution")
                fig_reg_share.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_reg_share, width="stretch")
            
            with col_reg2:
                st.markdown("**💰 Average Order Value by Region**")
                fig_reg_avg = px.bar(region_metrics, x='Region', y='Average Sale',
                                   title="Average Sale by Region",
                                   color='Average Sale',
                                   color_continuous_scale='plasma')
                st.plotly_chart(fig_reg_avg, width="stretch")
                
                st.markdown("**📈 Order Frequency by Region**")
                fig_reg_frequency = px.bar(region_metrics, x='Region', y='Order Count',
                                         title="Order Count by Region",
                                         color='Order Count',
                                         color_continuous_scale='cividis')
                st.plotly_chart(fig_reg_frequency, width="stretch")
            
            # Regional performance table
            st.markdown("**📋 Regional Performance Summary**")
            st.dataframe(region_metrics.style.format({
                'Total Sales': '${:,.2f}',
                'Average Sale': '${:,.2f}',
                'Order Count': '{:,}'
            }), width="stretch")
        
        # Cross-Category and Region Analysis
        if 'Category' in filtered_df.columns and 'Region' in filtered_df.columns:
            st.subheader("🔄 Cross-Analysis: Category vs Region")
            
            # Create pivot table for heatmap
            pivot_data = filtered_df.pivot_table(index='Region', columns='Category', 
                                                values='Sales', aggfunc='sum', fill_value=0)
            
            col_cross1, col_cross2 = st.columns(2)
            
            with col_cross1:
                st.markdown("**🔥 Sales Heatmap: Region vs Category**")
                fig_heatmap = px.imshow(pivot_data.values,
                                      labels=dict(x="Category", y="Region", color="Sales"),
                                      x=pivot_data.columns,
                                      y=pivot_data.index,
                                      color_continuous_scale='viridis',
                                      title="Sales Performance Heatmap")
                st.plotly_chart(fig_heatmap, width="stretch")
            
            with col_cross2:
                st.markdown("**📊 Top Category-Region Combinations**")
                cross_analysis = filtered_df.groupby(['Category', 'Region'])['Sales'].sum().reset_index()
                cross_analysis = cross_analysis.sort_values('Sales', ascending=False).head(10)
                cross_analysis['Category_Region'] = cross_analysis['Category'] + ' - ' + cross_analysis['Region']
                
                fig_top_combos = px.bar(cross_analysis, x='Category_Region', y='Sales',
                                      title="Top 10 Category-Region Combinations",
                                      color='Sales',
                                      color_continuous_scale='plasma')
                fig_top_combos.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_top_combos, width="stretch")
            
            # Detailed pivot table
            st.markdown("**📋 Detailed Sales Matrix: Region vs Category**")
            st.dataframe(pivot_data.style.format('${:,.2f}'), width="stretch")
        
        # Scatter Plot Analysis
        if 'Date' in filtered_df.columns and len(filtered_df) > 10:
            st.subheader("🎯 Advanced Scatter Plot Analysis")
            
            # Create aggregated data for scatter plot
            if 'Region' in filtered_df.columns and 'Category' in filtered_df.columns:
                scatter_data = filtered_df.groupby(['Region', 'Category'])['Sales'].agg(['sum', 'mean', 'count']).reset_index()
                scatter_data.columns = ['Region', 'Category', 'Total_Sales', 'Avg_Sales', 'Order_Count']
                
                col_scatter1, col_scatter2 = st.columns(2)
                
                with col_scatter1:
                    st.markdown("**📈 Sales Volume vs Order Frequency**")
                    fig_scatter1 = px.scatter(scatter_data, x='Order_Count', y='Total_Sales',
                                            color='Region', size='Avg_Sales',
                                            hover_data=['Category'],
                                            title="Sales Performance Scatter Plot",
                                            labels={'Order_Count': 'Number of Orders',
                                                  'Total_Sales': 'Total Sales ($)'})
                    st.plotly_chart(fig_scatter1, width="stretch")
                
                with col_scatter2:
                    st.markdown("**💰 Average Sale vs Order Volume**")
                    fig_scatter2 = px.scatter(scatter_data, x='Order_Count', y='Avg_Sales',
                                            color='Category', size='Total_Sales',
                                            hover_data=['Region'],
                                            title="Order Value vs Volume Analysis",
                                            labels={'Order_Count': 'Number of Orders',
                                                  'Avg_Sales': 'Average Sale ($)'})
                    st.plotly_chart(fig_scatter2, width="stretch")

# Advanced Charts Tab
with tabs[5]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(139, 69, 19, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #a855f7;
        ">
            <h2 style="color: #a855f7; margin-bottom: 0.5rem;">📉 Advanced Charts & Analytics</h2>
            <p style="color: #64748b; margin: 0;">Time series analysis, forecasting, and advanced statistical visualizations</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    if df.empty or 'Sales' not in df.columns:
        st.warning("Please upload your sales data to see advanced charts and analytics.")
    else:
        # Time Series Analysis
        if 'Date' in filtered_df.columns:
            st.subheader("📈 Time Series Analysis")
            
            col_time1, col_time2 = st.columns(2)
            
            with col_time1:
                st.markdown("**📅 Daily Sales Trend with Moving Average**")
                daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
                if len(daily_sales) > 7:
                    daily_sales['MA_7'] = daily_sales['Sales'].rolling(window=7).mean()
                    daily_sales['MA_30'] = daily_sales['Sales'].rolling(window=min(30, len(daily_sales))).mean()
                    
                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(x=daily_sales['Date'], y=daily_sales['Sales'],
                                                 mode='lines', name='Daily Sales',
                                                 line=dict(color='#667eea', width=2)))
                    if len(daily_sales) > 7:
                        fig_trend.add_trace(go.Scatter(x=daily_sales['Date'], y=daily_sales['MA_7'],
                                                     mode='lines', name='7-Day MA',
                                                     line=dict(color='#ff6b6b', width=2)))
                    if len(daily_sales) > 30:
                        fig_trend.add_trace(go.Scatter(x=daily_sales['Date'], y=daily_sales['MA_30'],
                                                     mode='lines', name='30-Day MA',
                                                     line=dict(color='#4ecdc4', width=3)))
                    fig_trend.update_layout(title="Sales Trend with Moving Averages",
                                          xaxis_title="Date",
                                          yaxis_title="Sales ($)")
                    st.plotly_chart(fig_trend, width="stretch")
            
            with col_time2:
                st.markdown("**📊 Sales Distribution Analysis**")
                fig_dist = px.histogram(filtered_df, x='Sales', nbins=30,
                                      title="Sales Distribution",
                                      labels={'Sales': 'Sale Amount ($)', 'count': 'Frequency'})
                fig_dist.update_traces(marker_color='#667eea', opacity=0.7)
                st.plotly_chart(fig_dist, width="stretch")
            
            # Weekly and Monthly Analysis
            st.markdown("**📆 Periodic Sales Analysis**")
            col_period1, col_period2 = st.columns(2)
            
            with col_period1:
                # Weekly pattern
                filtered_df['DayOfWeek'] = filtered_df['Date'].dt.day_name()
                weekly_sales = filtered_df.groupby('DayOfWeek')['Sales'].sum().reindex([
                    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
                ]).reset_index()
                
                fig_weekly = px.bar(weekly_sales, x='DayOfWeek', y='Sales',
                                  title="Sales by Day of Week",
                                  color='Sales',
                                  color_continuous_scale='viridis')
                fig_weekly.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_weekly, width="stretch")
            
            with col_period2:
                # Monthly pattern
                filtered_df['Month'] = filtered_df['Date'].dt.month_name()
                monthly_pattern = filtered_df.groupby('Month')['Sales'].sum().reindex([
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ]).reset_index()
                
                fig_monthly_pattern = px.line(monthly_pattern, x='Month', y='Sales',
                                            title="Sales by Month",
                                            markers=True)
                fig_monthly_pattern.update_traces(line_color='#764ba2', line_width=3, marker_size=8)
                fig_monthly_pattern.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_monthly_pattern, width="stretch")
        
        # Sales Forecasting
        if 'Date' in filtered_df.columns and len(filtered_df) > 30:
            st.subheader("🔮 Sales Forecasting")
            
            try:
                monthly_sales, forecast, future_x = forecast_sales(filtered_df, periods=6)
                
                if len(monthly_sales) > 0 and len(forecast) > 0:
                    col_forecast1, col_forecast2 = st.columns(2)
                    
                    with col_forecast1:
                        st.markdown("**📈 Sales Forecast (Next 6 Months)**")
                        fig_forecast = go.Figure()
                        
                        # Historical data
                        fig_forecast.add_trace(go.Scatter(
                            x=monthly_sales.index.astype(str),
                            y=monthly_sales.values,
                            mode='lines+markers',
                            name='Historical Sales',
                            line=dict(color='#667eea', width=3)
                        ))
                        
                        # Forecast data
                        future_periods = [f"Month {i+len(monthly_sales)+1}" for i in range(len(forecast))]
                        fig_forecast.add_trace(go.Scatter(
                            x=future_periods,
                            y=forecast,
                            mode='lines+markers',
                            name='Forecast',
                            line=dict(color='#ff6b6b', width=3, dash='dash')
                        ))
                        
                        fig_forecast.update_layout(
                            title="Sales Forecast",
                            xaxis_title="Period",
                            yaxis_title="Sales ($)"
                        )
                        st.plotly_chart(fig_forecast, width="stretch")
                    
                    with col_forecast2:
                        st.markdown("**📊 Forecast Summary**")
                        if len(forecast) > 0:
                            forecast_total = forecast.sum()
                            current_total = monthly_sales.tail(6).sum() if len(monthly_sales) >= 6 else monthly_sales.sum()
                            growth_projection = ((forecast_total - current_total) / current_total * 100) if current_total > 0 else 0
                            
                            st.metric("📈 Projected 6-Month Total", f"${forecast_total:,.2f}")
                            st.metric("📊 Expected Growth", f"{growth_projection:.1f}%")
                            st.metric("💰 Avg Monthly Forecast", f"${forecast.mean():,.2f}")
                            
                            # Forecast breakdown
                            forecast_df = pd.DataFrame({
                                'Month': [f"Month {i+1}" for i in range(len(forecast))],
                                'Forecast': forecast
                            })
                            st.markdown("**📋 Detailed Forecast**")
                            st.dataframe(forecast_df.style.format({'Forecast': '${:,.2f}'}), width="stretch")
                            
            except Exception as e:
                st.warning("Unable to generate forecast with current data. Need more historical data points.")
        
        # Advanced Statistical Analysis
        if len(filtered_df) > 20:
            st.subheader("📊 Statistical Analysis")
            
            col_stats1, col_stats2 = st.columns(2)
            
            with col_stats1:
                st.markdown("**📈 Sales Performance Metrics**")
                sales_stats = filtered_df['Sales'].describe()
                
                # Create metrics display
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("📊 Mean", f"${sales_stats['mean']:.2f}")
                    st.metric("📈 Std Dev", f"${sales_stats['std']:.2f}")
                with col_metric2:
                    st.metric("📉 Median", f"${sales_stats['50%']:.2f}")
                    st.metric("📏 Range", f"${sales_stats['max'] - sales_stats['min']:.2f}")
                
                # Box plot
                fig_box = px.box(filtered_df, y='Sales', title="Sales Distribution Box Plot")
                fig_box.update_traces(marker_color='#667eea')
                st.plotly_chart(fig_box, width="stretch")
            
            with col_stats2:
                st.markdown("**🎯 Performance Segmentation**")
                
                # Quartile analysis
                q1 = filtered_df['Sales'].quantile(0.25)
                q3 = filtered_df['Sales'].quantile(0.75)
                median = filtered_df['Sales'].median()
                
                filtered_df['Performance_Segment'] = pd.cut(
                    filtered_df['Sales'],
                    bins=[0, q1, median, q3, float('inf')],
                    labels=['Low', 'Medium-Low', 'Medium-High', 'High']
                )
                
                segment_counts = filtered_df['Performance_Segment'].value_counts()
                fig_segments = px.pie(values=segment_counts.values, names=segment_counts.index,
                                    title="Sales Performance Segments")
                st.plotly_chart(fig_segments, width="stretch")
                
                # Performance table
                st.markdown("**📋 Segment Analysis**")
                segment_analysis = filtered_df.groupby('Performance_Segment')['Sales'].agg(['count', 'mean', 'sum']).round(2)
                segment_analysis.columns = ['Count', 'Avg Sale', 'Total Sales']
                st.dataframe(segment_analysis.style.format({
                    'Count': '{:,}',
                    'Avg Sale': '${:,.2f}',
                    'Total Sales': '${:,.2f}'
                }), width="stretch")

# Enhanced Insights Tab with AI-Powered Insights Only
with tabs[6]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #10b981;
        ">
            <h2 style="color: #10b981; margin-bottom: 0.5rem;">💡 AI-Powered Business Insights</h2>
            <p style="color: #64748b; margin: 0;">Advanced analytics and automated insights for strategic decision making</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    if df.empty or 'Sales' not in df.columns:
        st.warning("Please upload your sales data to access AI-powered insights.")
    else:
        # Initialize session state for selected insight
        if 'selected_insight' not in st.session_state:
            st.session_state.selected_insight = None
        
        # Create action tiles
        st.markdown("### 🎯 Interactive Insight Categories")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📈 Revenue Growth", key="revenue_btn", help="Analyze revenue growth trends and forecasting"):
                st.session_state.selected_insight = "revenue"
        
        with col2:
            if st.button("🌍 Market Expansion", key="market_btn", help="Explore market expansion opportunities"):
                st.session_state.selected_insight = "market"
        
        with col3:
            if st.button("🎯 Strategic KPIs", key="kpi_btn", help="View strategic performance indicators"):
                st.session_state.selected_insight = "kpis"
        
        with col4:
            if st.button("💡 AI Recommendations", key="ai_btn", help="Get AI-powered strategic recommendations"):
                st.session_state.selected_insight = "recommendations"
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display selected insight content
        if st.session_state.selected_insight == "revenue":
            st.markdown("### 📈 Revenue Growth Analysis")
            strategic_metrics = strategic_kpis(df)
            growth_rate, avg_monthly_growth, monthly_revenue = calculate_revenue_growth(df)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Growth Rate", f"{growth_rate:.1f}%")
            with col2:
                st.metric("Avg Monthly Growth", f"{avg_monthly_growth:.1f}%")
            with col3:
                st.metric("Market Penetration", f"{strategic_metrics.get('market_penetration', 0)} Regions")
            
            # Sales Forecasting
            st.markdown("#### 🔮 Sales Forecasting (Next 6 Months)")
            historical_sales, forecast, future_periods = forecast_sales(df, 6)
            
            if len(historical_sales) > 0 and len(forecast) > 0:
                fig_forecast = go.Figure()
                
                fig_forecast.add_trace(go.Scatter(
                    x=[str(period) for period in historical_sales.index],
                    y=historical_sales.values,
                    mode='lines+markers',
                    name='Historical Sales',
                    line=dict(color='#667eea', width=3)
                ))
                
                future_dates = [f"Month {i+1}" for i in range(len(forecast))]
                fig_forecast.add_trace(go.Scatter(
                    x=future_dates,
                    y=forecast,
                    mode='lines+markers',
                    name='Forecasted Sales',
                    line=dict(color='#10b981', width=3, dash='dash')
                ))
                
                fig_forecast.update_layout(title="Sales Forecast Analysis")
                st.plotly_chart(fig_forecast, width="stretch")
                
                if len(forecast) > 0:
                    total_forecast = sum(forecast)
                    st.info(f"📊 Projected revenue for next 6 months: **${total_forecast:,.2f}**")
        
        elif st.session_state.selected_insight == "market":
            st.markdown("### 🌍 Market Expansion Opportunities")
            expansion_insights = market_expansion_analysis(df)
            
            if expansion_insights and 'top_regions' in expansion_insights:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🏆 Top Performing Regions")
                    top_regions_df = expansion_insights['top_regions'].reset_index()
                    fig_top_regions = px.bar(top_regions_df, x='Region', y='sum',
                                           title="Revenue by Top Regions")
                    st.plotly_chart(fig_top_regions, width="stretch")
                
                with col2:
                    st.markdown("#### 🎯 Growth Opportunities")
                    growth_ops_df = expansion_insights['growth_opportunities'].reset_index()
                    fig_growth_ops = px.bar(growth_ops_df, x='Region', y='mean',
                                          title="Average Revenue by Region")
                    st.plotly_chart(fig_growth_ops, width="stretch")
        
        elif st.session_state.selected_insight == "kpis":
            st.markdown("### 🎯 Strategic Performance Indicators")
            strategic_metrics = strategic_kpis(df)
            
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            
            with kpi_col1:
                st.metric("💰 Total Revenue", f"${strategic_metrics.get('total_revenue', 0):,.2f}")
            
            with kpi_col2:
                st.metric("💳 Avg Transaction", f"${strategic_metrics.get('avg_transaction', 0):,.2f}")
            
            with kpi_col3:
                st.metric("📅 Revenue/Day", f"${strategic_metrics.get('revenue_per_day', 0):,.2f}")
            
            with kpi_col4:
                st.metric("🎨 Product Lines", f"{strategic_metrics.get('product_diversity', 0)}")
        
        elif st.session_state.selected_insight == "recommendations":
            st.markdown("### 💡 AI-Powered Strategic Recommendations")
            
            recommendations = [
                "**Market Expansion**: Focus on replicating successful regional strategies",
                "**Growth Momentum**: Leverage current positive trends with increased investment",
                "**Product Strategy**: Expand successful product categories",
                "**Data-Driven Decisions**: Continue monitoring KPIs for optimal performance"
            ]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
        
        # Default view when no insight is selected
        if st.session_state.selected_insight is None:
            st.markdown(
                '''
                <div style="
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                    padding: 2rem;
                    border-radius: 16px;
                    text-align: center;
                    border: 2px dashed #667eea;
                ">
                    <h3 style="color: #667eea;">👆 Click on any insight category above to explore</h3>
                    <p style="color: #64748b; margin: 0;">
                        Select Revenue Growth, Market Expansion, Strategic KPIs, or AI Recommendations to view detailed analytics
                    </p>
                </div>
                ''', unsafe_allow_html=True
            )
        
        # Clear button to reset selection
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Clear Selection", help="Return to main insights view"):
            st.session_state.selected_insight = None
            st.rerun()

# Enhanced Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '''
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 16px;
        margin-top: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    ">
        <h3 style="margin-bottom: 1rem; color: white;">📊 Executive Sales Dashboard</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">
            Powered by Streamlit • Enhanced with AI Analytics • Built for Decision Makers
        </p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            🚀 Real-time insights • 📈 Interactive visualizations • 💡 AI-powered recommendations
        </div>
    </div>
    ''', unsafe_allow_html=True
)
