**Sales Dashboard**
This is a Streamlit-based sales dashboard application.

🚀 **Live Demo**: https://ai-powered-eda-dashboard.streamlit.app/

**Features**
Interactive sales analytics
Real-time data visualization with Plotly
Hosted on Render

Sample Sales EDA Dashboard
This is a Streamlit-powered dashboard for exploratory data analysis (EDA) of a sample sales dataset. The dashboard allows users to visualize and analyze sales data, apply filters, and explore various business insights in a user-friendly interface.

**Features**
File Upload: Upload a CSV file or use the default sales.csv dataset.
Date Range Filtering: Filter data based on a date range for better analysis.
Sidebar Filters: Filter by Region, State, and City.
Sales Visualizations: Visualize sales by Category, Region, Segment, and more.
Time Series Analysis: View a time series of sales data over months.
Treemap: Analyze hierarchical sales data across Region, Category, and Sub-Category.
Download Options: Download various filtered data and visualizations in CSV format.
Scatter Plot: Visualize the relationship between Sales, Profit, and Quantity.

# 📊 AI-Powered Sales EDA Dashboard

An interactive **Streamlit application** for **Sales Exploratory Data Analysis (EDA)** powered by **advanced visualizations** and **AI-driven insights**.  
This project brings together **pandas, matplotlib, seaborn, plotly** for data exploration and the **OpenAI API** to automatically generate **business-friendly insights** from your sales data.

---

## 🌟 Key Highlights
- 📂 **Data Upload & Handling** – Upload CSV/Excel sales data or auto-load from GitHub  
- ⚡ **Fast Performance** – Cached data processing with `st.cache_data`  
- 🎨 **Professional Visuals** – Dynamic charts using Matplotlib, Seaborn, Plotly  
- 🔎 **Interactive EDA** – Explore sales by **Category, Region, and Time**  
- 🤖 **AI Insights Layer** – GPT-powered analysis converts numbers into plain English takeaways  
- ⏳ **Forecasting Preview** – Trend forecasting with statistical models (Prophet/ARIMA)  
- ☁️ **Cloud Ready** – Deploy seamlessly on **Streamlit Cloud** or any containerized environment  

---
## 🛠️ Tech Stack
**Core:** Streamlit, Python 3.9+  
**EDA:** Pandas, NumPy  
**Visualization:** Matplotlib, Seaborn, Plotly  
**Forecasting Models:** Statsmodels, Prophet, Scikit-learn  
**AI Integration:** OpenAI GPT (chat completions API) 


Sales Analysis

**Introduction**

The Sales Analysis is an interactive dashboard created using Streamlit and Plotly to conduct exploratory data analysis (EDA) on retail sales data. Users can upload datasets and explore sales trends, category performance, and regional distribution through dynamic visualizations.

With features like interactive filters, time-series analysis, and hierarchical treemaps, users can gain deeper insights into their business data. The dashboard supports filtering by Region, State, and City, allowing for precise data exploration. Additionally, it enables users to analyze sales vs. profit relationships and track seasonal trends over time.

A default dataset is available for demonstration, ensuring ease of use. The tool also offers downloadable processed data, making it convenient for further reporting and analysis. Designed for efficiency and ease of use, this dashboard transforms complex data into actionable insights, making retail analysis more accessible and engaging.

**Workflow**

Step 1: Upload Your Dataset

The app allows users to upload CSV, TXT, XLSX, or XLS files.

If no file is uploaded, a default sample dataset is loaded automatically.

Step 2: Data Processing & Cleaning

The uploaded file is read into a Pandas DataFrame.

The Order Date column is converted into a datetime format.

The system identifies the minimum and maximum dates for filtering.

Step 3: Applying Filters

Users can dynamically filter data by Region, State, and City to narrow down insights.

Date range selectors allow for time-based analysis, making it easy to explore seasonal trends.

Step 4: Data Visualization

Category-wise Sales: A bar chart illustrates sales across different product categories.

Regional Sales: A pie chart displays sales distribution across various regions.

Time Series Analysis: A line chart presents sales trends over months.

Hierarchical TreeMap: A layered visualization to analyze relationships between categories and subcategories.

Sales vs. Profit Scatter Plot: Highlights correlations between revenue and profitability.

Segment & Category Sales: Pie charts for additional breakdowns.

Summary Table: Provides an overview of key sales and profit metrics.

Step 5: Data Download & Export

Users can download processed datasets for further offline analysis.

The system provides multiple dataset formats for customized reporting.

What Makes This Project Unique?

Live Data Filtering & Insights: Instantly apply filters and watch data visualizations update in real time.

Comprehensive Time-Series Analysis: Users can track business performance over various time periods.

Interactive Treemap Visualization: Explore how sales and profit vary across regions, categories, and subcategories in a hierarchical view.

User-Friendly Interface: The dashboard is intuitive, requiring minimal technical expertise to operate.

Custom Export Feature: Download specific data segments for further analysis in external tools.

Conclusion

This project provides a powerful yet simple way to analyze retail sales data. Whether you're a business owner, analyst, or data enthusiast, the Superstore Sales Analysis Dashboard helps uncover trends, optimize decision-making, and enhance business intelligence. Get started today and explore your sales data like never before!
