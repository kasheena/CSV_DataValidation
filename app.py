import streamlit as st
import pandas as pd

def read_file(file_path):
    if file_path.name.endswith(('.csv', '.CSV')):
        df = pd.read_csv(file_path)
    elif file_path.name.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
        # Use pandas to read Excel files without 'openpyxl'
        df = pd.read_excel(pd.ExcelFile(file_path), engine='xlrd')
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    file1 = st.sidebar.file_uploader("Upload Workbook (CSV 1 or Excel)", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])
    file2 = st.sidebar.file_uploader("Upload CSV 2 or Excel", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

    if file1 and file2:
        df1 = read_file(file1)
        df2 = read_file(file2)

        if df1 is not None and df2 is not None:
            st.header("DataFrame 1 (Ignoring Null Values)")
            
            # Create a DataFrame excluding rows with null values
            df1_cleaned = df1.dropna()

            st.table(df1_cleaned)

            st.header("DataFrame 2")
            st.table(df2)

            # Data validation
            validation_result = pd.merge(df1_cleaned, df2, how='left', indicator=True).query('_merge == "left_only"').drop('_merge', axis=1)
            
            st.header("Validation Result")
            st.table(validation_result)

if __name__ == "__main__":
    main()
