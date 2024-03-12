import streamlit as st
import pandas as pd
import tabula

def read_pdf(file_path):
    # Read PDF file into DataFrame
    df = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
    return df

def read_file(file_path):
    if file_path.name.endswith('.pdf'):
        df = read_pdf(file_path)
    elif file_path.name.endswith(('.csv', '.CSV')):
        df = pd.read_csv(file_path)
    elif file_path.name.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
        df = pd.read_excel(file_path)
    else:
        st.error("Unsupported file format. Please upload a PDF, CSV, or Excel file.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload PDF, CSV, or Excel", type=["pdf", "csv", "xls", "xlsx", "xlsm", "xlsb"])

    if uploaded_file1:
        uploaded_file2 = st.sidebar.file_uploader("Upload CSV, or Excel", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

        if uploaded_file2:
            df1 = read_file(uploaded_file1)
            df2 = read_file(uploaded_file2)

            if df1 is not None and df2 is not None:
                st.header("DataFrame 1")

                # Check if df1 is a list of DataFrames (result from PDF parsing)
                if isinstance(df1, list):
                    # Concatenate all DataFrames into one
                    df1_concatenated = pd.concat(df1, ignore_index=True)
                    # Filter columns that are not null
                    df1_filtered = df1_concatenated.dropna(axis=1, how='all')
                else:
                    # For CSV or Excel files, filter columns that are not null
                    df1_filtered = df1.dropna(axis=1, how='all')

                st.table(df1_filtered)

                st.header("DataFrame 2")
                st.table(df2)

                # Data validation
                # Check if records from DataFrame 1 exist in DataFrame 2
                validation_result = []
                for index, row in df1_filtered.iterrows():
                    if row.values.tolist() in df2.values.tolist():
                        validation_result.append(True)
                    else:
                        validation_result.append(False)

                st.header("Validation Result")
                if all(validation_result):
                    st.write("All records from DataFrame 1 are present in DataFrame 2.")
                else:
                    st.write("Some records from DataFrame 1 are not present in DataFrame 2.")

if __name__ == "__main__":
    main()
