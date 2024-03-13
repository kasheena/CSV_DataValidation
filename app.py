import streamlit as st
import pandas as pd

def read_file(file_path, sheet_name):
    if file_path.name.endswith('.xlsx'):
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            # If no sheet selected, read the first sheet by default
            df = pd.read_excel(file_path, sheet_name=0)
    else:
        st.error("Unsupported file format. Please upload an Excel file for DataFrame 1.")
        return None
    return df

def read_csv(file_path):
    if file_path.name.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        st.error("Unsupported file format. Please upload a CSV file for DataFrame 2.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Excel file for DataFrame 1", type=["xlsx", "xls"])
    uploaded_file2 = st.sidebar.file_uploader("Upload CSV file for DataFrame 2", type=["csv"])

    if uploaded_file1 and uploaded_file2:
        selected_sheet = st.sidebar.selectbox("Select sheet", [""] + pd.ExcelFile(uploaded_file1).sheet_names)
        df1 = read_file(uploaded_file1, selected_sheet)
        df2 = read_csv(uploaded_file2)

        if df1 is not None and df2 is not None:
            # Select only 'PCL code' column from DataFrame 2
            df2 = df2[['PCL code']]

            # Compare DataFrames to find records in DataFrame 1 that don't exist in DataFrame 2
            df3 = pd.merge(df1, df2, how='left', left_on='PCL code', right_on='PCL code', indicator=True)
            df3 = df3[df3['_merge'] == 'left_only'].drop('_merge', axis=1)

            st.header("DataFrame 1")
            st.table(df1)

            st.header("DataFrame 2 (PCL code)")
            st.table(df2)

            st.header("Records not present in DataFrame 2")
            st.table(df3)

if __name__ == "__main__":
    main()
