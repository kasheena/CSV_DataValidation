import streamlit as st
import pandas as pd

def read_excel_sheets(file_path):
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    sheet_choice = st.selectbox("Select a sheet from the workbook:", sheet_names)
    df = pd.read_excel(file_path, sheet_name=sheet_choice)
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload CSV Files")
    file1 = st.sidebar.file_uploader("Upload Workbook (CSV 1)", type=["csv", "xlsx"])
    file2 = st.sidebar.file_uploader("Upload CSV 2", type=["csv", "xlsx"])

    if file1 and file2:
        df1 = read_excel_sheets(file1) if file1.name.endswith(".xlsx") else pd.read_csv(file1)
        df2 = read_excel_sheets(file2) if file2.name.endswith(".xlsx") else pd.read_csv(file2)

        st.header("DataFrame 1 (Editable)")
        editable_df1 = st.table(df1)

        # Allow user to edit DataFrame 1
        st.write("Edit DataFrame 1 as needed:")
        new_df1 = editable_df1.editable()
        
        st.header("DataFrame 2")
        st.table(df2)

        # Data validation
        validation_result = pd.merge(new_df1, df2, how='left', indicator=True).query('_merge == "left_only"').drop('_merge', axis=1)
        
        st.header("Validation Result")
        st.table(validation_result)

if __name__ == "__main__":
    main()
