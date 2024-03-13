import streamlit as st
import pandas as pd
import re

def read_excel_file(file_path, sheet_name):
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=9)
    else:
        df = pd.read_excel(file_path, sheet_name=0, skiprows=9)
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

            # Initialize the input_dict
            input_dict = {}
            
            # Define the headers
            headers = ["Sales", "Gross Profit", "Incentives", "Chargeback"]
            
            # Iterate through the headers
            for header in headers:
                if header == "Sales":
                    # Include values with 'C' and starting with a number
                    input_dict[header] = [value for value in text_values_list_1_1 if 'C' in value and re.match(r'^\d', value)]
                elif header == "Gross Profit":
                    # Include values with 'E' or 'e+' and starting with a number
                    input_dict[header] = [value.upper().replace('E+', 'E') for value in text_values_list_1_1 if ('E' in value or 'e+' in value) and re.match(r'^\d', value)]
                elif header == "Incentives":
                    # Include values with 'G' and starting with a number
                    input_dict[header] = [value for value in text_values_list_1_1 if 'G' in value and re.match(r'^\d', value)]
                elif header == "Chargeback":
                    # Include values with 'D' and starting with a number
                    input_dict[header] = [value for value in text_values_list_1_1 if 'D' in value and re.match(r'^\d', value)]

            st.header("Input Dictionary")
            st.write(input_dict)

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)
    
        if df2 is not None:
            st.header("DataFrame 2")
            st.table(df2)
    
            # Extract unique values from df2['PCL code']
            df2_values = set(df2['PCL code'].dropna().values)
    
            # Check for validation
            validation_result = df1.applymap(lambda x: x in df2_values if not pd.isna(x) else False)
    
            # Filter out NaN values in DataFrame 1 before creating DataFrame 3
            unmatched_records = df1[~validation_result.any(axis=1) & ~df1.isna().any(axis=1)]
    
            # Check for values in input_dict that do not match df2_values
            mismatched_values = {}
            for header, values in input_dict.items():
                for value in values:
                    if value not in df2_values:
                        if header not in mismatched_values:
                            mismatched_values[header] = []
                        mismatched_values[header].append(value)
    
            if not mismatched_values:
                st.success("All values in input_dict exist in df2_values.")
            else:
                st.error("Some values in input_dict do not exist in df2_values.")
                st.header("Mismatched Values")
                st.write(mismatched_values)

        # Additional functionality
        if 'Line Label' in df2.columns and 'PCL code' in df2.columns:
            sales_mapping = {}
            for index, row in df2.iterrows():
                if 'sales' in str(row['Line Label']).lower() and 'C' in str(row['PCL code']):
                    sales_mapping[row['Line Label']] = row['PCL code']
            
            st.header("Sales Mapping")
            st.write(sales_mapping)
if __name__ == "__main__":
    main()
