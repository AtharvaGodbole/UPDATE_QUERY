import streamlit as st
import pandas as pd
import random
from datetime import datetime
import io


# --- Helper Functions from Your Original Script (Updated for Excel) ---

def generate_random_value():
    return random.randint(10000, 20000)


def generate_random_rate():
    return round(random.uniform(0.3, 0.8), 2)


def read_columns_from_input(file_stream):
    """Reads columns from the uploaded Excel file stream."""

    # MODIFICATION 1: Changed pd.read_csv to pd.read_excel
    # Assumes the column names are in the first row (header=0) and the data is in the first sheet.
    df = pd.read_excel(file_stream, header=0)

    # Extract columns for each category based on index, as in the original script
    # The columns are: General, Rate, Transaction, Acquisition, and Input (OBA)
    general_columns = df.iloc[:, 0].dropna().tolist()
    rate_columns = df.iloc[:, 1].dropna().tolist()
    trans_columns = df.iloc[:, 2].dropna().tolist()
    acq_columns = df.iloc[:, 3].dropna().tolist()
    input_columns = df.iloc[:, 4].dropna().tolist()  # Mapped to OBA Columns

    return general_columns, rate_columns, trans_columns, acq_columns, input_columns


def build_update_query(columns, fic_mis_date, v_ri_group_code, table_name='fsi_ri_group_input_detail'):
    set_clause = [f"{column} = {generate_random_value()}" for column in columns]
    set_clause_str = ", ".join(set_clause)
    where_clause = f"fic_mis_date = TO_DATE('{fic_mis_date}', 'DD-MON-YYYY') AND v_ri_group_code = '{v_ri_group_code}'"
    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause};"


def build_update_query_for_rates(columns, fic_mis_date, v_ri_group_code, table_name='fsi_ri_group_input_detail'):
    set_clause = [f"{column} = {generate_random_rate()}" for column in columns]
    set_clause_str = ", ".join(set_clause)
    where_clause = f"fic_mis_date = TO_DATE('{fic_mis_date}', 'DD-MON-YYYY') AND v_ri_group_code = '{v_ri_group_code}'"
    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause};"


def build_update_query_for_trans(columns, fic_mis_date, v_ri_group_code, table_name='fsi_ri_group_input_detail'):
    set_clause = [f"{column} = 0" for column in columns]
    set_clause_str = ", ".join(set_clause)
    where_clause = f"fic_mis_date = TO_DATE('{fic_mis_date}', 'DD-MON-YYYY') AND v_ri_group_code = '{v_ri_group_code}'"
    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause};"


def build_update_query_for_acq(columns, fic_mis_date, v_ri_group_code, table_name='fsi_ri_group_input_detail'):
    set_clause = [f"{column} = 0" for column in columns]
    set_clause_str = ", ".join(set_clause)
    where_clause = f"fic_mis_date = TO_DATE('{fic_mis_date}', 'DD-MON-YYYY') AND v_ri_group_code = '{v_ri_group_code}'"
    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause};"


def build_update_query_for_input_columns(columns, fic_mis_date, v_ri_group_code,
                                        table_name='fsi_ri_group_input_detail'):
    set_clause = [f"{column} = 0" for column in columns]
    set_clause_str = ", ".join(set_clause)
    where_clause = f"fic_mis_date = TO_DATE('{fic_mis_date}', 'DD-MON-YYYY') AND v_ri_group_code = '{v_ri_group_code}'"
    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause};"


# --- Main Streamlit Application Logic ---

st.title("Reinsurance SQL UPDATE Query Generator (RI) ⚙️")
st.markdown(
    "Upload the column definition **Excel** file and enter the required parameters for the `fsi_ri_group_input_detail` table.")

# 1. File Uploader
# MODIFICATION 2: Changed file name prompt and allowed type to 'xlsx'
uploaded_file = st.file_uploader(
    "Upload the 'ri_columns.xlsx' file:",
    type=['xlsx']
)

# 2. Date Input
fic_mis_date_str = st.text_input(
    "Enter the fic_mis_date (e.g., 31-DEC-2024):"
).strip()

# 3. Number of Group Codes Input
num_group_codes = st.number_input(
    "How many RI Group Code (`v_ri_group_code`) values do you need?",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

# 4. RI Group Code Input fields
group_codes = []
for i in range(int(num_group_codes)):
    group_code = st.text_input(f"Enter RI Group Code #{i + 1}:", key=f"ri_group_code_{i}").strip()
    if group_code:
        group_codes.append(group_code)

if st.button("Generate RI Queries"):

    # Validation checks
    if not uploaded_file:
        st.error("Please upload the Excel column definition file.")
        st.stop()

    if not fic_mis_date_str:
        st.error("Please enter the fic_mis_date.")
        st.stop()

    if not all(group_codes):
        st.error("Please enter all required RI group codes.")
        st.stop()

    try:
        # 1. Read Input and Extract Columns
        general_columns, rate_columns, trans_columns, acq_columns, input_columns = read_columns_from_input(
            uploaded_file)

        # 2. Generate all queries
        all_queries = []
        for group_code in group_codes:
            # Generate the UPDATE queries for the current group_code
            update_query = build_update_query(general_columns, fic_mis_date_str, group_code)
            rate_update_query = build_update_query_for_rates(rate_columns, fic_mis_date_str, group_code)
            trans_update_query = build_update_query_for_trans(trans_columns, fic_mis_date_str, group_code)
            acq_update_query = build_update_query_for_acq(acq_columns, fic_mis_date_str, group_code)
            input_update_query = build_update_query_for_input_columns(input_columns, fic_mis_date_str, group_code)

            # Add all queries to the list
            all_queries.extend([
                update_query,
                rate_update_query,
                trans_update_query,
                acq_update_query,
                input_update_query
            ])

        # 3. Display the results
        st.success(f"Successfully generated {len(all_queries)} Reinsurance queries.")

        queries_text = "\n\n".join(all_queries)

        # Display the queries in a text area
        st.text_area(
            "Generated SQL Queries",
            queries_text,
            height=300
        )

        # 4. Provide a download button
        st.download_button(
            label="Download Queries as .txt",
            data=queries_text,
            file_name="ri_update_queries.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please ensure your file is a valid Excel file with at least 5 columns of data in the first sheet.")
