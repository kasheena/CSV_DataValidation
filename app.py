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
            
            # Filter columns with words and records with a combination of 2 or 3 numbers and exactly 1 alphabet
            filtered_text_values_df1 = text_values_df1.loc[:, text_values_df1.apply(lambda col: col.str.contains(r'\b\w+\d{2,3}[a-zA-Z]\d{0,2}\b').any())]

            # Drop columns with all NaN values
            filtered_text_values_df1 = filtered_text_values_df1.dropna(axis=1, how='all')

            st.write(filtered_text_values_df1)
            
            st.write(text_values_df1)
            st.write(text_values_list_1_1)
            # Initialize the input_dict
            input_dict = {}
            
            # Define the headers
            headers = ["Sales", "Gross Profit", "Incentives", "Chargeback"]
            
    # Iterate through the headers
    for header in headers:
        if header == "Sales":
            # Include values starting with 'A' and starting with a number
            sales_values_starting_with_A = [value for value in text_values_list_1_1 if 'A' in value and re.match(r'^\d', value)]
            if sales_values_starting_with_A:
                input_dict[header] = sales_values_starting_with_A
            else:
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
    
            # PCL Mapping Criteria 
            # Check if all records with 'sales' or 'customer' in Line Label meet the PCL mapping criteria
            pass_sales_criteria = all(('sales' in str(row['Line Label']).lower() or 'customer' in str(row['Line Label']).lower()) and 'C' in str(row.get('PCL code', row.get('PCL codes', ''))) for index, row in df2.iterrows())
    
            # Check if all records with 'cost' in Line Label meet the PCL mapping criteria
            pass_cost_criteria = all('cost' in str(row['Line Label']).lower() and ('E' in str(row.get('PCL code', row.get('PCL codes', ''))) or 'D' in str(row.get('PCL code', row.get('PCL codes', '')))) for index, row in df2.iterrows())
    
            # Check if all records with 'incent' or 'New Other Cost' in Line Label meet the PCL mapping criteria
            pass_incent_criteria = all(('incent' in str(row['Line Label']).lower() or 'new other cost' in str(row['Line Label']).lower()) and 'G' in str(row.get('PCL code', row.get('PCL codes', ''))) for index, row in df2.iterrows())
    
            st.header("PCL Mapping Criteria")
    
            # Filter mismatched records
            mismatched_records = df2[~(df2.apply(lambda row: (('sales' in str(row['Line Label']).lower() or 'customer' in str(row['Line Label']).lower()) and 'C' in str(row.get('PCL code', row.get('PCL codes', '')))) or 
                                                                ('cost' in str(row['Line Label']).lower() and ('E' in str(row.get('PCL code', row.get('PCL codes', ''))) or 'D' in str(row.get('PCL code', row.get('PCL codes', ''))))) or
                                                                (('incent' in str(row['Line Label']).lower() or 'new other cost' in str(row['Line Label']).lower()) and 'G' in str(row.get('PCL code', row.get('PCL codes', '')))), axis=1))]
            mismatched_records = mismatched_records.dropna()
            if mismatched_records.empty:
                st.success("PCL mapping criteria passed")
            else:
                st.write(mismatched_records)
    
            st.write("Data Validation")
            # Extract unique values from df2['PCL code'] or df2['PCL codes']
            pcl_code_column = 'PCL code' if 'PCL code' in df2.columns else 'PCL codes'
            df2_values = set(df2[pcl_code_column].dropna().values)
    
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

if __name__ == "__main__":
    main()
