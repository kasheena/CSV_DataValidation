import streamlit as st
import pandas as pd
import re

def read_excel_file(file_path, sheet_name):
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=9)
    else:
        df = pd.read_excel(file_path, sheet_name=0, skiprows=9)
    return df

def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Excel file for DataFrame 1", type=["xlsx", "xls"])
    uploaded_file2 = st.sidebar.file_uploader("Upload CSV file for DataFrame 2", type=["csv"])

    if uploaded_file1:
        selected_sheet = st.sidebar.selectbox("Select sheet", [""] + pd.ExcelFile(uploaded_file1).sheet_names)
        df1 = read_excel_file(uploaded_file1, selected_sheet)

        if df1 is not None:
            # Exclude the last 3 rows independently
            df1 = df1.iloc[:-3]

            # Convert non-numeric data to string
            df1 = df1.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) else x)

            # Create List 1.1 with only text values from DataFrame 1
            text_values_df1 = df1.select_dtypes(include=['object'])
            text_values_df1 = text_values_df1.applymap(lambda x: x if isinstance(x, str) and x != 'nan' else None)
            text_values_df1 = text_values_df1.dropna(axis=1, how='all')
            text_values_list_1_1 = text_values_df1.stack().tolist()

            # Initialize the input_dict
            input_dict = {}
            
            # Define the headers
            headers = ["Sales", "Gross Profit", "Incentives", "Chargeback"]
            
            # Iterate through the headers
            for header in headers:
                # Include values with corresponding header letters and starting with a number
                if header == "Sales":
                    input_dict[header] = [value for value in text_values_list_1_1 if 'C' in value and re.match(r'^\d', value)]
                elif header == "Gross Profit":
                    input_dict[header] = [value.upper().replace('E+', 'E') for value in text_values_list_1_1 if ('E' in value or 'e+' in value) and re.match(r'^\d', value)]
                elif header == "Incentives":
                    input_dict[header] = [value for value in text_values_list_1_1 if 'G' in value and re.match(r'^\d', value)]
                elif header == "Chargeback":
                    input_dict[header] = [value for value in text_values_list_1_1 if 'D' in value and re.match(r'^\d', value)]

            st.header("Input Dictionary")
            st.write(input_dict)

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)

        if df2 is not None:
            st.header("DataFrame 2")
            st.table(df2)

            # Check for validation
            df2_values = df2['PCL code'].dropna().values
            validation_result = df1.applymap(lambda x: x in df2_values if not pd.isna(x) else False)

            # Filter out NaN values in DataFrame 1 before creating DataFrame 3
            unmatched_records = df1[~validation_result.any(axis=1) & ~df1.isna().any(axis=1)]

            if not unmatched_records.empty:
                # Create DataFrame 4 with only text values from DataFrame 3
                text_values_df4 = unmatched_records.select_dtypes(include=['object'])
                text_values_df4 = text_values_df4.applymap(lambda x: x if isinstance(x, str) and x != 'nan' else None)
                text_values_df4 = text_values_df4.dropna(axis=1, how='all')
                text_values_dict = text_values_df4.to_dict(orient='list')
            
                # Initialize input_dict with headers
                input_dict = {header: [] for header in headers}
            
                # Iterate over text_values_dict and apply conditions for each header
                for header in headers:
                    if header == "Sales":
                        input_dict[header] = [value for value in text_values_dict.get(header, []) if 'C' in value and re.match(r'^\d', value)]
                    elif header == "Gross Profit":
                        input_dict[header] = [value.upper().replace('E+', 'E') for value in text_values_dict.get(header, []) if ('E' in value or 'e+' in value) and re.match(r'^\d', value)]
                    elif header == "Incentives":
                        input_dict[header] = [value for value in text_values_dict.get(header, []) if 'G' in value and re.match(r'^\d', value)]
                    elif header == "Chargeback":
                        input_dict[header] = [value for value in text_values_dict.get(header, []) if 'D' in value and re.match(r'^\d', value)]  
            
                st.header("Input Dictionary")
                st.write(input_dict)
            else:
                st.success("All valid records from DataFrame 1 are present in DataFrame 2.")

if __name__ == "__main__":
    main()
