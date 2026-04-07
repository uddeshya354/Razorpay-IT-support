import streamlit as st
import pandas as pd
import json
import re
import io
import numpy as np
from scipy.stats import entropy  # Added missing import for user entropy

# --- 1. Define the Mapping Dictionary ---
location_mapping = {
    "THVM": {"City": "Thivim", "State": "Goa"},
    "katpadi": {"City": "Katpadi", "State": "Tamil Nadu"},
    "CHZ": {"City": "Charlapalli", "State": "Telangana"},
    "PUNE": {"City": "Pune", "State": "Maharashtra"},
    "AJMER": {"City": "Ajmer", "State": "Rajasthan"},
    "BSP": {"City": "Bilaspur", "State": "Chhattisgarh"},
    "Visvesvaraya Museum": {"City": "Bengaluru", "State": "Karnataka"},
    "Varanasi": {"City": "Varanasi", "State": "Uttar Pradesh"},
    "Nagpur": {"City": "Nagpur", "State": "Maharashtra"},
    "KRP": {"City": "Krishna Raj Puram", "State": "Bengaluru"},
    "KP": {"City": "Pune", "State": "Maharashtra"},
    "UD": {"City": "Udupi", "State": "Karnataka"},
    "Ludhiana": {"City": "Ludhiana", "State": "Punjab"},
    "Amritsar": {"City": "Amritsar", "State": "Punjab"},
    "Nagapattinam": {"City": "Nagapattinam", "State": "Tamil Nadu"},
    "Hubballi Bus Stand": {"City": "Hubballi", "State": "Karnataka"},
    "Villupuram": {"City": "Villupuram", "State": "Tamil Nadu"},
    "BRC": {"City": "Vadodara", "State": "Gujarat"},
    "RN": {"City": "Ratnagiri", "State": "Maharashtra"},
    "Tiruvannamalai": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
    "GHM": {"City": "Ghoom", "State": "West Bengal"},
    "KSR": {"City": "Bengaluru", "State": "Karnataka"},
    "Melmaruvathur": {"City": "Melmaruvathur", "State": "Tamil Nadu"},
    "Shirdi": {"City": "Shirdi", "State": "Maharashtra"},
    "MMR": {"City": "Manmad", "State": "Maharashtra"},
    "JAM": {"City": "Jamnagar", "State": "Gujarat"},
    "Jasidih": {"City": "Jasidih", "State": "Jharkhand"},
    "Manglore Central K": {"City": "Mangaluru", "State": "Karnataka"},
    "Tirur": {"City": "Tirur", "State": "Kerala"},
    "Kannur": {"City": "Kannur", "State": "Kerala"},
    "CSMT": {"City": "Mumbai", "State": "Maharashtra"},
    "Jalandhar": {"City": "Jalandhar", "State": "Punjab"},
    "SEG": {"City": "Shegaon", "State": "Maharashtra"},
    "Tiruvannamalai Arunachaleswarar Temple": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
    "Ayodhya": {"City": "Ayodhya", "State": "Uttar Pradesh"},
    "Lucknow": {"City": "Lucknow", "State": "Uttar Pradesh"},
    "SANTRAGACHI": {"City": "Howrah", "State": "West Bengal"},
    "Shalimar": {"City": "Howrah", "State": "West Bengal"},
    "Statue of Unity": {"City": "Kevadia", "State": "Gujarat"},
    "Ahmedabad": {"City": "Ahmedabad", "State": "Gujarat"},
    "Kozhikode": {"City": "Kozhikode", "State": "Kerala"}
}
mapping_lower = {k.lower(): v for k, v in location_mapping.items()}

# --- 2. Helper Functions ---
def extract_locker_bank(notes):
    if pd.isna(notes): return ""
    try:
        data = json.loads(notes)
        locker_name = data.get("Locker Bank Name", data.get("lockerBankName", ""))
        if locker_name and locker_name.strip().lower() != "luggage":
            return locker_name
        locker_location = data.get("lockerBankLocation", "")
        if locker_location and locker_location.strip().lower() not in ["", "luggage"]:
            return locker_location
        tenant = data.get("tenant", "")
        if tenant:
            if "http" in tenant:
                match = re.search(r'://([^.]+)\.', tenant)
                if match: return match.group(1)
            else: return tenant
        tenant_url = data.get("Tenant Name", data.get("tenant_host", ""))
        if tenant_url:
            match = re.search(r'://([^.]+)\.', tenant_url)
            if match: return match.group(1)
        return ""
    except:
        return ""

def clean_locker_name(name):
    if not name: return ""
    clean_name = re.sub(r'(?i)\b(luggage|station|railway|temple|junction)\b', '', str(name))
    clean_name = re.sub(r'[- ]+[A-G]$', '', clean_name)
    return clean_name.strip(' -')

# --- 3. Main Processing Logic ---
def process_dataframe(df, backend_df=None):
    if 'payment_notes' not in df.columns:
        st.error("Error: The settlement file does not contain a 'payment_notes' column.")
        return df

    df['Raw_Locker_Bank'] = df['payment_notes'].apply(extract_locker_bank)
    df['Cleaned_Location'] = df['Raw_Locker_Bank'].apply(clean_locker_name)
    df['City'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
    df['State'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))
    
    if backend_df is not None and 'entity_id' in df.columns:
        unknown_mask = df['City'] == "Unknown"
        if unknown_mask.any() and 'Payment ID' in backend_df.columns and 'Locker Bank' in backend_df.columns:
            backend_lookup = backend_df.drop_duplicates(subset=['Payment ID']).set_index('Payment ID')['Locker Bank'].to_dict()
            df.loc[unknown_mask, 'Backend_Raw_Name'] = df.loc[unknown_mask, 'entity_id'].map(backend_lookup)
            df.loc[unknown_mask, 'Backend_Cleaned'] = df.loc[unknown_mask, 'Backend_Raw_Name'].apply(clean_locker_name)
            df.loc[unknown_mask, 'City'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
                lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown") if pd.notna(loc) else "Unknown"
            )
            df.loc[unknown_mask, 'State'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
                lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown") if pd.notna(loc) else "Unknown"
            )
            df = df.drop(columns=['Backend_Raw_Name', 'Backend_Cleaned'], errors='ignore')

    df = df.drop(columns=['Raw_Locker_Bank', 'Cleaned_Location'])
    return df

def generate_backend_analytics(backend_df):
    """Processes backend data for advanced analytics and User RFM inferences"""
    
    # 1. Strip hidden spaces from column names just in case
    backend_df.columns = backend_df.columns.str.strip()
    
    # 2. BULLETPROOF FILTERING: Clean spaces, make lowercase, convert to string safely
    if 'Payment Type' in backend_df.columns:
        mask = backend_df['Payment Type'].astype(str).str.strip().str.lower() == 'payment'
        df_filtered = backend_df[mask].copy()
    else:
        df_filtered = backend_df.copy()
        
    # 3. Force 'Amount' to be a clean number (fixes text-number issues)
    if 'Amount' in df_filtered.columns:
        df_filtered['Amount'] = pd.to_numeric(df_filtered['Amount'], errors='coerce').fillna(0)

    # 4. Map Cities
    if 'Locker Bank' in df_filtered.columns:
        df_filtered['Cleaned_Location'] = df_filtered['Locker Bank'].astype(str).apply(clean_locker_name)
        df_filtered['City'] = df_filtered['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))

    # --- Time of Day Analysis ---
    if 'Date Created' in df_filtered.columns:
        df_filtered['Date Created'] = pd.to_datetime(df_filtered['Date Created'], errors='coerce')
        def get_tod(hour):
            if pd.isna(hour): return 'Unknown'
            if 6 <= hour < 12: return 'Morning (6AM - 12PM)'
            elif 12 <= hour < 18: return 'Afternoon (12PM - 6PM)'
            else: return 'Night (6PM - 6AM)'
        
        df_filtered['Time_of_Day'] = df_filtered['Date Created'].dt.hour.apply(get_tod)
        time_dist = df_filtered['Time_of_Day'].value_counts(normalize=True).reset_index()
        time_dist.columns = ['Time of Day', 'Percentage']
        time_dist['Percentage'] = (time_dist['Percentage'] * 100).round(2).astype(str) + '%'
    else:
        time_dist = pd.DataFrame()

    # --- Location Performance ---
    def calc_entropy(series):
        counts = series.value_counts(normalize=True)
        return -(counts * np.log2(counts)).sum()

    if 'Locker Bank' in df_filtered.columns and 'Amount' in df_filtered.columns:
        loc_rev = df_filtered.groupby('Locker Bank')['Amount'].agg(
            Total_Revenue='sum',
            Total_Transactions='count',
            AOV='mean',
            Revenue_Std_Dev='std'
        ).reset_index()
        
        loc_rev['Total_Revenue'] = loc_rev['Total_Revenue'].round(2)
        loc_rev['AOV'] = loc_rev['AOV'].round(2)
        loc_rev['Revenue_Std_Dev'] = loc_rev['Revenue_Std_Dev'].fillna(0).round(2)
        loc_rev = loc_rev.sort_values(by='Total_Revenue', ascending=False)
        
        if 'Locker Size' in df_filtered.columns:
            entropy_df = df_filtered.groupby('Locker Bank')['Locker Size'].apply(calc_entropy).reset_index(name='Size Entropy')
            loc_rev = pd.merge(loc_rev, entropy_df, on='Locker Bank', how='left')
            loc_rev['Size Entropy'] = loc_rev['Size Entropy'].round(3)
            
            bank_sizes = pd.crosstab(df_filtered['Locker Bank'], df_filtered['Locker Size'], normalize='index') * 100
            bank_sizes = bank_sizes.round(2).astype(str) + '%'
            bank_sizes.columns = [f"% {col}" for col in bank_sizes.columns]
            bank_sizes = bank_sizes.reset_index()
            
            loc_rev = pd.merge(loc_rev, bank_sizes, on='Locker Bank', how='left')
    else:
        loc_rev = pd.DataFrame()

    # --- City Revenue ---
    if 'City' in df_filtered.columns and 'Amount' in df_filtered.columns:
        city_rev = df_filtered.groupby('City')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False)
    else:
        city_rev = pd.DataFrame()

    # --- User Behavior & Cohort Inferences ---
    user_df = pd.DataFrame()
    repeat_users = pd.DataFrame()
    
    if 'User Mobile' in df_filtered.columns and 'Date Updated' in df_filtered.columns:
        df_users = df_filtered.dropna(subset=['Date Updated', 'User Mobile']).copy()
        
        if not df_users.empty:
            df_users['date_only'] = df_users['Date Updated'].dt.date
            
            user_df = df_users.groupby('User Mobile').agg(
                total_transactions=('Reference Id', 'count') if 'Reference Id' in df_users.columns else ('Amount', 'count'),
                active_days=('date_only', 'nunique'),
                first_usage=('Date Updated', 'min'),
                last_usage=('Date Updated', 'max'),
                total_amount=('Amount', 'sum')
            ).reset_index()

            repeat_users = user_df[
                (user_df['total_transactions'] >= 2) & 
                (user_df['active_days'] >= 2)
            ].copy().sort_values('total_transactions', ascending=False)
            
            if 'Locker Size' in df_users.columns:
                size_map = {'Medium': 'M', 'Large': 'L', 'Extra Large': 'XL'}
                df_users['size_clean'] = df_users['Locker Size'].map(size_map).fillna('unknown')
                
                size_counts = df_users.groupby(['User Mobile', 'size_clean']).size().unstack(fill_value=0)
                size_pct = size_counts.div(size_counts.sum(axis=1), axis=0).fillna(0) * 100
                size_pct = size_pct.rename(columns={'M': 'pct_M', 'L': 'pct_L', 'XL': 'pct_XL'})
                
                user_df = user_df.merge(size_pct, left_on='User Mobile', right_index=True, how='left').fillna(0)
                
                size_cols = [c for c in ['pct_M', 'pct_L', 'pct_XL'] if c in user_df.columns]
                if size_cols:
                    user_df['dominant_size'] = user_df[size_cols].idxmax(axis=1).str.replace('pct_', '')
                    user_df['size_entropy'] = user_df[size_cols].apply(
                        lambda row: entropy(row.values / 100) if row.sum() > 0 else 0.0, axis=1
                    ).round(3)

    return loc_rev, city_rev, time_dist, user_df, repeat_users
    # --- 4. Streamlit UI ---
st.set_page_config(page_title="Locker Analytics Processor", layout="wide")

st.title("🧳 Locker Data Processor & Analytics")

tab1, tab2 = st.tabs(["⚙️ Data Processing", "📊 Advanced Analytics Dashboard"])

with tab1:
    st.write("Upload files to map missing locations and generate reports.")
    col1, col2 = st.columns(2)
    with col1:
        settlement_file = st.file_uploader("1. Upload Settlement .xlsx/.csv", type=['xlsx', 'csv'], key="settlement")
    with col2:
        backend_file = st.file_uploader("2. Upload Backend .xlsx/.csv (For mapping & analytics)", type=['xlsx', 'csv'], key="backend")

    if settlement_file is not None:
        try:
            df = pd.read_csv(settlement_file) if settlement_file.name.endswith('.csv') else pd.read_excel(settlement_file)
            backend_df = None
            loc_rev, city_rev, time_dist, user_df, repeat_users = None, None, None, pd.DataFrame(), pd.DataFrame()

            if backend_file is not None:
                backend_df = pd.read_csv(backend_file) if backend_file.name.endswith('.csv') else pd.read_excel(backend_file)
                # Catching all 5 variables safely!
                loc_rev, city_rev, time_dist, user_df, repeat_users = generate_backend_analytics(backend_df)
                st.success("Backend data loaded. Missing locations cross-referenced and Analytics generated!")
            
            processed_df = process_dataframe(df, backend_df)
            
            st.write("### Processed Data Preview")
            st.dataframe(processed_df[['entity_id', 'payment_notes', 'City', 'State']].head())
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
                
                if backend_file is not None:
                    loc_rev.to_excel(writer, index=False, sheet_name='Bank_Performance')
                    city_rev.to_excel(writer, index=False, sheet_name='Revenue_By_City')
                    time_dist.to_excel(writer, index=False, sheet_name='Time_of_Day_Stats')
                    
                    if not user_df.empty:
                        user_df.to_excel(writer, index=False, sheet_name='All_User_Analytics')
                        repeat_users.to_excel(writer, index=False, sheet_name='Top_Repeat_Users')

            st.download_button(
                label="📥 Download Advanced Multi-Sheet Report",
                data=output.getvalue(),
                file_name=f"Advanced_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

with tab2:
    if backend_file is None:
        st.info("👈 Please upload the Backend Data file in the 'Data Processing' tab to view analytics.")
    else:
        st.subheader("📊 Backend Operations Insights")
        st.write("*Note: Filtering for rows where `Payment Type` = 'Payment'*")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("### 🕒 Bookings by Time of Day")
            st.dataframe(time_dist, use_container_width=True)
            
        with c2:
            st.write("### 🏙️ Revenue by City")
            st.dataframe(city_rev, use_container_width=True)
            
        st.markdown("---")
        st.write("### 📍 Location Performance: Revenue, Entropy & Size Distribution")
        st.caption("This table breaks down total revenue, AOV, Standard Deviation, and exact percentage of M, L, XL locker bookings for **each individual location**.")
        st.dataframe(loc_rev, use_container_width=True)
        
        st.markdown("---")
        st.subheader("👥 User Behavior & Cohort Inferences")
        
        if not user_df.empty:
            total_users = len(user_df)
            total_repeat = len(repeat_users)
            repeat_rate = (total_repeat / total_users) * 100 if total_users > 0 else 0
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Unique Users", f"{total_users}")
            kpi2.metric("Highly Loyal Users (≥2 bookings)", f"{total_repeat}")
            kpi3.metric("Customer Retention Rate", f"{repeat_rate:.1f}%")
            
            st.write("### 🏆 Top Repeat Customers Profile")
            st.caption("These are your most valuable users. High 'Size Entropy' indicates they use multiple locker sizes depending on their needs.")
            
            display_cols = ['User Mobile', 'total_transactions', 'active_days', 'total_amount']
            if 'dominant_size' in user_df.columns:
                display_cols.extend(['dominant_size', 'size_entropy'])
                
            st.dataframe(repeat_users[display_cols].head(15), use_container_width=True)
        else:
            st.warning("Not enough user data to generate cohort inferences.")