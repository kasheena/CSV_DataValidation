import streamlit as st
import pandas as pd
import openpyxl
from functools import reduce

def read_sheets(file):
    """Read multiple sheets from an Excel file."""
    df_list = []
    wb = openpyxl.load_workbook(file)
    for sheet in wb.sheetnames:
        df_list.append(pd.read_excel(file, sheet_name=sheet))
    return df_list

def validate_data(df1, df2):
    """Check if records in df1 exist in df2."""
    matches = df1.apply(lambda x: df2.eq(x, axis=0).any(1), axis=1)
    return df1[~matches]

st.title("Data Validation App")

uploaded_file1 = st.file_uploader("Upload first CSV file (Workbook)", type="csv")
uploaded_file2 = st.file_uploader("Upload second CSV file", type="csv")

if uploaded_file1 and uploaded_file2:
    df_list1 = read_sheets(uploaded_file1)
    df_selector = st.selectbox("Select a sheet from the first file", df_list1.keys())
    df1 = df_list1[df_selector]

    # Display the first dataframe with editable options
    df1, selected_columns, selected_rows = st.columns((2, 1, 1))([df1, None, None])
    if st.button("Make Editable"):
        df1 = df1.set_index(selected_columns.multiselect("Select columns to set as index", df1.columns))
        df1 = df1.loc[selected_rows.multiselect("Select rows to display", df1.index)]

    df2 = pd.read_csv(uploaded_file2)

    # Validate data
    if st.button("Validate Data"):
        df_validated = validate_data(df1, df2)
        st.subheader("Validated Data")
        st.write(df_validated)
