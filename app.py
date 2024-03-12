import streamlit as st
import pandas as pd
import pdfplumber

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        df_list = []
        for page in pages:
            table = page.extract_tables()
            for tab in table:
                df_list.append(pd.DataFrame(tab))
        df = pd.concat(df_list, ignore_index=True)
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
                st.table(df1)

                st.header("DataFrame 2")
                st.table(df2)

                # Data validation
                # Check if records from DataFrame 1 exist in DataFrame 2
                validation_result = []
                for index, row in df1.iterrows():
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
