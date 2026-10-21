
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
import uuid

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).with_name("transactions.csv")
BUDGET_FILE = Path(__file__).with_name("budget.txt")

CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills", "Education",
    "Health", "Entertainment", "Travel", "Salary",
    "Freelance", "Gift", "Other"
]

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
html, body, [class*="st-"] {
    font-size: 18px !important;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    font-size: 38px !important;
    color: #17365D !important;
}
h2 {
    font-size: 30px !important;
    color: #17365D !important;
}
h3 {
    font-size: 24px !important;
    color: #17365D !important;
}
p, label, li, .stMarkdown {
    font-size: 18px !important;
    line-height: 1.6 !important;
}
.stButton button, .stFormSubmitButton button {
    font-size: 18px !important;
    min-height: 45px;
    font-weight: 600;
}
[data-testid="stMetricValue"] {
    font-size: 28px !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATA STORAGE ----------------
def load_transactions():
    columns = [
        "id", "date", "type", "category", "amount", "description"
    ]

    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)

            for column in columns:
                if column not in df.columns:
                    df[column] = ""

            df = df[columns]
            df["amount"] = pd.to_numeric(
                df["amount"], errors="coerce"
            ).fillna(0)

            df["date"] = pd.to_datetime(
                df["date"], errors="coerce"
            ).dt.date

            return df.dropna(subset=["date"])

        except (OSError, ValueError, pd.errors.ParserError):
            st.error("Unable to read transactions.csv.")
    
    return pd.DataFrame(columns=columns)


def save_transactions(df):
    df.to_csv(DATA_FILE, index=False)


def load_budget():
    if BUDGET_FILE.exists():
        try:
            return max(
                1.0,
                float(BUDGET_FILE.read_text(encoding="utf-8"))
            )
        except (ValueError, OSError):
            pass
    return 5000.0


def save_budget(amount):
    BUDGET_FILE.write_text(str(float(amount)), encoding="utf-8")


def currency(amount):
    return f"₹{amount:,.2f}"


def get_totals(df):
    income = df.loc[df["type"] == "Income", "amount"].sum()
    expenses = df.loc[df["type"] == "Expense", "amount"].sum()
    return float(income), float(expenses), float(income - expenses)


if "transactions" not in st.session_state:
    st.session_state.transactions = load_transactions()

if "budget" not in st.session_state:
    st.session_state.budget = load_budget()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("💰 Expense Tracker")
    st.write("Track your money easily.")
    st.divider()

    page = st.radio(
        "Select a Page",
        [
            "Dashboard",
            "Add Transaction",
            "Transaction History",
            "Budget Settings"
        ]
    )

    st.divider()
    st.write("📊 Visual financial tracking")
    st.write("💾 Automatic local CSV storage")
    st.write("🎯 Budget monitoring")
    st.caption("Currency: Indian Rupees (₹)")


# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Smart Expense Tracker")
    st.write(
        "Track income, monitor spending, and visualize "
        "your financial activity with graphs."
    )

    df = st.session_state.transactions.copy()
    income, expenses, balance = get_totals(df)

    # Summary cards
    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total Income", currency(income))
    col2.metric("💸 Total Expenses", currency(expenses))
    col3.metric("💰 Remaining Balance", currency(balance))

    st.divider()

    # GRAPH 1: Income versus expenses
    st.subheader("📊 Income vs Expenses Graph")

    comparison = pd.DataFrame({
        "Type": ["Income", "Expenses"],
        "Amount": [income, expenses]
    }).set_index("Type")

    st.bar_chart(
        comparison,
        y="Amount",
        height=400
    )

    st.caption("Compare the total amount of income and expenses.")

    st.divider()

    # GRAPH 2: Expense category graph
    st.subheader("💸 Spending by Category")

    expense_df = df[df["type"] == "Expense"].copy()

    if not expense_df.empty:
        category_data = (
            expense_df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            category_data,
            height=400
        )
        st.caption("See which categories account for your spending.")
    else:
        st.info(
            "Add expense transactions to display the category graph."
        )

    st.divider()

    # GRAPH 3: Daily transaction trend
    st.subheader("📈 Daily Income and Expense Tracking")

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        daily = (
            df.dropna(subset=["date"])
            .groupby(["date", "type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .sort_index()
        )

        if "Income" not in daily.columns:
            daily["Income"] = 0.0

        if "Expense" not in daily.columns:
            daily["Expense"] = 0.0

        daily = daily.rename(columns={"Expense": "Expenses"})

        st.line_chart(
            daily[["Income", "Expenses"]],
            height=400
        )
        st.caption(
            "Track how recorded income and expenses change by date."
        )
    else:
        st.info(
            "Add transactions on different dates to build your trend graph."
        )

    st.divider()

    # Budget progress
    st.subheader("🎯 Budget Tracking")

    budget = float(st.session_state.budget)
    percentage = expenses / budget * 100 if budget > 0 else 0

    st.write(f"Your expense budget: **{currency(budget)}**")
    st.write(f"Total recorded expenses: **{currency(expenses)}**")

    st.progress(min(percentage / 100, 1.0))
    st.write(f"Budget used: **{percentage:.1f}%**")

    if expenses > budget:
        st.error(
            f"Budget exceeded by {currency(expenses - budget)}."
        )
    elif percentage >= 80:
        st.warning("You have used at least 80% of your budget.")
    else:
        st.success(
            f"Budget remaining: {currency(budget - expenses)}"
        )

    st.caption(
        "The budget compares against all recorded expenses, "
        "not only the current month."
    )

    st.divider()

    # Recent transactions
    st.subheader("🕒 Recent Transactions")

    if not df.empty:
        recent = df.sort_values(
            "date", ascending=False
        ).head(5).copy()

        recent["date"] = recent["date"].astype(str)
        recent["amount"] = recent["amount"].map(currency)

        st.dataframe(
            recent[
                ["date", "type", "category", "amount", "description"]
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "No transactions recorded yet. Select Add Transaction "
            "to begin tracking."
        )


# ---------------- ADD TRANSACTION ----------------
elif page == "Add Transaction":
    st.title("➕ Add Transaction")
    st.write("Enter the information to record your income or expense.")

    with st.form("transaction_form", clear_on_submit=True):
        transaction_type = st.selectbox(
            "Transaction Type",
            ["Expense", "Income"]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=100.0,
            step=10.0,
            format="%.2f"
        )

        category = st.selectbox("Category", CATEGORIES)
        transaction_date = st.date_input(
            "Transaction Date",
            value=date.today()
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Lunch, bus ticket, salary"
        )

        submitted = st.form_submit_button(
            "Save Transaction",
            use_container_width=True
        )

        if submitted:
            transaction = {
                "id": str(uuid.uuid4()),
                "date": transaction_date.isoformat(),
                "type": transaction_type,
                "category": category,
                "amount": float(amount),
                "description": description.strip()
            }

            updated = pd.concat(
                [
                    st.session_state.transactions,
                    pd.DataFrame([transaction])
                ],
                ignore_index=True
            )

            st.session_state.transactions = updated
            save_transactions(updated)

            st.success("Transaction saved successfully!")
            st.rerun()


# ---------------- TRANSACTION HISTORY ----------------
elif page == "Transaction History":
    st.title("📋 Transaction History")
    st.write("Search, filter, download, or delete transactions.")

    df = st.session_state.transactions.copy()

    if df.empty:
        st.info("No transactions available yet.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            type_filter = st.selectbox(
                "Transaction Type",
                ["All", "Income", "Expense"]
            )

        with col2:
            category_options = sorted(
                df["category"].dropna().astype(str).unique().tolist()
            )

            category_filter = st.selectbox(
                "Category",
                ["All"] + category_options
            )

        search_text = st.text_input("Search by description or category")

        filtered = df.copy()

        if type_filter != "All":
            filtered = filtered[filtered["type"] == type_filter]

        if category_filter != "All":
            filtered = filtered[
                filtered["category"] == category_filter
            ]

        if search_text.strip():
            term = search_text.strip()

            matches = (
                filtered["description"].astype(str).str.contains(
                    term, case=False, na=False
                )
                | filtered["category"].astype(str).str.contains(
                    term, case=False, na=False
                )
            )

            filtered = filtered[matches]

        display_df = filtered.copy()
        display_df["date"] = display_df["date"].astype(str)
        display_df["amount"] = display_df["amount"].map(currency)

        st.dataframe(
            display_df[
                ["date", "type", "category", "amount", "description"]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.write(f"Number of transactions: **{len(filtered)}**")

        st.download_button(
            "⬇️ Download Transactions as CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="my_transactions.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()
        st.subheader("🗑️ Delete a Transaction")

        if not filtered.empty:
            ids = filtered["id"].astype(str).tolist()

            selected_id = st.selectbox(
                "Choose a transaction to delete",
                ids,
                format_func=lambda transaction_id: (
                    f"{filtered.loc[filtered['id'].astype(str) == transaction_id, 'date'].iloc[0]} | "
                    f"{filtered.loc[filtered['id'].astype(str) == transaction_id, 'type'].iloc[0]} | "
                    f"{currency(float(filtered.loc[filtered['id'].astype(str) == transaction_id, 'amount'].iloc[0]))}"
                )
            )

            if st.button("Delete Selected Transaction"):
                remaining = st.session_state.transactions[
                    st.session_state.transactions["id"].astype(str)
                    != selected_id
                ].copy()

                st.session_state.transactions = remaining
                save_transactions(remaining)

                st.success("Transaction deleted successfully.")
                st.rerun()


# ---------------- BUDGET SETTINGS ----------------
elif page == "Budget Settings":
    st.title("🎯 Budget Settings")
    st.write("Set a spending limit and monitor your expenses.")

    with st.form("budget_form"):
        new_budget = st.number_input(
            "Total Expense Budget (₹)",
            min_value=1.0,
            value=float(st.session_state.budget),
            step=500.0,
            format="%.2f"
        )

        submitted = st.form_submit_button(
            "Save Budget",
            use_container_width=True
        )

        if submitted:
            st.session_state.budget = float(new_budget)
            save_budget(new_budget)

            st.success("Budget saved successfully!")
            st.rerun()


# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Smart Expense Tracker | Python + Streamlit + Pandas | "
    "Local CSV Storage"
)
