import streamlit as st
import pandas as pd
import json
import re
import io
import difflib
import csv
import base64
import urllib.request
from pathlib import Path

# Location -> City/State mapping lives in locations.csv (columns: Location, City, State).
# To add a new site, add a row there. "Location" can be written the way it appears in
# payment_notes (e.g. "Katpadi Railway Station - A"); it is cleaned the same way as the data.
LOCATIONS_FILE = Path(__file__).parent / "locations.csv"
NO_NAME = "(no locker name in payment_notes)"

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
    # Collapse gaps left by removed words (e.g. "KSR Railway Station Bengaluru" -> "KSR Bengaluru")
    clean_name = re.sub(r'\s+', ' ', clean_name).strip()
    clean_name = re.sub(r'(?i)[- ]+[A-G]$', '', clean_name)
    return clean_name.strip()

def normalize_location(name):
    """Lookup key used for BOTH the data and locations.csv, so they always compare like-for-like."""
    cleaned = clean_locker_name(name).lower()
    return re.sub(r'[^0-9a-z]+', ' ', cleaned).strip()

def load_location_mapping(path=LOCATIONS_FILE):
    """Read locations.csv fresh on every run so edits show up immediately.
    Returns (lookup {normalized_key: (City, State, Location)}, table for display, list of problems).
    Raises ValueError if the file is unusable."""
    table = pd.read_csv(path, dtype=str, keep_default_na=False, encoding='utf-8-sig')
    table.columns = [c.strip() for c in table.columns]
    missing = {'Location', 'City', 'State'} - set(table.columns)
    if missing:
        raise ValueError(f"{path.name} is missing column(s) {sorted(missing)}. Found: {list(table.columns)}")
    table = table[['Location', 'City', 'State']].apply(lambda col: col.str.strip())

    lookup, problems, conflicted = {}, [], set()
    for line_no, row in enumerate(table.itertuples(index=False), start=2):
        if not (row.Location and row.City and row.State):
            problems.append(f"Line {line_no}: '{row.Location}' skipped - Location, City and State are all required.")
            continue
        key = normalize_location(row.Location)
        if not key:
            problems.append(f"Line {line_no}: '{row.Location}' skipped - nothing left after removing words like Station/Railway/Luggage.")
            continue
        value = (row.City, row.State, row.Location)
        if key in lookup and lookup[key][:2] != value[:2]:
            problems.append(
                f"Line {line_no}: '{row.Location}' conflicts with '{lookup[key][2]}' "
                f"({lookup[key][0]}, {lookup[key][1]} vs {row.City}, {row.State}). Both ignored until fixed."
            )
            conflicted.add(key)
        lookup.setdefault(key, value)
    for key in conflicted:
        del lookup[key]
    return lookup, table, problems

def match_location(raw_name, lookup):
    """Returns (City, State, match_type, matched_location).
    1. exact: cleaned name equals a cleaned Location.
    2. partial: a Location appears as whole words inside the name (e.g. "KSR Bengaluru" -> KSR).
       If the words found point to different City/State, it is NOT guessed (ambiguous)."""
    if not raw_name:
        return "Unknown", "Unknown", "no name", ""
    key = normalize_location(raw_name)
    if key in lookup:
        city, state, loc = lookup[key]
        return city, state, "exact", loc

    tokens = key.split()
    # Known City names count as words to look for too (e.g. "Udupi" -> Udupi, Karnataka)
    candidates = list(lookup.items()) + [
        (normalize_location(city), (city, state, f"City: {city}")) for city, state, _ in lookup.values()
    ]
    hits = []
    for loc_key, value in candidates:
        if not loc_key: continue
        loc_tokens = loc_key.split()
        n = len(loc_tokens)
        for i in range(len(tokens) - n + 1):
            if tokens[i:i + n] == loc_tokens:
                hits.append((i, i + n, value))
    # Ignore a hit that sits inside a longer hit ("Tiruvannamalai" inside "Tiruvannamalai Arunachaleswarar")
    hits = [h for h in hits if not any(o is not h and o[0] <= h[0] and h[1] <= o[1] and (o[1] - o[0]) > (h[1] - h[0]) for o in hits)]
    places = {h[2][:2] for h in hits}
    if len(places) == 1:
        city, state, _ = hits[0][2]
        labels = sorted({h[2][2] for h in hits if not h[2][2].startswith("City: ")}) or [hits[0][2][2]]
        return city, state, "partial", " / ".join(labels)
    if len(places) > 1:
        return "Unknown", "Unknown", "ambiguous", " / ".join(sorted({h[2][2] for h in hits}))
    return "Unknown", "Unknown", "not found", ""

def process_dataframe(df, lookup):
    """Returns (processed_df, review_df). Caller must ensure 'payment_notes' exists."""
    raw_names = df['payment_notes'].apply(extract_locker_bank).map(lambda n: n if isinstance(n, str) else str(n))
    # Match each distinct locker name once
    results = {name: match_location(name, lookup) for name in raw_names.unique()}
    df['City'] = raw_names.map(lambda n: results[n][0])
    df['State'] = raw_names.map(lambda n: results[n][1])

    counts = raw_names.value_counts()
    sample_notes = df['payment_notes'].groupby(raw_names).first()
    lookup_names = {normalize_location(v[2]): v[2] for v in lookup.values()}
    review_rows = []
    for name, (city, state, match_type, matched) in results.items():
        if match_type == "exact":
            continue
        suggestion = ""
        if match_type == "not found":
            close = difflib.get_close_matches(normalize_location(name), list(lookup_names), n=1, cutoff=0.75)
            suggestion = lookup_names[close[0]] if close else ""
        review_rows.append({
            "Locker_Name_Found": name or NO_NAME,
            "Lookup_Key": normalize_location(name),
            "Result": match_type,
            "Matched_Location": matched,
            "City": city,
            "State": state,
            "Did_You_Mean (not applied)": suggestion,
            "Rows": int(counts[name]),
            "Sample_payment_notes": "" if name else str(sample_notes[name])[:300],
        })
    review_df = pd.DataFrame(review_rows, columns=[
        "Locker_Name_Found", "Lookup_Key", "Result", "Matched_Location", "City", "State",
        "Did_You_Mean (not applied)", "Rows", "Sample_payment_notes"])
    review_df = review_df.sort_values('Rows', ascending=False).reset_index(drop=True)
    return df, review_df

def to_excel_bytes(df):
    # Excel cannot store timezone-aware datetimes; keep the same wall-clock time, drop only the tz label
    export_df = df.copy()
    for col in export_df.select_dtypes(include=['datetimetz']).columns:
        export_df[col] = export_df[col].dt.tz_localize(None)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Processed_Settlements')
    return output.getvalue()

INDIAN_STATES = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
    "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry",
    "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal",
]

def _append_rows_to_csv_text(text, rows):
    """Append (Location, City, State) rows to existing CSV text, with correct quoting."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    for row in rows:
        writer.writerow(row)
    if text and not text.endswith("\n"):
        text += "\r\n"
    return text + buffer.getvalue()

def _save_to_github(rows):
    """Commit new rows to locations.csv in GitHub so they survive restarts/redeploys.
    Needs st.secrets["github"] = {token, repo, branch (optional), path (optional)}.
    Returns (True, msg) / (False, msg) / (None, msg) when GitHub is not configured."""
    try:
        cfg = st.secrets["github"]
        token, repo = cfg["token"], cfg["repo"]
    except Exception:
        return None, "GitHub saving is not configured"
    branch, path = cfg.get("branch", "main"), cfg.get("path", "locations.csv")
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
               "User-Agent": "locker-settlement-app"}
    try:
        req = urllib.request.Request(f"{url}?ref={branch}", headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            current = json.loads(resp.read())
        remote_text = base64.b64decode(current["content"]).decode("utf-8-sig")
        # Never write a row the remote file already has (e.g. someone else added it a moment ago)
        remote_keys = {normalize_location(r[0]) for r in csv.reader(io.StringIO(remote_text)) if r}
        new_rows = [r for r in rows if normalize_location(r[0]) not in remote_keys]
        if not new_rows:
            return True, "already in GitHub"
        body = json.dumps({
            "message": f"Add {len(new_rows)} location(s) via app: " + ", ".join(r[0] for r in new_rows)[:150],
            "content": base64.b64encode(_append_rows_to_csv_text(remote_text, new_rows).encode("utf-8")).decode(),
            "sha": current["sha"], "branch": branch,
        }).encode()
        put = urllib.request.Request(url, data=body, headers=headers, method="PUT")
        with urllib.request.urlopen(put, timeout=20) as resp:
            resp.read()
        return True, "saved to GitHub"
    except Exception as e:
        return False, f"GitHub save failed: {e}"

def save_new_locations(rows, lookup):
    """Validate and save [(Location, City, State)]. Returns (saved_count, messages)."""
    messages, to_save, seen = [], [], set()
    for location, city, state in rows:
        location, city, state = location.strip(), city.strip(), state.strip()
        key = normalize_location(location)
        if not (location and city and state):
            messages.append(f"'{location}': Location, City and State are all required."); continue
        if not key:
            messages.append(f"'{location}': nothing left after removing words like Station/Railway/Luggage."); continue
        if state not in INDIAN_STATES:
            messages.append(f"'{location}': '{state}' is not a recognised State/UT."); continue
        if key in lookup:
            existing = lookup[key]
            if existing[:2] == (city, state):
                continue  # already present, nothing to do
            messages.append(f"'{location}' already exists as '{existing[2]}' -> {existing[0]}, {existing[1]}. Not changed.")
            continue
        if key in seen:
            messages.append(f"'{location}' was entered twice."); continue
        seen.add(key)
        to_save.append((location, city, state))
    if not to_save:
        return 0, messages

    # 1) local file: visible to the app immediately
    try:
        text = LOCATIONS_FILE.read_text(encoding="utf-8-sig") if LOCATIONS_FILE.exists() else "Location,City,State\r\n"
        LOCATIONS_FILE.write_text(_append_rows_to_csv_text(text, to_save), encoding="utf-8", newline="")
    except Exception as e:
        return 0, messages + [f"Could not save: {e}"]
    # 2) GitHub: makes it permanent across restarts/redeploys
    ok, info = _save_to_github(to_save)
    if ok is None:
        messages.append("⚠️ Saved on this server only. It may be lost when the app restarts, because permanent saving "
                        "(GitHub) is not set up. Ask the app owner to configure it.")
    elif ok is False:
        messages.append(f"⚠️ Saved on this server only. {info}. It may be lost when the app restarts.")
    return len(to_save), messages

def render_add_locations(unknown):
    """Form to map unmatched locker names directly from the page."""
    todo = unknown[(unknown['Result'] == "not found") & (unknown['Locker_Name_Found'] != NO_NAME)]
    if todo.empty:
        return
    st.write("#### ➕ Add missing locations")
    st.caption("Enter the City and State for each name below and save. The file is re-processed automatically.")
    with st.form("add_locations"):
        entries = []
        for row in todo.itertuples():
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.markdown(f"**{row.Locker_Name_Found}**  \n{row.Rows} rows")
            city = c2.text_input("City", key=f"city_{row.Locker_Name_Found}", placeholder="City", label_visibility="collapsed")
            state = c3.selectbox("State", [""] + INDIAN_STATES, key=f"state_{row.Locker_Name_Found}", label_visibility="collapsed")
            entries.append((row.Locker_Name_Found, city, state))
        submitted = st.form_submit_button("💾 Save new locations")
    if submitted:
        filled = [e for e in entries if e[1].strip() or e[2].strip()]
        if not filled:
            st.info("Nothing entered yet.")
            return
        saved, messages = save_new_locations(filled, lookup)
        if saved:
            st.session_state["flash"] = [f"✅ {saved} location(s) saved."] + messages
            st.rerun()
        for m in messages:
            st.warning(m)

def render_add_manual():
    """Add a location before it shows up in any file."""
    with st.expander("➕ Add a location manually"):
        with st.form("add_manual"):
            location = st.text_input("Location name (as it appears in the data)")
            city = st.text_input("City")
            state = st.selectbox("State", [""] + INDIAN_STATES)
            submitted = st.form_submit_button("💾 Save location")
        if submitted:
            saved, messages = save_new_locations([(location, city, state)], lookup)
            if saved:
                st.session_state["flash"] = [f"✅ {saved} location(s) saved."] + messages
                st.rerun()
            for m in messages:
                st.warning(m)

st.set_page_config(page_title="Locker Settlement Processor", layout="centered")

st.title("🧳 Locker Settlement Processor")
st.write("Upload a settlement `.xlsx` or `.csv` file. The app will extract the locker location and append **City** and **State** columns.")

# Load the mapping fresh on every run - no restart needed after editing locations.csv
try:
    lookup, locations_table, mapping_problems = load_location_mapping()
except Exception as e:
    lookup = None
    st.error(f"Could not load the location list from '{LOCATIONS_FILE.name}': {e}. No file will be processed until this is fixed.")

if lookup is not None:
    with st.expander(f"📍 Locations currently loaded: {len(lookup)} (from {LOCATIONS_FILE.name})"):
        st.caption(
            "New sites can be added from this page (see below). Words like Station/Railway/Luggage and "
            "suffixes like '- A' are handled automatically."
        )
        st.dataframe(locations_table)
    for message in st.session_state.pop("flash", []):
        if message:
            (st.success if message.startswith("✅") else st.warning)(message)
    for problem in mapping_problems:
        st.warning(f"locations.csv: {problem}")
    render_add_manual()

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=['xlsx', 'csv'])

if uploaded_file is not None and lookup is not None:
    # Load the data
    try:
        if uploaded_file.name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            excel_file = pd.ExcelFile(uploaded_file)
            if len(excel_file.sheet_names) > 1:
                st.warning(
                    f"This workbook has {len(excel_file.sheet_names)} sheets {excel_file.sheet_names}. "
                    f"Only the first sheet '{excel_file.sheet_names[0]}' is processed."
                )
            df = pd.read_excel(excel_file, sheet_name=0)

        if 'payment_notes' not in df.columns:
            st.error(
                "Error: The uploaded file does not contain a 'payment_notes' column. "
                f"Columns found: {list(df.columns)}"
            )
        else:
            st.success("File uploaded successfully! Processing data...")

            # Process the data
            processed_df, review_df = process_dataframe(df, lookup)

            unknown = review_df[review_df['City'] == "Unknown"]
            partial = review_df[review_df['Result'] == "partial"]
            unknown_rows = int(unknown['Rows'].sum())
            if unknown_rows:
                st.warning(
                    f"⚠️ {unknown_rows} of {len(processed_df)} rows could not be mapped and are marked "
                    "City/State = 'Unknown'. Add them in the form below "
                    "('ambiguous' means the name contains two different known locations):"
                )
                st.dataframe(unknown.drop(columns=['City', 'State']))
                render_add_locations(unknown)
            else:
                st.info(f"All {len(processed_df)} rows were mapped to a City/State.")
            if not partial.empty:
                st.warning(
                    f"🔎 {int(partial['Rows'].sum())} rows were mapped by a partial name match. "
                    "Please verify; add an exact row to locations.csv if any is wrong:"
                )
                st.dataframe(partial.drop(columns=['Did_You_Mean (not applied)', 'Sample_payment_notes']))

            # Show a preview of the processed data to the user
            st.write("### Data Preview (First 5 Rows)")
            st.dataframe(processed_df[['payment_notes', 'City', 'State']].head())

            # Create Download Button
            st.download_button(
                label="📥 Download Processed Excel File",
                data=to_excel_bytes(processed_df),
                file_name=f"Processed_{uploaded_file.name.rsplit('.', 1)[0]}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
