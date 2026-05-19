from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)
Path("outputs/charts").mkdir(parents=True, exist_ok=True)
Path("reports").mkdir(parents=True, exist_ok=True)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
import os


# -----------------------------
# SYNTHETIC DATASET CREATION
# -----------------------------

categories = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education"
]

payment_methods = [
    "Cash",
    "UPI",
    "Card",
    "Net Banking"
]

descriptions = [
    "Lunch",
    "Uber Ride",
    "Amazon Purchase",
    "Electricity Bill",
    "Movie Ticket",
    "Medicine",
    "Books"
]

data = []

start_date = datetime(2026, 1, 1)

for i in range(200):

    date = start_date + timedelta(days=random.randint(0, 120))

    category = random.choice(categories)

    amount = random.randint(100, 5000)

    payment = random.choice(payment_methods)

    note = random.choice(descriptions)

    data.append([
        date.strftime("%Y-%m-%d"),
        category,
        amount,
        payment,
        note
    ])

df = pd.DataFrame(data, columns=[
    "Date",
    "Category",
    "Amount",
    "Payment_Method",
    "Description"
])

# Save dataset
df.to_csv("data/expenses.csv", index=False)

print("Synthetic dataset created.")

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("data/expenses.csv")

print("\nDataset Preview:")
print(df.head())

# -----------------------------
# DATA CLEANING
# -----------------------------

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.to_period("M")

# -----------------------------
# CATEGORY ANALYSIS
# -----------------------------

category_expense = df.groupby("Category")["Amount"].sum()

print("\nCategory-wise Expense:")
print(category_expense)

highest_category = category_expense.idxmax()

print(f"\nHighest Spending Category: {highest_category}")

# -----------------------------
# MONTHLY ANALYSIS
# -----------------------------

monthly_expense = df.groupby("Month")["Amount"].sum()

print("\nMonthly Expense:")
print(monthly_expense)

# -----------------------------
# PAYMENT METHOD ANALYSIS
# -----------------------------

payment_analysis = df.groupby("Payment_Method")["Amount"].sum()

print("\nPayment Method Analysis:")
print(payment_analysis)

# -----------------------------
# DAILY SPENDING
# -----------------------------

daily_spending = df.groupby("Date")["Amount"].sum()

average_daily = daily_spending.mean()

print(f"\nAverage Daily Spending: ₹{average_daily:.2f}")

# -----------------------------
# VISUALIZATIONS
# -----------------------------

sns.set_style("whitegrid")

# CATEGORY BAR CHART
plt.figure(figsize=(10,6))
category_expense.plot(kind='bar')
plt.title("Category-wise Spending")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("outputs/charts/category_bar_chart.png")
plt.close()

# MONTHLY LINE CHART
plt.figure(figsize=(10,6))
monthly_expense.plot(kind='line', marker='o')
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("outputs/charts/monthly_trend_chart.png")
plt.close()

# PAYMENT METHOD PIE CHART
plt.figure(figsize=(8,8))
payment_analysis.plot(kind='pie', autopct='%1.1f%%')
plt.title("Payment Method Analysis")
plt.ylabel("")
plt.tight_layout()
plt.savefig("outputs/charts/payment_pie_chart.png")
plt.close()

# DAILY SPENDING TREND
plt.figure(figsize=(12,6))
daily_spending.plot()
plt.title("Daily Spending Trend")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("outputs/charts/daily_spending_chart.png")
plt.close()

print("\nCharts generated successfully.")

# -----------------------------
# REPORT GENERATION
# -----------------------------

summary_report = pd.DataFrame({
    "Metric": [
        "Total Spending",
        "Average Daily Spending",
        "Highest Spending Category"
    ],
    "Value": [
        df["Amount"].sum(),
        round(average_daily, 2),
        highest_category
    ]
})

summary_report.to_csv(
    "reports/monthly_summary_report.csv",
    index=False
)

print("\nReport generated successfully.")

print("\nPROJECT EXECUTION COMPLETED.")