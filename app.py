# # import streamlit as st
# # import pandas as pd
# # import json
# # import re
# # import io
# # import numpy as np
# # from scipy.stats import entropy
# # import holidays
# # # import pulp
# # # --- 1. Define the Mapping Dictionaries ---
# # location_mapping = {
# #     "THVM": {"City": "Thivim", "State": "Goa"},
# #     "katpadi": {"City": "Katpadi", "State": "Tamil Nadu"},
# #     "CHZ": {"City": "Charlapalli", "State": "Telangana"},
# #     "PUNE": {"City": "Pune", "State": "Maharashtra"},
# #     "AJMER": {"City": "Ajmer", "State": "Rajasthan"},
# #     "BSP": {"City": "Bilaspur", "State": "Chhattisgarh"},
# #     "Visvesvaraya Museum": {"City": "Bengaluru", "State": "Karnataka"},
# #     "Varanasi": {"City": "Varanasi", "State": "Uttar Pradesh"},
# #     "Nagpur": {"City": "Nagpur", "State": "Maharashtra"},
# #     "KRP": {"City": "Krishna Raj Puram", "State": "Karnataka"},
# #     "KP": {"City": "Pune", "State": "Maharashtra"},
# #     "UD": {"City": "Udupi", "State": "Karnataka"},
# #     "Ludhiana": {"City": "Ludhiana", "State": "Punjab"},
# #     "Amritsar": {"City": "Amritsar", "State": "Punjab"},
# #     "Nagapattinam": {"City": "Nagapattinam", "State": "Tamil Nadu"},
# #     "Hubballi Bus Stand": {"City": "Hubballi", "State": "Karnataka"},
# #     "Villupuram": {"City": "Villupuram", "State": "Tamil Nadu"},
# #     "BRC": {"City": "Vadodara", "State": "Gujarat"},
# #     "RN": {"City": "Ratnagiri", "State": "Maharashtra"},
# #     "Tiruvannamalai": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
# #     "GHM": {"City": "Ghoom", "State": "West Bengal"},
# #     "KSR": {"City": "Bengaluru", "State": "Karnataka"},
# #     "Melmaruvathur": {"City": "Melmaruvathur", "State": "Tamil Nadu"},
# #     "Shirdi": {"City": "Shirdi", "State": "Maharashtra"},
# #     "MMR": {"City": "Manmad", "State": "Maharashtra"},
# #     "JAM": {"City": "Jamnagar", "State": "Gujarat"},
# #     "Jasidih": {"City": "Jasidih", "State": "Jharkhand"},
# #     "Manglore Central K": {"City": "Mangaluru", "State": "Karnataka"},
# #     "Tirur": {"City": "Tirur", "State": "Kerala"},
# #     "Kannur": {"City": "Kannur", "State": "Kerala"},
# #     "CSMT": {"City": "Mumbai", "State": "Maharashtra"},
# #     "Jalandhar": {"City": "Jalandhar", "State": "Punjab"},
# #     "SEG": {"City": "Shegaon", "State": "Maharashtra"},
# #     "Tiruvannamalai Arunachaleswarar Temple": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
# #     "Ayodhya": {"City": "Ayodhya", "State": "Uttar Pradesh"},
# #     "Lucknow": {"City": "Lucknow", "State": "Uttar Pradesh"},
# #     "SANTRAGACHI": {"City": "Howrah", "State": "West Bengal"},
# #     "Shalimar": {"City": "Howrah", "State": "West Bengal"},
# #     "Statue of Unity": {"City": "Kevadia", "State": "Gujarat"},
# #     "Ahmedabad": {"City": "Ahmedabad", "State": "Gujarat"},
# #     "Kozhikode": {"City": "Kozhikode", "State": "Kerala"}
# # }
# # mapping_lower = {k.lower(): v for k, v in location_mapping.items()}

# # state_codes = {
# #     'Maharashtra': 'MH', 'Tamil Nadu': 'TN', 'Goa': 'GA', 'Telangana': 'TG',
# #     'Rajasthan': 'RJ', 'Chhattisgarh': 'CG', 'Karnataka': 'KA', 'Uttar Pradesh': 'UP',
# #     'Odisha': 'OR', 'Punjab': 'PB', 'Gujarat': 'GJ', 'West Bengal': 'WB',
# #     'Jharkhand': 'JH', 'Kerala': 'KL'
# # }

# # def extract_locker_bank(notes):
# #     if pd.isna(notes): return ""
# #     try:
# #         data = json.loads(notes)
# #         locker_name = data.get("Locker Bank Name", data.get("lockerBankName", ""))
# #         if locker_name and locker_name.strip().lower() != "luggage": return locker_name
# #         locker_location = data.get("lockerBankLocation", "")
# #         if locker_location and locker_location.strip().lower() not in ["", "luggage"]: return locker_location
# #         tenant = data.get("tenant", "")
# #         if tenant:
# #             if "http" in tenant:
# #                 match = re.search(r'://([^.]+)\.', tenant)
# #                 if match: return match.group(1)
# #             else: return tenant
# #         tenant_url = data.get("Tenant Name", data.get("tenant_host", ""))
# #         if tenant_url:
# #             match = re.search(r'://([^.]+)\.', tenant_url)
# #             if match: return match.group(1)
# #         return ""
# #     except:
# #         return ""

# # def clean_locker_name(name):
# #     if not name: return ""
# #     clean_name = re.sub(r'(?i)\b(luggage|station|railway|temple|junction)\b', '', str(name))
# #     clean_name = re.sub(r'[- ]+[A-G]$', '', clean_name)
# #     return clean_name.strip(' -')

# # # --- 3. Main Processing Logic ---
# # def process_dataframe(df, backend_df=None):
# #     if 'payment_notes' not in df.columns:
# #         st.error("Error: The settlement file does not contain a 'payment_notes' column.")
# #         return df

# #     df['Raw_Locker_Bank'] = df['payment_notes'].apply(extract_locker_bank)
# #     df['Cleaned_Location'] = df['Raw_Locker_Bank'].apply(clean_locker_name)
# #     df['City'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
# #     df['State'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))
    
# #     if backend_df is not None and 'entity_id' in df.columns:
# #         backend_cols_lower = [c.strip().lower() for c in backend_df.columns]
# #         if 'payment id' in backend_cols_lower and 'locker bank' in backend_cols_lower:
# #             backend_df_clean = backend_df.copy()
# #             backend_df_clean.columns = backend_cols_lower
            
# #             unknown_mask = df['City'] == "Unknown"
# #             if unknown_mask.any():
# #                 backend_lookup = backend_df_clean.drop_duplicates(subset=['payment id']).set_index('payment id')['locker bank'].to_dict()
# #                 df.loc[unknown_mask, 'Backend_Raw_Name'] = df.loc[unknown_mask, 'entity_id'].map(backend_lookup)
# #                 df.loc[unknown_mask, 'Backend_Cleaned'] = df.loc[unknown_mask, 'Backend_Raw_Name'].apply(clean_locker_name)
# #                 df.loc[unknown_mask, 'City'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
# #                     lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown") if pd.notna(loc) else "Unknown"
# #                 )
# #                 df.loc[unknown_mask, 'State'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
# #                     lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown") if pd.notna(loc) else "Unknown"
# #                 )
# #                 df = df.drop(columns=['Backend_Raw_Name', 'Backend_Cleaned'], errors='ignore')

# #     df = df.drop(columns=['Raw_Locker_Bank', 'Cleaned_Location'])
# #     return df

# # def generate_backend_analytics(raw_backend_df):
# #     """Processes backend data making it completely immune to hidden spaces or uppercase letters"""
# #     df_filtered = raw_backend_df.copy()
# #     df_filtered.columns = df_filtered.columns.str.strip().str.lower()
    
# #     # if 'payment type' in df_filtered.columns:
# #     #     mask = df_filtered['payment type'].astype(str).str.strip().str.lower() == 'payment'
# #     #     df_filtered = df_filtered[mask].copy()
# #     if 'status' in df_filtered.columns:
# #         mask_initiated = df_filtered['status'].astype(str).str.strip().str.lower() == 'initiated'
# #         df_filtered_initiated = df_filtered[mask_initiated].copy()
# #         mask_completed = df_filtered['status'].astype(str).str.strip().str.lower() == 'completed'
# #         df_filtered_completed = df_filtered[mask_completed].copy()

# #     if 'amount' in df_filtered.columns:
# #         df_filtered['amount'] = pd.to_numeric(df_filtered_completed['amount'], errors='coerce').fillna(0)
# #         df_filtered['Initiated amount'] = pd.to_numeric(df_filtered_initiated['amount'], errors = 'coerce').fillna(0)
# #     if 'locker bank' in df_filtered.columns:
# #         df_filtered['cleaned_location'] = df_filtered['locker bank'].astype(str).apply(clean_locker_name)
# #         df_filtered['city'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
# #         df_filtered['state'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))

# #     # --- Time, Weekend & Holiday Analysis ---
# #     if 'date created' in df_filtered.columns:
# #         df_filtered['date created'] = pd.to_datetime(df_filtered['date created'], errors='coerce')
# #         df_filtered['date_only'] = df_filtered['date created'].dt.date
# #         df_filtered['is_weekend'] = df_filtered['date created'].dt.weekday >= 5
        
# #         def check_holiday(row):
# #             try:
# #                 state_name = row.get('state', '')
# #                 code = state_codes.get(state_name)
# #                 if code and pd.notna(row['date_only']):
# #                     in_holidays = holidays.IN(subdiv=code, years=row['date_only'].year)
# #                     return row['date_only'] in in_holidays
# #             except: pass
# #             return False
            
# #         df_filtered['is_holiday'] = df_filtered.apply(check_holiday, axis=1)
# #         df_filtered['is_weekend_or_holiday'] = df_filtered['is_weekend'] | df_filtered['is_holiday']
# #         df_filtered['No. Initiated Transaction'] = df_filtered
# #         def get_tod(hour):
# #             if pd.isna(hour): return 'Unknown'
# #             if 6 <= hour < 12: return 'Morning (6AM - 12PM)'
# #             elif 12 <= hour < 18: return 'Afternoon (12PM - 6PM)'
# #             else: return 'Night (6PM - 6AM)'
            
# #         df_filtered['time_of_day'] = df_filtered['date created'].dt.hour.apply(get_tod)
# #         time_dist = df_filtered['time_of_day'].value_counts(normalize=True).reset_index()
# #         time_dist.columns = ['Time of Day', 'Percentage']
# #         time_dist['Percentage'] = (time_dist['Percentage'] * 100).round(2).astype(str) + '%'
# #     else:
# #         time_dist = pd.DataFrame()

# #     # --- Location Performance ---
# #     def calc_entropy(series):
# #         counts = series.value_counts(normalize=True)
# #         return -(counts * np.log2(counts)).sum()

# #     loc_rev = pd.DataFrame()
# #     if 'locker bank' in df_filtered.columns and 'amount' in df_filtered.columns:
# #         loc_rev = df_filtered.groupby('locker bank').agg(
# #             Total_Revenue=('amount', 'sum'),
# #             Initiated_Revenue = ('Initiated amount', 'sum'),
# #             Total_Transactions=('amount', 'count'),
# #             Total_Initiated_Transactions = ('Initiated amount', 'count'),
# #             AOV=('amount', 'mean'),
# #             Pct_Weekend_Holiday=('is_weekend_or_holiday', 'mean')
# #         ).reset_index()
        
# #         loc_rev.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
# #         loc_rev['Total_Revenue'] = loc_rev['Total_Revenue'].round(2)
# #         loc_rev['AOV'] = loc_rev['AOV'].round(2)
# #         loc_rev['Pct_Weekend_Holiday'] = (loc_rev['Pct_Weekend_Holiday'] * 100).round(1).astype(str) + '%'
# #         loc_rev = loc_rev.sort_values(by='Total_Revenue', ascending=False)
        
# #         if 'locker size' in df_filtered.columns:
# #             entropy_df = df_filtered.groupby('locker bank')['locker size'].apply(calc_entropy).reset_index(name='Size Entropy')
# #             entropy_df.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
# #             loc_rev = pd.merge(loc_rev, entropy_df, on='Locker Bank', how='left')
# #             loc_rev['Size Entropy'] = loc_rev['Size Entropy'].round(3)
            
# #             bank_sizes = pd.crosstab(df_filtered['locker bank'], df_filtered['locker size'], normalize='index') * 100
# #             bank_sizes = bank_sizes.round(1).astype(str) + '%'
# #             bank_sizes.columns = [f"% {col}" for col in bank_sizes.columns]
# #             bank_sizes = bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
# #             loc_rev = pd.merge(loc_rev, bank_sizes, on='Locker Bank', how='left')

# #     # --- City Revenue ---
# #     if 'city' in df_filtered.columns and 'amount' in df_filtered.columns:
# #         city_rev = df_filtered.groupby('city')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)
# #         city_rev.rename(columns={'city': 'City', 'amount': 'Amount'}, inplace=True)
# #     else:
# #         city_rev = pd.DataFrame()

# #     # --- User Behavior & Cohort Inferences ---
# #     user_df = pd.DataFrame()
# #     repeat_users = pd.DataFrame()
# #     loc_repeat_stats = pd.DataFrame()
    
# #     if 'user mobile' in df_filtered.columns and 'date updated' in df_filtered.columns:
# #         df_users = df_filtered.dropna(subset=['date updated', 'user mobile']).copy()
        
# #         if not df_users.empty:
# #             df_users['date updated'] = pd.to_datetime(df_users['date updated'], errors='coerce')
# #             df_users['date_only'] = df_users['date updated'].dt.date
            
# #             user_df = df_users.groupby('user mobile').agg(
# #                 total_transactions=('amount', 'count'),
# #                 active_days=('date_only', 'nunique'),
# #                 total_amount=('amount', 'sum')
# #             ).reset_index()
            
# #             # Safe Renaming
# #             user_df.rename(columns={'user mobile': 'User Mobile'}, inplace=True)
            
# #             if 'locker size' in df_users.columns:
# #                 size_map = {'Medium': 'M', 'Large': 'L', 'Extra Large': 'XL'}
# #                 df_users['size_clean'] = df_users['locker size'].map(size_map).fillna('unknown')
                
# #                 size_counts = df_users.groupby(['user mobile', 'size_clean']).size().unstack(fill_value=0)
# #                 size_pct = size_counts.div(size_counts.sum(axis=1), axis=0).fillna(0) * 100
# #                 size_pct = size_pct.rename(columns={'M': 'pct_M', 'L': 'pct_L', 'XL': 'pct_XL'})
# #                 size_pct.index.name = 'User Mobile'
                
# #                 user_df = user_df.merge(size_pct, on='User Mobile', how='left').fillna(0)
                
# #                 size_cols = [c for c in ['pct_M', 'pct_L', 'pct_XL'] if c in user_df.columns]
# #                 if size_cols:
# #                     user_df['dominant_size'] = user_df[size_cols].idxmax(axis=1).str.replace('pct_', '')
# #                     user_df['size_entropy'] = user_df[size_cols].apply(
# #                         lambda row: entropy(row.values / 100) if row.sum() > 0 else 0.0, axis=1
# #                     ).round(3)

# #             # Create Repeat Users Safely
# #             repeat_users = user_df[
# #                 (user_df['total_transactions'] >= 2) & 
# #                 (user_df['active_days'] >= 2)
# #             ].copy()
            
# #             # Location-Wise Stats FOR REPEAT USERS ONLY
# #             if not repeat_users.empty and 'locker bank' in df_users.columns:
# #                 repeat_mobiles = repeat_users['User Mobile'].tolist()
# #                 df_rep_only = df_users[df_users['user mobile'].isin(repeat_mobiles)].copy()
                
# #                 df_rep_only = df_rep_only.sort_values(['locker bank', 'user mobile', 'date updated'])
# #                 df_rep_only['prev_date'] = df_rep_only.groupby(['locker bank', 'user mobile'])['date_only'].shift(1)
# #                 df_rep_only['gap_days'] = (pd.to_datetime(df_rep_only['date_only']) - pd.to_datetime(df_rep_only['prev_date'])).dt.days

# #                 loc_repeat_stats = df_rep_only.groupby('locker bank').agg(
# #                     Loyal_Transactions=('amount', 'count'),
# #                     Avg_Gap_Days=('gap_days', 'mean')
# #                 ).reset_index()
                
# #                 loc_repeat_stats['Avg_Gap_Days'] = loc_repeat_stats['Avg_Gap_Days'].round(1)
# #                 loc_repeat_stats.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
                
# #                 if 'locker size' in df_rep_only.columns:
# #                     rep_bank_sizes = pd.crosstab(df_rep_only['locker bank'], df_rep_only['locker size'], normalize='index') * 100
# #                     rep_bank_sizes = rep_bank_sizes.round(1).astype(str) + '%'
# #                     rep_bank_sizes.columns = [f"Loyal % {col}" for col in rep_bank_sizes.columns]
# #                     rep_bank_sizes = rep_bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
# #                     loc_repeat_stats = pd.merge(loc_repeat_stats, rep_bank_sizes, on='Locker Bank', how='left')

# #     return loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats

# # # --- 4. Streamlit UI ---
# # # --- 4. Streamlit UI ---
# # st.set_page_config(page_title="Locker Analytics Processor", layout="wide")

# # st.title("🧳 Locker Data Processor & Analytics")

# # tab1, tab2, tab3 = st.tabs(["⚙️ Data Processing", "📊 Advanced Analytics Dashboard", "🛠️ Hardware Optimizer"])

# # # 1. Initialize variables globally so the app NEVER crashes if a file is missing
# # loc_rev = pd.DataFrame()
# # city_rev = pd.DataFrame()
# # time_dist = pd.DataFrame()
# # user_df = pd.DataFrame()
# # repeat_users = pd.DataFrame()
# # loc_repeat_stats = pd.DataFrame()
# # processed_df = pd.DataFrame()
# # backend_df = None

# # with tab1:
# #     st.write("Upload files to map missing locations or generate backend reports.")
# #     col1, col2 = st.columns(2)
# #     with col1:
# #         settlement_file = st.file_uploader("1. Upload Settlement .xlsx/.csv (Optional)", type=['xlsx', 'csv'], key="settlement")
# #     with col2:
# #         backend_file = st.file_uploader("2. Upload Backend .xlsx/.csv (For Analytics)", type=['xlsx', 'csv'], key="backend")

# #     # --- INDEPENDENT BACKEND PROCESSING ---
# #     if backend_file is not None:
# #         try:
# #             backend_df = pd.read_csv(backend_file) if backend_file.name.endswith('.csv') else pd.read_excel(backend_file)
# #             loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats = generate_backend_analytics(backend_df)
# #             st.success("✅ Backend data loaded & Analytics generated!")
# #         except Exception as e:
# #             st.error(f"Error processing Backend Data: {e}")

# #     # --- INDEPENDENT SETTLEMENT PROCESSING ---
# #     if settlement_file is not None:
# #         try:
# #             df = pd.read_csv(settlement_file) if settlement_file.name.endswith('.csv') else pd.read_excel(settlement_file)
# #             processed_df = process_dataframe(df, backend_df)
# #             st.success("✅ Settlement mapping complete!")
# #             st.write("### Processed Data Preview")
# #             st.dataframe(processed_df[['entity_id', 'payment_notes', 'City', 'State']].head())
# #         except Exception as e:
# #             st.error(f"Error processing Settlement Data: {e}")

# #     # --- UNIFIED DOWNLOAD BUTTON ---
# #     if settlement_file is not None or backend_file is not None:
# #         output = io.BytesIO()
# #         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
# #             if not processed_df.empty:
# #                 processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
            
# #             if backend_file is not None:
# #                 if not loc_rev.empty: loc_rev.to_excel(writer, index=False, sheet_name='Bank_Performance')
# #                 if not city_rev.empty: city_rev.to_excel(writer, index=False, sheet_name='Revenue_By_City')
# #                 if not time_dist.empty: time_dist.to_excel(writer, index=False, sheet_name='Time_of_Day_Stats')
# #                 if not loc_repeat_stats.empty: loc_repeat_stats.to_excel(writer, index=False, sheet_name='Loyalty_Stats')
# #                 if not user_df.empty:
# #                     user_df.to_excel(writer, index=False, sheet_name='All_User_Analytics')
# #                     repeat_users.to_excel(writer, index=False, sheet_name='Top_Repeat_Users')

# #         st.download_button(
# #             label="📥 Download Advanced Multi-Sheet Report",
# #             data=output.getvalue(),
# #             file_name="Advanced_Locker_Report.xlsx",
# #             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #         )

# # with tab2:
# #     if backend_file is None:
# #         st.info("👈 Please upload the Backend Data file in the 'Data Processing' tab to view analytics.")
# #     else:
# #         st.subheader("📊 Backend Operations Insights")
        
# #         if loc_rev.empty and city_rev.empty:
# #             st.error("⚠️ No usable data found. All rows were filtered out.")
# #         else:
# #             st.write("*Note: Filtering for rows where `Payment Type` = 'Payment'*")
            
# #             c1, c2 = st.columns(2)
# #             with c1:
# #                 st.write("### 🕒 Bookings by Time of Day")
# #                 st.dataframe(time_dist, use_container_width=True)
                
# #             with c2:
# #                 st.write("### 🏙️ Revenue by City")
# #                 st.dataframe(city_rev, use_container_width=True)
                
# #             st.markdown("---")
# #             st.write("### 📍 Location Performance: Revenue, Entropy & Size Distribution")
# #             st.dataframe(loc_rev, use_container_width=True)
            
# #             st.markdown("---")
# #             st.write("### 💎 Location-Wise Repeat Customer Behavior")
# #             if not loc_repeat_stats.empty:
# #                 st.dataframe(loc_repeat_stats, use_container_width=True)
# #             else:
# #                 st.warning("Not enough repeat users to generate loyalty stats.")
            
# #             st.markdown("---")
# #             st.subheader("👥 User Behavior & Cohort Inferences")
            
# #             if not user_df.empty:
# #                 total_users = len(user_df)
# #                 total_repeat = len(repeat_users)
# #                 repeat_rate = (total_repeat / total_users) * 100 if total_users > 0 else 0
                
# #                 kpi1, kpi2, kpi3 = st.columns(3)
# #                 kpi1.metric("Total Unique Users", f"{total_users}")
# #                 kpi2.metric("Highly Loyal Users (≥2 bookings)", f"{total_repeat}")
# #                 kpi3.metric("Customer Retention Rate", f"{repeat_rate:.1f}%")
                
# #                 st.write("### 🏆 Top Repeat Customers Profile")
# #                 display_cols = ['User Mobile', 'total_transactions', 'active_days', 'total_amount']
# #                 display_cols = [c for c in display_cols if c in repeat_users.columns] 
# #                 if 'dominant_size' in repeat_users.columns:
# #                     display_cols.extend(['dominant_size', 'size_entropy'])
                    
# #                 if not repeat_users.empty:
# #                     st.dataframe(repeat_users.sort_values('total_transactions', ascending=False)[display_cols].head(15), use_container_width=True)

# # # with tab3:
# # #     st.subheader("🛠️ AI Hardware Layout Optimizer")
# # #     st.write("Use historical backend data to generate optimal locker blueprints for new sites using PuLP.")
    
# # #     if backend_file is not None and not loc_rev.empty:
# # #         try:
# # #             import pulp
# # #             c1, c2 = st.columns(2)
# # #             with c1:
# # #                 target_station = st.selectbox("Select existing station to use as Demand Profile:", loc_rev['Locker Bank'].tolist())
# # #                 total_cols_available = st.number_input("Max Columns Available at New Site:", min_value=10, max_value=200, value=46)
            
# # #             with c2:
# # #                 st.info("Physical Hardware Specs")
# # #                 lockers_per_col_M = st.number_input("M Lockers per column:", value=4)
# # #                 lockers_per_col_L = st.number_input("L Lockers per column:", value=3)
# # #                 lockers_per_col_XL = st.number_input("XL Lockers per column:", value=2)

# # #             station_data = loc_rev[loc_rev['Locker Bank'] == target_station].iloc[0]
            
# # #             st.write("---")
# # #             st.write(f"**Extracted Live Profile for {target_station}:**")
# # #             st.write(f"Average Order Value: ₹{station_data['AOV']}")
            
# # #             if st.button("🚀 Run PuLP Optimization"):
# # #                 with st.spinner("Running integer optimization..."):
# # #                     base_aov = station_data['AOV']
# # #                     rev_per_locker = {'M': base_aov * 0.8, 'L': base_aov * 1.2, 'XL': base_aov * 1.8}
# # #                     lockers_per_column = {'M': lockers_per_col_M, 'L': lockers_per_col_L, 'XL': lockers_per_col_XL}
                    
# # #                     pct_m = float(str(station_data.get('% M', '0')).replace('%','')) / 100
# # #                     pct_l = float(str(station_data.get('% L', '0')).replace('%','')) / 100
# # #                     pct_xl = float(str(station_data.get('% XL', '0')).replace('%','')) / 100
                    
# # #                     min_columns = {
# # #                         'M': max(2, int(total_cols_available * pct_m * 0.5)),
# # #                         'L': max(2, int(total_cols_available * pct_l * 0.5)),
# # #                         'XL': max(2, int(total_cols_available * pct_xl * 0.5))
# # #                     }

# # #                     prob = pulp.LpProblem("Locker_Revenue_Optimization", pulp.LpMaximize)
# # #                     c = pulp.LpVariable.dicts("columns", ['M', 'L', 'XL'], lowBound=0, cat='Integer')

# # #                     prob += pulp.lpSum(c[size] * lockers_per_column[size] * rev_per_locker[size] for size in ['M', 'L', 'XL'])
# # #                     prob += pulp.lpSum(c[size] for size in ['M', 'L', 'XL']) <= total_cols_available
# # #                     for size in ['M', 'L', 'XL']: prob += c[size] >= min_columns[size]

# # #                     prob.solve(pulp.PULP_CBC_CMD(msg=0))

# # #                     if pulp.LpStatus[prob.status] == 'Optimal':
# # #                         solution = {size: int(c[size].value()) for size in ['M', 'L', 'XL']}
# # #                         st.success("✅ Optimal Blueprint Generated!")
# # #                         r1, r2, r3 = st.columns(3)
# # #                         r1.metric("Medium Columns", solution['M'], f"{solution['M'] * lockers_per_col_M} doors")
# # #                         r2.metric("Large Columns", solution['L'], f"{solution['L'] * lockers_per_col_L} doors")
# # #                         r3.metric("XL Columns", solution['XL'], f"{solution['XL'] * lockers_per_col_XL} doors")
# # #                         st.write(f"**Projected Daily Revenue Capability:** ₹{int(pulp.value(prob.objective)):,}")
# # #                     else:
# # #                         st.error("Could not find an optimal solution with the given constraints.")
# # #         except ImportError:
# # #             st.error("⚠️ The `pulp` library is not installed. Please run `pip install pulp` in your terminal.")
# # #     else:
# # #         st.info("Upload backend data in Tab 1 to unlock the Hardware Optimizer.")

# # # with tab3:
# # #     st.subheader("🛠️ AI Hardware Layout Optimizer")
# # #     st.write("Use historical backend data to generate mathematically optimal locker blueprints for new sites using PuLP.")
    
# # #     if backend_file is not None and not loc_rev.empty:
# # #         # 1. UI for User Inputs
# # #         c1, c2 = st.columns(2)
# # #         with c1:
# # #             target_station = st.selectbox("Select existing station to use as Demand Profile:", loc_rev['Locker Bank'].tolist())
# # #             total_cols_available = st.number_input("Max Columns Available at New Site:", min_value=10, max_value=200, value=46)
        
# # #         with c2:
# # #             st.info("Physical Hardware Specs")
# # #             lockers_per_col_M = st.number_input("M Lockers per column:", value=4)
# # #             lockers_per_col_L = st.number_input("L Lockers per column:", value=3)
# # #             lockers_per_col_XL = st.number_input("XL Lockers per column:", value=2)

# # #         # 2. Extract live parameters from your generated analytics!
# # #         station_data = loc_rev[loc_rev['Locker Bank'] == target_station].iloc[0]
        
# # #         st.write("---")
# # #         st.write(f"**Extracted Live Profile for {target_station}:**")
# # #         st.write(f"Average Order Value: ₹{station_data['AOV']}")
# # #         st.write(f"Historical Demand: **{station_data.get('% M', '0%')}** Medium | **{station_data.get('% L', '0%')}** Large | **{station_data.get('% XL', '0%')}** Extra Large")
        
# # #         if st.button("🚀 Run PuLP Optimization"):
# # #             with st.spinner("Running integer optimization..."):
# # #                 # Translate your dynamic AOV into the rev_per_locker input
# # #                 # (You would normally calculate size-specific AOV here, but using base AOV with multipliers for demo)
# # #                 base_aov = station_data['AOV']
# # #                 rev_per_locker = {'M': base_aov * 0.8, 'L': base_aov * 1.2, 'XL': base_aov * 1.8}
                
# # #                 lockers_per_column = {'M': lockers_per_col_M, 'L': lockers_per_col_L, 'XL': lockers_per_col_XL}
                
# # #                 # Dynamic Min Constraints based on actual percentage demand
# # #                 pct_m = float(str(station_data.get('% M', '0')).replace('%','')) / 100
# # #                 pct_l = float(str(station_data.get('% L', '0')).replace('%','')) / 100
# # #                 pct_xl = float(str(station_data.get('% XL', '0')).replace('%','')) / 100
                
# # #                 # Minimums dynamically set to ensure we build for actual observed demand
# # #                 min_columns = {
# # #                     'M': max(2, int(total_cols_available * pct_m * 0.5)),
# # #                     'L': max(2, int(total_cols_available * pct_l * 0.5)),
# # #                     'XL': max(2, int(total_cols_available * pct_xl * 0.5))
# # #                 }

# # #                 # Your exact PuLP Logic
# # #                 prob = pulp.LpProblem("Locker_Revenue_Optimization", pulp.LpMaximize)
# # #                 c = pulp.LpVariable.dicts("columns", ['M', 'L', 'XL'], lowBound=0, cat='Integer')

# # #                 # Objective
# # #                 prob += pulp.lpSum(c[size] * lockers_per_column[size] * rev_per_locker[size] for size in ['M', 'L', 'XL'])

# # #                 # Total Space Constraint
# # #                 prob += pulp.lpSum(c[size] for size in ['M', 'L', 'XL']) <= total_cols_available
                
# # #                 # Min Constraints
# # #                 for size in ['M', 'L', 'XL']:
# # #                     prob += c[size] >= min_columns[size]

# # #                 prob.solve(pulp.PULP_CBC_CMD(msg=0))

# # #                 if pulp.LpStatus[prob.status] == 'Optimal':
# # #                     solution = {size: int(c[size].value()) for size in ['M', 'L', 'XL']}
                    
# # #                     st.success("✅ Optimal Blueprint Generated!")
# # #                     r1, r2, r3 = st.columns(3)
# # #                     r1.metric("Medium Columns", solution['M'], f"{solution['M'] * lockers_per_col_M} total doors")
# # #                     r2.metric("Large Columns", solution['L'], f"{solution['L'] * lockers_per_col_L} total doors")
# # #                     r3.metric("XL Columns", solution['XL'], f"{solution['XL'] * lockers_per_col_XL} total doors")
                    
# # #                     st.write(f"**Projected Daily Revenue Capability:** ₹{int(pulp.value(prob.objective)):,}")
# # #                 else:
# # #                     st.error("Could not find an optimal solution with the given constraints.")
# # #     else:
# # #         st.info("Upload backend data in Tab 1 to unlock the Hardware Optimizer.")\

# import streamlit as st
# import pandas as pd
# import json
# import re
# import io
# import numpy as np
# from scipy.stats import entropy
# import holidays
# # import pulp

# # --- 1. Define the Mapping Dictionaries ---
# # location_mapping = {
# #     "THVM": {"City": "Thivim", "State": "Goa"},
# #     "katpadi": {"City": "Katpadi", "State": "Tamil Nadu"},
# #     "CHZ": {"City": "Charlapalli", "State": "Telangana"},
# #     "PUNE": {"City": "Pune", "State": "Maharashtra"},
# #     "AJMER": {"City": "Ajmer", "State": "Rajasthan"},
# #     "BSP": {"City": "Bilaspur", "State": "Chhattisgarh"},
# #     "Visvesvaraya Museum": {"City": "Bengaluru", "State": "Karnataka"},
# #     "Varanasi": {"City": "Varanasi", "State": "Uttar Pradesh"},
# #     "Nagpur": {"City": "Nagpur", "State": "Maharashtra"},
# #     "KRP": {"City": "Krishna Raj Puram", "State": "Karnataka"},
# #     "KP": {"City": "Pune", "State": "Maharashtra"},
# #     "UD": {"City": "Udupi", "State": "Karnataka"},
# #     "Ludhiana": {"City": "Ludhiana", "State": "Punjab"},
# #     "Amritsar": {"City": "Amritsar", "State": "Punjab"},
# #     "Nagapattinam": {"City": "Nagapattinam", "State": "Tamil Nadu"},
# #     "Hubballi Bus Stand": {"City": "Hubballi", "State": "Karnataka"},
# #     "Villupuram": {"City": "Villupuram", "State": "Tamil Nadu"},
# #     "BRC": {"City": "Vadodara", "State": "Gujarat"},
# #     "RN": {"City": "Ratnagiri", "State": "Maharashtra"},
# #     "Tiruvannamalai": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
# #     "GHM": {"City": "Ghoom", "State": "West Bengal"},
# #     "KSR": {"City": "Bengaluru", "State": "Karnataka"},
# #     "Melmaruvathur": {"City": "Melmaruvathur", "State": "Tamil Nadu"},
# #     "Shirdi": {"City": "Shirdi", "State": "Maharashtra"},
# #     "MMR": {"City": "Manmad", "State": "Maharashtra"},
# #     "JAM": {"City": "Jamnagar", "State": "Gujarat"},
# #     "Jasidih": {"City": "Jasidih", "State": "Jharkhand"},
# #     "Manglore Central K": {"City": "Mangaluru", "State": "Karnataka"},
# #     "Tirur": {"City": "Tirur", "State": "Kerala"},
# #     "Kannur": {"City": "Kannur", "State": "Kerala"},
# #     "CSMT": {"City": "Mumbai", "State": "Maharashtra"},
# #     "Jalandhar": {"City": "Jalandhar", "State": "Punjab"},
# #     "SEG": {"City": "Shegaon", "State": "Maharashtra"},
# #     "Tiruvannamalai Arunachaleswarar Temple": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
# #     "Ayodhya": {"City": "Ayodhya", "State": "Uttar Pradesh"},
# #     "Lucknow": {"City": "Lucknow", "State": "Uttar Pradesh"},
# #     "SANTRAGACHI": {"City": "Howrah", "State": "West Bengal"},
# #     "Shalimar": {"City": "Howrah", "State": "West Bengal"},
# #     "Statue of Unity": {"City": "Kevadia", "State": "Gujarat"},
# #     "Ahmedabad": {"City": "Ahmedabad", "State": "Gujarat"},
# #     "Kozhikode": {"City": "Kozhikode", "State": "Kerala"}
# # }
# # mapping_lower = {k.lower(): v for k, v in location_mapping.items()}

# # state_codes = {
# #     'Maharashtra': 'MH', 'Tamil Nadu': 'TN', 'Goa': 'GA', 'Telangana': 'TG',
# #     'Rajasthan': 'RJ', 'Chhattisgarh': 'CG', 'Karnataka': 'KA', 'Uttar Pradesh': 'UP',
# #     'Odisha': 'OR', 'Punjab': 'PB', 'Gujarat': 'GJ', 'West Bengal': 'WB',
# #     'Jharkhand': 'JH', 'Kerala': 'KL'
# # }
# if 'location_mapping' not in st.session_state:
#     st.session_state.location_mapping = {
#         "THVM": {"City": "Thivim", "State": "Goa"},
#         "katpadi": {"City": "Katpadi", "State": "Tamil Nadu"},
#         "CHZ": {"City": "Charlapalli", "State": "Telangana"},
#         "PUNE": {"City": "Pune", "State": "Maharashtra"},
#         "AJMER": {"City": "Ajmer", "State": "Rajasthan"},
#         "BSP": {"City": "Bilaspur", "State": "Chhattisgarh"},
#         "Visvesvaraya Museum": {"City": "Bengaluru", "State": "Karnataka"},
#         "Varanasi": {"City": "Varanasi", "State": "Uttar Pradesh"},
#         "Nagpur": {"City": "Nagpur", "State": "Maharashtra"},
#         "KRP": {"City": "Krishna Raj Puram", "State": "Karnataka"},
#         "KP": {"City": "Pune", "State": "Maharashtra"},
#         "UD": {"City": "Udupi", "State": "Karnataka"},
#         "Ludhiana": {"City": "Ludhiana", "State": "Punjab"},
#         "Amritsar": {"City": "Amritsar", "State": "Punjab"},
#         "Nagapattinam": {"City": "Nagapattinam", "State": "Tamil Nadu"},
#         "Hubballi Bus Stand": {"City": "Hubballi", "State": "Karnataka"},
#         "Villupuram": {"City": "Villupuram", "State": "Tamil Nadu"},
#         "BRC": {"City": "Vadodara", "State": "Gujarat"},
#         "RN": {"City": "Ratnagiri", "State": "Maharashtra"},
#         "Tiruvannamalai": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
#         "GHM": {"City": "Ghoom", "State": "West Bengal"},
#         "KSR": {"City": "Bengaluru", "State": "Karnataka"},
#         "Melmaruvathur": {"City": "Melmaruvathur", "State": "Tamil Nadu"},
#         "Shirdi": {"City": "Shirdi", "State": "Maharashtra"},
#         "MMR": {"City": "Manmad", "State": "Maharashtra"},
#         "JAM": {"City": "Jamnagar", "State": "Gujarat"},
#         "Jasidih": {"City": "Jasidih", "State": "Jharkhand"},
#         "Manglore Central K": {"City": "Mangaluru", "State": "Karnataka"},
#         "Tirur": {"City": "Tirur", "State": "Kerala"},
#         "Kannur": {"City": "Kannur", "State": "Kerala"},
#         "CSMT": {"City": "Mumbai", "State": "Maharashtra"},
#         "Jalandhar": {"City": "Jalandhar", "State": "Punjab"},
#         "SEG": {"City": "Shegaon", "State": "Maharashtra"},
#         "Tiruvannamalai Arunachaleswarar Temple": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
#         "Ayodhya": {"City": "Ayodhya", "State": "Uttar Pradesh"},
#         "Lucknow": {"City": "Lucknow", "State": "Uttar Pradesh"},
#         "SANTRAGACHI": {"City": "Howrah", "State": "West Bengal"},
#         "Shalimar": {"City": "Howrah", "State": "West Bengal"},
#         "Statue of Unity": {"City": "Kevadia", "State": "Gujarat"},
#         "Ahmedabad": {"City": "Ahmedabad", "State": "Gujarat"},
#         "Kozhikode": {"City": "Kozhikode", "State": "Kerala"}
#     }

# if 'state_codes' not in st.session_state:
#     st.session_state.state_codes = {
#         'Maharashtra': 'MH', 'Tamil Nadu': 'TN', 'Goa': 'GA', 'Telangana': 'TG',
#         'Rajasthan': 'RJ', 'Chhattisgarh': 'CG', 'Karnataka': 'KA', 'Uttar Pradesh': 'UP',
#         'Odisha': 'OR', 'Punjab': 'PB', 'Gujarat': 'GJ', 'West Bengal': 'WB',
#         'Jharkhand': 'JH', 'Kerala': 'KL'
#     }

# # Compute lowercased mapping dynamically based on the current session memory
# mapping_lower = {k.lower(): v for k, v in st.session_state.location_mapping.items()}
# state_codes = st.session_state.state_codes
# def extract_locker_bank(notes):
#     if pd.isna(notes): return ""
#     try:
#         data = json.loads(notes)
#         locker_name = data.get("Locker Bank Name", data.get("lockerBankName", ""))
#         if locker_name and locker_name.strip().lower() != "luggage": return locker_name
#         locker_location = data.get("lockerBankLocation", "")
#         if locker_location and locker_location.strip().lower() not in ["", "luggage"]: return locker_location
#         tenant = data.get("tenant", "")
#         if tenant:
#             if "http" in tenant:
#                 match = re.search(r'://([^.]+)\.', tenant)
#                 if match: return match.group(1)
#             else: return tenant
#         tenant_url = data.get("Tenant Name", data.get("tenant_host", ""))
#         if tenant_url:
#             match = re.search(r'://([^.]+)\.', tenant_url)
#             if match: return match.group(1)
#         return ""
#     except:
#         return ""

# def clean_locker_name(name):
#     if not name: return ""
#     clean_name = re.sub(r'(?i)\b(luggage|station|railway|temple|junction)\b', '', str(name))
#     clean_name = re.sub(r'[- ]+[A-G]$', '', clean_name)
#     return clean_name.strip(' -')

# # --- 3. Main Processing Logic ---
# def process_dataframe(df, backend_df=None):
#     if 'payment_notes' not in df.columns:
#         st.error("Error: The settlement file does not contain a 'payment_notes' column.")
#         return df

#     df['Raw_Locker_Bank'] = df['payment_notes'].apply(extract_locker_bank)
#     df['Cleaned_Location'] = df['Raw_Locker_Bank'].apply(clean_locker_name)
#     df['City'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
#     df['State'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))
    
#     if backend_df is not None and 'entity_id' in df.columns:
#         backend_cols_lower = [c.strip().lower() for c in backend_df.columns]
#         if 'payment id' in backend_cols_lower and 'locker bank' in backend_cols_lower:
#             backend_df_clean = backend_df.copy()
#             backend_df_clean.columns = backend_cols_lower
            
#             unknown_mask = df['City'] == "Unknown"
#             if unknown_mask.any():
#                 backend_lookup = backend_df_clean.drop_duplicates(subset=['payment id']).set_index('payment id')['locker bank'].to_dict()
#                 df.loc[unknown_mask, 'Backend_Raw_Name'] = df.loc[unknown_mask, 'entity_id'].map(backend_lookup)
#                 df.loc[unknown_mask, 'Backend_Cleaned'] = df.loc[unknown_mask, 'Backend_Raw_Name'].apply(clean_locker_name)
#                 df.loc[unknown_mask, 'City'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
#                     lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown") if pd.notna(loc) else "Unknown"
#                 )
#                 df.loc[unknown_mask, 'State'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
#                     lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown") if pd.notna(loc) else "Unknown"
#                 )
#                 df = df.drop(columns=['Backend_Raw_Name', 'Backend_Cleaned'], errors='ignore')

#     df = df.drop(columns=['Raw_Locker_Bank', 'Cleaned_Location'])
#     return df

# # def generate_backend_analytics(raw_backend_df):
# #     df_filtered = raw_backend_df.copy()
# #     df_filtered.columns = df_filtered.columns.str.strip().str.lower()
    
# #     # --- 1. SAFELY PROCESS AMOUNTS & STATUS (Using np.where) ---
# #     if 'amount' in df_filtered.columns:
# #         df_filtered['amount'] = pd.to_numeric(df_filtered['amount'], errors='coerce').fillna(0)
# #     else:
# #         df_filtered['amount'] = 0

# #     if 'status' in df_filtered.columns:
# #         status_clean = df_filtered['status'].astype(str).str.strip().str.lower()
        
# #         # Create columns dynamically without losing rows
# #         df_filtered['Completed_Amount'] = np.where(status_clean == 'completed', df_filtered['amount'], 0)
# #         df_filtered['Initiated_Amount'] = np.where(status_clean == 'initiated', df_filtered['amount'], 0)
        
# #         # Create flag columns to easily count transactions later
# #         df_filtered['Is_Completed'] = np.where(status_clean == 'completed', 1, 0)
# #         df_filtered['Is_Initiated'] = np.where(status_clean == 'initiated', 1, 0)
# #     else:
# #         # Fallbacks if status column doesn't exist
# #         df_filtered['Completed_Amount'] = df_filtered['amount']
# #         df_filtered['Initiated_Amount'] = 0
# #         df_filtered['Is_Completed'] = 1
# #         df_filtered['Is_Initiated'] = 0

# #     if 'locker bank' in df_filtered.columns:
# #         df_filtered['cleaned_location'] = df_filtered['locker bank'].astype(str).apply(clean_locker_name)
# #         df_filtered['city'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
# #         df_filtered['state'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))

# #     # --- Time, Weekend & Holiday Analysis ---
# #     if 'date created' in df_filtered.columns:
# #         df_filtered['date created'] = pd.to_datetime(df_filtered['date created'], errors='coerce')
# #         df_filtered['date_only'] = df_filtered['date created'].dt.date
# #         df_filtered['is_weekend'] = df_filtered['date created'].dt.weekday >= 5
        
# #         def check_holiday(row):
# #             try:
# #                 state_name = row.get('state', '')
# #                 code = state_codes.get(state_name)
# #                 if code and pd.notna(row['date_only']):
# #                     in_holidays = holidays.IN(subdiv=code, years=row['date_only'].year)
# #                     return row['date_only'] in in_holidays
# #             except: pass
# #             return False
            
# #         df_filtered['is_holiday'] = df_filtered.apply(check_holiday, axis=1)
# #         df_filtered['is_weekend_or_holiday'] = df_filtered['is_weekend'] | df_filtered['is_holiday']

# #         def get_tod(hour):
# #             if pd.isna(hour): return 'Unknown'
# #             if 6 <= hour < 12: return 'Morning (6AM - 12PM)'
# #             elif 12 <= hour < 18: return 'Afternoon (12PM - 6PM)'
# #             else: return 'Night (6PM - 6AM)'
            
# #         df_filtered['time_of_day'] = df_filtered['date created'].dt.hour.apply(get_tod)
# #         time_dist = df_filtered[df_filtered['Is_Completed'] == 1]['time_of_day'].value_counts(normalize=True).reset_index()
# #         time_dist.columns = ['Time of Day', 'Percentage']
# #         time_dist['Percentage'] = (time_dist['Percentage'] * 100).round(2).astype(str) + '%'
# #     else:
# #         time_dist = pd.DataFrame()
# def generate_backend_analytics(raw_backend_df):
#     df_filtered = raw_backend_df.copy()
#     df_filtered.columns = df_filtered.columns.str.strip().str.lower()
    
#     # --- 1. FILTER FOR 'PAYMENT' TYPE ONLY ---
#     # if 'payment type' in df_filtered.columns:
#     #     mask_payment = df_filtered['payment type'].astype(str).str.strip().str.lower() == 'payment'
#     #     df_filtered = df_filtered[mask_payment].copy()

#     # --- 2. SAFELY PROCESS AMOUNTS (Handles commas like "1,000") ---
#     if 'amount' in df_filtered.columns:
#         clean_amount = df_filtered['amount'].astype(str).str.replace(',', '', regex=True)
#         df_filtered['amount'] = pd.to_numeric(clean_amount, errors='coerce').fillna(0)
#     else:
#         df_filtered['amount'] = 0

#     # --- 3. BULLETPROOF STATUS MASKING (Using .str.contains) ---
#     if 'status' in df_filtered.columns:
#         status_clean = df_filtered['status'].astype(str).str.lower()
#     if 'payment type' in df_filtered.columns:
#         payment_clean = df_filtered['payment type'].astype(str).str.lower()
#         # .contains() is much safer than ==. It catches "Initiated", " Initiated ", "Payment Initiated", etc.
#         is_completed = status_clean.str.contains('complet', na=False)
#         is_initiated = status_clean.str.contains('initiat', na=False)
#         is_overdue = payment_clean.str.contains('overdue', na=False)
#         df_filtered['Completed_Amount'] = np.where(is_completed, df_filtered['amount'], 0)
#         df_filtered['Initiated_Amount'] = np.where(is_initiated, df_filtered['amount'], 0)
#         df_filtered['Overdue_Amount'] = np.where(is_overdue, df_filtered['amount'], 0)
#         df_filtered['Is_Completed'] = np.where(is_completed, 1, 0)
#         df_filtered['Is_Initiated'] = np.where(is_initiated, 1, 0)
#     else:
#         df_filtered['Completed_Amount'] = df_filtered['amount']
#         df_filtered['Initiated_Amount'] = 0
#         df_filtered['Is_Completed'] = 1
#         df_filtered['Is_Initiated'] = 0

#     # --- Location Mapping ---
#     if 'locker bank' in df_filtered.columns:
#         df_filtered['cleaned_location'] = df_filtered['locker bank'].astype(str).apply(clean_locker_name)
#         df_filtered['city'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
#         df_filtered['state'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))

#     # --- Time, Weekend & Holiday Analysis ---
#     if 'date created' in df_filtered.columns:
#         df_filtered['date created'] = pd.to_datetime(df_filtered['date created'], errors='coerce')
#         df_filtered['date_only'] = df_filtered['date created'].dt.date
#         df_filtered['is_weekend'] = df_filtered['date created'].dt.weekday >= 5
        
#         def check_holiday(row):
#             try:
#                 state_name = row.get('state', '')
#                 code = state_codes.get(state_name)
#                 if code and pd.notna(row['date_only']):
#                     in_holidays = holidays.IN(subdiv=code, years=row['date_only'].year)
#                     return row['date_only'] in in_holidays
#             except: pass
#             return False
            
#         df_filtered['is_holiday'] = df_filtered.apply(check_holiday, axis=1)
#         df_filtered['is_weekend_or_holiday'] = df_filtered['is_weekend'] | df_filtered['is_holiday']

#         def get_tod(hour):
#             if pd.isna(hour): return 'Unknown'
#             if 6 <= hour < 12: return 'Morning (6AM - 12PM)'
#             elif 12 <= hour < 18: return 'Afternoon (12PM - 6PM)'
#             else: return 'Night (6PM - 6AM)'
            
#         df_filtered['time_of_day'] = df_filtered['date created'].dt.hour.apply(get_tod)
#         time_dist = df_filtered[df_filtered['Is_Completed'] == 1]['time_of_day'].value_counts(normalize=True).reset_index()
#         time_dist.columns = ['Time of Day', 'Percentage']
#         time_dist['Percentage'] = (time_dist['Percentage'] * 100).round(2).astype(str) + '%'
#     else:
#         time_dist = pd.DataFrame()

#     # --- Location Performance ---
#     def calc_entropy(series):
#         counts = series.value_counts(normalize=True)
#         return -(counts * np.log2(counts)).sum()

#     loc_rev = pd.DataFrame()
#     if 'locker bank' in df_filtered.columns:
#         loc_rev = df_filtered.groupby('locker bank').agg(
#             Total_Revenue=('Completed_Amount', 'sum'),
#             Overdue_Revenue=('Overdue_Amount', 'sum'), 
#             Initiated_Revenue=('Initiated_Amount', 'sum'),
#             Total_Transactions=('Is_Completed', 'sum'),
#             Total_Initiated_Transactions=('Is_Initiated', 'sum'),
#             Pct_Weekend_Holiday=('is_weekend_or_holiday', 'mean')
#         ).reset_index()
        
#         loc_rev.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
        
#         loc_rev['AOV'] = (loc_rev['Total_Revenue'] / loc_rev['Total_Transactions'].replace(0, 1)).round(2)
#         loc_rev['Total_Revenue'] = loc_rev['Total_Revenue'].round(2)
#         loc_rev['Initiated_Revenue'] = loc_rev['Initiated_Revenue'].round(2)
#         loc_rev['Pct_Weekend_Holiday'] = (loc_rev['Pct_Weekend_Holiday'] * 100).round(1).astype(str) + '%'
#         loc_rev = loc_rev.sort_values(by='Total_Revenue', ascending=False)
        
#         df_completed = df_filtered[df_filtered['Is_Completed'] == 1]
        
#         if 'locker size' in df_completed.columns:
#             entropy_df = df_completed.groupby('locker bank')['locker size'].apply(calc_entropy).reset_index(name='Size Entropy')
#             entropy_df.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
#             loc_rev = pd.merge(loc_rev, entropy_df, on='Locker Bank', how='left')
#             loc_rev['Size Entropy'] = loc_rev['Size Entropy'].round(3)
            
#             bank_sizes = pd.crosstab(df_completed['locker bank'], df_completed['locker size'], normalize='index') * 100
#             bank_sizes = bank_sizes.round(1).astype(str) + '%'
#             bank_sizes.columns = [f"% {col}" for col in bank_sizes.columns]
#             bank_sizes = bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
#             loc_rev = pd.merge(loc_rev, bank_sizes, on='Locker Bank', how='left')

#     # --- City Revenue ---
#     if 'city' in df_filtered.columns:
#         city_rev = df_filtered.groupby('city')['Completed_Amount'].sum().reset_index().sort_values(by='Completed_Amount', ascending=False)
#         city_rev.rename(columns={'city': 'City', 'Completed_Amount': 'Amount'}, inplace=True)
#     else:
#         city_rev = pd.DataFrame()

#     # --- User Behavior & Cohort Inferences ---
#     user_df = pd.DataFrame()
#     repeat_users = pd.DataFrame()
#     loc_repeat_stats = pd.DataFrame()
    
#     if 'user mobile' in df_filtered.columns and 'date updated' in df_filtered.columns:
#         df_users = df_filtered[df_filtered['Is_Completed'] == 1].dropna(subset=['date updated', 'user mobile']).copy()
        
#         if not df_users.empty:
#             df_users['date updated'] = pd.to_datetime(df_users['date updated'], errors='coerce')
#             df_users['date_only'] = df_users['date updated'].dt.date
            
#             user_df = df_users.groupby('user mobile').agg(
#                 total_transactions=('Completed_Amount', 'count'),
#                 active_days=('date_only', 'nunique'),
#                 total_amount=('Completed_Amount', 'sum')
#             ).reset_index()
            
#             user_df.rename(columns={'user mobile': 'User Mobile'}, inplace=True)
            
#             if 'locker size' in df_users.columns:
#                 size_map = {'Medium': 'M', 'Large': 'L', 'Extra Large': 'XL'}
#                 df_users['size_clean'] = df_users['locker size'].map(size_map).fillna('unknown')
                
#                 size_counts = df_users.groupby(['user mobile', 'size_clean']).size().unstack(fill_value=0)
#                 size_pct = size_counts.div(size_counts.sum(axis=1), axis=0).fillna(0) * 100
#                 size_pct = size_pct.rename(columns={'M': 'pct_M', 'L': 'pct_L', 'XL': 'pct_XL'})
#                 size_pct.index.name = 'User Mobile'
                
#                 user_df = user_df.merge(size_pct, on='User Mobile', how='left').fillna(0)
                
#                 size_cols = [c for c in ['pct_M', 'pct_L', 'pct_XL'] if c in user_df.columns]
#                 if size_cols:
#                     user_df['dominant_size'] = user_df[size_cols].idxmax(axis=1).str.replace('pct_', '')
#                     user_df['size_entropy'] = user_df[size_cols].apply(
#                         lambda row: entropy(row.values / 100) if row.sum() > 0 else 0.0, axis=1
#                     ).round(3)

#             repeat_users = user_df[
#                 (user_df['total_transactions'] >= 2) & 
#                 (user_df['active_days'] >= 2)
#             ].copy()
            
#             if not repeat_users.empty and 'locker bank' in df_users.columns:
#                 repeat_mobiles = repeat_users['User Mobile'].tolist()
#                 df_rep_only = df_users[df_users['user mobile'].isin(repeat_mobiles)].copy()
                
#                 df_rep_only = df_rep_only.sort_values(['locker bank', 'user mobile', 'date updated'])
#                 df_rep_only['prev_date'] = df_rep_only.groupby(['locker bank', 'user mobile'])['date_only'].shift(1)
#                 df_rep_only['gap_days'] = (pd.to_datetime(df_rep_only['date_only']) - pd.to_datetime(df_rep_only['prev_date'])).dt.days

#                 loc_repeat_stats = df_rep_only.groupby('locker bank').agg(
#                     Loyal_Transactions=('Completed_Amount', 'count'),
#                     Avg_Gap_Days=('gap_days', 'mean')
#                 ).reset_index()
                
#                 loc_repeat_stats['Avg_Gap_Days'] = loc_repeat_stats['Avg_Gap_Days'].round(1)
#                 loc_repeat_stats.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
                
#                 if 'locker size' in df_rep_only.columns:
#                     rep_bank_sizes = pd.crosstab(df_rep_only['locker bank'], df_rep_only['locker size'], normalize='index') * 100
#                     rep_bank_sizes = rep_bank_sizes.round(1).astype(str) + '%'
#                     rep_bank_sizes.columns = [f"Loyal % {col}" for col in rep_bank_sizes.columns]
#                     rep_bank_sizes = rep_bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
#                     loc_repeat_stats = pd.merge(loc_repeat_stats, rep_bank_sizes, on='Locker Bank', how='left')

#     return loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats
#     # --- Location Performance ---
#     def calc_entropy(series):
#         counts = series.value_counts(normalize=True)
#         return -(counts * np.log2(counts)).sum()

#     loc_rev = pd.DataFrame()
#     if 'locker bank' in df_filtered.columns:
#         # Group by all rows, but sum our safely mapped columns
#         loc_rev = df_filtered.groupby('locker bank').agg(
#             Total_Revenue=('Completed_Amount', 'sum'),
#             Initiated_Revenue=('Initiated_Amount', 'sum'),
#             Total_Transactions=('Is_Completed', 'sum'),
#             Total_Initiated_Transactions=('Is_Initiated', 'sum'),
#             Pct_Weekend_Holiday=('is_weekend_or_holiday', 'mean')
#         ).reset_index()
        
#         loc_rev.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
        
#         # Calculate AOV Safely (Revenue / Completed Transactions)
#         loc_rev['AOV'] = (loc_rev['Total_Revenue'] / loc_rev['Total_Transactions'].replace(0, 1)).round(2)
        
#         loc_rev['Total_Revenue'] = loc_rev['Total_Revenue'].round(2)
#         loc_rev['Initiated_Revenue'] = loc_rev['Initiated_Revenue'].round(2)
#         loc_rev['Pct_Weekend_Holiday'] = (loc_rev['Pct_Weekend_Holiday'] * 100).round(1).astype(str) + '%'
#         loc_rev = loc_rev.sort_values(by='Total_Revenue', ascending=False)
        
#         # Only calculate sizes and entropy for COMPLETED transactions
#         df_completed = df_filtered[df_filtered['Is_Completed'] == 1]
        
#         if 'locker size' in df_completed.columns:
#             entropy_df = df_completed.groupby('locker bank')['locker size'].apply(calc_entropy).reset_index(name='Size Entropy')
#             entropy_df.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
#             loc_rev = pd.merge(loc_rev, entropy_df, on='Locker Bank', how='left')
#             loc_rev['Size Entropy'] = loc_rev['Size Entropy'].round(3)
            
#             bank_sizes = pd.crosstab(df_completed['locker bank'], df_completed['locker size'], normalize='index') * 100
#             bank_sizes = bank_sizes.round(1).astype(str) + '%'
#             bank_sizes.columns = [f"% {col}" for col in bank_sizes.columns]
#             bank_sizes = bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
#             loc_rev = pd.merge(loc_rev, bank_sizes, on='Locker Bank', how='left')

#     # --- City Revenue ---
#     if 'city' in df_filtered.columns:
#         city_rev = df_filtered.groupby('city')['Completed_Amount'].sum().reset_index().sort_values(by='Completed_Amount', ascending=False)
#         city_rev.rename(columns={'city': 'City', 'Completed_Amount': 'Amount'}, inplace=True)
#     else:
#         city_rev = pd.DataFrame()

#     # --- User Behavior & Cohort Inferences ---
#     user_df = pd.DataFrame()
#     repeat_users = pd.DataFrame()
#     loc_repeat_stats = pd.DataFrame()
    
#     if 'user mobile' in df_filtered.columns and 'date updated' in df_filtered.columns:
#         # We only want to run user RFM analytics on COMPLETED transactions
#         df_users = df_filtered[df_filtered['Is_Completed'] == 1].dropna(subset=['date updated', 'user mobile']).copy()
        
#         if not df_users.empty:
#             df_users['date updated'] = pd.to_datetime(df_users['date updated'], errors='coerce')
#             df_users['date_only'] = df_users['date updated'].dt.date
            
#             user_df = df_users.groupby('user mobile').agg(
#                 total_transactions=('Completed_Amount', 'count'),
#                 active_days=('date_only', 'nunique'),
#                 total_amount=('Completed_Amount', 'sum')
#             ).reset_index()
            
#             user_df.rename(columns={'user mobile': 'User Mobile'}, inplace=True)
            
#             if 'locker size' in df_users.columns:
#                 size_map = {'Medium': 'M', 'Large': 'L', 'Extra Large': 'XL'}
#                 df_users['size_clean'] = df_users['locker size'].map(size_map).fillna('unknown')
                
#                 size_counts = df_users.groupby(['user mobile', 'size_clean']).size().unstack(fill_value=0)
#                 size_pct = size_counts.div(size_counts.sum(axis=1), axis=0).fillna(0) * 100
#                 size_pct = size_pct.rename(columns={'M': 'pct_M', 'L': 'pct_L', 'XL': 'pct_XL'})
#                 size_pct.index.name = 'User Mobile'
                
#                 user_df = user_df.merge(size_pct, on='User Mobile', how='left').fillna(0)
                
#                 size_cols = [c for c in ['pct_M', 'pct_L', 'pct_XL'] if c in user_df.columns]
#                 if size_cols:
#                     user_df['dominant_size'] = user_df[size_cols].idxmax(axis=1).str.replace('pct_', '')
#                     user_df['size_entropy'] = user_df[size_cols].apply(
#                         lambda row: entropy(row.values / 100) if row.sum() > 0 else 0.0, axis=1
#                     ).round(3)

#             repeat_users = user_df[
#                 (user_df['total_transactions'] >= 2) & 
#                 (user_df['active_days'] >= 2)
#             ].copy()
            
#             if not repeat_users.empty and 'locker bank' in df_users.columns:
#                 repeat_mobiles = repeat_users['User Mobile'].tolist()
#                 df_rep_only = df_users[df_users['user mobile'].isin(repeat_mobiles)].copy()
                
#                 df_rep_only = df_rep_only.sort_values(['locker bank', 'user mobile', 'date updated'])
#                 df_rep_only['prev_date'] = df_rep_only.groupby(['locker bank', 'user mobile'])['date_only'].shift(1)
#                 df_rep_only['gap_days'] = (pd.to_datetime(df_rep_only['date_only']) - pd.to_datetime(df_rep_only['prev_date'])).dt.days

#                 loc_repeat_stats = df_rep_only.groupby('locker bank').agg(
#                     Loyal_Transactions=('Completed_Amount', 'count'),
#                     Avg_Gap_Days=('gap_days', 'mean')
#                 ).reset_index()
                
#                 loc_repeat_stats['Avg_Gap_Days'] = loc_repeat_stats['Avg_Gap_Days'].round(1)
#                 loc_repeat_stats.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
                
#                 if 'locker size' in df_rep_only.columns:
#                     rep_bank_sizes = pd.crosstab(df_rep_only['locker bank'], df_rep_only['locker size'], normalize='index') * 100
#                     rep_bank_sizes = rep_bank_sizes.round(1).astype(str) + '%'
#                     rep_bank_sizes.columns = [f"Loyal % {col}" for col in rep_bank_sizes.columns]
#                     rep_bank_sizes = rep_bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
#                     loc_repeat_stats = pd.merge(loc_repeat_stats, rep_bank_sizes, on='Locker Bank', how='left')

#     return loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats

# # --- 4. Streamlit UI ---
# # st.set_page_config(page_title="Locker Analytics Processor", layout="wide")
# # with st.sidebar:
# #     st.header("⚙️ Configuration")
# #     with st.expander("📍 Add New Location Mapping", expanded=False):
# #         st.write("Add missing locations so they map correctly to a City and State.")
# #         new_code = st.text_input("Locker Bank Code (e.g., NDLS)")
# #         new_city = st.text_input("City Name")
# #         new_state = st.text_input("State Name (e.g., Delhi)")
# #         new_holiday_code = st.text_input("Holiday State Code (e.g., DL) *Optional", help="Used to calculate regional holidays. E.g., MH, TN, DL")
        
# #         if st.button("➕ Add Location"):
# #             if new_code and new_city and new_state:
# #                 # 1. Add to Location Mapping
# #                 st.session_state.location_mapping[new_code] = {"City": new_city, "State": new_state}
# #                 # 2. Add to State Codes if provided
# #                 if new_holiday_code:
# #                     st.session_state.state_codes[new_state] = new_holiday_code.upper()
# #                 st.success(f"Successfully added {new_code} mapping!")
# #                 st.rerun() # Refresh the page to apply the new mapping immediately
# #             else:
# #                 st.warning("Please fill in Code, City, and State.")


# # st.title("🧳 Locker Data Processor & Analytics")

# # tab1, tab2, tab3 = st.tabs(["⚙️ Data Processing", "📊 Advanced Analytics Dashboard", "🛠️ Hardware Optimizer"])

# # loc_rev = pd.DataFrame()
# # city_rev = pd.DataFrame()
# # time_dist = pd.DataFrame()
# # user_df = pd.DataFrame()
# # repeat_users = pd.DataFrame()
# # loc_repeat_stats = pd.DataFrame()
# # processed_df = pd.DataFrame()
# # backend_df = None

# # with tab1:
# #     st.write("Upload files to map missing locations or generate backend reports.")
# #     col1, col2 = st.columns(2)
# #     with col1:
# #         settlement_file = st.file_uploader("1. Upload Settlement .xlsx/.csv (Optional)", type=['xlsx', 'csv'], key="settlement")
# #     with col2:
# #         backend_file = st.file_uploader("2. Upload Backend .xlsx/.csv (For Analytics)", type=['xlsx', 'csv'], key="backend")

# #     if backend_file is not None:
# #         try:
# #             backend_df = pd.read_csv(backend_file) if backend_file.name.endswith('.csv') else pd.read_excel(backend_file)
# #             loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats = generate_backend_analytics(backend_df)
# #             st.success("✅ Backend data loaded & Analytics generated!")
# #         except Exception as e:
# #             st.error(f"Error processing Backend Data: {e}")

# #     if settlement_file is not None:
# #         try:
# #             df = pd.read_csv(settlement_file) if settlement_file.name.endswith('.csv') else pd.read_excel(settlement_file)
# #             processed_df = process_dataframe(df, backend_df)
# #             st.success("✅ Settlement mapping complete!")
# #             st.write("### Processed Data Preview")
# #             st.dataframe(processed_df[['entity_id', 'payment_notes', 'City', 'State']].head())
# #         except Exception as e:
# #             st.error(f"Error processing Settlement Data: {e}")

# #     if settlement_file is not None or backend_file is not None:
# #         output = io.BytesIO()
# #         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
# #             if not processed_df.empty:
# #                 processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
            
# #             if backend_file is not None:
# #                 if not loc_rev.empty: loc_rev.to_excel(writer, index=False, sheet_name='Bank_Performance')
# #                 if not city_rev.empty: city_rev.to_excel(writer, index=False, sheet_name='Revenue_By_City')
# #                 if not time_dist.empty: time_dist.to_excel(writer, index=False, sheet_name='Time_of_Day_Stats')
# #                 if not loc_repeat_stats.empty: loc_repeat_stats.to_excel(writer, index=False, sheet_name='Loyalty_Stats')
# #                 if not user_df.empty:
# #                     user_df.to_excel(writer, index=False, sheet_name='All_User_Analytics')
# #                     repeat_users.to_excel(writer, index=False, sheet_name='Top_Repeat_Users')

# #         st.download_button(
# #             label="📥 Download Advanced Multi-Sheet Report",
# #             data=output.getvalue(),
# #             file_name="Advanced_Locker_Report.xlsx",
# #             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #         )

# # with tab2:
# #     if backend_file is None:
# #         st.info("👈 Please upload the Backend Data file in the 'Data Processing' tab to view analytics.")
# #     else:
# #         st.subheader("📊 Backend Operations Insights")
        
# #         if loc_rev.empty and city_rev.empty:
# #             st.error("⚠️ No usable data found. All rows were filtered out.")
# #         else:
# #             c1, c2 = st.columns(2)
# #             with c1:
# #                 st.write("### 🕒 Bookings by Time of Day")
# #                 st.dataframe(time_dist, use_container_width=True)
                
# #             with c2:
# #                 st.write("### 🏙️ Revenue by City")
# #                 st.dataframe(city_rev, use_container_width=True)
                
# #             st.markdown("---")
# #             st.write("### 📍 Location Performance: Revenue, Entropy & Size Distribution")
# #             st.caption("Displays Completed Revenue vs Initiated Revenue, and exact % of locker sizes booked.")
# #             st.dataframe(loc_rev, use_container_width=True)
            
# #             st.markdown("---")
# #             st.write("### 💎 Location-Wise Repeat Customer Behavior")
# #             if not loc_repeat_stats.empty:
# #                 st.dataframe(loc_repeat_stats, use_container_width=True)
# #             else:
# #                 st.warning("Not enough repeat users to generate loyalty stats.")
            
# #             st.markdown("---")
# #             st.subheader("👥 User Behavior & Cohort Inferences")
            
# #             if not user_df.empty:
# #                 total_users = len(user_df)
# #                 total_repeat = len(repeat_users)
# #                 repeat_rate = (total_repeat / total_users) * 100 if total_users > 0 else 0
                
# #                 kpi1, kpi2, kpi3 = st.columns(3)
# #                 kpi1.metric("Total Unique Users", f"{total_users}")
# #                 kpi2.metric("Highly Loyal Users (≥2 bookings)", f"{total_repeat}")
# #                 kpi3.metric("Customer Retention Rate", f"{repeat_rate:.1f}%")
                
# #                 st.write("### 🏆 Top Repeat Customers Profile")
# #                 display_cols = ['User Mobile', 'total_transactions', 'active_days', 'total_amount']
# #                 display_cols = [c for c in display_cols if c in repeat_users.columns] 
# #                 if 'dominant_size' in repeat_users.columns:
# #                     display_cols.extend(['dominant_size', 'size_entropy'])
                    
# #                 if not repeat_users.empty:
# #                     st.dataframe(repeat_users.sort_values('total_transactions', ascending=False)[display_cols].head(15), use_container_width=True)

# # with tab3:
# #     st.subheader("🛠️ AI Hardware Layout Optimizer")
# #     st.write("Use historical backend data to generate optimal locker blueprints for new sites using PuLP.")
    
# #     if backend_file is not None and not loc_rev.empty:
# #         try:
# #             import pulp
# #             c1, c2 = st.columns(2)
# #             with c1:
# #                 target_station = st.selectbox("Select existing station to use as Demand Profile:", loc_rev['Locker Bank'].tolist())
# #                 total_cols_available = st.number_input("Max Columns Available at New Site:", min_value=10, max_value=200, value=46)
            
# #             with c2:
# #                 st.info("Physical Hardware Specs")
# #                 lockers_per_col_M = st.number_input("M Lockers per column:", value=4)
# #                 lockers_per_col_L = st.number_input("L Lockers per column:", value=3)
# #                 lockers_per_col_XL = st.number_input("XL Lockers per column:", value=2)

# #             station_data = loc_rev[loc_rev['Locker Bank'] == target_station].iloc[0]
            
# #             st.write("---")
# #             st.write(f"**Extracted Live Profile for {target_station}:**")
# #             st.write(f"Average Order Value: ₹{station_data['AOV']}")
            
# #             if st.button("🚀 Run PuLP Optimization"):
# #                 with st.spinner("Running integer optimization..."):
# #                     base_aov = station_data['AOV']
# #                     rev_per_locker = {'M': base_aov * 0.8, 'L': base_aov * 1.2, 'XL': base_aov * 1.8}
# #                     lockers_per_column = {'M': lockers_per_col_M, 'L': lockers_per_col_L, 'XL': lockers_per_col_XL}
                    
# #                     pct_m = float(str(station_data.get('% M', '0')).replace('%','')) / 100
# #                     pct_l = float(str(station_data.get('% L', '0')).replace('%','')) / 100
# #                     pct_xl = float(str(station_data.get('% XL', '0')).replace('%','')) / 100
                    
# #                     min_columns = {
# #                         'M': max(2, int(total_cols_available * pct_m * 0.5)),
# #                         'L': max(2, int(total_cols_available * pct_l * 0.5)),
# #                         'XL': max(2, int(total_cols_available * pct_xl * 0.5))
# #                     }

# #                     prob = pulp.LpProblem("Locker_Revenue_Optimization", pulp.LpMaximize)
# #                     c = pulp.LpVariable.dicts("columns", ['M', 'L', 'XL'], lowBound=0, cat='Integer')

# #                     prob += pulp.lpSum(c[size] * lockers_per_column[size] * rev_per_locker[size] for size in ['M', 'L', 'XL'])
# #                     prob += pulp.lpSum(c[size] for size in ['M', 'L', 'XL']) <= total_cols_available
# #                     for size in ['M', 'L', 'XL']: prob += c[size] >= min_columns[size]

# #                     prob.solve(pulp.PULP_CBC_CMD(msg=0))

# #                     if pulp.LpStatus[prob.status] == 'Optimal':
# #                         solution = {size: int(c[size].value()) for size in ['M', 'L', 'XL']}
# #                         st.success("✅ Optimal Blueprint Generated!")
# #                         r1, r2, r3 = st.columns(3)
# #                         r1.metric("Medium Columns", solution['M'], f"{solution['M'] * lockers_per_col_M} doors")
# #                         r2.metric("Large Columns", solution['L'], f"{solution['L'] * lockers_per_col_L} doors")
# #                         r3.metric("XL Columns", solution['XL'], f"{solution['XL'] * lockers_per_col_XL} doors")
# #                         st.write(f"**Projected Daily Revenue Capability:** ₹{int(pulp.value(prob.objective)):,}")
# #                     else:
# #                         st.error("Could not find an optimal solution with the given constraints.")
# #         except ImportError:
# #             st.error("⚠️ The `pulp` library is not installed. Please run `pip install pulp` in your terminal.")
# #     else:
# #         st.info("Upload backend data in Tab 1 to unlock the Hardware Optimizer.")
# # --- 4. Streamlit UI ---
# st.set_page_config(page_title="Locker Analytics Processor", layout="wide")

# # --- SIDEBAR FOR DYNAMIC LOCATION MAPPING ---
# with st.sidebar:
#     st.header("⚙️ Configuration")
#     with st.expander("📍 Add New Location Mapping", expanded=False):
#         st.write("Add missing locations so they map correctly to a City and State.")
#         new_code = st.text_input("Locker Bank Code (e.g., NDLS)")
#         new_city = st.text_input("City Name")
#         new_state = st.text_input("State Name (e.g., Delhi)")
#         new_holiday_code = st.text_input("Holiday State Code (e.g., DL) *Optional", help="Used to calculate regional holidays. E.g., MH, TN, DL")
        
#         if st.button("➕ Add Location"):
#             if new_code and new_city and new_state:
#                 st.session_state.location_mapping[new_code] = {"City": new_city, "State": new_state}
#                 if new_holiday_code:
#                     st.session_state.state_codes[new_state] = new_holiday_code.upper()
#                 st.success(f"Successfully added {new_code} mapping!")
#                 st.rerun()
#             else:
#                 st.warning("Please fill in Code, City, and State.")

# st.title("🧳 Locker Data Processor & Analytics")

# tab1, tab2, tab3 = st.tabs(["⚙️ Data Processing", "📊 Advanced Analytics Dashboard", "🛠️ Hardware Optimizer"])

# loc_rev = pd.DataFrame()
# city_rev = pd.DataFrame()
# time_dist = pd.DataFrame()
# user_df = pd.DataFrame()
# repeat_users = pd.DataFrame()
# loc_repeat_stats = pd.DataFrame()
# processed_df = pd.DataFrame()
# backend_df = None

# with tab1:
#     st.write("Upload multiple files to merge them and generate combined backend reports.")
#     col1, col2 = st.columns(2)
#     with col1:
#         # NEW: accept_multiple_files=True
#         settlement_files = st.file_uploader("1. Upload Settlement .xlsx/.csv (Optional)", type=['xlsx', 'csv'], accept_multiple_files=True, key="settlement")
#     with col2:
#         # NEW: accept_multiple_files=True
#         backend_files = st.file_uploader("2. Upload Backend .xlsx/.csv (For Analytics)", type=['xlsx', 'csv'], accept_multiple_files=True, key="backend")

#     if backend_files: # If the list is not empty
#         try:
#             # Loop through all uploaded files, read them, and combine into one DataFrame
#             dfs = [pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f) for f in backend_files]
#             backend_df = pd.concat(dfs, ignore_index=True)
            
#             loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats = generate_backend_analytics(backend_df)
#             st.success(f"✅ {len(backend_files)} Backend file(s) combined & Analytics generated!")
#         except Exception as e:
#             st.error(f"Error processing Backend Data: {e}")

#     if settlement_files:
#         try:
#             dfs = [pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f) for f in settlement_files]
#             df = pd.concat(dfs, ignore_index=True)
            
#             processed_df = process_dataframe(df, backend_df)
#             st.success(f"✅ {len(settlement_files)} Settlement file(s) combined & mapping complete!")
#             st.write("### Processed Data Preview")
#             st.dataframe(processed_df[['entity_id', 'payment_notes', 'City', 'State']].head())
#         except Exception as e:
#             st.error(f"Error processing Settlement Data: {e}")

#     if settlement_files or backend_files:
#         output = io.BytesIO()
#         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#             if not processed_df.empty:
#                 processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
            
#             if backend_files:
#                 if not loc_rev.empty: loc_rev.to_excel(writer, index=False, sheet_name='Bank_Performance')
#                 if not city_rev.empty: city_rev.to_excel(writer, index=False, sheet_name='Revenue_By_City')
#                 if not time_dist.empty: time_dist.to_excel(writer, index=False, sheet_name='Time_of_Day_Stats')
#                 if not loc_repeat_stats.empty: loc_repeat_stats.to_excel(writer, index=False, sheet_name='Loyalty_Stats')
#                 if not user_df.empty:
#                     user_df.to_excel(writer, index=False, sheet_name='All_User_Analytics')
#                     repeat_users.to_excel(writer, index=False, sheet_name='Top_Repeat_Users')

#         st.download_button(
#             label="📥 Download Combined Advanced Report",
#             data=output.getvalue(),
#             file_name="Combined_Advanced_Locker_Report.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

# with tab2:
#     if not backend_files:
#         st.info("👈 Please upload the Backend Data file(s) in the 'Data Processing' tab to view analytics.")
#     else:
#         st.subheader("📊 Backend Operations Insights")
        
#         if loc_rev.empty and city_rev.empty:
#             st.error("⚠️ No usable data found. All rows were filtered out.")
#         else:
#             c1, c2 = st.columns(2)
#             with c1:
#                 st.write("### 🕒 Bookings by Time of Day")
#                 st.dataframe(time_dist, use_container_width=True)
                
#             with c2:
#                 st.write("### 🏙️ Revenue by City")
#                 st.dataframe(city_rev, use_container_width=True)
                
#             st.markdown("---")
#             st.write("### 📍 Location Performance: Revenue, Entropy & Size Distribution")
#             st.caption("Displays Completed Revenue vs Initiated Revenue, and exact % of locker sizes booked.")
#             st.dataframe(loc_rev, use_container_width=True)
            
#             st.markdown("---")
#             st.write("### 💎 Location-Wise Repeat Customer Behavior")
#             if not loc_repeat_stats.empty:
#                 st.dataframe(loc_repeat_stats, use_container_width=True)
#             else:
#                 st.warning("Not enough repeat users to generate loyalty stats.")
            
#             st.markdown("---")
#             st.subheader("👥 User Behavior & Cohort Inferences")
            
#             if not user_df.empty:
#                 total_users = len(user_df)
#                 total_repeat = len(repeat_users)
#                 repeat_rate = (total_repeat / total_users) * 100 if total_users > 0 else 0
                
#                 kpi1, kpi2, kpi3 = st.columns(3)
#                 kpi1.metric("Total Unique Users", f"{total_users}")
#                 kpi2.metric("Highly Loyal Users (≥2 bookings)", f"{total_repeat}")
#                 kpi3.metric("Customer Retention Rate", f"{repeat_rate:.1f}%")
                
#                 st.write("### 🏆 Top Repeat Customers Profile")
#                 display_cols = ['User Mobile', 'total_transactions', 'active_days', 'total_amount']
#                 display_cols = [c for c in display_cols if c in repeat_users.columns] 
#                 if 'dominant_size' in repeat_users.columns:
#                     display_cols.extend(['dominant_size', 'size_entropy'])
                    
#                 if not repeat_users.empty:
#                     st.dataframe(repeat_users.sort_values('total_transactions', ascending=False)[display_cols].head(15), use_container_width=True)

# # with tab3:
# #     st.subheader("🛠️ AI Hardware Layout Optimizer")
# #     st.write("Use historical backend data to generate optimal locker blueprints for new sites using PuLP.")
    
# #     if backend_files and not loc_rev.empty:
# #         try:
# #             import pulp
# #             c1, c2 = st.columns(2)
# #             with c1:
# #                 target_station = st.selectbox("Select existing station to use as Demand Profile:", loc_rev['Locker Bank'].tolist())
# #                 total_cols_available = st.number_input("Max Columns Available at New Site:", min_value=10, max_value=200, value=46)
            
# #             with c2:
# #                 st.info("Physical Hardware Specs")
# #                 lockers_per_col_M = st.number_input("M Lockers per column:", value=4)
# #                 lockers_per_col_L = st.number_input("L Lockers per column:", value=3)
# #                 lockers_per_col_XL = st.number_input("XL Lockers per column:", value=2)

# #             station_data = loc_rev[loc_rev['Locker Bank'] == target_station].iloc[0]
            
# #             st.write("---")
# #             st.write(f"**Extracted Live Profile for {target_station}:**")
# #             st.write(f"Average Order Value: ₹{station_data['AOV']}")
            
# #             if st.button("🚀 Run PuLP Optimization"):
# #                 with st.spinner("Running integer optimization..."):
# #                     base_aov = station_data['AOV']
# #                     rev_per_locker = {'M': base_aov * 0.8, 'L': base_aov * 1.2, 'XL': base_aov * 1.8}
# #                     lockers_per_column = {'M': lockers_per_col_M, 'L': lockers_per_col_L, 'XL': lockers_per_col_XL}
                    
# #                     pct_m = float(str(station_data.get('% M', '0')).replace('%','')) / 100
# #                     pct_l = float(str(station_data.get('% L', '0')).replace('%','')) / 100
# #                     pct_xl = float(str(station_data.get('% XL', '0')).replace('%','')) / 100
                    
# #                     min_columns = {
# #                         'M': max(2, int(total_cols_available * pct_m * 0.5)),
# #                         'L': max(2, int(total_cols_available * pct_l * 0.5)),
# #                         'XL': max(2, int(total_cols_available * pct_xl * 0.5))
# #                     }

# #                     prob = pulp.LpProblem("Locker_Revenue_Optimization", pulp.LpMaximize)
# #                     c = pulp.LpVariable.dicts("columns", ['M', 'L', 'XL'], lowBound=0, cat='Integer')

# #                     prob += pulp.lpSum(c[size] * lockers_per_column[size] * rev_per_locker[size] for size in ['M', 'L', 'XL'])
# #                     prob += pulp.lpSum(c[size] for size in ['M', 'L', 'XL']) <= total_cols_available
# #                     for size in ['M', 'L', 'XL']: prob += c[size] >= min_columns[size]

# #                     prob.solve(pulp.PULP_CBC_CMD(msg=0))

# #                     if pulp.LpStatus[prob.status] == 'Optimal':
# #                         solution = {size: int(c[size].value()) for size in ['M', 'L', 'XL']}
# #                         st.success("✅ Optimal Blueprint Generated!")
# #                         r1, r2, r3 = st.columns(3)
# #                         r1.metric("Medium Columns", solution['M'], f"{solution['M'] * lockers_per_col_M} doors")
# #                         r2.metric("Large Columns", solution['L'], f"{solution['L'] * lockers_per_col_L} doors")
# #                         r3.metric("XL Columns", solution['XL'], f"{solution['XL'] * lockers_per_col_XL} doors")
# #                         st.write(f"**Projected Daily Revenue Capability:** ₹{int(pulp.value(prob.objective)):,}")
# #                     else:
# #                         st.error("Could not find an optimal solution with the given constraints.")
# #         except ImportError:
# #             st.error("⚠️ The `pulp` library is not installed. Please run `pip install pulp` in your terminal.")
# #     else:
# #         st.info("Upload backend data in Tab 1 to unlock the Hardware Optimizer.")

import streamlit as st
import pandas as pd
import json
import re
import io
import numpy as np
from scipy.stats import entropy
import holidays
# import pulp

# --- 1. Define the Mapping Dictionaries (Session State) ---
if 'location_mapping' not in st.session_state:
    st.session_state.location_mapping = {
        "THVM": {"City": "Thivim", "State": "Goa"},
        "katpadi": {"City": "Katpadi", "State": "Tamil Nadu"},
        "CHZ": {"City": "Charlapalli", "State": "Telangana"},
        "PUNE": {"City": "Pune", "State": "Maharashtra"},
        "AJMER": {"City": "Ajmer", "State": "Rajasthan"},
        "BSP": {"City": "Bilaspur", "State": "Chhattisgarh"},
        "Visvesvaraya Museum": {"City": "Bengaluru", "State": "Karnataka"},
        "Varanasi": {"City": "Varanasi", "State": "Uttar Pradesh"},
        "Nagpur": {"City": "Nagpur", "State": "Maharashtra"},
        "KRP": {"City": "Krishna Raj Puram", "State": "Karnataka"},
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

if 'state_codes' not in st.session_state:
    st.session_state.state_codes = {
        'Maharashtra': 'MH', 'Tamil Nadu': 'TN', 'Goa': 'GA', 'Telangana': 'TG',
        'Rajasthan': 'RJ', 'Chhattisgarh': 'CG', 'Karnataka': 'KA', 'Uttar Pradesh': 'UP',
        'Odisha': 'OR', 'Punjab': 'PB', 'Gujarat': 'GJ', 'West Bengal': 'WB',
        'Jharkhand': 'JH', 'Kerala': 'KL'
    }

mapping_lower = {k.lower(): v for k, v in st.session_state.location_mapping.items()}
state_codes = st.session_state.state_codes

# --- 2. Helper Functions ---
def extract_locker_bank(notes):
    if pd.isna(notes): return ""
    try:
        data = json.loads(notes)
        locker_name = data.get("Locker Bank Name", data.get("lockerBankName", ""))
        if locker_name and locker_name.strip().lower() != "luggage": return locker_name
        locker_location = data.get("lockerBankLocation", "")
        if locker_location and locker_location.strip().lower() not in ["", "luggage"]: return locker_location
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
        backend_cols_lower = [c.strip().lower() for c in backend_df.columns]
        if 'payment id' in backend_cols_lower and 'locker bank' in backend_cols_lower:
            backend_df_clean = backend_df.copy()
            backend_df_clean.columns = backend_cols_lower
            
            unknown_mask = df['City'] == "Unknown"
            if unknown_mask.any():
                backend_lookup = backend_df_clean.drop_duplicates(subset=['payment id']).set_index('payment id')['locker bank'].to_dict()
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

def generate_backend_analytics(raw_backend_df, raw_refund_df=None):
    df_filtered = raw_backend_df.copy()
    df_filtered.columns = df_filtered.columns.str.strip().str.lower()
    
    # --- 1. SAFELY PROCESS AMOUNTS & STATUS (Using np.where) ---
    if 'amount' in df_filtered.columns:
        clean_amount = df_filtered['amount'].astype(str).str.replace(',', '', regex=True)
        df_filtered['amount'] = pd.to_numeric(clean_amount, errors='coerce').fillna(0)
    else:
        df_filtered['amount'] = 0

    if 'status' in df_filtered.columns:
        status_clean = df_filtered['status'].astype(str).str.lower()
    
    if 'payment type' in df_filtered.columns:
        payment_clean = df_filtered['payment type'].astype(str).str.lower()
        
        is_completed = status_clean.str.contains('complet', na=False)
        is_initiated = status_clean.str.contains('initiat', na=False)
        is_overdue = payment_clean.str.contains('overdue', na=False)
        
        df_filtered['Completed_Amount'] = np.where(is_completed, df_filtered['amount'], 0)
        df_filtered['Initiated_Amount'] = np.where(is_initiated, df_filtered['amount'], 0)
        df_filtered['Overdue_Amount'] = np.where(is_overdue, df_filtered['amount'], 0)
        df_filtered['Is_Completed'] = np.where(is_completed, 1, 0)
        df_filtered['Is_Initiated'] = np.where(is_initiated, 1, 0)
    else:
        df_filtered['Completed_Amount'] = df_filtered['amount']
        df_filtered['Initiated_Amount'] = 0
        df_filtered['Is_Completed'] = 1
        df_filtered['Is_Initiated'] = 0

    # --- 1B. NEW: INTEGRATE REFUND DATA ---
    df_filtered['Refunded_Amount'] = 0 # Default if no file provided
    
    if raw_refund_df is not None and not raw_refund_df.empty:
        rdf = raw_refund_df.copy()
        rdf.columns = rdf.columns.str.strip().str.lower()
        
        # Standardize payment id column name from the refund file
        if 'payment id' in rdf.columns:
            rdf.rename(columns={'payment id': 'payment_id'}, inplace=True)
            
        if 'payment_id' in rdf.columns and 'amount' in rdf.columns:
            # Filter for processed refunds only
            if 'status' in rdf.columns:
                rdf = rdf[rdf['status'].astype(str).str.lower().str.contains('process', na=False)]
            
            clean_ref_amt = rdf['amount'].astype(str).str.replace(',', '', regex=True)
            rdf['refund_amount_val'] = pd.to_numeric(clean_ref_amt, errors='coerce').fillna(0)
            
            # Group by payment_id (in case a single transaction had multiple partial refunds)
            refund_agg = rdf.groupby('payment_id')['refund_amount_val'].sum().reset_index()
            
            # Map it onto the backend dataframe using a LEFT JOIN
            if 'payment id' in df_filtered.columns:
                df_filtered = df_filtered.merge(refund_agg, left_on='payment id', right_on='payment_id', how='left')
                df_filtered['Refunded_Amount'] = df_filtered['refund_amount_val'].fillna(0)

    # --- Location Mapping ---
    if 'locker bank' in df_filtered.columns:
        df_filtered['cleaned_location'] = df_filtered['locker bank'].astype(str).apply(clean_locker_name)
        df_filtered['city'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
        df_filtered['state'] = df_filtered['cleaned_location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))

    # --- Time, Weekend & Holiday Analysis ---
    if 'date created' in df_filtered.columns:
        df_filtered['date created'] = pd.to_datetime(df_filtered['date created'], errors='coerce')
        df_filtered['date_only'] = df_filtered['date created'].dt.date
        df_filtered['is_weekend'] = df_filtered['date created'].dt.weekday >= 5
        
        def check_holiday(row):
            try:
                state_name = row.get('state', '')
                code = state_codes.get(state_name)
                if code and pd.notna(row['date_only']):
                    in_holidays = holidays.IN(subdiv=code, years=row['date_only'].year)
                    return row['date_only'] in in_holidays
            except: pass
            return False
            
        df_filtered['is_holiday'] = df_filtered.apply(check_holiday, axis=1)
        df_filtered['is_weekend_or_holiday'] = df_filtered['is_weekend'] | df_filtered['is_holiday']

        def get_tod(hour):
            if pd.isna(hour): return 'Unknown'
            if 6 <= hour < 12: return 'Morning (6AM - 12PM)'
            elif 12 <= hour < 18: return 'Afternoon (12PM - 6PM)'
            else: return 'Night (6PM - 6AM)'
            
        df_filtered['time_of_day'] = df_filtered['date created'].dt.hour.apply(get_tod)
        time_dist = df_filtered[df_filtered['Is_Completed'] == 1]['time_of_day'].value_counts(normalize=True).reset_index()
        time_dist.columns = ['Time of Day', 'Percentage']
        time_dist['Percentage'] = (time_dist['Percentage'] * 100).round(2).astype(str) + '%'
    else:
        time_dist = pd.DataFrame()

    # --- Location Performance ---
    def calc_entropy(series):
        counts = series.value_counts(normalize=True)
        return -(counts * np.log2(counts)).sum()

    loc_rev = pd.DataFrame()
    if 'locker bank' in df_filtered.columns:
        loc_rev = df_filtered.groupby('locker bank').agg(
            Total_Revenue=('Completed_Amount', 'sum'),
            Refunded_amount=('Refunded_Amount', 'sum'), # <--- NEW REFUND METRIC ADDED!
            Overdue_Revenue=('Overdue_Amount', 'sum'), 
            Initiated_Revenue=('Initiated_Amount', 'sum'),
            Total_Transactions=('Is_Completed', 'sum'),
            Total_Initiated_Transactions=('Is_Initiated', 'sum'),
            Pct_Weekend_Holiday=('is_weekend_or_holiday', 'mean')
        ).reset_index()
        
        loc_rev.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
        
        loc_rev['AOV'] = (loc_rev['Total_Revenue'] / loc_rev['Total_Transactions'].replace(0, 1)).round(2)
        loc_rev['Total_Revenue'] = loc_rev['Total_Revenue'].round(2)
        loc_rev['Refunded_amount'] = loc_rev['Refunded_amount'].round(2) # <--- Clean rounding
        loc_rev['Initiated_Revenue'] = loc_rev['Initiated_Revenue'].round(2)
        loc_rev['Pct_Weekend_Holiday'] = (loc_rev['Pct_Weekend_Holiday'] * 100).round(1).astype(str) + '%'
        loc_rev = loc_rev.sort_values(by='Total_Revenue', ascending=False)
        
        df_completed = df_filtered[df_filtered['Is_Completed'] == 1]
        
        if 'locker size' in df_completed.columns:
            entropy_df = df_completed.groupby('locker bank')['locker size'].apply(calc_entropy).reset_index(name='Size Entropy')
            entropy_df.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
            loc_rev = pd.merge(loc_rev, entropy_df, on='Locker Bank', how='left')
            loc_rev['Size Entropy'] = loc_rev['Size Entropy'].round(3)
            
            bank_sizes = pd.crosstab(df_completed['locker bank'], df_completed['locker size'], normalize='index') * 100
            bank_sizes = bank_sizes.round(1).astype(str) + '%'
            bank_sizes.columns = [f"% {col}" for col in bank_sizes.columns]
            bank_sizes = bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
            loc_rev = pd.merge(loc_rev, bank_sizes, on='Locker Bank', how='left')

    # --- City Revenue ---
    if 'city' in df_filtered.columns:
        city_rev = df_filtered.groupby('city')['Completed_Amount'].sum().reset_index().sort_values(by='Completed_Amount', ascending=False)
        city_rev.rename(columns={'city': 'City', 'Completed_Amount': 'Amount'}, inplace=True)
    else:
        city_rev = pd.DataFrame()

    # --- User Behavior & Cohort Inferences ---
    user_df = pd.DataFrame()
    repeat_users = pd.DataFrame()
    loc_repeat_stats = pd.DataFrame()
    
    if 'user mobile' in df_filtered.columns and 'date updated' in df_filtered.columns:
        df_users = df_filtered[df_filtered['Is_Completed'] == 1].dropna(subset=['date updated', 'user mobile']).copy()
        
        if not df_users.empty:
            df_users['date updated'] = pd.to_datetime(df_users['date updated'], errors='coerce')
            df_users['date_only'] = df_users['date updated'].dt.date
            
            user_df = df_users.groupby('user mobile').agg(
                total_transactions=('Completed_Amount', 'count'),
                active_days=('date_only', 'nunique'),
                total_amount=('Completed_Amount', 'sum')
            ).reset_index()
            
            user_df.rename(columns={'user mobile': 'User Mobile'}, inplace=True)
            
            if 'locker size' in df_users.columns:
                size_map = {'Medium': 'M', 'Large': 'L', 'Extra Large': 'XL'}
                df_users['size_clean'] = df_users['locker size'].map(size_map).fillna('unknown')
                
                size_counts = df_users.groupby(['user mobile', 'size_clean']).size().unstack(fill_value=0)
                size_pct = size_counts.div(size_counts.sum(axis=1), axis=0).fillna(0) * 100
                size_pct = size_pct.rename(columns={'M': 'pct_M', 'L': 'pct_L', 'XL': 'pct_XL'})
                size_pct.index.name = 'User Mobile'
                
                user_df = user_df.merge(size_pct, on='User Mobile', how='left').fillna(0)
                
                size_cols = [c for c in ['pct_M', 'pct_L', 'pct_XL'] if c in user_df.columns]
                if size_cols:
                    user_df['dominant_size'] = user_df[size_cols].idxmax(axis=1).str.replace('pct_', '')
                    user_df['size_entropy'] = user_df[size_cols].apply(
                        lambda row: entropy(row.values / 100) if row.sum() > 0 else 0.0, axis=1
                    ).round(3)

            repeat_users = user_df[
                (user_df['total_transactions'] >= 2) & 
                (user_df['active_days'] >= 2)
            ].copy()
            
            if not repeat_users.empty and 'locker bank' in df_users.columns:
                repeat_mobiles = repeat_users['User Mobile'].tolist()
                df_rep_only = df_users[df_users['user mobile'].isin(repeat_mobiles)].copy()
                
                df_rep_only = df_rep_only.sort_values(['locker bank', 'user mobile', 'date updated'])
                df_rep_only['prev_date'] = df_rep_only.groupby(['locker bank', 'user mobile'])['date_only'].shift(1)
                df_rep_only['gap_days'] = (pd.to_datetime(df_rep_only['date_only']) - pd.to_datetime(df_rep_only['prev_date'])).dt.days

                loc_repeat_stats = df_rep_only.groupby('locker bank').agg(
                    Loyal_Transactions=('Completed_Amount', 'count'),
                    Avg_Gap_Days=('gap_days', 'mean')
                ).reset_index()
                
                loc_repeat_stats['Avg_Gap_Days'] = loc_repeat_stats['Avg_Gap_Days'].round(1)
                loc_repeat_stats.rename(columns={'locker bank': 'Locker Bank'}, inplace=True)
                
                if 'locker size' in df_rep_only.columns:
                    rep_bank_sizes = pd.crosstab(df_rep_only['locker bank'], df_rep_only['locker size'], normalize='index') * 100
                    rep_bank_sizes = rep_bank_sizes.round(1).astype(str) + '%'
                    rep_bank_sizes.columns = [f"Loyal % {col}" for col in rep_bank_sizes.columns]
                    rep_bank_sizes = rep_bank_sizes.reset_index().rename(columns={'locker bank': 'Locker Bank'})
                    loc_repeat_stats = pd.merge(loc_repeat_stats, rep_bank_sizes, on='Locker Bank', how='left')

    return loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats

# --- 4. Streamlit UI ---
st.set_page_config(page_title="Locker Analytics Processor", layout="wide")

with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("📍 Add New Location Mapping", expanded=False):
        st.write("Add missing locations so they map correctly to a City and State.")
        new_code = st.text_input("Locker Bank Code (e.g., NDLS)")
        new_city = st.text_input("City Name")
        new_state = st.text_input("State Name (e.g., Delhi)")
        new_holiday_code = st.text_input("Holiday State Code (e.g., DL) *Optional", help="Used to calculate regional holidays. E.g., MH, TN, DL")
        
        if st.button("➕ Add Location"):
            if new_code and new_city and new_state:
                st.session_state.location_mapping[new_code] = {"City": new_city, "State": new_state}
                if new_holiday_code:
                    st.session_state.state_codes[new_state] = new_holiday_code.upper()
                st.success(f"Successfully added {new_code} mapping!")
                st.rerun()
            else:
                st.warning("Please fill in Code, City, and State.")

st.title("🧳 Locker Data Processor & Analytics")

tab1, tab2, tab3 = st.tabs(["⚙️ Data Processing", "📊 Advanced Analytics Dashboard", "🛠️ Hardware Optimizer"])

loc_rev = pd.DataFrame()
city_rev = pd.DataFrame()
time_dist = pd.DataFrame()
user_df = pd.DataFrame()
repeat_users = pd.DataFrame()
loc_repeat_stats = pd.DataFrame()
processed_df = pd.DataFrame()
backend_df = None
refund_df = None

with tab1:
    st.write("Upload files to map missing locations or generate backend reports.")
    # UI updated to 3 columns to accommodate the Refund upload!
    col1, col2, col3 = st.columns(3)
    with col1:
        settlement_files = st.file_uploader("1. Settlement .xlsx/.csv", type=['xlsx', 'csv'], accept_multiple_files=True, key="settlement")
    with col2:
        backend_files = st.file_uploader("2. Backend .xlsx/.csv (Required for Analytics)", type=['xlsx', 'csv'], accept_multiple_files=True, key="backend")
    with col3:
        refund_files = st.file_uploader("3. Refund .xlsx/.csv (Optional)", type=['xlsx', 'csv'], accept_multiple_files=True, key="refund")

    # Process Refund Files first if they exist
    if refund_files:
        try:
            dfs = [pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f) for f in refund_files]
            refund_df = pd.concat(dfs, ignore_index=True)
            st.success(f"✅ {len(refund_files)} Refund file(s) loaded!")
        except Exception as e:
            st.error(f"Error processing Refund Data: {e}")

    # Process Backend Data & generate analytics
    if backend_files:
        try:
            dfs = [pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f) for f in backend_files]
            backend_df = pd.concat(dfs, ignore_index=True)
            # We now pass both the backend_df AND the refund_df into our analytics engine
            loc_rev, city_rev, time_dist, user_df, repeat_users, loc_repeat_stats = generate_backend_analytics(backend_df, refund_df)
            st.success(f"✅ {len(backend_files)} Backend file(s) combined & Analytics generated!")
        except Exception as e:
            st.error(f"Error processing Backend Data: {e}")

    # Process Settlement Data
    if settlement_files:
        try:
            dfs = [pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f) for f in settlement_files]
            df = pd.concat(dfs, ignore_index=True)
            
            processed_df = process_dataframe(df, backend_df)
            st.success(f"✅ {len(settlement_files)} Settlement file(s) combined & mapping complete!")
            st.write("### Processed Data Preview")
            st.dataframe(processed_df[['entity_id', 'payment_notes', 'City', 'State']].head())
        except Exception as e:
            st.error(f"Error processing Settlement Data: {e}")

    if settlement_files or backend_files:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if not processed_df.empty:
                processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
            
            if backend_files:
                if not loc_rev.empty: loc_rev.to_excel(writer, index=False, sheet_name='Bank_Performance')
                if not city_rev.empty: city_rev.to_excel(writer, index=False, sheet_name='Revenue_By_City')
                if not time_dist.empty: time_dist.to_excel(writer, index=False, sheet_name='Time_of_Day_Stats')
                if not loc_repeat_stats.empty: loc_repeat_stats.to_excel(writer, index=False, sheet_name='Loyalty_Stats')
                if not user_df.empty:
                    user_df.to_excel(writer, index=False, sheet_name='All_User_Analytics')
                    repeat_users.to_excel(writer, index=False, sheet_name='Top_Repeat_Users')

        st.download_button(
            label="📥 Download Combined Advanced Report",
            data=output.getvalue(),
            file_name="Combined_Advanced_Locker_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab2:
    if not backend_files:
        st.info("👈 Please upload the Backend Data file(s) in the 'Data Processing' tab to view analytics.")
    else:
        st.subheader("📊 Backend Operations Insights")
        
        if loc_rev.empty and city_rev.empty:
            st.error("⚠️ No usable data found. All rows were filtered out.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.write("### 🕒 Bookings by Time of Day")
                st.dataframe(time_dist, use_container_width=True)
                
            with c2:
                st.write("### 🏙️ Revenue by City")
                st.dataframe(city_rev, use_container_width=True)
                
            st.markdown("---")
            st.write("### 📍 Location Performance: Revenue, Entropy & Size Distribution")
            st.caption("Displays Total Revenue vs Refunded Revenue, and exact % of locker sizes booked.")
            st.dataframe(loc_rev, use_container_width=True)
            
            st.markdown("---")
            st.write("### 💎 Location-Wise Repeat Customer Behavior")
            if not loc_repeat_stats.empty:
                st.dataframe(loc_repeat_stats, use_container_width=True)
            else:
                st.warning("Not enough repeat users to generate loyalty stats.")
            
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
                display_cols = ['User Mobile', 'total_transactions', 'active_days', 'total_amount']
                display_cols = [c for c in display_cols if c in repeat_users.columns] 
                if 'dominant_size' in repeat_users.columns:
                    display_cols.extend(['dominant_size', 'size_entropy'])
                    
                if not repeat_users.empty:
                    st.dataframe(repeat_users.sort_values('total_transactions', ascending=False)[display_cols].head(15), use_container_width=True)

with tab3:
    st.subheader("🛠️ AI Hardware Layout Optimizer")
    st.write("Use historical backend data to generate optimal locker blueprints for new sites using PuLP.")
    
    if backend_files and not loc_rev.empty:
        try:
            import pulp
            c1, c2 = st.columns(2)
            with c1:
                target_station = st.selectbox("Select existing station to use as Demand Profile:", loc_rev['Locker Bank'].tolist())
                total_cols_available = st.number_input("Max Columns Available at New Site:", min_value=10, max_value=200, value=46)
            
            with c2:
                st.info("Physical Hardware Specs")
                lockers_per_col_M = st.number_input("M Lockers per column:", value=4)
                lockers_per_col_L = st.number_input("L Lockers per column:", value=3)
                lockers_per_col_XL = st.number_input("XL Lockers per column:", value=2)

            station_data = loc_rev[loc_rev['Locker Bank'] == target_station].iloc[0]
            
            st.write("---")
            st.write(f"**Extracted Live Profile for {target_station}:**")
            st.write(f"Average Order Value: ₹{station_data['AOV']}")
            
            if st.button("🚀 Run PuLP Optimization"):
                with st.spinner("Running integer optimization..."):
                    base_aov = station_data['AOV']
                    rev_per_locker = {'M': base_aov * 0.8, 'L': base_aov * 1.2, 'XL': base_aov * 1.8}
                    lockers_per_column = {'M': lockers_per_col_M, 'L': lockers_per_col_L, 'XL': lockers_per_col_XL}
                    
                    pct_m = float(str(station_data.get('% M', '0')).replace('%','')) / 100
                    pct_l = float(str(station_data.get('% L', '0')).replace('%','')) / 100
                    pct_xl = float(str(station_data.get('% XL', '0')).replace('%','')) / 100
                    
                    min_columns = {
                        'M': max(2, int(total_cols_available * pct_m * 0.5)),
                        'L': max(2, int(total_cols_available * pct_l * 0.5)),
                        'XL': max(2, int(total_cols_available * pct_xl * 0.5))
                    }

                    prob = pulp.LpProblem("Locker_Revenue_Optimization", pulp.LpMaximize)
                    c = pulp.LpVariable.dicts("columns", ['M', 'L', 'XL'], lowBound=0, cat='Integer')

                    prob += pulp.lpSum(c[size] * lockers_per_column[size] * rev_per_locker[size] for size in ['M', 'L', 'XL'])
                    prob += pulp.lpSum(c[size] for size in ['M', 'L', 'XL']) <= total_cols_available
                    for size in ['M', 'L', 'XL']: prob += c[size] >= min_columns[size]

                    prob.solve(pulp.PULP_CBC_CMD(msg=0))

                    if pulp.LpStatus[prob.status] == 'Optimal':
                        solution = {size: int(c[size].value()) for size in ['M', 'L', 'XL']}
                        st.success("✅ Optimal Blueprint Generated!")
                        r1, r2, r3 = st.columns(3)
                        r1.metric("Medium Columns", solution['M'], f"{solution['M'] * lockers_per_col_M} doors")
                        r2.metric("Large Columns", solution['L'], f"{solution['L'] * lockers_per_col_L} doors")
                        r3.metric("XL Columns", solution['XL'], f"{solution['XL'] * lockers_per_col_XL} doors")
                        st.write(f"**Projected Daily Revenue Capability:** ₹{int(pulp.value(prob.objective)):,}")
                    else:
                        st.error("Could not find an optimal solution with the given constraints.")
        except ImportError:
            st.error("⚠️ The `pulp` library is not installed. Please run `pip install pulp` in your terminal.")
    else:
        st.info("Upload backend data in Tab 1 to unlock the Hardware Optimizer.")