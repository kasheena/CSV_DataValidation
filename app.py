def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload Workbook (CSV 1 or Excel)", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])
    selected_sheets = None

    if uploaded_file1 and uploaded_file1.name.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
        st.sidebar.write("Choose sheets from CSV file:")
        selected_sheets = st.sidebar.multiselect("Select sheets from the workbook:", [])

    uploaded_file2 = st.sidebar.file_uploader("Upload CSV 2 or Excel", type=["csv", "xls", "xlsx", "xlsm", "xlsb"])

    if uploaded_file1 and uploaded_file2:
        df1 = read_file(uploaded_file1, selected_sheets)
        df2 = read_file(uploaded_file2)

        if df1 is not None and df2 is not None:
            st.header("DataFrame 1")

            # Display DataFrame 1
            st.table(df1)

            st.header("DataFrame 2")
            st.table(df2)

            # Data validation
            validation_result = pd.merge(df1, df2, how='left', indicator=True).query('_merge == "left_only"').drop('_merge', axis=1)

            st.header("Validation Result")
            st.table(validation_result)

if __name__ == "__main__":
    main()
