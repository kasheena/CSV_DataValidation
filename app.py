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

def filter_records(df):
    # Filter records with specific values
    prefixes = ['5C', '5E', '5G', '6C', '6E', '6G', '7E', '7C', '7G', '7D', '8E', '8C', '8G', '9E', '9C']
    mask = df.apply(lambda row: any(row.str.startswith(prefix) for prefix in prefixes), axis=1)
    filtered_df = df[mask]
    return filtered_df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Workbook (CSV 1 or Excel)", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

    if uploaded_file1:
        uploaded_file2 = st.sidebar.file_uploader("Upload CSV 2 or Excel", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

        if uploaded_file2:
            df1 = read_file(uploaded_file1)
            df2 = read_file(uploaded_file2)

            if df1 is not None and df2 is not None:
                st.header("DataFrame 1")

                # Filter records from DataFrame based on the specified prefixes
                df1_filtered = filter_records(df1)

                st.table(df1_filtered)

                st.header("DataFrame 2")
                st.table(df2)

                # Data validation
                # Perform cross-join (cartesian product) between the two DataFrames
                validation_result = pd.merge(df1_filtered.assign(key=1), df2.assign(key=1), on='key', suffixes=('_df1', '_df2'), indicator=True)
                validation_result = validation_result[validation_result['_merge'] == 'both'].drop(columns='_merge')

                st.header("Validation Result")
                if validation_result.empty:
                    st.write("No records from DataFrame 1 are present in DataFrame 2.")
                else:
                    st.table(validation_result.drop(columns='key'))

if __name__ == "__main__":
    main()
