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
    return pd.read_csv(file_path)

def main():
    st.title("Data Validation App")
    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Excel file for DataFrame 1", type=["xlsx", "xls"])
    uploaded_file2 = st.sidebar.file_uploader("Upload CSV file for DataFrame 2", type=["csv"])
    if uploaded_file1:
        selected_sheet = st.sidebar.selectbox("Select sheet", [""] + pd.ExcelFile(uploaded_file1).sheet_names)
        df1 = read_excel_file(uploaded_file1, selected_sheet)

        if df1 is not None:
            df1 = df1.iloc[:-3]
            df1 = df1.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) else x)
            text_values_df1 = df1.select_dtypes(include=['object']).dropna(axis=1, how='all')
            text_values_list_1_1 = text_values_df1.stack().tolist()

            input_dict = {}
            headers = ["Sales", "Gross Profit", "Incentives", "Chargeback"]
            for header in headers:
                if header == "Sales":
                    input_dict[header] = [value for value in text_values_list_1_1 if 'C' in value and re.match(r'^\d', value)]
                elif header == "Gross Profit":
                    input_dict[header] = [value.upper().replace('E+', 'E') for value in text_values_list_1_1 if ('E' in value or 'e+' in value) and re.match(r'^\d', value)]
                elif header == "Incentives":
                    input_dict[header] = [value for value in text_values_list_1_1 if 'G' in value and re.match(r'^\d', value)]
                elif header == "Chargeback":
                    input_dict[header] = [value for value in text_values_list_1_1 if 'D' in value and re.match(r'^\d', value)]

            st.header("Input Dictionary")
            st.write(input_dict)

    if uploaded_file2:
        df2 = read_csv_file(uploaded_file2)

        if df2 is not None:
            st.header("DataFrame 2")
            st.table(df2)

            df2_values = set(df2['PCL code'].dropna().values)
            mapping_criteria = {
                "Sales": ("C", lambda x: 'sales' in x.lower() or 'customer' in x.lower()),
                "Cost": ("E/D", lambda x: 'cost' in x.lower()),
                "Incentives": ("G", lambda x: 'incent' in x.lower() or 'new other cost' in x.lower())
            }
            mismatched_records = df2[~df2.apply(lambda row: any(pc in str(row['PCL code']) and criteria(str(row['Line Label'])) for pc, criteria in mapping_criteria.values()), axis=1)]

            if mismatched_records.empty:
                st.success("PCL mapping criteria passed")
            else:
                st.write(mismatched_records)

    st.write("Data Validation")
    df2_values = set(df2['PCL code'].dropna().values)
    validation_result = df1.applymap(lambda x: x in df2_values if not pd.isna(x) else False)
    mismatched_values = {}
    for header, values in input_dict.items():
        for value in values:
            if value not in df2_values:
                mismatched_values.setdefault(header, []).append(value)

    if not mismatched_values:
        st.success("All values in input_dict exist in df2_values.")
    else:
        st.error("Some values in input_dict do not exist in df2_values.")
        st.header("Mismatched Values")
        st.write(mismatched_values)

if __name__ == "__main__":
    main()
