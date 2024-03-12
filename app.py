import streamlit as st
import pandas as pd

def read_excel_sheets(file_path):
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    selected_sheets = st.multiselect("Select sheets from the workbook:", sheet_names)
    
    if not selected_sheets:
        st.warning("Please select at least one sheet.")
        return None
    
    df_list = [pd.read_excel(xls, sheet_name=sheet) for sheet in selected_sheets]
    df = pd.concat(df_list, ignore_index=True)
    
    return df

def read_file(file_path, selected_sheets=None):
    if file_path.name.endswith(('.csv', '.CSV')):
        df = pd.read_csv(file_path)
    elif file_path.name.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
        if selected_sheets is not None:
            df = read_excel_sheets(file_path)
        else:
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
        selected_sheets = None

        if file1.name.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
            selected_sheets = st.sidebar.checkbox("Select sheets from Workbook (CSV 1)", value=True)

        df1 = read_file(file1, selected_sheets)
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
