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

            # Select only columns 9 to 30
            df1 = df1.iloc[:, 8:30]

            # Convert non-numeric data to string
            df1 = df1.applymap(str)

            st.header("DataFrame 1")
            st.table(df1)

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)

        if df2 is not None:
            st.header("DataFrame 2")
            st.table(df2)

            # Check for validation
            df2_values = df2['PCL code'].values
            validation_result = df1.applymap(lambda x: x not in df2_values)

            # Filter out matching records from DataFrame 1 to create DataFrame 3
            unmatched_records = df1[validation_result.any(axis=1)]

            # Filter DataFrame 3 to include only text values
            text_records_df3 = unmatched_records.applymap(lambda x: x if isinstance(x, str) else '')

            if not text_records_df3.empty:
                st.header("Records not present in DataFrame 2")
                st.table(text_records_df3)
            else:
                st.success("All records from DataFrame 1 are present in DataFrame 2.")

if __name__ == "__main__":
    main()
