import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💸",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3 {
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

conn = sqlite3.connect(
    "expenses.db",
    check_same_thread=False
)

cursor = conn.cursor()

# -----------------------------
# CREATE TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    payment_method TEXT,
    description TEXT
)
""")

conn.commit()

# -----------------------------
# TITLE
# -----------------------------

st.title("💸 Personal Expense Tracker")

# -----------------------------
# SIDEBAR MENU
# -----------------------------

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Add Expense",
        "View Expenses"
    ]
)

# =====================================================
# ADD EXPENSE
# =====================================================

if menu == "Add Expense":

    st.header("➕ Add New Expense")

    date = st.date_input("Date")

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education"
        ]
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "💵 Cash",
            "📱 UPI",
            "💳 Credit Card",
            "🏦 Bank Transfer",
            "🟢 PhonePe",
            "🔵 Google Pay"
        ]
    )

    description = st.text_input("Description")

    # SAVE BUTTON

    if st.button("Save Expense"):

        cursor.execute(
            """
            INSERT INTO expenses
            (date, category, amount, payment_method, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(date),
                category,
                amount,
                payment_method,
                description
            )
        )

        conn.commit()

        st.success("✅ Expense Added Successfully")

# =====================================================
# VIEW EXPENSES
# =====================================================

elif menu == "View Expenses":

    st.header("📋 Expense Records")

    # DELETE ALL RECORDS

    if st.button("🗑 Delete All Records"):

        cursor.execute("DELETE FROM expenses")

        conn.commit()

        st.success("All Records Deleted Successfully")

        st.rerun()

    # LOAD DATA

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    st.dataframe(df)

    # DOWNLOAD CSV

    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name="expenses.csv",
        mime="text/csv"
    )

# =====================================================
# DASHBOARD
# =====================================================

elif menu == "Dashboard":

    st.header("📊 Expense Dashboard")

    # LOAD DATA

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    if len(df) == 0:

        st.warning("No data available")

    else:

        # -----------------------------
        # KPI METRICS
        # -----------------------------

        total_expense = df["amount"].sum()

        average_expense = df["amount"].mean()

        top_category = (
            df.groupby("category")["amount"]
            .sum()
            .idxmax()
        )

        monthly_budget = 15000

        savings = monthly_budget - total_expense

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "💰 Total Expense",
            f"₹{total_expense:,.0f}"
        )

        c2.metric(
            "📈 Average Expense",
            f"₹{average_expense:,.0f}"
        )

        c3.metric(
            "🏆 Top Category",
            top_category
        )

        c4.metric(
            "💵 Estimated Savings",
            f"₹{savings:,.0f}"
        )

        # -----------------------------
        # BUDGET ALERT
        # -----------------------------

        if total_expense > monthly_budget:

            st.error(
                "⚠ Monthly Budget Exceeded!"
            )

        else:

            st.success(
                "✅ Budget Under Control"
            )

        # -----------------------------
        # FILTER
        # -----------------------------

        selected_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(df["category"].unique())
        )

        if selected_category != "All":

            filtered_df = df[
                df["category"] == selected_category
            ]

        else:

            filtered_df = df

        # -----------------------------
        # CATEGORY BAR CHART
        # -----------------------------

        category_data = (
            filtered_df.groupby("category")["amount"]
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            category_data,
            x="category",
            y="amount",
            color="category",
            title="Category-wise Spending"
        )

        st.plotly_chart(
            fig1,
            width="stretch"
        )

        # -----------------------------
        # PAYMENT METHOD PIE CHART
        # -----------------------------

        payment_data = (
            filtered_df.groupby("payment_method")["amount"]
            .sum()
            .reset_index()
        )

        fig2 = px.pie(
            payment_data,
            names="payment_method",
            values="amount",
            title="Payment Method Distribution"
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

        # -----------------------------
        # DAILY TREND LINE CHART
        # -----------------------------

        trend_data = (
            filtered_df.groupby("date")["amount"]
            .sum()
            .reset_index()
        )

        fig3 = px.line(
            trend_data,
            x="date",
            y="amount",
            markers=True,
            title="Daily Expense Trend"
        )

        st.plotly_chart(
            fig3,
            width="stretch"
        )

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
    "### ✅ Built using Python, Streamlit, SQLite & Plotly"
)