import streamlit as st
import pandas as pd

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

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)

        if df2 is not None:
            # Check for validation
            df2_values = df2['PCL code'].dropna().values
            validation_result = df1.applymap(lambda x: x in df2_values if not pd.isna(x) else False)

            # Filter out NaN values in DataFrame 1 before creating DataFrame 3
            unmatched_records = df1[~validation_result.any(axis=1) & ~df1.isna().any(axis=1)]

            if not unmatched_records.empty:
                st.header("Records not present in DataFrame 2")
                st.table(unmatched_records)
            else:
                st.success("All valid records from DataFrame 1 are present in DataFrame 2.")

    if not unmatched_records.empty:
        input_dict = {}
        # Define the headers
        headers = ["Sales", "Gross Profit", "Incentives", "Chargeback"]
        
        # Initialize the input_dict
        for header in headers:
            input_dict[header] = []

        for header in headers:
            if header == "Sales":
                # Include values with 'C' and starting with a number
                input_dict[header] = [value for value in unmatched_records[3:] if 'C' in value and re.match(r'^\d', value)]
            elif header == "Gross Profit":
                # Include values with 'E' or 'e+' and starting with a number
                input_dict[header] = [value.upper().replace('E+', 'E') for value in unmatched_records[5:] if ('E' in value or 'e+' in value) and re.match(r'^\d', value)]
            elif header == "Incentives":
                # Include values with 'G' and starting with a number
                input_dict[header] = [value for value in unmatched_records[3:] if 'G' in value and re.match(r'^\d', value)]
            elif header == "Chargeback":
                # Include values with 'D' and starting with a number
                input_dict[header] = [value for value in unmatched_records[3:] if 'D' in value and re.match(r'^\d', value)]

        st.header("Input Dict (Records not present in DataFrame 2)")
        st.write(input_dict)

if __name__ == "__main__":
    main()
