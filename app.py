import streamlit as st
import pandas as pd
import json
import re
import io

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
    "Tiruvannamalai Arunachaleswarar": {"City": "Tiruvannamalai", "State": "Tamil Nadu"},
    "Ayodhya": {"City": "Ayodhya", "State": "Uttar Pradesh"},
    "Lucknow": {"City": "Lucknow", "State": "Uttar Pradesh"},
    "SANTRAGACHI": {"City": "Howrah", "State": "West Bengal"},
    "Shalimar": {"City": "Howrah", "State": "West Bengal"},
    "Statue of Unity": {"City": "Kevadia", "State": "Gujarat"},
    "Ahmedabad": {"City": "Ahmedabad", "State": "Gujarat"},
    "Kozhikode": {"City": "Kozhikode", "State": "Kerala"} # Added Kozhikode
}

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
            else:
                return tenant
                
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

    # Step 1: Initial Extraction from JSON
    df['Raw_Locker_Bank'] = df['payment_notes'].apply(extract_locker_bank)
    df['Cleaned_Location'] = df['Raw_Locker_Bank'].apply(clean_locker_name)
    
    mapping_lower = {k.lower(): v for k, v in location_mapping.items()}
    
    df['City'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown"))
    df['State'] = df['Cleaned_Location'].apply(lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown"))
    
    # Step 2: Fallback to Backend Data if City is Unknown
    if backend_df is not None and 'entity_id' in df.columns:
        # Find which rows failed mapping
        unknown_mask = df['City'] == "Unknown"
        
        if unknown_mask.any():
            # Check if backend file has the required columns
            if 'Payment ID' in backend_df.columns and 'Locker Bank' in backend_df.columns:
                
                # Create a lookup dictionary mapping Payment ID -> Locker Bank
                backend_lookup = backend_df.drop_duplicates(subset=['Payment ID']).set_index('Payment ID')['Locker Bank'].to_dict()
                
                # Apply the lookup to find missing locker banks using entity_id
                df.loc[unknown_mask, 'Backend_Raw_Name'] = df.loc[unknown_mask, 'entity_id'].map(backend_lookup)
                
                # Clean the newly found backend names
                df.loc[unknown_mask, 'Backend_Cleaned'] = df.loc[unknown_mask, 'Backend_Raw_Name'].apply(clean_locker_name)
                
                # Map the City and State for these newly found locations
                df.loc[unknown_mask, 'City'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
                    lambda loc: mapping_lower.get(str(loc).lower(), {}).get("City", "Unknown") if pd.notna(loc) else "Unknown"
                )
                df.loc[unknown_mask, 'State'] = df.loc[unknown_mask, 'Backend_Cleaned'].apply(
                    lambda loc: mapping_lower.get(str(loc).lower(), {}).get("State", "Unknown") if pd.notna(loc) else "Unknown"
                )
                
                # Drop temporary backend lookup columns
                df = df.drop(columns=['Backend_Raw_Name', 'Backend_Cleaned'], errors='ignore')
            else:
                st.warning("Could not cross-reference. Backend file is missing 'Payment ID' or 'Locker Bank' columns.")

    # Drop intermediate columns
    df = df.drop(columns=['Raw_Locker_Bank', 'Cleaned_Location'])
    return df

# --- 4. Streamlit UI ---
st.set_page_config(page_title="Locker Settlement Processor", layout="wide")

st.title(" Locker Settlement Processor")
st.write("Upload your Settlement file. If some locations fail to map, upload the Backend Data to cross-reference them automatically.")

# Create two columns for uploading the two files side-by-side
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Settlement Data")
    settlement_file = st.file_uploader("Upload Settlement .xlsx/.csv", type=['xlsx', 'csv'], key="settlement")

with col2:
    st.subheader("2. Backend Data (Optional)")
    backend_file = st.file_uploader("Upload Backend .xlsx/.csv", type=['xlsx', 'csv'], key="backend")


if settlement_file is not None:
    try:
        # Load Settlement file
        df = pd.read_csv(settlement_file) if settlement_file.name.endswith('.csv') else pd.read_excel(settlement_file)
        
        # Load Backend file if provided
        backend_df = None
        if backend_file is not None:
            backend_df = pd.read_csv(backend_file) if backend_file.name.endswith('.csv') else pd.read_excel(backend_file)
            st.success("Both files loaded. Cross-referencing missing locations...")
        else:
            st.info("Processing without backend data. Any unmapped locations will show as 'Unknown'.")
        
        # Process data
        processed_df = process_dataframe(df, backend_df)
        
        # Show results
        st.write("### Data Preview (First 5 Rows)")
        st.dataframe(processed_df[['entity_id', 'payment_notes', 'City', 'State']].head())
        
        # Count unknowns
        unknowns = processed_df[processed_df['City'] == 'Unknown'].shape[0]
        if unknowns > 0:
            st.warning(f"⚠️ There are still {unknowns} rows with 'Unknown' locations.")
        else:
            st.success("✅ All locations mapped successfully!")
        
        # Download button
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            processed_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
        
        st.download_button(
            label="📥 Download Processed Excel File",
            data=output.getvalue(),
            file_name=f"Processed_{settlement_file.name.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"An error occurred: {e}")