import streamlit as st
import pandas as pd
from models import InvestmentPlatform
import storage
import reports
from config import CURRENCY_SYMBOL

# --- Page Configuration ---
st.set_page_config(
    page_title="Savings Tracker",
    page_icon="💰",
    layout="wide"
)

# --- Load Data ---
# Use Streamlit's session state to keep data loaded across interactions
if 'platforms' not in st.session_state:
    st.session_state.platforms = storage.load_platforms()

def save_data():
    """Helper function to save the current state."""
    storage.save_platforms(st.session_state.platforms)

# --- App Header ---
st.title("💰 Multi-Platform Savings Tracker")
st.markdown("Track your investments, interest, and withdrawals with ease.")

# --- Main Dashboard ---
st.header("Dashboard")

# Create columns for layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Balance")
    total_balance = sum(p.balance for p in st.session_state.platforms.values())
    st.metric(label="All Platforms", value=f"{CURRENCY_SYMBOL} {total_balance:,.2f}")

with col2:
    st.subheader("Platform Overview")
    if st.session_state.platforms:
        # Prepare data for the chart
        platform_names = list(st.session_state.platforms.keys())
        platform_balances = [p.balance for p in st.session_state.platforms.values()]
        chart_data = pd.DataFrame({
            'Balance': platform_balances,
        }, index=platform_names)
        st.bar_chart(chart_data)
    else:
        st.info("No platforms to display. Add one from the sidebar.")

st.markdown("---")


# --- Sidebar for Actions ---
st.sidebar.header("Actions")

# Section: Add New Platform
with st.sidebar.expander("➕ Add New Platform"):
    with st.form("new_platform_form", clear_on_submit=True):
        new_name = st.text_input("Platform Name")
        new_balance = st.number_input("Initial Balance", min_value=0.0, format="%.2f")
        new_rate = st.number_input("Interest Rate (%)", min_value=0.0, format="%.2f")
        
        submitted = st.form_submit_button("Add Platform")
        if submitted and new_name:
            if new_name not in st.session_state.platforms:
                st.session_state.platforms[new_name] = InvestmentPlatform(new_name, new_balance, new_rate)
                save_data()
                st.sidebar.success(f"Platform '{new_name}' added!")
            else:
                st.sidebar.error("Platform already exists.")

# Section: Update Existing Platform
if st.session_state.platforms:
    st.sidebar.subheader("🔄 Update a Platform")
    platform_to_update = st.sidebar.selectbox("Select Platform", options=list(st.session_state.platforms.keys()))
    
    if platform_to_update:
        platform = st.session_state.platforms[platform_to_update]
        
        # Deposit
        with st.sidebar.expander("Deposit Funds"):
            deposit_amount = st.number_input("Deposit Amount", min_value=0.01, format="%.2f", key=f"deposit_{platform_to_update}")
            if st.button("Confirm Deposit", key=f"btn_deposit_{platform_to_update}"):
                platform.deposit(deposit_amount)
                save_data()
                st.success(f"Deposited {CURRENCY_SYMBOL} {deposit_amount:,.2f} to {platform.name}")

        # Withdraw
        with st.sidebar.expander("Withdraw Funds"):
            withdraw_amount = st.number_input("Withdrawal Amount", min_value=0.01, max_value=platform.balance, format="%.2f", key=f"withdraw_{platform_to_update}")
            if st.button("Confirm Withdrawal", key=f"btn_withdraw_{platform_to_update}"):
                platform.withdraw(withdraw_amount)
                save_data()
                st.success(f"Withdrew {CURRENCY_SYMBOL} {withdraw_amount:,.2f} from {platform.name}")

        # Apply Interest
        if st.sidebar.button(f"Apply Interest to {platform.name}", key=f"btn_interest_{platform_to_update}"):
            interest = platform.apply_interest()
            save_data()
            st.success(f"Applied {CURRENCY_SYMBOL} {interest:,.2f} interest to {platform.name}")

st.markdown("---")

# --- Transaction History ---
st.header("Transaction History")

if st.session_state.platforms:
    history_platform = st.selectbox("View history for", options=list(st.session_state.platforms.keys()))
    if history_platform:
        platform = st.session_state.platforms[history_platform]
        if platform.history:
            # Display history in a more structured way
            for record in reversed(platform.history): # Show most recent first
                col1, col2, col3 = st.columns(3)
                col1.text(record['type'])
                col2.text(f"{CURRENCY_SYMBOL} {record['amount']:,.2f}")
                col3.text(f"New Balance: {CURRENCY_SYMBOL} {record['balance']:,.2f}")
        else:
            st.info("No transaction history for this platform yet.")
else:
    st.info("No platforms created yet. Add one from the sidebar to begin.")