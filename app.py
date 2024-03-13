import streamlit as st
import pandas as pd

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

            # Select only columns 9 to 30
            df1 = df1.iloc[:, 8:30]

            # Convert non-numeric data to string
            df1 = df1.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) else x)

            st.header("DataFrame 1")
            st.table(df1)

            # Create List 1.1 with only text values from DataFrame 1
            text_values_df1 = df1.select_dtypes(include=['object'])
            text_values_df1 = text_values_df1.applymap(lambda x: x if isinstance(x, str) and x != 'nan' else None)
            text_values_df1 = text_values_df1.dropna(axis=1, how='all')
            text_values_list_1_1 = text_values_df1.stack().tolist()

            st.header("Text Values in List 1.1 (Excluding 'nan')")
            st.write(text_values_list_1_1)

            # Create dictionary 'input'
            input_dict = {}
            headers = text_values_list_1_1[:3]  # Get first three records as headers
            for header in headers:
                if header == headers[0]:  # If it's the first header
                    input_dict[header] = [value for value in text_values_list_1_1 if 'C' in value]
                elif header == headers[1]:  # If it's the second header
                    input_dict[header] = [value for value in text_values_list_1_1 if 'E' in value]
                elif header == headers[2]:  # If it's the third header
                    input_dict[header] = [value for value in text_values_list_1_1 if 'G' in value]

            st.header("Input Dictionary")
            st.write(input_dict)

 
