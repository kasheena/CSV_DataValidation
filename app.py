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
            # Extract unique values from df2['PCL code'] or df2['PCL codes']
            pcl_code_column = next((col for col in df2.columns if 'PCL' in col), None)
            # PCL Mapping Criteria 
            st.header("PCL Mapping Criteria")
            
            # Check if all records with 'sales' or 'customer' in Line Label meet the PCL mapping criteria
            sales_criteria_codes = ['C', 'A', 'E']
            pass_sales_criteria = all(('sales' in str(row['Line Label']).lower() or 'customer' in str(row['Line Label']).lower()) and any(code in str(row.get('PCL code', row.get('PCL codes', ''))) for code in sales_criteria_codes) for index, row in df2.iterrows())
            
            # Check if all records with 'cost' in Line Label meet the PCL mapping criteria
            cost_criteria_codes = ['B', 'E', 'D', 'F']
            pass_cost_criteria = all('cost' in str(row['Line Label']).lower() and any(code in str(row.get('PCL code', row.get('PCL codes', ''))) for code in cost_criteria_codes) for index, row in df2.iterrows())
            
            # Check if all records with 'incent' or 'New Other Cost' in Line Label meet the PCL mapping criteria
            pass_incent_criteria = all(('incent' in str(row['Line Label']).lower() or 'new other cost' in str(row['Line Label']).lower()) and 'G' in str(row.get('PCL code', row.get('PCL codes', ''))) for index, row in df2.iterrows())

            # Combine all criteria into a single condition
            pass_all_criteria = pass_sales_criteria and pass_cost_criteria and pass_incent_criteria
            
            if pass_all_criteria:
                st.success("All criteria passed")
            else:
                st.error("One or more criteria not met")
            
                # Filter mismatched records for all criteria
                mismatched_records = df2[~(((df2['Line Label'].str.lower().str.contains('sales') | df2['Line Label'].str.lower().str.contains('customer')) & 
                                             df2[pcl_code_column].isin(sales_criteria_codes)) |
                                            ((df2['Line Label'].str.lower().str.contains('cost')) & 
                                             df2[pcl_code_column].isin(cost_criteria_codes)) |
                                            ((df2['Line Label'].str.lower().str.contains('incent') | df2['Line Label'].str.lower().str.contains('new other cost')) & 
                                             df2[pcl_code_column].str.contains('G', case=False)))]
            
                if not mismatched_records.empty:
                    st.header("Mismatched Records")
                    st.table(mismatched_records)

            st.write("Data Validation")
            df2_values = set(df2[pcl_code_column].dropna().values)

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
