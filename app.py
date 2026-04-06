import streamlit as st
import pandas as pd
import json
import re
import io

location_mapping = {     "THVM": {"City": "Thivim", "State": "Goa"},   "katpadi"  : {"City" : "katpadi",  "State" : "Tamil Nadu"},  "CHZ": {"City": "Charlapalli", "State": "Telangana"},     "PUNE": {"City": "Pune", "State": "Maharashtra"},     "AJMER": {"City": "Ajmer", "State": "Rajasthan"},     "BSP": {"City": "Bilaspur", "State": "Chhattisgarh"},     "Visvesvaraya Museum": {"City": "Bengaluru", "State": "Karnataka"},     "Varanasi": {"City": "Varanasi", "State": "Uttar Pradesh"},     "Nagpur": {"City": "Nagpur", "State": "Maharashtra"},     "KRP": {"City": "krishna raj puram", "State": "Bengalurur"}, "KP": {"City": "Pune", "State": "Maharashtra"}, "UD": {"City": "Udupi", "State": "Karnataka"},     "Ludhiana": {"City": "Ludhiana", "State": "Punjab"},     "Amritsar": {"City": "Amritsar", "State": "Punjab"},     "Nagapattinam": {"City": "Nagapattinam", "State": "Tamil Nadu"},     "Hubballi Bus Stand": {"City": "Hubballi", "State": "Karnataka"},     "Villupuram": {"City": "Villupuram", "State": "Tamil Nadu"},     "BRC": {"City": "Vadodara", "State": "Gujarat"},     "RN": {"City": "Ratnagiri", "State": "Maharashtra"},     "Tiruvannamalai": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},     "GHM": {"City": "Ghoom", "State": "West Bengal"},     "KSR": {"City": "Bengaluru", "State": "Karnataka"},"Melmaruvathur": {"City": "Melmaruvathur", "State": "Tamil Nadu"},     "Shirdi": {"City": "Shirdi", "State": "Maharashtra"},     "MMR": {"City": "Manmad", "State": "Maharashtra"},     "JAM": {"City": "Jamnagar", "State": "Gujarat"},     "Jasidih": {"City": "Jasidih", "State": "Jharkhand"},     "Manglore Central K": {"City": "Mangaluru", "State": "Karnataka"},     "Tirur": {"City": "Tirur", "State": "Kerala"},     "Kannur": {"City": "Kannur", "State": "Kerala"},     "CSMT": {"City": "Mumbai", "State": "Maharashtra"},     "Jalandhar": {"City": "Jalandhar", "State": "Punjab"},     "SEG": {"City": "Shegaon", "State": "Maharashtra"},     "Tiruvannamalai Arunachaleswarar": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},     "Ayodhya": {"City": "Ayodhya", "State": "Uttar Pradesh"},     "Lucknow": {"City": "Lucknow", "State": "Uttar Pradesh"},     "SANTRAGACHI": {"City": "Howrah", "State": "West Bengal"}, "Shalimar": {"City": "Howrah", "State": "West Bengal"}, "Statue of Unity": {"City": "Kevadia", "State": "Gujarat"}, "Ahmedabad": {"City": "Ahmedabad", "State": "Gujarat"} }
 
# def extract_locker_bank(notes):
#     if pd.isna(notes): return ""
#     try:
#         data = json.loads(notes)
#         return data.get("Locker Bank Name", data.get("lockerBankName", ""))
#     except:
#         return ""
# def extract_locker_bank(notes):
#     if pd.isna(notes): return ""
#     try:
#         data = json.loads(notes)
        
#         # 1. Try the normal keys first
#         locker_name = data.get("Locker Bank Name", data.get("lockerBankName", ""))
        
#         # 2. If the name is literally just "Luggage" (or empty), use the "tenant" key
#         if locker_name.strip().lower() == "luggage" or not locker_name:
#             tenant_name = data.get("tenant", "")
#             if tenant_name:
#                 return tenant_name # This will return "katpadi"
                
#         return locker_name
#     except:
#         return ""

def extract_locker_bank(notes):
    if pd.isna(notes): return ""
    try:
        data = json.loads(notes)
        
        # 1. Try standard name keys
        locker_name = data.get("Locker Bank Name", data.get("lockerBankName", ""))
        if locker_name and locker_name.strip().lower() != "luggage":
            return locker_name
            
        # 2. Try the newly discovered lockerBankLocation key!
        locker_location = data.get("lockerBankLocation", "")
        if locker_location and locker_location.strip().lower() not in ["", "luggage"]:
            return locker_location
            
        # 3. Check "tenant" key (If it's a URL, extract the word. If not, just use the word)
        tenant = data.get("tenant", "")
        if tenant:
            if "http" in tenant:
                match = re.search(r'://([^.]+)\.', tenant)
                if match: return match.group(1)
            else:
                return tenant
                
        # 4. Check "Tenant Name" or "tenant_host"
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
    return clean_name.strip()

def process_dataframe(df):
    if 'payment_notes' not in df.columns:
        st.error("Error: The uploaded file does not contain a 'payment_notes' column.")
        return df

    df['Raw_Locker_Bank'] = df['payment_notes'].apply(extract_locker_bank)
    df['Cleaned_Location'] = df['Raw_Locker_Bank'].apply(clean_locker_name)
    
    # NEW: Create a case-insensitive mapping dictionary on the fly
    mapping_lower = {k.lower(): v for k, v in location_mapping.items()}
    
    # NEW: Apply the mapping while forcing the search word to lowercase
    df['City'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
    df['State'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))
    
    df = df.drop(columns=['Raw_Locker_Bank', 'Cleaned_Location'])
    return df
    
st.set_page_config(page_title="Locker Settlement Processor", layout="centered")

st.title("🧳 Locker Settlement Processor")
st.write("Upload a settlement `.xlsx` or `.csv` file. The app will extract the locker location and append **City** and **State** columns.")

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=['xlsx', 'csv'])

if uploaded_file is not None:
    # Load the data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("File uploaded successfully! Processing data...")
        
        # Process the data
        processed_df = process_dataframe(df)
        
        # Show a preview of the processed data to the user
        st.write("### Data Preview (First 5 Rows)")
        st.dataframe(processed_df[['payment_notes', 'City', 'State']].head())
        
        # Convert DataFrame to an Excel file in memory for downloading
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
        
        # Create Download Button
        st.download_button(
            label="📥 Download Processed Excel File",
            data=output.getvalue(),
            file_name=f"Processed_{uploaded_file.name.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
