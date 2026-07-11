import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import numpy as np
import seaborn as sns

# ----------------------------------------------------------
# DATABASE CONNECTION
# ----------------------------------------------------------

engine = create_engine(
    "mysql+pymysql://root:saro20@localhost/ecommerce"
)

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_sql(
    "SELECT * FROM ecommerce_sales",
    engine
)

# ----------------------------------------------------------
# BASIC INFORMATION
# ----------------------------------------------------------

print("\nFIRST 5 RECORDS")
print(df.head())

print("\nLAST 5 RECORDS")
print(df.tail())

print("\nDATASET SHAPE")
print(df.shape)

print(f"\nRows : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATA TYPES")
print(df.dtypes)

print("\nDATASET INFO")
df.info()

print("\nSTATISTICAL SUMMARY")
print(df.describe())

# ----------------------------------------------------------
# MISSING VALUES
# ----------------------------------------------------------

print("\nMISSING VALUES")
print(df.isnull().sum())

# ----------------------------------------------------------
# DUPLICATES
# ----------------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDUPLICATE RECORDS")
print(duplicates)

# ----------------------------------------------------------
# DATE CONVERSION
# ----------------------------------------------------------

df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# ----------------------------------------------------------
# FEATURE ENGINEERING
# ----------------------------------------------------------

df['Year'] = df['Order_Date'].dt.year
df['Month'] = df['Order_Date'].dt.month
df['Month_Name'] = df['Order_Date'].dt.month_name()
df['Day'] = df['Order_Date'].dt.day

df['Profit_Margin'] = (
    df['Profit'] / df['Sales']
) * 100

print("\nFEATURE ENGINEERING COMPLETED")

# ----------------------------------------------------------
# UNIQUE VALUES
# ----------------------------------------------------------

print("\nUNIQUE CATEGORIES")
print(df['Category'].unique())

print("\nUNIQUE REGIONS")
print(df['Region'].unique())

# ----------------------------------------------------------
# BEST SELLING PRODUCTS
# ----------------------------------------------------------

best_products = (
    df.groupby('Product_Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 BEST SELLING PRODUCTS")
print(best_products)

# ----------------------------------------------------------
# REGION PROFIT
# ----------------------------------------------------------

region_profit = (
    df.groupby('Region')['Profit']
    .sum()
    .sort_values(ascending=False)
)

print("\nPROFIT BY REGION")
print(region_profit)

# ----------------------------------------------------------
# CATEGORY PERFORMANCE
# ----------------------------------------------------------

category_sales = (
    df.groupby('Category')['Sales']
    .sum()
    .sort_values(ascending=False)
)

print("\nCATEGORY PERFORMANCE")
print(category_sales)

# ----------------------------------------------------------
# MONTHLY SALES TREND
# ----------------------------------------------------------

monthly_sales = (
    df.groupby('Month_Name')['Sales']
    .sum()
)

print("\nMONTHLY SALES")
print(monthly_sales)

# ----------------------------------------------------------
# VISUALIZATION 1
# ----------------------------------------------------------

plt.figure(figsize=(8,5))
plt.hist(df['Sales'], bins=20)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.show()

# ----------------------------------------------------------
# VISUALIZATION 2
# ----------------------------------------------------------

best_products.plot(kind='bar', figsize=(10,5))
plt.title("Top 10 Best Selling Products")
plt.ylabel("Sales")
plt.show()

# ----------------------------------------------------------
# VISUALIZATION 3
# ----------------------------------------------------------

region_profit.plot(kind='bar', figsize=(8,5))
plt.title("Profit by Region")
plt.ylabel("Profit")
plt.show()

print("\nPROJECT ANALYSIS COMPLETED SUCCESSFULLY")

plt.figure(figsize=(8,5))
plt.hist(df['Profit'], bins=20)
plt.title("Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Frequency")
plt.show()

# ----------------------------------------------------------
# 17. CATEGORY-WISE SALES
# ----------------------------------------------------------

category_sales = (
    df.groupby('Category')['Sales']
      .sum()
      .sort_values(ascending=False)
)

print("\nCATEGORY SALES")
print(category_sales)

plt.figure(figsize=(8,5))
category_sales.plot(kind='bar')
plt.title("Category Wise Sales")
plt.ylabel("Sales")
plt.show()

# ----------------------------------------------------------
# 18. REGION-WISE PROFIT
# ----------------------------------------------------------

region_profit = (
    df.groupby('Region')['Profit']
      .sum()
      .sort_values(ascending=False)
)

print("\nREGION PROFIT")
print(region_profit)

plt.figure(figsize=(8,5))
region_profit.plot(kind='bar')
plt.title("Region Wise Profit")
plt.ylabel("Profit")
plt.show()

# ----------------------------------------------------------
# 19. TOP 10 PRODUCTS
# ----------------------------------------------------------

top_products = (
    df.groupby('Product_Name')['Sales']
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\nTOP PRODUCTS")
print(top_products)

plt.figure(figsize=(10,5))
top_products.plot(kind='bar')
plt.title("Top 10 Products")
plt.ylabel("Sales")
plt.show()

# ----------------------------------------------------------
# 20. MONTHLY SALES TREND
# ----------------------------------------------------------

monthly_sales = (
    df.groupby(['Year','Month_Name'])['Sales']
      .sum()
      .reset_index()
)

print("\nMONTHLY SALES TREND")
print(monthly_sales)

# ----------------------------------------------------------
# 21. CORRELATION MATRIX
# ----------------------------------------------------------

numeric_df = df.select_dtypes(include=np.number)

corr_matrix = numeric_df.corr()

print("\nCORRELATION MATRIX")
print(corr_matrix)

plt.figure(figsize=(10,6))
sns.heatmap(
    corr_matrix,
    annot=True
)
plt.title("Correlation Heatmap")
plt.show()

# ----------------------------------------------------------
# 22. OUTLIER DETECTION
# ----------------------------------------------------------

plt.figure(figsize=(8,5))
sns.boxplot(x=df['Sales'])
plt.title("Sales Outliers")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x=df['Profit'])
plt.title("Profit Outliers")
plt.show()

# ----------------------------------------------------------
# 23. BUSINESS INSIGHTS
# ----------------------------------------------------------

print("\nBUSINESS INSIGHTS")

print(
    "Highest Sales Category :",
    category_sales.idxmax()
)

print(
    "Most Profitable Region :",
    region_profit.idxmax()
)

print(
    "Best Selling Product :",
    top_products.index[0]
)

# ----------------------------------------------------------
# 24. SAVE CLEANED DATASET
# ----------------------------------------------------------

df.to_csv(
    "ecommerce_sales_cleaned.csv",
    index=False
)

print("Cleaned Dataset Saved")

import os

print(os.getcwd())


df.to_sql(
    name='ecommerce_sales_cleaned',
    con=engine,
    if_exists='replace',
    index=False
)

print("✅ Cleaned dataset stored in MySQL successfully!")
