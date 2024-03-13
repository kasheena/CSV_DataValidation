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
            input_dict = {}
            headers = ["Sales", "Gross Profit", "Incentives", "Chargeback"]

            # Iterate through the headers
            for header in headers:
                if header == "Sales":
                    input_dict[header] = [value for value in df1.iloc[:, 0].astype(str).values if 'C' in value and re.match(r'^\d', value)]
                elif header == "Gross Profit":
                    input_dict[header] = [value.upper().replace('E+', 'E') for value in df1.iloc[:, 1].astype(str).values if ('E' in value or 'e+' in value) and re.match(r'^\d', value)]
                elif header == "Incentives":
                    input_dict[header] = [value for value in df1.iloc[:, 2].astype(str).values if 'G' in value and re.match(r'^\d', value)]
                elif header == "Chargeback":
                    input_dict[header] = [value for value in df1.iloc[:, 3].astype(str).values if 'D' in value and re.match(r'^\d', value)]

            st.header("Input Dictionary")
            st.write(input_dict)

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)

        if df2 is not None:
            st.header("DataFrame 2")
            st.table(df2)

            # Validate if all values in input_dict are present in DataFrame 2
            validation_result = all(all(value in df2[col].astype(str).values for value in values) for col, values in input_dict.items())
            if validation_result:
                st.success("All values in Input Dictionary are present in DataFrame 2.")
            else:
                st.error("Not all values in Input Dictionary are present in DataFrame 2.")

if __name__ == "__main__":
    main()
