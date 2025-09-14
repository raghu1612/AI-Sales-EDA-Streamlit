import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time
import io

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

# --- Data Loading & Validation Functions ---
@st.cache_data(ttl=300)
def load_default_github_data():
    """Load the default dataset from GitHub raw link with column mapping"""
    try:
        github_url = "https://raw.githubusercontent.com/raghu1612/AI-Sales-EDA-Streamlit/main/sales_data.csv"
        df = pd.read_csv(github_url)
        
        # Handle column mapping and missing columns
        df = handle_column_mapping(df)
        
        return df
    except Exception as e:
        st.error(f"Error loading default GitHub dataset: {e}")
        return pd.DataFrame()

def handle_column_mapping(df):
    """Handle column mapping and add missing columns"""
    try:
        # Map Category to Product if Product doesn't exist
        if 'Category' in df.columns and 'Product' not in df.columns:
            df['Product'] = df['Category']
        
        # Add Region if missing (use dummy values)
        if 'Region' not in df.columns:
            regions = ['North', 'South', 'East', 'West']
            df['Region'] = np.random.choice(regions, len(df))
        
        # Add Profit if missing (calculate as % of Sales)
        if 'Profit' not in df.columns:
            # Generate profit as 15-25% of sales with some randomness
            profit_margin = np.random.uniform(0.15, 0.25, len(df))
            df['Profit'] = (df['Sales'] * profit_margin).round(2)
        
        # Ensure Date column is properly formatted
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error in column mapping: {e}")
        return df

@st.cache_data(ttl=300)
def generate_sample_data():
    """Generate sample sales data for demonstration"""
    try:
        # Generate date range and get the actual number of days
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        num_days = len(dates)
        
        sample_data = {
            'Date': dates,
            'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'], num_days),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], num_days),
            'Sales': np.random.normal(1000, 300, num_days).round(2),
            'Profit': np.random.normal(200, 50, num_days).round(2)
        }
        return pd.DataFrame(sample_data)
    except Exception as e:
        st.error(f"Error generating sample data: {e}")
        return pd.DataFrame()

def validate_schema(df):
    """Validate that the dataframe has required columns with flexible mapping"""
    # Essential columns that must exist
    essential_columns = ["Date", "Sales"]
    
    # Check for essential columns
    missing_essential = [col for col in essential_columns if col not in df.columns]
    if missing_essential:
        st.error(f"❌ Missing essential columns: {', '.join(missing_essential)}")
        return False
    
    # Check for Product/Category column (flexible)
    has_product = 'Product' in df.columns or 'Category' in df.columns
    if not has_product:
        st.error("❌ Missing Product or Category column")
        return False
    
    # Region is optional but recommended
    if 'Region' not in df.columns:
        st.warning("⚠️ Region column not found - some features may be limited")
    
    # Profit is optional - we can calculate it or use dummy values
    if 'Profit' not in df.columns:
        st.info("ℹ️ Profit column not found - will generate estimated values")
    
    return True

@st.cache_data(ttl=300)
def load_and_validate_data(uploaded_file, use_sample_data):
    """Load data with proper prioritization and validation"""
    df = pd.DataFrame()
    data_source = ""
    
    # Priority 1: User uploaded file
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Apply column mapping to uploaded files
            df = handle_column_mapping(df)
            data_source = f"📁 Uploaded file: {uploaded_file.name}"
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
            df = pd.DataFrame()
    
    # Priority 2: Sample data if requested
    elif use_sample_data:
        df = generate_sample_data()
        data_source = "🎯 Sample dataset generated"
    
    # Priority 3: Default GitHub dataset
    else:
        df = load_default_github_data()
        data_source = "🌐 Default GitHub dataset loaded"
    
    return df, data_source

st.set_page_config(
    page_title="Executive Sales Dashboard", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Initialize session state for refresh timestamp
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# --- Enhanced Professional Theme with Rich UI/UX ---
st.markdown(
    '''<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important;
        color: #1e293b !important;
    }
    
    /* Main container with glass morphism effect */
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
    
    .block-container:hover {
        box-shadow: 0 12px 48px rgba(31, 38, 135, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Header styling with gradient text */
    .main-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Enhanced tab styling */
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
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #667eea !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        border: none !important;
    }
    
    /* Enhanced metric cards with animations */
    .stMetric {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: left 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stMetric:hover::before {
        left: 0;
    }
    
    /* Button enhancements with gradients */
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg, .stSidebar > div {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 0 20px 20px 0 !important;
        border-right: 2px solid rgba(102, 126, 234, 0.2) !important;
        box-shadow: 4px 0 20px rgba(0,0,0,0.1) !important;
    }
    
    /* Input field enhancements */
    .stTextInput > div > input, .stSelectbox > div, .stMultiSelect > div {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 12px !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
        padding: 0.8rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > input:focus, .stSelectbox > div:focus {
        border: 2px solid #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Data frame styling */
    .stDataFrame, .stTable {
        background: white !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        overflow: hidden !important;
    }
    
    /* Success/warning/info message styling */
    .stSuccess, .stWarning, .stInfo {
        border-radius: 12px !important;
        border-left: 4px solid #667eea !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05) !important;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05) !important;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #667eea, transparent) !important;
    }
    
    /* Caption styling */
    .caption {
        color: #64748b !important;
        font-style: italic !important;
        font-size: 0.9rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Header sections with icons */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 1.5rem 0 1rem 0;
        padding: 1rem;
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }
    
    /* Animation keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-element {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Loading spinner enhancement */
    .stSpinner {
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #667eea);
    }
    
    /* Enhanced file uploader */
    .uploadedFile {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 12px !important;
        border: 2px dashed #667eea !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .uploadedFile:hover {
        border-color: #764ba2 !important;
        background: rgba(255,255,255,1) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Progress bars */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 8px !important;
        height: 8px !important;
    }
    
    /* Enhanced alerts */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.9);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.5);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    /* Dashboard stats */
    .stat-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9));
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .stat-container:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 24px rgba(102, 126, 234, 0.15);
    }
    
    /* --- New Additions for Enhanced UI/UX --- */
    
    /* Floating action button */
    .floating-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
        border: none;
        text-decoration: none;
    }
    
    .floating-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Enhanced loading animations */
    .stSpinner > div {
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    /* Smooth transitions for all interactive elements */
    .stButton > button, .stSelectbox, .stMultiSelect, .stTextInput > div > input {
        transition: all 0.2s ease;
    }
    
    /* Enhanced focus states */
    .stButton > button:focus {
        outline: 3px solid rgba(102, 126, 234, 0.5);
        outline-offset: 2px;
    }
    
    /* Loading state improvements */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        animation: progress-animation 1.5s ease-in-out infinite;
    }
    
    @keyframes progress-animation {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    </style>''', unsafe_allow_html=True)

# --- Enhanced Header with Animation (Simple Version) ---
st.markdown(
    f'''
    <div style="
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        animation: fadeInUp 1s ease-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        position: relative;
    ">
        📊 Executive Sales Dashboard
        <div style="
            position: absolute;
            top: 1rem;
            right: 1.5rem;
            background: rgba(16, 185, 129, 0.1);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            border: 1px solid rgba(16, 185, 129, 0.3);
            font-size: 0.8rem;
            color: #10b981;
            font-weight: 500;
        ">
            🔄 Last Updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}
        </div>
    </div>
    <div style="
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        font-weight: 500;
        animation: fadeInUp 1.2s ease-out;
    ">
        Real-time insights • Interactive analytics • Executive reporting
    </div>
    ''', unsafe_allow_html=True
)

# --- Data Loading Section (Must be before tabs) ---
# Initialize data variables
uploaded_file = None
use_sample_data = False

# This will be set from sidebar widgets later
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'use_sample_data' not in st.session_state:
    st.session_state.use_sample_data = False

# Load and validate data
df, data_source = load_and_validate_data(st.session_state.uploaded_file, st.session_state.use_sample_data)

# Validate schema
if not df.empty:
    if not validate_schema(df):
        df = pd.DataFrame()
        st.error("❌ Invalid data schema. Required columns: Date, Product, Region, Sales, Profit")
    else:
        # Map columns for compatibility
        if 'Product' in df.columns and 'Category' not in df.columns:
            df['Category'] = df['Product']

# --- Data Status Indicator (After data loading) ---
st.markdown(
    f'''
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    ">
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: #667eea;
            font-weight: 500;
        ">
            📊 {len(df):,} Total Records
        </div>
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: #10b981;
            font-weight: 500;
        ">
            {'🟢 Data Loaded' if not df.empty else '🔴 No Data'}
        </div>
        <div style="
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            border: 1px solid rgba(245, 158, 11, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: #f59e0b;
            font-weight: 500;
        ">
            ⏱️ Last Refresh: {st.session_state.last_refresh.strftime('%H:%M:%S')}
        </div>
    </div>
    ''', unsafe_allow_html=True
)

# --- Enhanced Sidebar Filters ---
# Ensure 'Date' is datetime and drop nulls before filtering
if not df.empty and 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

st.sidebar.header("Filters")

filtered_df = df.copy() if not df.empty else df

# Date Range Filter
if not filtered_df.empty and 'Date' in filtered_df.columns:
    min_date = filtered_df['Date'].min().date()
    max_date = filtered_df['Date'].max().date()
    date_range = st.sidebar.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['Date'].dt.date >= start_date) & (filtered_df['Date'].dt.date <= end_date)]

# Category Filter
if not filtered_df.empty and 'Category' in filtered_df.columns:
    categories = ['All'] + sorted(filtered_df['Category'].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=categories,
        default=['All']
    )
    if 'All' not in selected_categories and selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

# Region Filter
if not filtered_df.empty and 'Region' in filtered_df.columns:
    regions = ['All'] + sorted(filtered_df['Region'].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=regions,
        default=['All']
    )
    if 'All' not in selected_regions and selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]

# --- Refresh and Data Upload Section (Sidebar) ---
with st.sidebar:
    st.markdown("---")
    st.markdown("### Data Upload & Refresh")
    
    # File uploader for custom data
    uploaded_file = st.file_uploader(
        "Upload your sales data file (CSV or Excel)",
        type=['csv', 'xlsx'],
        label_visibility="collapsed"
    )
    
    # Sample data toggle
    use_sample_data = st.checkbox(
        "Use sample data for demo",
        value=False,
        label_visibility="collapsed"
    )
    
    # Display data source
    st.markdown(f"**Data Source:** {data_source}")
    
    # Refresh button
    if st.button("🔄 Refresh Data", help="Reload dataset and clear cache"):
        st.cache_data.clear()
        st.session_state.last_refresh = datetime.now()
        st.rerun()

# --- Enhanced Navigation Tabs ---
tabs = st.tabs([
    "🏠 Home", 
    "🔍 Data Preview", 
    "📊 Visuals", 
    "🗂️ Category & Region", 
    "🤖 Insights",
    "📈 KPIs & Visuals"
])

# --- Enhanced Home Tab ---
with tabs[0]:
    # ...existing Home tab code using filtered_df...
    if not filtered_df.empty:
        st.markdown("### 📈 Quick Data Insights")
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
            st.metric("Total Records", f"{len(filtered_df):,}")
        with col_info2:
            st.metric("Columns", f"{len(filtered_df.columns)}")
        with col_info3:
            st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}" if 'Sales' in filtered_df.columns else "N/A")
        with col_info4:
            st.metric("Regions", f"{filtered_df['Region'].nunique()}" if 'Region' in filtered_df.columns else "N/A")
        st.markdown("### 🔍 Data Sample")
        st.dataframe(filtered_df.head(), use_container_width=True)
    else:
        st.info("No data loaded. Please use the sidebar to upload a file or generate sample data.")
    # ...existing Home tab highlights and tips...

# --- Data Preview Tab ---
with tabs[1]:
    # ...existing Data Preview tab code using filtered_df...
    if not filtered_df.empty:
        st.markdown("### 📊 Data Insights")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric("📈 Total Records", f"{len(filtered_df):,}")
        with metric_col2:
            st.metric("📊 Columns", f"{len(filtered_df.columns)}")
        with metric_col3:
            if 'Sales' in filtered_df.columns:
                total_sales = filtered_df['Sales'].sum()
                st.metric("💰 Total Sales", f"${total_sales:,.2f}")
            else:
                st.metric("💰 Total Sales", "N/A")
        with metric_col4:
            if 'Date' in filtered_df.columns and len(filtered_df) > 0:
                date_span = (filtered_df['Date'].max() - filtered_df['Date'].min()).days
                st.metric("📅 Date Span", f"{date_span} days")
            else:
                st.metric("📅 Date Span", "N/A")
        # Enhanced data table with search
        st.markdown("### 🔍 Dataset Explorer")
        search_term = st.text_input("🔎 Search in data", placeholder="Search across all columns...")
        preview_df = filtered_df.copy()
        if search_term:
            mask = preview_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            preview_df = preview_df[mask]
            st.info(f"🔍 Found {len(preview_df)} records matching '{search_term}'")
        st.dataframe(
            preview_df,
            use_container_width=True,
            height=400,
            column_config={
                "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                "Sales": st.column_config.NumberColumn("Sales", format="$%.2f"),
                "Profit": st.column_config.NumberColumn("Profit", format="$%.2f") if 'Profit' in preview_df.columns else None
            }
        )
        # ...existing code for downloads and summary...
    else:
        st.markdown(
            '''
            <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1)); border-radius: 16px; border: 1px solid rgba(239, 68, 68, 0.2);">
                <h3 style="color: #ef4444; margin-bottom: 1rem;">🚫 No Data Available</h3>
                <p style="color: #64748b;">Please use the sidebar to upload a file or generate sample data.</p>
            </div>
            ''', unsafe_allow_html=True
        )
# --- Visuals Tab ---
with tabs[2]:
    st.markdown("## 📊 Visuals")
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                px.line(filtered_df, x='Date', y='Sales', title='Sales Over Time'),
                use_container_width=True
            )
            st.plotly_chart(
                px.bar(filtered_df, x='Category', y='Sales', title='Sales by Category', color='Category'),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                px.bar(filtered_df, x='Region', y='Sales', title='Sales by Region', color='Region'),
                use_container_width=True
            )
            if 'Profit' in filtered_df.columns:
                st.plotly_chart(
                    px.line(filtered_df, x='Date', y='Profit', title='Profit Over Time'),
                    use_container_width=True
                )
        # Category vs Region Heatmap
        if 'Category' in filtered_df.columns and 'Region' in filtered_df.columns:
            pivot = filtered_df.pivot_table(index='Category', columns='Region', values='Sales', aggfunc='sum', fill_value=0)
            st.plotly_chart(
                px.imshow(pivot, text_auto=True, aspect='auto',
                          title='Sales Heatmap: Category vs Region'),
                use_container_width=True
            )
        # Monthly Sales Trend
        if 'Date' in filtered_df.columns:
            monthly = filtered_df.copy()
            monthly['Month'] = monthly['Date'].dt.to_period('M').astype(str)
            monthly_sales = monthly.groupby('Month')['Sales'].sum().reset_index()
            st.plotly_chart(
                px.bar(monthly_sales, x='Month', y='Sales', title='Monthly Sales Trend'),
                use_container_width=True
            )
        # Forecasting
        monthly_sales, forecast, future_x = forecast_sales(filtered_df)
        if len(monthly_sales) > 0 and len(forecast) > 0:
            forecast_index = [monthly_sales.index[-1] + i + 1 for i in range(len(forecast))]
            forecast_df = pd.DataFrame({
                'Month': list(monthly_sales.index.astype(str)) + [str(idx) for idx in forecast_index],
                'Sales': list(monthly_sales.values) + list(forecast),
                'Type': ['Actual'] * len(monthly_sales) + ['Forecast'] * len(forecast)
            })
            fig_forecast = px.line(forecast_df, x='Month', y='Sales', color='Type',
                                   title='Sales Forecast (Linear Trend)')
            st.plotly_chart(fig_forecast, use_container_width=True)
        # Histogram
        st.plotly_chart(
            px.histogram(filtered_df, x='Sales', nbins=30, title='Sales Distribution (Histogram)'),
            use_container_width=True
        )
        # Box Plot
        st.plotly_chart(
            px.box(filtered_df, y='Sales', points='all', title='Sales Distribution (Box Plot)'),
            use_container_width=True
        )
    else:
        st.info("No data available for visuals.")

# --- Category & Region Tab ---
with tabs[3]:
    st.markdown("## 🗂️ Category & Region Deep Dive")
    if filtered_df.empty or 'Sales' not in filtered_df.columns:
        st.warning("Please upload your sales data to see category and region analysis.")
    else:
        # Category Analysis Section
        if 'Category' in filtered_df.columns:
            st.subheader("🏷️ Category Performance Analysis")
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
                st.plotly_chart(fig_cat_performance, use_container_width=True)
            with col_cat2:
                st.markdown("**🎯 Average Order Value by Category**")
                fig_cat_avg = px.bar(cat_metrics, x='Category', y='Average Sale',
                                   title="Average Sale by Category",
                                   color='Average Sale',
                                   color_continuous_scale='plasma')
                fig_cat_avg.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cat_avg, use_container_width=True)
            with col_cat3:
                st.markdown("**📊 Order Volume by Category**")
                fig_cat_volume = px.pie(cat_metrics, names='Category', values='Order Count',
                                      title="Order Volume Distribution")
                fig_cat_volume.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_cat_volume, use_container_width=True)
            st.markdown("**📋 Category Performance Summary**")
            st.dataframe(cat_metrics.style.format({
                'Total Sales': '${:,.2f}',
                'Average Sale': '${:,.2f}',
                'Order Count': '{:,}'
            }), use_container_width=True)
        # Region Analysis Section
        if 'Region' in filtered_df.columns:
            st.subheader("🌍 Regional Performance Analysis")
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
                st.plotly_chart(fig_reg_performance, use_container_width=True)
                st.markdown("**📊 Regional Market Share**")
                fig_reg_share = px.pie(region_metrics, names='Region', values='Total Sales',
                                     title="Regional Sales Distribution")
                fig_reg_share.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_reg_share, use_container_width=True)
            with col_reg2:
                st.markdown("**💰 Average Order Value by Region**")
                fig_reg_avg = px.bar(region_metrics, x='Region', y='Average Sale',
                                   title="Average Sale by Region",
                                   color='Average Sale',
                                   color_continuous_scale='plasma')
                st.plotly_chart(fig_reg_avg, use_container_width=True)
                st.markdown("**📈 Order Frequency by Region**")
                fig_reg_frequency = px.bar(region_metrics, x='Region', y='Order Count',
                                         title="Order Count by Region",
                                         color='Order Count',
                                         color_continuous_scale='cividis')
                st.plotly_chart(fig_reg_frequency, use_container_width=True)
            st.markdown("**📋 Regional Performance Summary**")
            st.dataframe(region_metrics.style.format({
                'Total Sales': '${:,.2f}',
                'Average Sale': '${:,.2f}',
                'Order Count': '{:,}'
            }), use_container_width=True)
        # Cross-Category and Region Analysis
        if 'Category' in filtered_df.columns and 'Region' in filtered_df.columns:
            st.subheader("🔄 Cross-Analysis: Category vs Region")
            pivot_data = filtered_df.pivot_table(index='Region', columns='Category', values='Sales', aggfunc='sum', fill_value=0)
            col_cross1, col_cross2 = st.columns(2)
            with col_cross1:
                st.markdown("**🔥 Sales Heatmap: Region vs Category**")
                fig_heatmap = px.imshow(pivot_data.values,
                                      labels=dict(x="Category", y="Region", color="Sales"),
                                      x=pivot_data.columns,
                                      y=pivot_data.index,
                                      color_continuous_scale='viridis',
                                      title="Sales Performance Heatmap")
                st.plotly_chart(fig_heatmap, use_container_width=True)
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
                st.plotly_chart(fig_top_combos, use_container_width=True)
            st.markdown("**📋 Detailed Sales Matrix: Region vs Category**")
            st.dataframe(pivot_data.style.format('${:,.2f}'), use_container_width=True)
        # Scatter Plot Analysis
        if 'Date' in filtered_df.columns and len(filtered_df) > 10:
            st.subheader("🎯 Advanced Scatter Plot Analysis")
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
                    st.plotly_chart(fig_scatter1, use_container_width=True)
                with col_scatter2:
                    st.markdown("**💰 Average Sale vs Order Volume**")
                    fig_scatter2 = px.scatter(scatter_data, x='Order_Count', y='Avg_Sales',
                                            color='Category', size='Total_Sales',
                                            hover_data=['Region'],
                                            title="Order Value vs Volume Analysis",
                                            labels={'Order_Count': 'Number of Orders',
                                                  'Avg_Sales': 'Average Sale ($)'})
                    st.plotly_chart(fig_scatter2, use_container_width=True)
# --- Insights Tab (About AI) ---
with tabs[4]:
    st.markdown("""
    ## 🤖 AI Insights & About
    
    This dashboard leverages AI-driven analytics for sales insights, forecasting, and executive reporting. 
    
    - **AI Features:**
        - Revenue growth and trend analysis
        - Sales forecasting using linear regression
        - Market expansion and product opportunity analysis
    - **How it works:**
        - Upload your sales data or use the sample dataset
        - Apply filters for dynamic, real-time insights
        - Visualize trends, categories, and regions
    - **Built with:** Streamlit, Plotly, Pandas, and Python
    """)
    st.info("For more information or to extend AI features, contact your data science team.")

# --- AI Insights Tab ---
with tabs[5]:
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
    if filtered_df.empty or 'Sales' not in filtered_df.columns:
        st.warning("Please upload your sales data to access AI-powered insights.")
    else:
        if 'selected_insight' not in st.session_state:
            st.session_state.selected_insight = None
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
        if st.session_state.selected_insight == "revenue":
            st.markdown("### 📈 Revenue Growth Analysis")
            strategic_metrics = strategic_kpis(filtered_df)
            growth_rate, avg_monthly_growth, monthly_revenue = calculate_revenue_growth(filtered_df)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Growth Rate", f"{growth_rate:.1f}%")
            with col2:
                st.metric("Avg Monthly Growth", f"{avg_monthly_growth:.1f}%")
            with col3:
                st.metric("Market Penetration", f"{strategic_metrics.get('market_penetration', 0)} Regions")
            st.markdown("#### 🔮 Sales Forecasting (Next 6 Months)")
            historical_sales, forecast, future_periods = forecast_sales(filtered_df, 6)
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
                st.plotly_chart(fig_forecast, use_container_width=True)
                if len(forecast) > 0:
                    total_forecast = sum(forecast)
                    st.info(f"📊 Projected revenue for next 6 months: **${total_forecast:,.2f}**")
        elif st.session_state.selected_insight == "market":
            st.markdown("### 🌍 Market Expansion Opportunities")
            expansion_insights = market_expansion_analysis(filtered_df)
            if expansion_insights and 'top_regions' in expansion_insights:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🏆 Top Performing Regions")
                    top_regions_df = expansion_insights['top_regions'].reset_index()
                    fig_top_regions = px.bar(top_regions_df, x='Region', y='sum',
                                           title="Revenue by Top Regions")
                    st.plotly_chart(fig_top_regions, use_container_width=True)
                with col2:
                    st.markdown("#### 🎯 Growth Opportunities")
                    growth_ops_df = expansion_insights['growth_opportunities'].reset_index()
                    fig_growth_ops = px.bar(growth_ops_df, x='Region', y='mean',
                                          title="Average Revenue by Region")
                    st.plotly_chart(fig_growth_ops, use_container_width=True)
        elif st.session_state.selected_insight == "kpis":
            st.markdown("### 🎯 Strategic Performance Indicators")
            strategic_metrics = strategic_kpis(filtered_df)
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
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Clear Selection", help="Return to main insights view"):
            st.session_state.selected_insight = None
            st.rerun()
# --- KPIs & Visuals Tab ---
with tabs[5]:
    # ...existing KPIs & Visuals tab code using filtered_df...
    if filtered_df.empty or 'Sales' not in filtered_df.columns:
        st.write("No data available for KPIs & Visuals.")
    else:
        filtered_df['Sales'] = pd.to_numeric(filtered_df['Sales'], errors='coerce').fillna(0)
        total_sales = filtered_df['Sales'].sum()
        avg_order = filtered_df['Sales'].mean() if not filtered_df['Sales'].empty else 0
        total_orders = len(filtered_df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'''
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 2rem; border-radius: 16px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3); margin-bottom: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
                    <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Total Sales</h3>
                    <h2 style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 700;">${total_sales:,.2f}</h2>
                </div>
                ''', unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f'''
                <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 2rem; border-radius: 16px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3); margin-bottom: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📦</div>
                    <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Total Orders</h3>
                    <h2 style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 700;">{total_orders:,}</h2>
                </div>
                ''', unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f'''
                <div style="background: linear-gradient(135deg, #f59e42, #fbbf24); padding: 2rem; border-radius: 16px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(251, 191, 36, 0.3); margin-bottom: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
                    <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Average Order</h3>
                    <h2 style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 700;">${avg_order:,.2f}</h2>
                </div>
                ''', unsafe_allow_html=True
            )
        # ...existing code for visuals, using filtered_df...

# --- Footer Section (Optional) ---
st.markdown(
    '''
    <div style="
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid rgba(255,255,255,0.2);
    ">
        &copy; 2024 Executive Sales Dashboard. All rights reserved.
    </div>
    ''', unsafe_allow_html=True
)


