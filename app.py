import streamlit as st
import pandas as pd

def read_file(file_path):
    if file_path.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    else:
        st.error("Unsupported file format. Please upload an Excel file.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Excel file for DataFrame 1", type=["xlsx", "xls"])

    if uploaded_file1:
        df1 = read_file(uploaded_file1)

        if df1 is not None:
            # Convert non-numeric columns to strings
            df1 = df1.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) else x)
            
            st.header("DataFrame 1")
            st.table(df1)

if __name__ == "__main__":
    main()
