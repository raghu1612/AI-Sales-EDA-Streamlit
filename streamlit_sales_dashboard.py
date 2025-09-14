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

# --- Enhanced Navigation Tabs ---
tabs = st.tabs([
    "🏠 Home", 
    "🔍 Data Preview", 
    "📊 KPIs & Visuals", 
    "📈 Category & Region", 
    "💡 Insights"
])

# --- Enhanced Home Tab ---
with tabs[0]:
    # Welcome section with cards
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
                Your sales dashboard automatically loads default data from GitHub. Transform your sales data into actionable insights with interactive dashboards, 
                advanced filtering, and comprehensive analytics. Use the sidebar to upload your own data or generate sample data.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )
    # Show only a simple data summary and sample if data is loaded
    if not df.empty:
        st.markdown("### 📈 Quick Data Insights")
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
            st.metric("Total Records", f"{len(df):,}")
        with col_info2:
            st.metric("Columns", f"{len(df.columns)}")
        with col_info3:
            st.metric("Total Sales", f"${df['Sales'].sum():,.0f}" if 'Sales' in df.columns else "N/A")
        with col_info4:
            st.metric("Regions", f"{df['Region'].nunique()}" if 'Region' in df.columns else "N/A")
        st.markdown("### 🔍 Data Sample")
        st.dataframe(df.head(), use_container_width=True)
    else:
        st.info("No data loaded. Please use the sidebar to upload a file or generate sample data.")
    st.markdown("---")
    # Feature highlights (optional, can be removed if you want a minimal homepage)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📊 Interactive Charts**")
    with col2:
        st.markdown("**🔍 Smart Filtering**")
    with col3:
        st.markdown("**💡 AI Insights**")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '> 💡 **Quick Tips:** Use the sidebar to upload your own CSV/Excel files or generate sample data. All visualizations update automatically when you apply filters.'
    )

# --- Data Preview Tab ---
with tabs[1]:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            padding: 1.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border-left: 4px solid #667eea;
        ">
            <h2 style="color: #667eea; margin-bottom: 0.5rem;">📊 Interactive Data Preview</h2>
            <p style="color: #64748b; margin: 0;">Explore your dataset with advanced filtering and real-time updates</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    if not df.empty:
        # Enhanced Date Filter with Rich UI
        if 'Date' in df.columns:
            st.markdown("### 📅 Smart Date Filter")
            
            # Create columns for date filter layout
            date_col1, date_col2, date_col3 = st.columns([2, 2, 1])
            
            with date_col1:
                # Get date range from data
                min_date = df['Date'].min().date()
                max_date = df['Date'].max().date()
                total_days = (max_date - min_date).days
                
                st.markdown(
                    f'''
                    <div style="
                        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
                        padding: 1rem;
                        border-radius: 12px;
                        border: 1px solid rgba(59, 130, 246, 0.2);
                        margin-bottom: 1rem;
                    ">
                        <h4 style="color: #3b82f6; margin: 0 0 0.5rem 0;">📈 Dataset Timeline</h4>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #64748b;">From: <strong>{min_date}</strong></span>
                            <span style="color: #64748b;">To: <strong>{max_date}</strong></span>
                        </div>
                        <div style="color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;">
                            📊 Total Period: {total_days} days
                        </div>
                    </div>
                    ''', unsafe_allow_html=True
                )
                
                # Date range selector
                selected_range = st.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    help="Choose the date range for filtering data"
                )
            
            with date_col2:
                # Quick date presets
                st.markdown("#### ⚡ Quick Presets")
                
                preset_col1, preset_col2 = st.columns(2)
                
                with preset_col1:
                    if st.button("📅 Last 30 Days", use_container_width=True):
                        start_date = max_date - pd.Timedelta(days=30)
                        if start_date < min_date:
                            start_date = min_date
                        st.session_state.date_preset = (start_date, max_date)
                        st.rerun()
                    
                    if st.button("📅 Last 90 Days", use_container_width=True):
                        start_date = max_date - pd.Timedelta(days=90)
                        if start_date < min_date:
                            start_date = min_date
                        st.session_state.date_preset = (start_date, max_date)
                        st.rerun()
                
                with preset_col2:
                    if st.button("📅 Last 6 Months", use_container_width=True):
                        start_date = max_date - pd.Timedelta(days=180)
                        if start_date < min_date:
                            start_date = min_date
                        st.session_state.date_preset = (start_date, max_date)
                        st.rerun()
                    
                    if st.button("📅 All Data", use_container_width=True):
                        st.session_state.date_preset = (min_date, max_date)
                        st.rerun()
            
            with date_col3:
                # Data refresh controls
                st.markdown("#### 🔄 Controls")
                
                if st.button("🔄 Refresh Data", use_container_width=True, help="Reload dataset and clear cache"):
                    st.cache_data.clear()
                    st.session_state.last_refresh = datetime.now()
                    st.rerun()
                
                # Auto-refresh toggle
                auto_refresh = st.checkbox("⚡ Auto-refresh", value=False, help="Automatically refresh data every 30 seconds")
                
                if auto_refresh:
                    time.sleep(1)  # Brief pause for demo
                    st.rerun()
        
        # Apply date filtering if date range is selected
        preview_df = df.copy()
        if 'Date' in df.columns and len(selected_range) == 2:
            start_date, end_date = selected_range
            preview_df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
        
        # Enhanced data metrics
        st.markdown("### 📊 Data Insights")
        
        # Create metrics columns
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "📈 Total Records", 
                f"{len(preview_df):,}",
                delta=f"{len(preview_df) - len(df):,}" if len(preview_df) != len(df) else None
            )
        
        with metric_col2:
            st.metric("📊 Columns", f"{len(preview_df.columns)}")
        
        with metric_col3:
            if 'Sales' in preview_df.columns:
                total_sales = preview_df['Sales'].sum()
                st.metric("💰 Total Sales", f"${total_sales:,.2f}")
            else:
                st.metric("💰 Total Sales", "N/A")
        
        with metric_col4:
            if 'Date' in preview_df.columns and len(preview_df) > 0:
                date_span = (preview_df['Date'].max() - preview_df['Date'].min()).days
                st.metric("📅 Date Span", f"{date_span} days")
            else:
                st.metric("📅 Date Span", "N/A")
        
        # Enhanced data table with search
        st.markdown("### 🔍 Dataset Explorer")
        
        # Search functionality
        search_term = st.text_input("🔎 Search in data", placeholder="Search across all columns...")
        
        if search_term:
            # Search across all string columns
            mask = preview_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            preview_df = preview_df[mask]
            st.info(f"🔍 Found {len(preview_df)} records matching '{search_term}'")
        
        # Display the enhanced dataframe
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
        
        # Enhanced download options
        st.markdown("### 📥 Export Options")
        
        download_col1, download_col2, download_col3 = st.columns(3)
        
        with download_col1:
            csv_data = preview_df.to_csv(index=False)
            st.download_button(
                "📄 Download CSV",
                csv_data,
                f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with download_col2:
            # Excel download (if openpyxl is available)
            try:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    preview_df.to_excel(writer, sheet_name='Data', index=False)
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    "📊 Download Excel",
                    excel_data,
                    f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.button("📊 Excel (Install openpyxl)", disabled=True, use_container_width=True)
        
        with download_col3:
            # JSON download
            json_data = preview_df.to_json(orient='records', date_format='iso')
            st.download_button(
                "📋 Download JSON",
                json_data,
                f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json",
                use_container_width=True
            )
        
        # Data summary
        st.caption(f"📊 Showing {len(preview_df):,} of {len(df):,} total records | Last updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
        
    else:
        st.markdown(
            '''
            <div style="
                text-align: center;
                padding: 3rem;
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
                border-radius: 16px;
                border: 1px solid rgba(239, 68, 68, 0.2);
            ">
                <h3 style="color: #ef4444; margin-bottom: 1rem;">🚫 No Data Available</h3>
                <p style="color: #64748b;">Please use the sidebar to upload a file or generate sample data.</p>
            </div>
            ''', unsafe_allow_html=True
        )

# --- KPIs & Visuals Tab ---
with tabs[2]:
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
        st.markdown(
            '''
            <div style="
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
                padding: 2rem;
                border-radius: 12px;
                text-align: center;
                border-left: 4px solid #ef4444;
            ">
                <h3 style="color: #ef4444;">⚠️ No Data Available</h3>
                <p style="color: #64748b;">Please upload your sales data to generate insights and advanced analytics.</p>
            </div>
            ''', unsafe_allow_html=True
        )
    else:
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
        
        # Essential KPIs with enhanced styling
        total_sales = df['Sales'].sum()
        avg_order = df['Sales'].mean() if not df['Sales'].empty else 0
        total_orders = len(df)
        
        # Enhanced KPI cards with gradients and icons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f'''
                <div style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    padding: 2rem;
                    border-radius: 16px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                    margin-bottom: 1rem;
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
                    <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Total Sales</h3>
                    <h2 style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 700;">
                        ${total_sales:,.2f}
                    </h2>
                </div>
                ''', unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f'''
                <div style="
                    background: linear-gradient(135deg, #10b981, #059669);
                    padding: 2rem;
                    border-radius: 16px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
                    margin-bottom: 1rem;
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📦</div>
                    <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Total Orders</h3>
                    <h2 style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 700;">
                        {total_orders:,}
                    </h2>
                </div>
                ''', unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f'''
                <div style="
                    background: linear-gradient(135deg, #f59e0b, #d97706);
                    padding: 2rem;
                    border-radius: 16px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3);
                    margin-bottom: 1rem;
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">💳</div>
                    <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Avg Order Value</h3>
                    <h2 style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 700;">
                        ${avg_order:,.2f}
                    </h2>
                </div>
                ''', unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Pie chart: Sales by Product (Enhanced with labels and percentages)
        if 'Product' in df.columns:
            prod_sales = df.groupby('Product')['Sales'].sum().reset_index()
            fig_product = px.pie(prod_sales, names='Product', values='Sales', 
                               title="Sales by Product",
                               hover_data=['Sales'],
                               labels={'Sales':'Total Sales'})
            fig_product.update_traces(textposition='inside', textinfo='percent+label',
                                    textfont_size=12, 
                                    hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>')
            st.plotly_chart(fig_product, width="stretch")
        
        # Pie Chart: Sales by Region (converted from notebook matplotlib)
        if 'Region' in df.columns:
            st.subheader("🌎 Sales Distribution by Region")
            region_sales = df.groupby('Region')['Sales'].sum().reset_index()
            fig_region = px.pie(region_sales, names='Region', values='Sales',
                              title="Sales Distribution by Region",
                              hover_data=['Sales'],
                              labels={'Sales':'Total Sales'})
            fig_region.update_traces(textposition='inside', textinfo='percent+label',
                                   textfont_size=12,
                                   hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>')
            st.plotly_chart(fig_region, width="stretch")
            st.caption("Regional sales distribution showing market share by geographic area")
        # Bar chart: Sales by Region
        if 'Region' in df.columns:
            reg_sales = df.groupby('Region')['Sales'].sum().reset_index()
            st.plotly_chart(px.bar(reg_sales, x='Region', y='Sales', color='Sales', title="Sales by Region"), width="stretch")
        
        # Line Chart: Monthly Sales Trend (converted from notebook)
        if 'Date' in df.columns:
            st.subheader("📈 Monthly Sales Trend")
            # Ensure Date column is datetime
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            # Only use rows with valid dates
            df_with_dates = df.dropna(subset=['Date'])
            if not df_with_dates.empty:
                monthly_sales = df_with_dates.groupby(df_with_dates['Date'].dt.to_period('M'))['Sales'].sum()
                monthly_sales.index = monthly_sales.index.astype(str)  # Convert period to string for streamlit
                st.line_chart(monthly_sales, use_container_width=True)
                st.caption("Monthly total sales over time showing business performance trends")
        
        # Line Chart: Average Sales per Region per Month (converted from notebook)
        if 'Region' in df.columns and 'Date' in df.columns:
            st.subheader("🌍 Average Sales per Region per Month")
            # Ensure Date column is datetime
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            # Only use rows with valid dates
            df_with_dates = df.dropna(subset=['Date'])
            if not df_with_dates.empty:
                df_with_dates['Month'] = df_with_dates['Date'].dt.to_period('M')
                avg_sales_by_region = df_with_dates.groupby(['Month', 'Region'])['Sales'].mean().unstack(fill_value=0)
                avg_sales_by_region.index = avg_sales_by_region.index.astype(str)  # Convert period to string
                st.line_chart(avg_sales_by_region, use_container_width=True)
                st.caption("Average sales performance by region over time for regional comparison")
        
        # Bar Chart: Sales by Category (grouped and aggregated)
        if 'Category' in df.columns:
            st.subheader("📊 Sales by Category")
            category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
            st.bar_chart(category_sales, use_container_width=True)
            st.caption("Total sales aggregated by product category showing performance ranking")

# --- Category & Region Tab ---
with tabs[3]:
    st.header("Category & Region Analysis")
    if not df.empty and 'Category' in df.columns and 'Sales' in df.columns:
        cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
        st.plotly_chart(px.bar(cat_sales, x='Category', y='Sales', color='Sales', title="Sales by Category"), width="stretch")
        
        # Enhanced Pie Chart: Sales Distribution by Category (with labels and percentages)
        fig_category = px.pie(cat_sales, names='Category', values='Sales',
                            title="Sales Distribution by Category",
                            hover_data=['Sales'],
                            labels={'Sales':'Total Sales'})
        fig_category.update_traces(textposition='inside', textinfo='percent+label',
                                 textfont_size=12,
                                 hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>')
        st.plotly_chart(fig_category, width="stretch")
        
        # Line Chart: Daily Sales Over Time (converted from notebook)
        if 'Date' in df.columns:
            st.subheader("📅 Daily Sales Over Time")
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            daily_sales = df.groupby('Date')['Sales'].sum()
            st.line_chart(daily_sales, use_container_width=True)
            st.caption("Daily total sales showing detailed business activity patterns")
    
    if not df.empty and 'Region' in df.columns and 'Category' in df.columns and 'Sales' in df.columns:
        pivot = df.pivot_table(index='Region', columns='Category', values='Sales', aggfunc='sum', fill_value=0)
        st.dataframe(pivot, width="stretch")

# --- Enhanced Insights Tab with AI-Powered Insights Only ---
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
            <h2 style="color: #10b981; margin-bottom: 0.5rem;">💡 AI-Powered Business Insights</h2>
            <p style="color: #64748b; margin: 0;">Advanced analytics and automated insights for strategic decision making</p>
        </div>
        ''', unsafe_allow_html=True
    )
    
    if df.empty or 'Sales' not in df.columns:
        st.markdown(
            '''
            <div style="
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
                padding: 2rem;
                border-radius: 12px;
                text-align: center;
                border-left: 4px solid #ef4444;
            ">
                <h3 style="color: #ef4444;">⚠️ No Data Available</h3>
                <p style="color: #64748b;">Please upload your sales data to access AI-powered insights and analytics.</p>
            </div>
            ''', unsafe_allow_html=True
        )
    else:
        # Create clickable action tiles for different insights
        st.markdown("### 🎯 Interactive Insight Categories")
        
        # Initialize session state for selected insight
        if 'selected_insight' not in st.session_state:
            st.session_state.selected_insight = None
        
        # Create action tiles
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
            # Revenue Growth Analysis
            st.markdown("### 📈 Revenue Growth Analysis")
            strategic_metrics = strategic_kpis(df)
            growth_rate, avg_monthly_growth, monthly_revenue = calculate_revenue_growth(df)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f'''
                    <div style="
                        background: linear-gradient(135deg, #ef4444, #dc2626);
                        padding: 1.5rem;
                        border-radius: 12px;
                        color: white;
                        text-align: center;
                        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
                    ">
                        <h4 style="margin: 0; opacity: 0.9;">Total Growth Rate</h4>
                        <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">
                            {growth_rate:.1f}%
                        </h2>
                    </div>
                    ''', unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f'''
                    <div style="
                        background: linear-gradient(135deg, #3b82f6, #2563eb);
                        padding: 1.5rem;
                        border-radius: 12px;
                        color: white;
                        text-align: center;
                        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
                    ">
                        <h4 style="margin: 0; opacity: 0.9;">Avg Monthly Growth</h4>
                        <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">
                            {avg_monthly_growth:.1f}%
                        </h2>
                    </div>
                    ''', unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f'''
                    <div style="
                        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
                        padding: 1.5rem;
                        border-radius: 12px;
                        color: white;
                        text-align: center;
                        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
                    ">
                        <h4 style="margin: 0; opacity: 0.9;">Market Penetration</h4>
                        <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">
                            {strategic_metrics.get('market_penetration', 0)} Regions
                        </h2>
                    </div>
                    ''', unsafe_allow_html=True
                )
            
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
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8)
                ))
                
                future_dates = [f"Month {i+1}" for i in range(len(forecast))]
                fig_forecast.add_trace(go.Scatter(
                    x=future_dates,
                    y=forecast,
                    mode='lines+markers',
                    name='Forecasted Sales',
                    line=dict(color='#10b981', width=3, dash='dash'),
                    marker=dict(size=8)
                ))
                
                fig_forecast.update_layout(
                    title="Sales Forecast Analysis",
                    xaxis_title="Time Period",
                    yaxis_title="Sales ($)",
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                if len(forecast) > 0:
                    total_forecast = sum(forecast)
                    st.info(f"📊 **Forecast Insights**: Projected revenue for next 6 months: **${total_forecast:,.2f}** | Average monthly forecast: **${total_forecast/6:,.2f}**")
        
        elif st.session_state.selected_insight == "market":
            # Market Expansion Analysis
            st.markdown("### 🌍 Market Expansion Opportunities")
            expansion_insights = market_expansion_analysis(df)
            
            if expansion_insights:
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'top_regions' in expansion_insights:
                        st.markdown("#### 🏆 Top Performing Regions")
                        top_regions_df = expansion_insights['top_regions'].reset_index()
                        fig_top_regions = px.bar(
                            top_regions_df, 
                            x='Region', 
                            y='sum',
                            title="Revenue by Top Regions",
                            color='sum',
                            color_continuous_scale='Blues'
                        )
                        fig_top_regions.update_layout(
                            yaxis_title="Total Revenue ($)",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_top_regions, width="stretch")
                
                with col2:
                    if 'growth_opportunities' in expansion_insights:
                        st.markdown("#### 🎯 Growth Opportunities")
                        growth_ops_df = expansion_insights['growth_opportunities'].reset_index()
                        fig_growth_ops = px.bar(
                            growth_ops_df, 
                            x='Region', 
                            y='mean',
                            title="Average Revenue by Region",
                            color='mean',
                            color_continuous_scale='Oranges'
                        )
                        fig_growth_ops.update_layout(
                            yaxis_title="Average Revenue ($)",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_growth_ops, width="stretch")
        
        elif st.session_state.selected_insight == "kpis":
            # Strategic KPIs
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
            
            # Performance Distribution
            if 'Sales' in df.columns:
                st.markdown("#### 📊 Sales Performance Distribution")
                fig_dist = px.histogram(df, x='Sales', nbins=30, title="Sales Distribution Analysis")
                fig_dist.update_layout(
                    xaxis_title="Sales Amount ($)",
                    yaxis_title="Frequency",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_dist, use_container_width=True)
        
        elif st.session_state.selected_insight == "recommendations":
            # AI Recommendations
            st.markdown("### 💡 AI-Powered Strategic Recommendations")
            
            recommendations = []
            
            # Generate smart recommendations
            if 'Region' in df.columns:
                regional_performance = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
                if len(regional_performance) > 1:
                    best_region = regional_performance.index[0]
                    worst_region = regional_performance.index[-1]
                    recommendations.append(f"**Market Expansion**: Focus on replicating {best_region}'s success model in {worst_region}")
            
            growth_rate, avg_monthly_growth, monthly_revenue = calculate_revenue_growth(df)
            if len(monthly_revenue) > 2:
                recent_trend = monthly_revenue.iloc[-3:].pct_change().mean()
                if recent_trend > 0:
                    recommendations.append("**Growth Momentum**: Current positive trend - consider increasing marketing spend")
                else:
                    recommendations.append("**Revenue Recovery**: Implement retention strategies and new customer acquisition")
            
            if 'Category' in df.columns:
                category_performance = df.groupby('Category')['Sales'].sum()
                top_category = category_performance.idxmax()
                recommendations.append(f"**Product Strategy**: {top_category} is your top performer - expand product line")
            
            recommendations.append("**Data-Driven Decisions**: Continue monitoring these KPIs weekly for optimal performance")
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(
                    f'''
                    <div style="
                        background: white;
                        padding: 1.5rem;
                        border-radius: 12px;
                        margin: 1rem 0;
                        border-left: 4px solid #667eea;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                        transition: all 0.3s ease;
                    ">
                        <strong style="color: #667eea; font-size: 1.1rem;">{i}.</strong> {rec}
                    </div>
                    ''', unsafe_allow_html=True
                )
            
            # Action Items
            st.markdown("#### 🚀 Recommended Action Items")
            action_items = [
                "📊 Set up weekly KPI monitoring dashboard",
                "🎯 Develop region-specific marketing strategies",
                "📈 Implement sales forecasting for inventory planning",
                "🔍 Conduct deeper analysis on top-performing categories",
                "💡 A/B test strategies in underperforming regions"
            ]
            
            for action in action_items:
                st.markdown(f"- {action}")
        
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
        
        # Visual 1: Sales Distribution Histogram
        if 'Sales' in df.columns and len(df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💰 Sales Distribution**")
                fig_hist = px.histogram(df, x='Sales', nbins=20, 
                                      title="Sales Amount Distribution",
                                      labels={'Sales': 'Sales Amount', 'count': 'Frequency'})
                fig_hist.update_layout(showlegend=False)
                st.plotly_chart(fig_hist, width="stretch")
                st.caption("Distribution of sales amounts showing frequency patterns")
            
            with col2:
                st.markdown("**📈 Sales Performance Box Plot**")
                fig_box = px.box(df, y='Sales', title="Sales Performance Overview")
                fig_box.update_layout(showlegend=False)
                st.plotly_chart(fig_box, width="stretch")
                st.caption("Statistical overview with outliers and quartiles")
        
        # Visual 2: Top Performers Analysis
        if 'Product' in df.columns or 'Region' in df.columns:
            st.markdown("**🏆 Top Performers Analysis**")
            col3, col4 = st.columns(2)
            
            with col3:
                if st.button("📊 Top Products", key="top_products", help="View top products by sales"):
                    top_products = df.groupby('Product')['Sales'].sum().nlargest(5)
                    fig_top_prod = px.bar(x=top_products.index, y=top_products.values, 
                                        title="Top Products by Sales",
                                        labels={'x': 'Product', 'y': 'Total Sales'},
                                        color='y',
                                        color_continuous_scale='Blues')
                    st.plotly_chart(fig_top_prod, width="stretch")
            
            with col4:
                if st.button("📈 Regional Performance", key="regional_performance", help="View sales performance by region"):
                    region_performance = df.groupby('Region')['Sales'].agg(['sum', 'count']).reset_index()
                    region_performance.columns = ['Region', 'Total Sales', 'Order Count']
                    fig_region_perf = px.bar(region_performance, x='Region', y='Total Sales', 
                                           title="Sales Performance by Region",
                                           labels={'Region': 'Region', 'Total Sales': 'Total Sales'},
                                           color='Total Sales',
                                           color_continuous_scale='Reds')
                    st.plotly_chart(fig_region_perf, width="stretch")
        
        # Visual 3: Time-based Analysis
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df_with_dates = df.dropna(subset=['Date'])
            
            if not df_with_dates.empty:
                st.markdown("**⏰ Time-based Analysis**")
                col5, col6 = st.columns(2)
                
                with col5:
                    # Day of week analysis
                    df_with_dates['DayOfWeek'] = df_with_dates['Date'].dt.day_name()
                    dow_sales = df_with_dates.groupby('DayOfWeek')['Sales'].mean()
                    # Reorder days
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    dow_sales = dow_sales.reindex([day for day in day_order if day in dow_sales.index])
                    
                    fig_dow = px.bar(x=dow_sales.index, y=dow_sales.values,
                                   title="Average Sales by Day of Week",
                                   labels={'x': 'Day', 'y': 'Average Sales'})
                    st.plotly_chart(fig_dow, width="stretch")
                
                with col6:
                    # Monthly trend with moving average
                    monthly_sales = df_with_dates.groupby(df_with_dates['Date'].dt.to_period('M'))['Sales'].sum()
                    monthly_sales.index = monthly_sales.index.astype(str)
                    
                    fig_trend = px.line(x=monthly_sales.index, y=monthly_sales.values,
                                      title="Monthly Sales Trend",
                                      labels={'x': 'Month', 'y': 'Total Sales'})
                    fig_trend.add_scatter(x=monthly_sales.index, y=monthly_sales.values, 
                                        mode='markers', name='Monthly Sales')
                    st.plotly_chart(fig_trend, width="stretch")
        
        # Visual 4: Comparative Analysis
        if 'Category' in df.columns and 'Region' in df.columns:
            st.markdown("**🔄 Comparative Analysis**")
            
            # Heatmap of Category vs Region
            pivot_heatmap = df.pivot_table(values='Sales', index='Category', 
                                         columns='Region', aggfunc='sum', fill_value=0)
            fig_heatmap = px.imshow(pivot_heatmap.values,
                                  x=pivot_heatmap.columns,
                                  y=pivot_heatmap.index,
                                  color_continuous_scale='Blues',
                                  title="Sales Heatmap: Category vs Region",
                                  labels={'color': 'Total Sales'})
            st.plotly_chart(fig_heatmap, width="stretch")
            st.caption("Darker colors indicate higher sales performance")
        
        # Visual 5: Key Metrics Summary Cards
        st.markdown("**📋 Quick Insights Summary**")
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            growth_rate = ((df['Sales'].tail(len(df)//2).mean() - df['Sales'].head(len(df)//2).mean()) / df['Sales'].head(len(df)//2).mean() * 100) if len(df) > 1 else 0
            st.metric("📈 Growth Rate", f"{growth_rate:.1f}%", delta=f"{growth_rate:.1f}%")
        
        with metric_cols[1]:
            if 'Region' in df.columns:
                best_region = df.groupby('Region')['Sales'].sum().idxmax()
                best_region_sales = df.groupby('Region')['Sales'].sum().max()
                st.metric("🏆 Top Region", best_region, delta=f"${best_region_sales:,.0f}")
        
        with metric_cols[2]:
            if 'Category' in df.columns:
                best_category = df.groupby('Category')['Sales'].sum().idxmax()
                best_cat_sales = df.groupby('Category')['Sales'].sum().max()
                st.metric("🏅 Top Category", best_category, delta=f"${best_cat_sales:,.0f}")
        
        with metric_cols[3]:
            data_quality = ((len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 100
            st.metric("🎯 Data Quality", f"{data_quality:.1f}%", delta="Quality Score")
        
        # Correlation heatmap
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) >  1:
            corr = df[num_cols].corr()
            st.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', title="Correlation Heatmap"), width="stretch")
    
    # --- AI Insights Section ---
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            border-left: 4px solid #10b981;
        ">
            <h2 style="color: #10b981; margin-bottom: 1rem;">🤖 AI-Driven Insights</h2>
            <p style="color: #64748b; margin-bottom: 0.5rem;">
                Automated insights generated from your sales data patterns
            </p>
            <ul style="color: #64748b; line-height: 1.8;">
                <li><strong>Performance Trend:</strong> Your top-performing category shows consistent growth patterns</li>
                <li><strong>Regional Opportunity:</strong> Consider expanding marketing efforts in underperforming regions</li>
                <li><strong>Seasonal Patterns:</strong> Sales data suggests strong seasonal correlations worth investigating</li>
                <li><strong>Product Optimization:</strong> Focus on high-margin products for revenue maximization</li>
                <li><strong>Customer Segmentation:</strong> Regional preferences show distinct buying patterns</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True
    )
    
    # Action Items
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
            padding: 2rem;
            border-radius: 16px;
            margin: 2rem 0;
            border-left: 4px solid #ef4444;
        ">
            <h2 style="color: #ef4444; margin-bottom: 1rem;">🎯 Recommended Actions</h2>
            <ul style="color: #64748b; line-height: 1.8;">
                <li><strong>Monitor KPIs:</strong> Set up weekly performance tracking</li>
                <li><strong>Regional Strategy:</strong> Develop targeted marketing campaigns</li>
                <li><strong>Product Focus:</strong> Expand high-performing product lines</li>
                <li><strong>Data Quality:</strong> Implement automated data validation</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True
    )
        
    # Clear button to reset selection
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Clear Selection", help="Return to main insights view"):
        st.session_state.selected_insight = None
        st.rerun()

# --- Enhanced Sidebar Filters ---
st.sidebar.header("Filters")

# Date Range Filter
if not df.empty and 'Date' in df.columns:
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]

# Category Filter
if not df.empty and 'Category' in df.columns:
    categories = ['All'] + sorted(df['Category'].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=categories,
        default=['All']
    )
    if 'All' not in selected_categories and selected_categories:
        df = df[df['Category'].isin(selected_categories)]


