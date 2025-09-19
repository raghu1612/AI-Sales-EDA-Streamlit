# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("sales_data_with_issues.csv")
df.head(10)


# %%
# Loading the data

salesData = pd.read_csv('sales_data_with_issues.csv')
salesData

# %%
#no.of rows n columns
df.shape

# %%
#column names
df.columns

# %%
#Data quality check
df.isnull().sum()

# %%
df.dtypes


# %%
df.nunique

# %%
# Data Insights and Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
sales_df = pd.read_csv('sales_data_with_issues.csv')

# 1. Missing values summary
print('Missing values by column:')
print(sales_df.isnull().sum())

# 2. Top performing categories
print('\nAverage sales by category:')
print(sales_df.groupby('Category')['Sales'].mean().sort_values(ascending=False))
sns.barplot(x='Category', y='Sales', data=sales_df)
plt.title('Average Sales by Category')
plt.show()

# 3. Regional sales distribution
print('\nTotal sales by region:')
print(sales_df.groupby('Region')['Sales'].sum().sort_values(ascending=False))
sns.barplot(x='Region', y='Sales', data=sales_df)
plt.title('Total Sales by Region')
plt.show()

# 4. Sales trends over time
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
monthly_sales = sales_df.groupby(sales_df['Date'].dt.to_period('M'))['Sales'].sum()
print('\nMonthly sales trend:')
print(monthly_sales)
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trend')
plt.ylabel('Sales')
plt.xlabel('Month')
plt.show()

# 5. Outlier detection (IQR method)
Q1 = sales_df['Sales'].quantile(0.25)
Q3 = sales_df['Sales'].quantile(0.75)
IQR = Q3 - Q1
outliers = sales_df[(sales_df['Sales'] < Q1 - 1.5 * IQR) | (sales_df['Sales'] > Q3 + 1.5 * IQR)]
print(f'\nNumber of sales outliers: {len(outliers)}')
print(outliers[['Date','Region','Category','Sales']])

# %%


# %%
# Top Performing KPIs
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')

# Total Sales
total_sales = sales_df['Sales'].sum()
print(f'Total Sales: {total_sales:.2f}')

# Average Sales per Transaction
average_sales = sales_df['Sales'].mean()
print(f'Average Sales per Transaction: {average_sales:.2f}')

# Top Region by Total Sales
top_region = sales_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).index[0]
print(f'Top Region by Total Sales: {top_region}')

# Top Category by Total Sales
top_category = sales_df.groupby('Category')['Sales'].sum().sort_values(ascending=False).index[0]
print(f'Top Category by Total Sales: {top_category}')

# Sales Growth (First vs Last Month)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
monthly_sales = sales_df.groupby(sales_df['Date'].dt.to_period('M'))['Sales'].sum()
if len(monthly_sales) > 1:
    growth = ((monthly_sales.iloc[-1] - monthly_sales.iloc[0]) / monthly_sales.iloc[0]) * 100
    print(f'Sales Growth (First vs Last Month): {growth:.2f}%')
else:
    print('Not enough data for sales growth calculation.')

# %%
# Average Sales per Region per Month
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Month'] = sales_df['Date'].dt.to_period('M')
avg_sales = sales_df.groupby(['Region', 'Month'])['Sales'].mean().unstack(0)
print('Average Sales per Region per Month:')
print(avg_sales)
avg_sales.plot(kind='line', marker='o', figsize=(12,6))
plt.title('Average Sales per Region per Month')
plt.ylabel('Average Sales')
plt.xlabel('Month')
plt.legend(title='Region')
plt.show()

# %%
# Line Chart of Sales Over Time
import pandas as pd
import matplotlib.pyplot as plt
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
daily_sales = sales_df.groupby('Date')['Sales'].sum()
plt.figure(figsize=(12,6))
daily_sales.plot(kind='line', marker='o')
plt.title('Total Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.grid(True)
plt.show()

# %%
# Pie Chart of Sales by Region
import pandas as pd
import matplotlib.pyplot as plt
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_by_region = sales_df.groupby('Region')['Sales'].sum()
plt.figure(figsize=(8,8))
sales_by_region.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Sales Distribution by Region')
plt.ylabel('')
plt.show()

# %%
# Identify Outliers in Sales Amount
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
Q1 = sales_df['Sales'].quantile(0.25)
Q3 = sales_df['Sales'].quantile(0.75)
IQR = Q3 - Q1
outliers = sales_df[(sales_df['Sales'] < Q1 - 1.5 * IQR) | (sales_df['Sales'] > Q3 + 1.5 * IQR)]
print(f'Number of outliers in Sales: {len(outliers)}')
print(outliers[['Date','Region','Category','Sales']])

# %%
# Sales by Year by Quarter
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Year'] = sales_df['Date'].dt.year
sales_df['Quarter'] = sales_df['Date'].dt.quarter
sales_by_yq = sales_df.groupby(['Year', 'Quarter'])['Sales'].sum().unstack(0)
print('Sales by Year by Quarter:')
print(sales_by_yq)
sales_by_yq.plot(kind='bar', figsize=(10,6))
plt.title('Sales by Year by Quarter')
plt.ylabel('Total Sales')
plt.xlabel('Quarter')
plt.legend(title='Year')
plt.show()

# %%
# Find Category and Region for Maximum Sales Amount
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
max_row = sales_df[sales_df['Sales'] == sales_df['Sales'].max()].iloc[0]
print('Maximum Sales Amount:', max_row['Sales'])
print('Category:', max_row['Category'])
print('Region:', max_row['Region'])

# %%
# Find Category and Region for Minimum Sales Amount
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
min_row = sales_df[sales_df['Sales'] == sales_df['Sales'].min()].iloc[0]
print('Minimum Sales Amount:', min_row['Sales'])
print('Category:', min_row['Category'])
print('Region:', min_row['Region'])

# %%
# Bar Chart of Sales by Category
import pandas as pd
import matplotlib.pyplot as plt
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
sales_by_category = sales_df.groupby('Category')['Sales'].sum()
plt.figure(figsize=(8,6))
sales_by_category.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Box Plot of Sales Distribution with Outliers Highlighted
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(8,6))
sns.boxplot(y=sales_df['Sales'], color='lightblue')
plt.title('Sales Distribution with Outliers Highlighted')
plt.ylabel('Sales Amount')
plt.show()

# %%
# Histogram of Sales Distribution with Outliers Highlighted
import matplotlib.pyplot as plt
import seaborn as sns
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
Q1 = sales_df['Sales'].quantile(0.25)
Q3 = sales_df['Sales'].quantile(0.75)
IQR = Q3 - Q1
outliers = sales_df[(sales_df['Sales'] < Q1 - 1.5 * IQR) | (sales_df['Sales'] > Q3 + 1.5 * IQR)]
plt.figure(figsize=(10,6))
sns.histplot(sales_df['Sales'], bins=30, kde=True, color='skyblue', label='Sales')
plt.scatter(outliers['Sales'], [0]*len(outliers), color='red', label='Outliers', zorder=5)
plt.title('Sales Distribution with Outliers Highlighted')
plt.xlabel('Sales Amount')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# %%
# Pivot Table: Sales by Year and Quarter
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Year'] = sales_df['Date'].dt.year
sales_df['Quarter'] = sales_df['Date'].dt.quarter
pivot = pd.pivot_table(sales_df, values='Sales', index='Year', columns='Quarter', aggfunc='sum', fill_value=0)
print('Pivot Table: Sales by Year and Quarter')
print(pivot)

# %%
# Heatmap of Sales by Year and Quarter
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(8,6))
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='Blues')
plt.title('Sales by Year and Quarter (Heatmap)')
plt.xlabel('Quarter')
plt.ylabel('Year')
plt.show()

# %%
# Grouped Bar Chart of Sales by Year and Quarter
import matplotlib.pyplot as plt
pivot.plot(kind='bar', figsize=(10,6))
plt.title('Sales by Year and Quarter (Grouped Bar Chart)')
plt.xlabel('Year')
plt.ylabel('Total Sales')
plt.legend(title='Quarter')
plt.tight_layout()
plt.show()

# %%
# Pivot Table: Count of Orders by Month
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Month'] = sales_df['Date'].dt.to_period('M')
pivot_count = sales_df.groupby('Month').size().to_frame('Order Count')
print('Pivot Table: Count of Orders by Month')
print(pivot_count)

# %% [markdown]
# # Key Takeaways from Sales Data
# 
# - **Office Supplies** is the leading category in total sales.
# - **South** and **East** regions contribute the most to overall sales.
# - The maximum sales amount is **4991.91** (Office Supplies, South), and the minimum is **513.56** (Office Supplies, North).
# - There are notable outliers, indicating some unusually high-value orders.
# - Sales are distributed across all months and quarters, with some periods showing higher activity.
# - Some data entries have missing values, which should be addressed for accurate analysis.
# 
# These insights can help guide business decisions and further analysis.

# %%
# Analyze Furniture Sales by Region and Month
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Month'] = sales_df['Date'].dt.to_period('M')
furniture_sales = sales_df[sales_df['Category'] == 'Furniture']
region_summary = furniture_sales.groupby('Region')['Sales'].sum().sort_values(ascending=False)
month_summary = furniture_sales.groupby('Month')['Sales'].sum().sort_values(ascending=False)
print('Furniture Sales by Region:')
print(region_summary)
print('\nFurniture Sales by Month:')
print(month_summary)


# %% [markdown]
# # Category Performance and Tips to Increase Sales
# 
# **Top Performing Category by Sales Amount:**
# - Office Supplies (based on previous analysis)
# - Furniture (also performs strongly)
# 
# **Least Performing Category by Sales Amount:**
# - Technology
# 
# ## Tips to Increase Sales for Technology Category
# - Analyze customer needs and update product offerings.
# - Run targeted promotions and discounts for Technology products.
# - Bundle Technology items with top-selling categories (e.g., Office Supplies).
# - Improve product visibility online and in-store.
# - Educate customers about new technology features and benefits.
# - Partner with businesses for bulk or corporate sales.
# - Collect and act on customer feedback to improve satisfaction.
# 
# These actions can help boost sales for the least performing category.

# %%
# Sales Trend by Category and Region
import matplotlib.pyplot as plt
categories = sales_df['Category'].unique()
regions = sales_df['Region'].unique()
plt.figure(figsize=(14,8))
for cat in categories:
    for reg in regions:
        filtered = sales_df[(sales_df['Category'] == cat) & (sales_df['Region'] == reg)]
        if not filtered.empty:
            trend = filtered.groupby('Date')['Sales'].sum()
            plt.plot(trend.index, trend.values, label=f'{cat} - {reg}')
plt.title('Sales Trend by Category and Region')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Additional Analysis: Top Category-Region Combinations
combo_sales = sales_df.groupby(['Category', 'Region'])['Sales'].sum().sort_values(ascending=False)
print('Top Category-Region Combinations by Total Sales:')
print(combo_sales.head(5))

# %%
# Breakdown: Sales by Category and Region (Bar Chart)
import matplotlib.pyplot as plt
import seaborn as sns
cat_reg_sales = sales_df.groupby(['Category', 'Region'])['Sales'].sum().reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x='Category', y='Sales', hue='Region', data=cat_reg_sales)
plt.title('Sales by Category and Region')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.show()


# Pie Chart: Sales Distribution by Category
plt.figure(figsize=(7,7))
sales_by_category = sales_df.groupby('Category')['Sales'].sum()
sales_by_category.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Sales Distribution by Category')
plt.ylabel('')
plt.show()

# %%
# Trend of Top 2 Regions by Total Sales
import matplotlib.pyplot as plt
region_totals = sales_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
top_regions = region_totals.index[:2]
plt.figure(figsize=(14,8))
for reg in top_regions:
    reg_data = sales_df[sales_df['Region'] == reg]
    trend = reg_data.groupby('Date')['Sales'].sum()
    plt.plot(trend.index, trend.values, label=reg)
plt.title('Sales Trend Over Time for Top 2 Regions')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
# Further Breakdown: Top 2 Regions by Category and Month
import matplotlib.pyplot as plt
import seaborn as sns
region_totals = sales_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
top_regions = region_totals.index[:2]
for reg in top_regions:
    reg_data = sales_df[sales_df['Region'] == reg]
    # Sales by Category
    cat_sales = reg_data.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    cat_sales.plot(kind='bar', color='orange')
    plt.title(f'Sales by Category in {reg}')
    plt.xlabel('Category')
    plt.ylabel('Total Sales')
    plt.tight_layout()
    plt.show()

# %%
# Analyze Furniture Sales by Region and Month
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Month'] = sales_df['Date'].dt.to_period('M')
furniture_sales = sales_df[sales_df['Category'] == 'Furniture']
region_summary = furniture_sales.groupby('Region')['Sales'].sum().sort_values(ascending=False)
month_summary = furniture_sales.groupby('Month')['Sales'].sum().sort_values(ascending=False)
print('Furniture Sales by Region:')
print(region_summary)
print('\nFurniture Sales by Month:')
print(month_summary)


# %% [markdown]
# # Category Performance and Tips to Increase Sales
# 
# **Top Performing Category by Sales Amount:**
# - Office Supplies (based on previous analysis)
# - Furniture (also performs strongly)
# 
# **Least Performing Category by Sales Amount:**
# - Technology
# 
# ## Tips to Increase Sales for Technology Category
# - Analyze customer needs and update product offerings.
# - Run targeted promotions and discounts for Technology products.
# - Bundle Technology items with top-selling categories (e.g., Office Supplies).
# - Improve product visibility online and in-store.
# - Educate customers about new technology features and benefits.
# - Partner with businesses for bulk or corporate sales.
# - Collect and act on customer feedback to improve satisfaction.
# 
# These actions can help boost sales for the least performing category.

# %%
# Sales Trend by Category and Region
import matplotlib.pyplot as plt
categories = sales_df['Category'].unique()
regions = sales_df['Region'].unique()
plt.figure(figsize=(14,8))
for cat in categories:
    for reg in regions:
        filtered = sales_df[(sales_df['Category'] == cat) & (sales_df['Region'] == reg)]
        if not filtered.empty:
            trend = filtered.groupby('Date')['Sales'].sum()
            plt.plot(trend.index, trend.values, label=f'{cat} - {reg}')
plt.title('Sales Trend by Category and Region')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Additional Analysis: Top Category-Region Combinations
combo_sales = sales_df.groupby(['Category', 'Region'])['Sales'].sum().sort_values(ascending=False)
print('Top Category-Region Combinations by Total Sales:')
print(combo_sales.head(5))

# %%
# Breakdown: Sales by Category and Region (Bar Chart)
import matplotlib.pyplot as plt
import seaborn as sns
cat_reg_sales = sales_df.groupby(['Category', 'Region'])['Sales'].sum().reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x='Category', y='Sales', hue='Region', data=cat_reg_sales)
plt.title('Sales by Category and Region')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.show()


# Pie Chart: Sales Distribution by Category
plt.figure(figsize=(7,7))
sales_by_category = sales_df.groupby('Category')['Sales'].sum()
sales_by_category.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Sales Distribution by Category')
plt.ylabel('')
plt.show()

# %%
# Trend of Top 2 Regions by Total Sales
import matplotlib.pyplot as plt
region_totals = sales_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
top_regions = region_totals.index[:2]
plt.figure(figsize=(14,8))
for reg in top_regions:
    reg_data = sales_df[sales_df['Region'] == reg]
    trend = reg_data.groupby('Date')['Sales'].sum()
    plt.plot(trend.index, trend.values, label=reg)
plt.title('Sales Trend Over Time for Top 2 Regions')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
# Further Breakdown: Top 2 Regions by Category and Month
import matplotlib.pyplot as plt
import seaborn as sns
region_totals = sales_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
top_regions = region_totals.index[:2]
for reg in top_regions:
    reg_data = sales_df[sales_df['Region'] == reg]
    # Sales by Category
    cat_sales = reg_data.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    cat_sales.plot(kind='bar', color='orange')
    plt.title(f'Sales by Category in {reg}')
    plt.xlabel('Category')
    plt.ylabel('Total Sales')
    plt.tight_layout()
    plt.show()

# %%
# Analyze Furniture Sales by Region and Month
import pandas as pd
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Month'] = sales_df['Date'].dt.to_period('M')
furniture_sales = sales_df[sales_df['Category'] == 'Furniture']
region_summary = furniture_sales.groupby('Region')['Sales'].sum().sort_values(ascending=False)
month_summary = furniture_sales.groupby('Month')['Sales'].sum().sort_values(ascending=False)
print('Furniture Sales by Region:')
print(region_summary)
print('\nFurniture Sales by Month:')
print(month_summary)


# %% [markdown]
# # Category Performance and Tips to Increase Sales
# 
# **Top Performing Category by Sales Amount:**
# - Office Supplies (based on previous analysis)
# - Furniture (also performs strongly)
# 
# **Least Performing Category by Sales Amount:**
# - Technology
# 
# ## Tips to Increase Sales for Technology Category
# - Analyze customer needs and update product offerings.
# - Run targeted promotions and discounts for Technology products.
# - Bundle Technology items with top-selling categories (e.g., Office Supplies).
# - Improve product visibility online and in-store.
# - Educate customers about new technology features and benefits.
# - Partner with businesses for bulk or corporate sales.
# - Collect and act on customer feedback to improve satisfaction.
# 
# These actions can help boost sales for the least performing category.

# %%
# Sales Dashboard (Matplotlib)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sales_df = pd.read_csv('sales_data_with_issues.csv')
sales_df = sales_df[pd.to_numeric(sales_df['Sales'], errors='coerce').notnull()]
sales_df['Sales'] = sales_df['Sales'].astype(float)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df['Month'] = sales_df['Date'].dt.to_period('M')

fig, axs = plt.subplots(2, 2, figsize=(16, 10))

# KPI: Total, Average, Count
total_sales = sales_df['Sales'].sum()
avg_sales = sales_df['Sales'].mean()
order_count = len(sales_df)
axs[0,0].text(0.1, 0.8, f'Total Sales: {total_sales:.2f}', fontsize=14)
axs[0,0].text(0.1, 0.6, f'Average Sales: {avg_sales:.2f}', fontsize=14)
axs[0,0].text(0.1, 0.4, f'Order Count: {order_count}', fontsize=14)
axs[0,0].axis('off')
axs[0,0].set_title('KPIs')

# Sales Trend
daily_sales = sales_df.groupby('Date')['Sales'].sum()
axs[0,1].plot(daily_sales.index, daily_sales.values, color='navy')
axs[0,1].set_title('Sales Trend Over Time')
axs[0,1].set_xlabel('Date')
axs[0,1].set_ylabel('Total Sales')
axs[0,1].grid(True)

# Sales by Category
sales_by_category = sales_df.groupby('Category')['Sales'].sum()
axs[1,0].bar(sales_by_category.index, sales_by_category.values, color='skyblue')
axs[1,0].set_title('Sales by Category')
axs[1,0].set_xlabel('Category')
axs[1,0].set_ylabel('Total Sales')

# Sales by Region
sales_by_region = sales_df.groupby('Region')['Sales'].sum()
axs[1,1].bar(sales_by_region.index, sales_by_region.values, color='orange')
axs[1,1].set_title('Sales by Region')
axs[1,1].set_xlabel('Region')
axs[1,1].set_ylabel('Total Sales')

plt.tight_layout()
plt.show()

# Outlier Detection (Box Plot)
plt.figure(figsize=(8,4))
sns.boxplot(y=sales_df['Sales'], color='lightgreen')
plt.title('Sales Amount Distribution & Outliers')
plt.ylabel('Sales Amount')
plt.show()

# %%
# Scatter plot: Sales vs. Date
import matplotlib.pyplot as plt
import pandas as pd

# If not already loaded, load the data
df = sales_df if 'sales_df' in globals() else pd.read_csv('sales_data_with_issues.csv', parse_dates=['Date'])

# Drop rows with missing sales values
df_clean = df.dropna(subset=['Sales'])

plt.figure(figsize=(10,6))
plt.scatter(df_clean['Date'], df_clean['Sales'], alpha=0.6, c='blue')
plt.title('Scatter Plot of Sales vs. Date')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.grid(True)
plt.tight_layout()
plt.show()


# %%
# Advanced Customer-Focused Analysis & Actionable Insights
import matplotlib.pyplot as plt
import pandas as pd

# Use existing cleaned data
df = df_clean if 'df_clean' in globals() else pd.read_csv('sales_data_with_issues.csv', parse_dates=['Date']).dropna(subset=['Sales'])

# Add month and quarter columns
df['Month'] = df['Date'].dt.month
fiscal_quarter = ((df['Date'].dt.month-1)//3)+1
df['Quarter'] = fiscal_quarter

# 1. Seasonality: Monthly and Quarterly Sales Trends
monthly_sales = df.groupby('Month')['Sales'].sum()
quarterly_sales = df.groupby('Quarter')['Sales'].sum()
fig, axs = plt.subplots(1, 2, figsize=(14,5))
axs[0].bar(monthly_sales.index, monthly_sales.values, color='skyblue')
axs[0].set_title('Total Sales by Month')
axs[0].set_xlabel('Month')
axs[0].set_ylabel('Sales')
axs[1].bar(quarterly_sales.index, quarterly_sales.values, color='orange')
axs[1].set_title('Total Sales by Quarter')
axs[1].set_xlabel('Quarter')
axs[1].set_ylabel('Sales')
plt.tight_layout()
plt.show()

# 2. Region-Category Interaction
pivot_rc = df.pivot_table(index='Region', columns='Category', values='Sales', aggfunc='sum')
pivot_rc.plot(kind='bar', figsize=(10,6))
plt.title('Sales by Region and Category')
plt.ylabel('Sales')
plt.tight_layout()
plt.show()

# 3. Top/Bottom Performers
best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()
worst_month = monthly_sales.idxmin()
worst_month_sales = monthly_sales.min()
best_region = df.groupby('Region')['Sales'].sum().idxmax()
best_region_sales = df.groupby('Region')['Sales'].sum().max()
worst_region = df.groupby('Region')['Sales'].sum().idxmin()
worst_region_sales = df.groupby('Region')['Sales'].sum().min()

print(f"Best Month: {best_month} with sales {best_month_sales:.2f}")
print(f"Worst Month: {worst_month} with sales {worst_month_sales:.2f}")
print(f"Best Region: {best_region} with sales {best_region_sales:.2f}")
print(f"Worst Region: {worst_region} with sales {worst_region_sales:.2f}")

# 4. Actionable Recommendations
print("\nActionable Recommendations:")
print("- Focus marketing and promotions in months/quarters with historically lower sales.")
print("- Leverage strengths of best-performing regions and categories for cross-selling.")
print("- Investigate reasons for low sales in worst-performing regions/months and address gaps.")
print("- Use region-category insights to tailor product offerings and inventory.")


# %%
# Sales Forecasting using Linear Regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Use cleaned data
df = df_clean if 'df_clean' in globals() else pd.read_csv('sales_data_with_issues.csv', parse_dates=['Date']).dropna(subset=['Sales'])

# Aggregate sales by month
df['YearMonth'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['Sales'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].dt.to_timestamp()

# Prepare data for regression
monthly_sales['MonthNum'] = np.arange(len(monthly_sales))
X = monthly_sales[['MonthNum']]
y = monthly_sales['Sales']

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

# Forecast next 6 months
future_months = np.arange(len(monthly_sales), len(monthly_sales)+6)
future_dates = pd.date_range(monthly_sales['YearMonth'].iloc[-1]+pd.offsets.MonthBegin(1), periods=6, freq='MS')
future_sales = model.predict(future_months.reshape(-1,1))

# Plot actual and forecasted sales
plt.figure(figsize=(10,6))
plt.plot(monthly_sales['YearMonth'], monthly_sales['Sales'], label='Actual Sales', marker='o')
plt.plot(future_dates, future_sales, label='Forecasted Sales', marker='x', linestyle='--', color='red')
plt.title('Sales Forecast for Next 6 Months (Linear Regression)')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print forecasted sales values
forecast_df = pd.DataFrame({'Month': future_dates.strftime('%Y-%m'), 'Forecasted Sales': future_sales})
print(forecast_df)


# %%
# Advanced Sales Forecasting using ARIMA
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Use cleaned data
df = df_clean if 'df_clean' in globals() else pd.read_csv('sales_data_with_issues.csv', parse_dates=['Date']).dropna(subset=['Sales'])

df['YearMonth'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['Sales'].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()

# Fit ARIMA model (order can be tuned)
model = ARIMA(monthly_sales, order=(1,1,1))
model_fit = model.fit()

# Forecast next 6 months
forecast = model_fit.forecast(steps=6)
forecast_index = pd.date_range(monthly_sales.index[-1]+pd.offsets.MonthBegin(1), periods=6, freq='MS')

# Plot actual and forecasted sales
plt.figure(figsize=(10,6))
plt.plot(monthly_sales.index, monthly_sales.values, label='Actual Sales', marker='o')
plt.plot(forecast_index, forecast.values, label='ARIMA Forecast', marker='x', linestyle='--', color='green')
plt.title('Sales Forecast for Next 6 Months (ARIMA)')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print forecasted sales values
forecast_df_arima = pd.DataFrame({'Month': forecast_index.strftime('%Y-%m'), 'ARIMA Forecasted Sales': forecast.values})
print(forecast_df_arima)


# %%
# Sales Forecast by Region and Category (Linear Regression)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Use cleaned data
df = df_clean if 'df_clean' in globals() else pd.read_csv('sales_data_with_issues.csv', parse_dates=['Date']).dropna(subset=['Sales'])
df['YearMonth'] = df['Date'].dt.to_period('M')

regions = df['Region'].dropna().unique()
categories = df['Category'].dropna().unique()

region_forecasts = {}
category_forecasts = {}
future_months = np.arange(df['YearMonth'].nunique(), df['YearMonth'].nunique()+6)
future_dates = pd.date_range(df['YearMonth'].dt.to_timestamp().max()+pd.offsets.MonthBegin(1), periods=6, freq='MS')

# Forecast by Region
for region in regions:
    reg_df = df[df['Region'] == region].groupby('YearMonth')['Sales'].sum().reset_index()
    reg_df['YearMonth'] = reg_df['YearMonth'].dt.to_timestamp()
    reg_df['MonthNum'] = np.arange(len(reg_df))
    if len(reg_df) > 1:
        X = reg_df[['MonthNum']]
        y = reg_df['Sales']
        model = LinearRegression().fit(X, y)
        forecast = model.predict(future_months.reshape(-1,1))
        region_forecasts[region] = forecast
        plt.plot(reg_df['YearMonth'], reg_df['Sales'], label=f'{region} Actual')
        plt.plot(future_dates, forecast, '--', label=f'{region} Forecast')
plt.title('Sales Forecast by Region (Next 6 Months)')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.tight_layout()
plt.show()

# Forecast by Category
for category in categories:
    cat_df = df[df['Category'] == category].groupby('YearMonth')['Sales'].sum().reset_index()
    cat_df['YearMonth'] = cat_df['YearMonth'].dt.to_timestamp()
    cat_df['MonthNum'] = np.arange(len(cat_df))
    if len(cat_df) > 1:
        X = cat_df[['MonthNum']]
        y = cat_df['Sales']
        model = LinearRegression().fit(X, y)
        forecast = model.predict(future_months.reshape(-1,1))
        category_forecasts[category] = forecast
        plt.plot(cat_df['YearMonth'], cat_df['Sales'], label=f'{category} Actual')
        plt.plot(future_dates, forecast, '--', label=f'{category} Forecast')
plt.title('Sales Forecast by Category (Next 6 Months)')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.tight_layout()
plt.show()

# Print forecasted sales values for each region and category
print('Forecasted Sales by Region (Next 6 Months):')
for region, forecast in region_forecasts.items():
    print(f'{region}:', np.round(forecast,2))
print('\nForecasted Sales by Category (Next 6 Months):')
for category, forecast in category_forecasts.items():
    print(f'{category}:', np.round(forecast,2))


# %%
# Pivot table: Sales over time (Month vs Region)
import pandas as pd

# Use cleaned data
df = df_clean if 'df_clean' in globals() else pd.read_csv('sales_data_with_issues.csv', parse_dates=['Date']).dropna(subset=['Sales'])
df['Month'] = df['Date'].dt.to_period('M')
pivot_month_region = pd.pivot_table(df, values='Sales', index='Month', columns='Region', aggfunc='sum', fill_value=0)

print('Pivot Table: Sales by Month and Region')
display(pivot_month_region)


# %%
# Region-wise Product Performance Analysis
import pandas as pd

# Load the sales data
df_sales = pd.read_csv('sales.csv')

# Group by Region and Product, summing Total Revenue and Units Sold
region_product_perf = df_sales.groupby(['Region', 'Product']).agg({'Total Revenue': 'sum', 'Units Sold': 'sum'}).reset_index()

# Sort within each region by Total Revenue descending
region_product_perf = region_product_perf.sort_values(['Region', 'Total Revenue'], ascending=[True, False])

print('Region-wise Product Performance:')
display(region_product_perf)


# %%
# Visualization: Region-wise Product Performance using Seaborn
import seaborn as sns
import matplotlib.pyplot as plt

# If not already loaded, load the data and summary
df_sales = pd.read_csv('sales.csv')
region_product_perf = df_sales.groupby(['Region', 'Product']).agg({'Total Revenue': 'sum', 'Units Sold': 'sum'}).reset_index()

plt.figure(figsize=(14, 6))
sns.barplot(data=region_product_perf, x='Region', y='Total Revenue', hue='Product')
plt.title('Total Revenue by Product and Region')
plt.ylabel('Total Revenue')
plt.xlabel('Region')
plt.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))
sns.barplot(data=region_product_perf, x='Region', y='Units Sold', hue='Product')
plt.title('Units Sold by Product and Region')
plt.ylabel('Units Sold')
plt.xlabel('Region')
plt.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
# Monthly Revenue Analysis
import pandas as pd
import matplotlib.pyplot as plt

df_sales = pd.read_csv('sales.csv', parse_dates=['Date'])
df_sales['Month'] = df_sales['Date'].dt.to_period('M')

monthly_revenue = df_sales.groupby('Month')['Total Revenue'].sum().reset_index()

print('Monthly Total Revenue:')
display(monthly_revenue)

plt.figure(figsize=(10,5))
plt.plot(monthly_revenue['Month'].astype(str), monthly_revenue['Total Revenue'], marker='o', color='teal')
plt.title('Monthly Total Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
# Revenue Forecasting using Linear Regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df_sales = pd.read_csv('sales.csv', parse_dates=['Date'])
df_sales['Month'] = df_sales['Date'].dt.to_period('M')
monthly_revenue = df_sales.groupby('Month')['Total Revenue'].sum().reset_index()
monthly_revenue['MonthNum'] = np.arange(len(monthly_revenue))

# Prepare data for regression
X = monthly_revenue[['MonthNum']]
y = monthly_revenue['Total Revenue']
model = LinearRegression().fit(X, y)

# Forecast next 6 months
future_months = np.arange(len(monthly_revenue), len(monthly_revenue)+6)
future_dates = pd.date_range(monthly_revenue['Month'].dt.to_timestamp().max()+pd.offsets.MonthBegin(1), periods=6, freq='MS')
future_revenue = model.predict(future_months.reshape(-1,1))

# Plot actual and forecasted revenue
plt.figure(figsize=(10,5))
plt.plot(monthly_revenue['Month'].astype(str), monthly_revenue['Total Revenue'], marker='o', label='Actual Revenue')
plt.plot(future_dates.strftime('%Y-%m'), future_revenue, marker='x', linestyle='--', color='red', label='Forecasted Revenue')
plt.title('Monthly Revenue Forecast (Linear Regression)')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Print forecasted revenue values
forecast_df = pd.DataFrame({'Month': future_dates.strftime('%Y-%m'), 'Forecasted Revenue': future_revenue})
print(forecast_df)


# %%
# Identify Unusually High or Low Total Revenue Records (Outlier Detection)
import pandas as pd

df_sales = pd.read_csv('sales.csv')

# Calculate IQR for Total Revenue
Q1 = df_sales['Total Revenue'].quantile(0.25)
Q3 = df_sales['Total Revenue'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df_sales[(df_sales['Total Revenue'] < lower_bound) | (df_sales['Total Revenue'] > upper_bound)]

print('Unusually High or Low Total Revenue Records:')
display(outliers)


# %%
# Pivot Table: Total Profit by Product Category and Region
import pandas as pd

# Load the salesone.csv data
df_salesone = pd.read_csv('salesone.csv')

# Create a pivot table: total profit by Product (category) and Region
pivot_profit = pd.pivot_table(df_salesone, values='Profit', index='Product', columns='Region', aggfunc='sum', fill_value=0)

print('Pivot Table: Total Profit by Product Category and Region')
display(pivot_profit)


# %%
# Compare Product-wise Revenue and Profit per Region
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the salesone.csv data
df_salesone = pd.read_csv('salesone.csv')

# Aggregate revenue and profit by product and region
agg = df_salesone.groupby(['Region', 'Product']).agg({'Total Revenue': 'sum', 'Profit': 'sum'}).reset_index()

# Melt for easier plotting
agg_melted = agg.melt(id_vars=['Region', 'Product'], value_vars=['Total Revenue', 'Profit'], var_name='Metric', value_name='Value')

# Plot grouped barplot for each region
regions = agg['Region'].unique()
for region in regions:
    plt.figure(figsize=(10,5))
    data = agg_melted[agg_melted['Region'] == region]
    sns.barplot(data=data, x='Product', y='Value', hue='Metric')
    plt.title(f'Product-wise Revenue and Profit in {region} Region')
    plt.ylabel('Amount')
    plt.xlabel('Product')
    plt.legend(title='Metric')
    plt.tight_layout()
    plt.show()


# %%
# Correlation between Profit and Other Available Columns
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_salesone = pd.read_csv('salesone.csv')

# Select relevant numerical columns
num_cols = ['Units Sold', 'Unit Price', 'Total Revenue', 'Profit']
corr_matrix = df_salesone[num_cols].corr()

print('Correlation Matrix (including Profit):')
display(corr_matrix)

# Visualize the correlation matrix
plt.figure(figsize=(6,4))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix: Profit vs Other Variables')
plt.tight_layout()
plt.show()


# %%
# Simulate Different Unit Price Scenarios and Revenue Impact
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_salesone = pd.read_csv('salesone.csv')

# Choose a product to simulate (or simulate for all products)
products = df_salesone['Product'].unique()

# Define price change scenarios (e.g., -20%, -10%, 0%, +10%, +20%)
price_changes = np.array([-0.2, -0.1, 0, 0.1, 0.2])

# Store results
scenario_results = []

for product in products:
    prod_df = df_salesone[df_salesone['Product'] == product]
    avg_units = prod_df['Units Sold'].mean()
    base_price = prod_df['Unit Price'].mean()
    for pct in price_changes:
        new_price = base_price * (1 + pct)
        # Assume units sold remains constant for simplicity
        new_revenue = avg_units * new_price * len(prod_df)
        scenario_results.append({'Product': product, 'Price Change %': pct*100, 'Simulated Revenue': new_revenue})

scenario_df = pd.DataFrame(scenario_results)

# Plot
plt.figure(figsize=(10,6))
for product in products:
    data = scenario_df[scenario_df['Product'] == product]
    plt.plot(data['Price Change %'], data['Simulated Revenue'], marker='o', label=product)
plt.title('Simulated Revenue Under Different Unit Price Scenarios')
plt.xlabel('Unit Price Change (%)')
plt.ylabel('Simulated Total Revenue')
plt.legend(title='Product')
plt.grid(True)
plt.tight_layout()
plt.show()

print('Simulated Revenue Table:')
display(scenario_df)


# %%
# Simulate Unit Price Scenarios with Demand Elasticity
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_salesone = pd.read_csv('salesone.csv')
products = df_salesone['Product'].unique()

# Define price change scenarios (e.g., -20%, -10%, 0%, +10%, +20%)
price_changes = np.array([-0.2, -0.1, 0, 0.1, 0.2])

# Assume a price elasticity of demand (negative means demand drops as price rises)
# Example: elasticity = -1.2 (for every 1% increase in price, units sold drops by 1.2%)
elasticity = -1.2

scenario_results = []

for product in products:
    prod_df = df_salesone[df_salesone['Product'] == product]
    avg_units = prod_df['Units Sold'].mean()
    base_price = prod_df['Unit Price'].mean()
    n_periods = len(prod_df)
    for pct in price_changes:
        new_price = base_price * (1 + pct)
        # Adjust units sold based on elasticity
        new_units = avg_units * (1 + elasticity * pct)
        new_units = max(new_units, 0)  # Units sold can't be negative
        new_revenue = new_units * new_price * n_periods
        scenario_results.append({'Product': product, 'Price Change %': pct*100, 'Simulated Revenue': new_revenue, 'Simulated Units Sold': new_units * n_periods})

scenario_df = pd.DataFrame(scenario_results)

# Plot revenue
plt.figure(figsize=(10,6))
for product in products:
    data = scenario_df[scenario_df['Product'] == product]
    plt.plot(data['Price Change %'], data['Simulated Revenue'], marker='o', label=product)
plt.title('Simulated Revenue Under Price Scenarios with Demand Elasticity')
plt.xlabel('Unit Price Change (%)')
plt.ylabel('Simulated Total Revenue')
plt.legend(title='Product')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot units sold
plt.figure(figsize=(10,6))
for product in products:
    data = scenario_df[scenario_df['Product'] == product]
    plt.plot(data['Price Change %'], data['Simulated Units Sold'], marker='s', label=product)
plt.title('Simulated Units Sold Under Price Scenarios with Demand Elasticity')
plt.xlabel('Unit Price Change (%)')
plt.ylabel('Simulated Total Units Sold')
plt.legend(title='Product')
plt.grid(True)
plt.tight_layout()
plt.show()

print('Simulated Revenue and Units Sold Table:')
display(scenario_df)


# %%
# Analyze Product Sales Peaks by Month
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)
df_salesone['Month'] = df_salesone['Date'].dt.strftime('%b')

# Group by Product and Month, sum Units Sold
monthly_product_sales = df_salesone.groupby(['Product', 'Month'])['Units Sold'].sum().reset_index()

# Order months chronologically
from pandas.api.types import CategoricalDtype
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_product_sales['Month'] = monthly_product_sales['Month'].astype(CategoricalDtype(categories=month_order, ordered=True))

plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_product_sales, x='Month', y='Units Sold', hue='Product', marker='o')
plt.title('Monthly Units Sold by Product')
plt.ylabel('Units Sold')
plt.xlabel('Month')
plt.legend(title='Product')
plt.tight_layout()
plt.show()

# Show table of peak month for each product
peak_months = monthly_product_sales.loc[monthly_product_sales.groupby('Product')['Units Sold'].idxmax()][['Product', 'Month', 'Units Sold']]
print('Peak Month for Each Product:')
display(peak_months)


# %%
# Estimate Reorder Point for High Demand Products
import pandas as pd
import numpy as np
from datetime import timedelta

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)

# Define high demand as top 3 products by total units sold
top_products = df_salesone.groupby('Product')['Units Sold'].sum().sort_values(ascending=False).head(3).index.tolist()

# Assume a starting inventory for each product (can be customized)
starting_inventory = 500  # units

# Calculate recent average daily sales rate (last 30 days in data)
last_date = df_salesone['Date'].max()
window_start = last_date - pd.Timedelta(days=30)
recent_sales = df_salesone[df_salesone['Date'] >= window_start]

reorder_estimates = []
for product in top_products:
    prod_sales = recent_sales[recent_sales['Product'] == product]
    if not prod_sales.empty:
        daily_rate = prod_sales['Units Sold'].sum() / 30
        if daily_rate > 0:
            days_left = starting_inventory / daily_rate
            est_runout_date = last_date + timedelta(days=days_left)
        else:
            days_left = np.inf
            est_runout_date = 'N/A'
    else:
        days_left = np.inf
        est_runout_date = 'N/A'
    reorder_estimates.append({'Product': product, 'Avg Daily Sales (last 30d)': round(daily_rate,2) if not np.isinf(days_left) else 0, 'Days Until Out': round(days_left,1) if not np.isinf(days_left) else 'N/A', 'Est Runout Date': est_runout_date})

reorder_df = pd.DataFrame(reorder_estimates)
print('Reorder Estimates for High Demand Products (Assuming 500 units in stock):')
display(reorder_df)


# %%
# Compare Average Sales per Product in Each Region
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_salesone = pd.read_csv('salesone.csv')

# Calculate average sales (units sold) per product in each region
avg_sales = df_salesone.groupby(['Region', 'Product'])['Units Sold'].mean().unstack()

print('Average Units Sold per Product in Each Region:')
display(avg_sales)

# Visualize as a heatmap
plt.figure(figsize=(10,6))
sns.heatmap(avg_sales, annot=True, fmt='.1f', cmap='YlGnBu')
plt.title('Average Units Sold per Product in Each Region')
plt.ylabel('Region')
plt.xlabel('Product')
plt.tight_layout()
plt.show()


# %%
# Revenue per Unit Sold Efficiency Matrix (Region vs Product)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_salesone = pd.read_csv('salesone.csv')

# Calculate revenue per unit sold for each product in each region
rev_per_unit = df_salesone.groupby(['Region', 'Product']).apply(lambda x: x['Total Revenue'].sum() / x['Units Sold'].sum() if x['Units Sold'].sum() > 0 else 0).unstack()

print('Revenue per Unit Sold Efficiency Matrix:')
display(rev_per_unit)

# Visualize as a heatmap
plt.figure(figsize=(10,6))
sns.heatmap(rev_per_unit, annot=True, fmt='.2f', cmap='OrRd')
plt.title('Revenue per Unit Sold Efficiency (Region vs Product)')
plt.ylabel('Region')
plt.xlabel('Product')
plt.tight_layout()
plt.show()


# %%
# Highlight Periods When Revenue Dropped from Previous Day
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)

# Aggregate total revenue by day
daily_revenue = df_salesone.groupby('Date')['Total Revenue'].sum().sort_index().reset_index()

# Calculate revenue change from previous day
daily_revenue['Revenue Change'] = daily_revenue['Total Revenue'].diff()
daily_revenue['Drop'] = daily_revenue['Revenue Change'] < 0

# Highlight drops on the plot
plt.figure(figsize=(12,6))
plt.plot(daily_revenue['Date'], daily_revenue['Total Revenue'], marker='o', label='Total Revenue')
plt.scatter(daily_revenue.loc[daily_revenue['Drop'], 'Date'],
            daily_revenue.loc[daily_revenue['Drop'], 'Total Revenue'],
            color='red', label='Revenue Drop', zorder=5)
plt.title('Daily Total Revenue with Drops Highlighted')
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.legend()
plt.tight_layout()
plt.show()

# Show table of drops
drops = daily_revenue[daily_revenue['Drop']][['Date', 'Total Revenue', 'Revenue Change']]
print('Days When Revenue Dropped from Previous Day:')
display(drops)


# %%
# Visualize Region Contribution in Units Sold Across Products
import pandas as pd
import matplotlib.pyplot as plt

df_salesone = pd.read_csv('salesone.csv')

# Pivot table: products as x, regions as stacked bars
units_by_region_product = df_salesone.pivot_table(index='Product', columns='Region', values='Units Sold', aggfunc='sum', fill_value=0)

# Plot stacked bar chart
units_by_region_product.plot(kind='bar', stacked=True, figsize=(12,6), colormap='tab20')
plt.title('Region Contribution in Units Sold Across Products')
plt.ylabel('Units Sold')
plt.xlabel('Product')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
# Analyze Top Product Combinations Contributing to Revenue by Region
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

# Load data
df_salesone = pd.read_csv('salesone.csv')

# For each region, find top 3 product pairs by total revenue
regions = df_salesone['Region'].unique()
combo_results = []

for region in regions:
    reg_df = df_salesone[df_salesone['Region'] == region]
    products = reg_df['Product'].unique()
    # All possible product pairs
    for prod1, prod2 in combinations(products, 2):
        combo_revenue = reg_df[reg_df['Product'].isin([prod1, prod2])]['Total Revenue'].sum()
        combo_results.append({'Region': region, 'Product Combo': f'{prod1} + {prod2}', 'Total Revenue': combo_revenue})

combo_df = pd.DataFrame(combo_results)

# For each region, get top 3 combos
top_combos = combo_df.sort_values(['Region', 'Total Revenue'], ascending=[True, False]).groupby('Region').head(3)

print('Top Product Combinations by Revenue for Each Region:')
display(top_combos)

# Visualize
plt.figure(figsize=(12,6))
sns.barplot(data=top_combos, x='Region', y='Total Revenue', hue='Product Combo')
plt.title('Top Product Combinations by Revenue for Each Region')
plt.ylabel('Total Revenue')
plt.xlabel('Region')
plt.legend(title='Product Combo', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
# Find Most Profitable Product in Each Region
import pandas as pd

df_salesone = pd.read_csv('salesone.csv')

# Group by Region and Product, sum Profit
profit_by_region_product = df_salesone.groupby(['Region', 'Product'])['Profit'].sum().reset_index()

# For each region, find the product with the highest profit
idx = profit_by_region_product.groupby('Region')['Profit'].idxmax()
most_profitable = profit_by_region_product.loc[idx].reset_index(drop=True)

print('Most Profitable Product in Each Region:')
display(most_profitable)


# %%
# Find Which Day of the Week Yields the Highest Revenue
import pandas as pd

df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)
df_salesone['DayOfWeek'] = df_salesone['Date'].dt.day_name()

# Group by day of week and sum revenue
dow_revenue = df_salesone.groupby('DayOfWeek')['Total Revenue'].sum().reset_index()

# Order days of week
from pandas.api.types import CategoricalDtype
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_revenue['DayOfWeek'] = dow_revenue['DayOfWeek'].astype(CategoricalDtype(categories=days_order, ordered=True))
dow_revenue = dow_revenue.sort_values('DayOfWeek')

print('Total Revenue by Day of the Week:')
display(dow_revenue)

# Find the day with the highest revenue
max_day = dow_revenue.loc[dow_revenue['Total Revenue'].idxmax()]
print(f"\nDay with Highest Revenue: {max_day['DayOfWeek']} (Revenue: {max_day['Total Revenue']})")


# %%
# Track How Revenue Grows Over Time
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)

# Aggregate daily revenue and calculate cumulative sum
daily_revenue = df_salesone.groupby('Date')['Total Revenue'].sum().sort_index().reset_index()
daily_revenue['Cumulative Revenue'] = daily_revenue['Total Revenue'].cumsum()

plt.figure(figsize=(12,6))
plt.plot(daily_revenue['Date'], daily_revenue['Cumulative Revenue'], marker='o', color='teal')
plt.title('Cumulative Revenue Growth Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Revenue')
plt.tight_layout()
plt.show()

print('Cumulative Revenue Table:')
display(daily_revenue)


# %%
# Filter and Display Only Rows Where Units Sold is in Top 10%
import pandas as pd

df_salesone = pd.read_csv('salesone.csv')

# Calculate the 90th percentile threshold
threshold = df_salesone['Units Sold'].quantile(0.9)

# Filter rows where units sold is in the top 10%
top10_df = df_salesone[df_salesone['Units Sold'] >= threshold]

print(f"Rows Where Units Sold is in the Top 10% (Threshold: {threshold}):")
display(top10_df[['Date', 'Product', 'Region', 'Units Sold']])


# %%
# Visualize Top 10% Units Sold Records by Product and Region
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_salesone = pd.read_csv('salesone.csv')
threshold = df_salesone['Units Sold'].quantile(0.9)
top10_df = df_salesone[df_salesone['Units Sold'] >= threshold]

plt.figure(figsize=(12,6))
sns.barplot(data=top10_df, x='Product', y='Units Sold', hue='Region')
plt.title('Top 10% Units Sold Records by Product and Region')
plt.ylabel('Units Sold')
plt.xlabel('Product')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
# Show Shortfall from a Monthly Revenue Target
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)
df_salesone['Month'] = df_salesone['Date'].dt.to_period('M')

# Set monthly revenue target (customize as needed)
monthly_target = 200000  # Example target

# Calculate monthly revenue
monthly_revenue = df_salesone.groupby('Month')['Total Revenue'].sum().reset_index()
monthly_revenue['Shortfall'] = monthly_target - monthly_revenue['Total Revenue']
monthly_revenue['Shortfall'] = monthly_revenue['Shortfall'].clip(lower=0)

print(f'Monthly Revenue Target: {monthly_target}')
display(monthly_revenue)

# Visualize shortfall
plt.figure(figsize=(10,5))
plt.bar(monthly_revenue['Month'].astype(str), monthly_revenue['Shortfall'], color='crimson')
plt.title('Monthly Revenue Shortfall from Target')
plt.xlabel('Month')
plt.ylabel('Shortfall')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
# Check How Each Product Deviates from Its Average Revenue
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_salesone = pd.read_csv('salesone.csv')

# Calculate average revenue per product
avg_revenue = df_salesone.groupby('Product')['Total Revenue'].mean().rename('Avg Revenue').reset_index()

# Merge with original data
df_merged = df_salesone.merge(avg_revenue, on='Product')
df_merged['Revenue Deviation'] = df_merged['Total Revenue'] - df_merged['Avg Revenue']

print('Sample of Revenue Deviation per Product:')
display(df_merged[['Date', 'Product', 'Region', 'Total Revenue', 'Avg Revenue', 'Revenue Deviation']].head())

# Visualize deviation for each product
plt.figure(figsize=(12,6))
sns.boxplot(data=df_merged, x='Product', y='Revenue Deviation', showmeans=True)
plt.title('Revenue Deviation from Product Average')
plt.ylabel('Deviation from Average Revenue')
plt.xlabel('Product')
plt.tight_layout()
plt.show()


# %%
# Auto-Detect Missing or Inconsistent Data
import pandas as pd

df_salesone = pd.read_csv('salesone.csv')

# Check for missing values
display(df_salesone.isnull().sum().to_frame('Missing Values'))

# Check for negative or zero values in columns that should be positive
num_cols = ['Units Sold', 'Unit Price', 'Total Revenue', 'Profit']
for col in num_cols:
    invalid = df_salesone[df_salesone[col] <= 0]
    if not invalid.empty:
        print(f'Rows with non-positive values in {col}:')
        display(invalid)

# Check for duplicate rows
duplicates = df_salesone[df_salesone.duplicated()]
if not duplicates.empty:
    print('Duplicate Rows Detected:')
    display(duplicates)
else:
    print('No duplicate rows detected.')


# %%
# Flag Sudden Day-over-Day Revenue Drop > 30%
import pandas as pd

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)

# Aggregate daily revenue
daily_revenue = df_salesone.groupby('Date')['Total Revenue'].sum().sort_index().reset_index()

# Calculate percent change from previous day
daily_revenue['Pct_Change'] = daily_revenue['Total Revenue'].pct_change()

# Flag days with >30% drop
daily_revenue['Flag_Drop_Over_30pct'] = daily_revenue['Pct_Change'] < -0.3

# Show flagged days
flagged = daily_revenue[daily_revenue['Flag_Drop_Over_30pct']][['Date', 'Total Revenue', 'Pct_Change']]
print('Days with Revenue Drop > 30% from Previous Day:')
display(flagged)


# %%
# Suggest Reasons for Unit Price * Units Sold Not Equal to Total Revenue
import pandas as pd

df_salesone = pd.read_csv('salesone.csv')
expected_revenue = df_salesone['Unit Price'] * df_salesone['Units Sold']
df_salesone['Revenue_Match'] = abs(df_salesone['Total Revenue'] - expected_revenue) < 1e-2
mismatches = df_salesone[~df_salesone['Revenue_Match']]

if mismatches.empty:
    print('All rows: Unit Price * Units Sold equals Total Revenue (within rounding tolerance).')
else:
    print('Rows where Unit Price * Units Sold does NOT equal Total Revenue:')
    display(mismatches[['Date', 'Product', 'Region', 'Units Sold', 'Unit Price', 'Total Revenue']])
    print('\nPossible reasons for mismatch:')
    print('- Discounts or promotions applied to sales')
    print('- Returns or refunds processed')
    print('- Data entry errors or rounding issues')
    print('- Bundled sales or package deals')
    print('- Taxes, fees, or additional charges not reflected in unit price')


# %%
# Heatmap of Product Demand by Region
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_salesone = pd.read_csv('salesone.csv')

# Pivot table: products as columns, regions as rows, values as total units sold
demand_matrix = df_salesone.pivot_table(index='Region', columns='Product', values='Units Sold', aggfunc='sum', fill_value=0)

print('Product Demand (Units Sold) by Region:')
display(demand_matrix)

plt.figure(figsize=(10,6))
sns.heatmap(demand_matrix, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('Heatmap of Product Demand by Region')
plt.ylabel('Region')
plt.xlabel('Product')
plt.tight_layout()
plt.show()


# %%
# Heatmaps of Product Demand by Region: Aggregated by Month and by Revenue
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)
df_salesone['Month'] = df_salesone['Date'].dt.strftime('%b')

# 1. Heatmap: Units Sold by Region and Month
units_month_region = df_salesone.pivot_table(index='Region', columns='Month', values='Units Sold', aggfunc='sum', fill_value=0)
plt.figure(figsize=(10,6))
sns.heatmap(units_month_region, annot=True, fmt='.0f', cmap='Blues')
plt.title('Units Sold by Region and Month')
plt.ylabel('Region')
plt.xlabel('Month')
plt.tight_layout()
plt.show()

# 2. Heatmap: Total Revenue by Region and Product
revenue_region_product = df_salesone.pivot_table(index='Region', columns='Product', values='Total Revenue', aggfunc='sum', fill_value=0)
plt.figure(figsize=(10,6))
sns.heatmap(revenue_region_product, annot=True, fmt='.0f', cmap='Greens')
plt.title('Total Revenue by Region and Product')
plt.ylabel('Region')
plt.xlabel('Product')
plt.tight_layout()
plt.show()


# %%
# Compare Revenue vs Units Sold Over Time Using Dual Axis Plot
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)

# Aggregate daily revenue and units sold
daily = df_salesone.groupby('Date').agg({'Total Revenue': 'sum', 'Units Sold': 'sum'}).sort_index().reset_index()

fig, ax1 = plt.subplots(figsize=(12,6))

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Total Revenue', color=color)
ax1.plot(daily['Date'], daily['Total Revenue'], color=color, marker='o', label='Total Revenue')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Units Sold', color=color)
ax2.plot(daily['Date'], daily['Units Sold'], color=color, marker='s', label='Units Sold')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Revenue vs Units Sold Over Time (Dual Axis)')
fig.tight_layout()
plt.show()


# %%
# Forecast Revenue Using Polynomial Regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Load data
df_salesone = pd.read_csv('salesone.csv', parse_dates=['Date'], dayfirst=True)
df_salesone['Month'] = df_salesone['Date'].dt.to_period('M')
monthly_revenue = df_salesone.groupby('Month')['Total Revenue'].sum().reset_index()
monthly_revenue['MonthNum'] = np.arange(len(monthly_revenue))

# Prepare data for polynomial regression
X = monthly_revenue[['MonthNum']]
y = monthly_revenue['Total Revenue']
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model = LinearRegression().fit(X_poly, y)

# Forecast next 6 months
future_months = np.arange(len(monthly_revenue), len(monthly_revenue)+6)
future_dates = pd.date_range(monthly_revenue['Month'].dt.to_timestamp().max()+pd.offsets.MonthBegin(1), periods=6, freq='MS')
future_X_poly = poly.transform(future_months.reshape(-1,1))
future_revenue = model.predict(future_X_poly)

# Plot actual and forecasted revenue
plt.figure(figsize=(10,5))
plt.plot(monthly_revenue['Month'].astype(str), monthly_revenue['Total Revenue'], marker='o', label='Actual Revenue')
plt.plot(future_dates.strftime('%Y-%m'), future_revenue, marker='x', linestyle='--', color='red', label='Forecasted Revenue (Poly)')
plt.title('Monthly Revenue Forecast (Polynomial Regression)')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Print forecasted revenue values
forecast_df = pd.DataFrame({'Month': future_dates.strftime('%Y-%m'), 'Forecasted Revenue': future_revenue})
print(forecast_df)


# %%
# Estimate Revenue Lost if Units Sold Was Capped Due to Inventory Shortage
import pandas as pd

# Load data
df_salesone = pd.read_csv('salesone.csv')

# Set hypothetical inventory cap per sale (customize as needed)
unit_cap = 100

# Calculate capped units sold and capped revenue
capped_units = df_salesone['Units Sold'].clip(upper=unit_cap)
df_salesone['Capped Revenue'] = capped_units * df_salesone['Unit Price']

# Calculate revenue lost due to cap
revenue_lost = df_salesone['Total Revenue'] - df_salesone['Capped Revenue']
df_salesone['Revenue Lost'] = revenue_lost.clip(lower=0)

total_lost = df_salesone['Revenue Lost'].sum()

print(f"Total Revenue Lost Due to Inventory Cap of {unit_cap} Units per Sale: {total_lost:.2f}")
display(df_salesone[df_salesone['Revenue Lost'] > 0][['Date', 'Product', 'Region', 'Units Sold', 'Unit Price', 'Total Revenue', 'Capped Revenue', 'Revenue Lost']])


# %%
# Suggest Optimal Pricing by Analyzing Price Points Driving Highest Revenue
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_salesone = pd.read_csv('salesone.csv')

# Bin unit prices for each product (bin width can be adjusted)
bin_width = 50
products = df_salesone['Product'].unique()
optimal_prices = []

for product in products:
    prod_df = df_salesone[df_salesone['Product'] == product]
    # Create price bins
    min_price, max_price = prod_df['Unit Price'].min(), prod_df['Unit Price'].max()
    bins = range(int(min_price), int(max_price) + bin_width, bin_width)
    prod_df['Price Bin'] = pd.cut(prod_df['Unit Price'], bins=bins, include_lowest=True)
    # Aggregate revenue by price bin
    bin_revenue = prod_df.groupby('Price Bin')['Total Revenue'].sum().reset_index()
    # Find price bin with highest revenue
    top_bin = bin_revenue.loc[bin_revenue['Total Revenue'].idxmax()]
    optimal_prices.append({'Product': product, 'Optimal Price Range': str(top_bin['Price Bin']), 'Revenue': top_bin['Total Revenue']})
    # Plot for each product
    plt.figure(figsize=(8,4))
    sns.barplot(data=bin_revenue, x='Price Bin', y='Total Revenue', color='skyblue')
    plt.title(f'Revenue by Unit Price Bin for {product}')
    plt.ylabel('Total Revenue')
    plt.xlabel('Unit Price Bin')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Show optimal price ranges
df_optimal = pd.DataFrame(optimal_prices)
print('Suggested Optimal Price Ranges by Product:')
display(df_optimal)


# %% [markdown]
# ## Sales Strategy Insights & Recommendations
# 
# - **Optimize Pricing:** Focus on price ranges that historically drive the highest revenue for each product. Adjust pricing strategies to maximize revenue in these optimal bins.
# - **Monitor Inventory for High Demand:** Products with frequent top 10% sales or those at risk of inventory shortfall should have proactive reorder strategies to avoid lost sales.
# - **Targeted Promotions:** Use monthly and regional demand heatmaps to time and localize promotions, especially in months or regions with lower sales or higher shortfall.
# - **Product Bundling:** Leverage top product combinations by region to create bundled offers that maximize revenue and cross-sell opportunities.
# - **Address Revenue Drops:** Investigate and address days or periods with significant revenue drops (>30%) to identify operational or market issues.
# - **Focus on Most Profitable Products:** Allocate marketing and inventory resources to the most profitable products in each region.
# - **Improve Data Quality:** Regularly audit for missing, inconsistent, or anomalous data to ensure reliable decision-making.
# - **Balance Revenue and Units Sold:** Use dual-axis and efficiency analyses to balance strategies between maximizing revenue and increasing sales volume.
# - **Adjust for Seasonality:** Plan for inventory and promotions around months or days of the week with peak demand or revenue.
# - **Elasticity-Aware Pricing:** Consider demand elasticity when adjusting prices to avoid revenue loss from reduced sales volume.
# 
# _These insights are based on the analyses and visualizations in this notebook. For best results, regularly update your data and revisit these strategies as market conditions change._
# 


