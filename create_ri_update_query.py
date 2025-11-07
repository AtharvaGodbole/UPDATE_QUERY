import pandas as pd
import random
from datetime import datetime

def read_columns_from_excel(excel_file):
    # Read the Excel file, assuming the first row contains column names
    df = pd.read_excel(excel_file, header=0)
    
    # Extract columns for each category
    general_columns = df.iloc[:, 0].dropna().tolist()  # 1st column
    rate_columns = df.iloc[:, 1].dropna().tolist()     # 2nd column
    trans_columns = df.iloc[:, 2].dropna().tolist()    # 3rd column
    acq_columns = df.iloc[:, 3].dropna().tolist()      # 4th column
    input_columns = df.iloc[:, 4].dropna().tolist()    # 5th column (new)
    
    return general_columns, rate_columns, trans_columns, acq_columns, input_columns

def generate_random_value():
    return random.randint(10000, 20000)

def generate_random_rate():
    return round(random.uniform(0.3, 0.8), 2)

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

def build_update_query_for_inputs(columns, fic_mis_date, v_ri_group_code, table_name='fsi_ri_group_input_detail'):
    set_clause = [f"{column} = 0" for column in columns]
    set_clause_str = ", ".join(set_clause)
    where_clause = f"fic_mis_date = TO_DATE('{fic_mis_date}', 'DD-MON-YYYY') AND v_ri_group_code = '{v_ri_group_code}'"
    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause};"

def write_queries_to_file(queries, file_name):
    with open(file_name, 'w') as file:
        for query in queries:
            file.write(query + "\n\n")
    print(f"\nThe update queries have been written to '{file_name}'.")

def main():
    excel_file = 'ri_columns.xlsx'
    
    fic_mis_date = input("Enter the fic_mis_date (DD-MON-YYYY): ").strip()
    try:
        datetime.strptime(fic_mis_date, '%d-%b-%Y')
    except ValueError:
        print("Invalid date format. Please enter in 'DD-MON-YYYY' format.")
        return

    general_columns, rate_columns, trans_columns, acq_columns, input_columns = read_columns_from_excel(excel_file)

    num_v_ri_group_codes = int(input("How many v_ri_group_code values would you like to input? ").strip())

    all_queries = []

    for _ in range(num_v_ri_group_codes):
        v_ri_group_code = input("Enter the v_ri_group_code: ").strip()
        
        update_query = build_update_query(general_columns, fic_mis_date, v_ri_group_code)
        rate_update_query = build_update_query_for_rates(rate_columns, fic_mis_date, v_ri_group_code)
        trans_update_query = build_update_query_for_trans(trans_columns, fic_mis_date, v_ri_group_code)
        acq_update_query = build_update_query_for_acq(acq_columns, fic_mis_date, v_ri_group_code)
        input_update_query = build_update_query_for_inputs(input_columns, fic_mis_date, v_ri_group_code)

        all_queries.extend([
            update_query,
            rate_update_query,
            trans_update_query,
            acq_update_query,
            input_update_query
        ])

    print("\nGenerated UPDATE Queries:")
    for query in all_queries:
        print(query)

    write_queries_to_file(all_queries, 'ri_update_queries.txt')

if __name__ == "__main__":
    main()
