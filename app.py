import streamlit as st
import pandas as pd

def read_file(file_path, sheet_name):
    if file_path.name.endswith(('.xlsx', '.xls')):
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            # If no sheet selected, read the first sheet by default
            df = pd.read_excel(file_path, sheet_name=0)
    else:
        st.error("Unsupported file format. Please upload an Excel file.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Excel file for DataFrame 1", type=["xlsx", "xls"])

    if uploaded_file1:
        selected_sheet = st.sidebar.selectbox("Select sheet", [""] + pd.ExcelFile(uploaded_file1).sheet_names)
        df1 = read_file(uploaded_file1, selected_sheet)

        if df1 is not None:
            # Select only columns 5 to 20
            df1 = df1.iloc[:, 4:20]

            # Convert non-numeric data to string
            df1 = df1.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) else x)

            st.header("Selected Columns from DataFrame 1")
            st.table(df1)

if __name__ == "__main__":
    main()
