import streamlit as st
import pandas as pd
import re

def read_excel_file(file_path, sheet_name):
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=9)
    else:
        df = pd.read_excel(file_path, sheet_name=0, skiprows=8)
    return df

def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Excel file for DataFrame 1", type=["xlsx", "xls"])
    uploaded_file2 = st.sidebar.file_uploader("Upload CSV file for DataFrame 2", type=["csv"])

    if uploaded_file1:
        selected_sheet = st.sidebar.selectbox("Select sheet", [""] + pd.ExcelFile(uploaded_file1).sheet_names)
        df1 = read_excel_file(uploaded_file1, selected_sheet)

        if df1 is not None:
            # Exclude the last 3 rows independently
            df1 = df1.iloc[:-3]

            # Convert non-numeric data to string
            df1 = df1.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) else x)

            # Create List 1.1 with only text values from DataFrame 1
            text_values_df1 = df1.select_dtypes(include=['object'])
            text_values_df1 = text_values_df1.applymap(lambda x: x if isinstance(x, str) and x != 'nan' else None)
            text_values_df1 = text_values_df1.dropna(axis=1, how='all')
            text_values_list_1_1 = text_values_df1.stack().tolist()

            # Filter columns with records matching the specified pattern
            text_values_df1 = text_values_df1.loc[:, text_values_df1.apply(lambda col: col.str.contains(r'\b(?:[1-9][A-G]|[A-G][1-9])[0-9]{2}\b').any())]

            # Create List 1.1 with only text values from filtered columns
            text_values_list_1_1 = text_values_df1.stack().tolist()
            # Filter values to include only those matching the specified pattern
            text_values_list_1_1 = [value for value in text_values_list_1_1 if re.match(r'\b(?:[1-9][A-G]|[A-G][1-9])[0-9]{2}\b', value)]

            st.write(text_values_list_1_1)

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)

        if df2 is not None:
            st.header("DataFrame 2")
            st.table(df2)

            # Define PCL code criteria
            pcl_criteria = {
                'sales_customer': ['C', 'A', 'E'],
                'cost': ['B', 'E', 'D', 'F'],
                'incent': ['G']
            }

            # Function to check PCL mapping criteria for a given row
            def check_pcl_criteria(row):
                line_label = str(row['Line Label']).lower()
                pcl_codes = str(row.get('PCL code', '')).upper()  # Ensure PCL codes are in uppercase
                for key, codes in pcl_criteria.items():
                    if key == 'sales_customer' and any(keyword in line_label for keyword in ['sales', 'customer']):
                        if any(code in pcl_codes for code in codes):
                            return True
                    elif key == 'cost' and 'cost' in line_label:
                        if any(code in pcl_codes for code in codes):
                            return True
                    elif key == 'incent' and 'incent' in line_label:
                        if any(code in pcl_codes for code in codes):
                            return True
                return False

            # Apply PCL mapping criteria
            df2['Pass PCL Criteria'] = df2.apply(check_pcl_criteria, axis=1)

            # Filter records that do not meet PCL mapping criteria
            mismatched_records = df2[~df2['Pass PCL Criteria']]
            mismatched_records = mismatched_records.dropna()
            if mismatched_records.empty:
                st.success("PCL mapping criteria passed")
            else:
                st.write(mismatched_records)

            st.write("Data Validation")
            # Extract unique values from df2['PCL code']
            pcl_code_column = 'PCL code'
            df2_values = set(df2[pcl_code_column].dropna().str.upper().values)

            # Check if all records in text_values_list_1_1 are available in pcl_code_column
            unmatched_records = [value for value in text_values_list_1_1 if value not in df2_values]

            if not unmatched_records:
                st.success("All records in text_values_list_1_1 are available in df2.")
            else:
                st.error("Some records in text_values_list_1_1 are not available in df2.")
                st.header("Unmatched Records")
                st.write(unmatched_records)

if __name__ == "__main__":
    main()
