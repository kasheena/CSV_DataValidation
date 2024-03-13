import streamlit as st
import pandas as pd
import PyPDF2
import io

def read_pdf(file_path):
    tables = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfFileReader(f)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extractText()
            # Extracting tables based on some patterns in the text (this is a simplified approach)
            table = [line.split() for line in text.split("\n") if line.strip()]
            if table:
                tables.append(pd.DataFrame(table))
    if not tables:
        st.error("No tables found in the PDF file.")
        return None
    df = pd.concat(tables, ignore_index=True)
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
    uploaded_file1 = st.sidebar.file_uploader("Upload PDF, CSV, or Excel for DataFrame 1", type=["pdf", "csv", "xls", "xlsx", "xlsm", "xlsb"])

    if uploaded_file1:
        uploaded_file2 = st.sidebar.file_uploader("Upload CSV, or Excel for DataFrame 2", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

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
