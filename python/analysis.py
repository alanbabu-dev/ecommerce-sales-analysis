import pandas as pd

# Load the cleaned e-commerce dataset
df = pd.read_csv("dataset/cleaned/ecommerce_sales_cleaned.csv")

# Display first 5 records
print("FIRST 5 RECORDS")
print(df.head())

# Display dataset dimensions
print("\nDATASET SHAPE")
print(df.shape)

# Display column names
print("\nCOLUMN NAMES")
print(df.columns)

# Check column names and data types
print("\nDATASET INFORMATION")
df.info()

# Count missing values in each column
print("\nMISSING VALUES")
print(df.isnull().sum())

# Statistical summary of numerical columns
print("\nSTATISTICAL SUMMARY")
print(df.describe())


# Convert OrderDate from string to datetime
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# Check the new data type
print("\nUPDATED ORDER DATE TYPE")
print(df["OrderDate"].dtype)



# Count duplicate rows
duplicate_count = df.duplicated().sum()

print("\nDUPLICATE RECORDS")
print("Total duplicates:", duplicate_count)



# DATA VALIDATION

print("\nDATA VALIDATION")

# Check for zero or negative quantities
print(
    "Invalid quantities:",
    (df["Quantity"] <= 0).sum()
)

# Check for zero or negative prices
print(
    "Invalid prices:",
    (df["UnitPrice"] <= 0).sum()
)

# Check for discounts outside 0% to 100%
print(
    "Invalid discounts:",
    ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
)



# CATEGORICAL DATA VALIDATION

print("\nUNIQUE VALUES IN CATEGORICAL COLUMNS")

categorical_columns = [
    "Gender",
    "PaymentMethod",
    "Region",
    "OrderStatus",
    "Category"
]

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].unique())



# REVENUE ANALYSIS

# Calculate revenue for every transaction
df["Revenue"] = (
    df["Quantity"]
    * df["UnitPrice"]
    * (1 - df["Discount"])
)

# Select only delivered orders
delivered_sales = df[
    df["OrderStatus"] == "Delivered"
]

# Calculate total revenue
total_revenue = delivered_sales["Revenue"].sum()

print("\nREVENUE ANALYSIS")
print("Total Revenue:", round(total_revenue, 2))



# REVENUE BY PRODUCT

product_revenue = (
    delivered_sales
    .groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nREVENUE BY PRODUCT")
print(product_revenue.round(2))



# REVENUE BY REGION

region_revenue = (
    delivered_sales
    .groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nREVENUE BY REGION")
print(region_revenue.round(2))


# MONTHLY REVENUE ANALYSIS

monthly_revenue = (
    delivered_sales
    .groupby(delivered_sales["OrderDate"].dt.month)["Revenue"]
    .sum()
    .sort_index()
)

print("\nMONTHLY REVENUE")
print(monthly_revenue.round(2))



# MONTH-OVER-MONTH REVENUE GROWTH

monthly_growth = monthly_revenue.pct_change() * 100

print("\nMONTHLY REVENUE GROWTH")
print(monthly_growth.round(2))


# TOP 10 CUSTOMERS BY REVENUE

customer_analysis = (
    delivered_sales
    .groupby("CustomerID")
    .agg(
        Total_Orders=("OrderID", "nunique"),
        Total_Revenue=("Revenue", "sum")
    )
    .sort_values("Total_Revenue", ascending=False)
    .head(10)
)

print("\nTOP 10 CUSTOMERS")
print(customer_analysis.round(2))



# REVENUE BY CATEGORY

category_revenue = (
    delivered_sales
    .groupby("Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nREVENUE BY CATEGORY")
print(category_revenue.round(2))



# AVERAGE ORDER VALUE (AOV)

total_orders = delivered_sales["OrderID"].nunique()
total_revenue = delivered_sales["Revenue"].sum()

average_order_value = total_revenue / total_orders

print("\nAVERAGE ORDER VALUE")
print("Total Orders:", total_orders)
print("Total Revenue:", round(total_revenue, 2))
print("Average Order Value:", round(average_order_value, 2))



# ORDER STATUS ANALYSIS

status_analysis = (
    df["OrderStatus"]
    .value_counts()
)

print("\nORDER STATUS ANALYSIS")
print(status_analysis)

print("\nORDER STATUS PERCENTAGE")
print(
    (df["OrderStatus"].value_counts(normalize=True) * 100)
    .round(2)
)


# PAYMENT METHOD ANALYSIS

payment_analysis = (
    delivered_sales["PaymentMethod"]
    .value_counts()
)

print("\nPAYMENT METHOD ANALYSIS")
print(payment_analysis)


# FINAL DATA QUALITY CHECK

print("\nFINAL DATA QUALITY CHECK")

print("Total records:", len(df))
print("Duplicate records:", df.duplicated().sum())
print("Missing values:")
print(df.isnull().sum())

print("\nRevenue validation")
print("Total delivered orders:", delivered_sales["OrderID"].nunique())
print("Total delivered revenue:", round(delivered_sales["Revenue"].sum(), 2))



# EXPORT ANALYSIS RESULTS FOR POWER BI

import os

# Create output folder if it doesn't exist
os.makedirs("python/outputs", exist_ok=True)

# 1. Delivered sales with calculated revenue
delivered_sales.to_csv(
    "python/outputs/delivered_sales.csv",
    index=False
)

# 2. Product revenue
product_revenue.to_csv(
    "python/outputs/product_revenue.csv"
)

# 3. Regional revenue
region_revenue.to_csv(
    "python/outputs/region_revenue.csv"
)

# 4. Monthly revenue
monthly_revenue.to_csv(
    "python/outputs/monthly_revenue.csv"
)

# 5. Monthly growth
monthly_growth.to_csv(
    "python/outputs/monthly_growth.csv"
)

# 6. Customer analysis
customer_analysis.to_csv(
    "python/outputs/top_customers.csv"
)

# 7. Category revenue
category_revenue.to_csv(
    "python/outputs/category_revenue.csv"
)

# 8. Order status
status_analysis.to_csv(
    "python/outputs/order_status.csv"
)

# 9. Payment method
payment_analysis.to_csv(
    "python/outputs/payment_analysis.csv"
)

print("\nALL ANALYSIS FILES EXPORTED SUCCESSFULLY!")
