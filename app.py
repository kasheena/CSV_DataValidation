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
            df = pd.read_excel(file_path)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Workbook (CSV 1 or Excel)", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

    if uploaded_file1:
        selected_sheets = st.sidebar.multiselect("Select sheets from the workbook:", [])
        uploaded_file2 = st.sidebar.file_uploader("Upload CSV 2 or Excel", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

        if uploaded_file2:
            df1 = read_file(uploaded_file1, selected_sheets)
            df2 = read_file(uploaded_file2)

            if df1 is not None and df2 is not None:
                st.header("DataFrame 1 Before Filtering")
                st.write(df1)

                # Remove columns that are entirely null from DataFrame 1
                df1_filtered = df1.dropna(axis=1, how='all')

                st.header("DataFrame 1 After Filtering")
                st.write(df1_filtered)

                st.header("DataFrame 2")
                st.write(df2)

                # Data validation
                # Check if records from DataFrame 1 exist in DataFrame 2
                validation_result = []
                for _, row in df1_filtered.iterrows():
                    if any(row.astype(str).isin(df2.values.flatten())):
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
