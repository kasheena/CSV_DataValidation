import streamlit as st
import pandas as pd

def read_csv(file_path):
    if file_path.name.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        st.error("Unsupported file format. Please upload a CSV file.")
        return None
    return df

def main():
    st.title("Data Validation App")

    st.sidebar.header("Upload Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload CSV file for DataFrame 1", type=["csv"])
    uploaded_file2 = st.sidebar.file_uploader("Upload CSV file for DataFrame 2", type=["csv"])

    if uploaded_file1 and uploaded_file2:
        # Read DataFrame 1
        df1 = read_csv(uploaded_file1)

        # Read DataFrame 2 and select 'PCL code' column
        df2 = read_csv(uploaded_file2)
        df2 = df2[['PCL code']]

        if df1 is not None and df2 is not None:
            # Compare DataFrames to find records in DataFrame 1 that don't exist in DataFrame 2
            df3 = pd.merge(df1, df2, how='left', left_on='PCL code', right_on='PCL code', indicator=True)
            df3 = df3[df3['_merge'] == 'left_only'].drop('_merge', axis=1)
            
            st.header("DataFrame 1")
            st.table(df1)

            st.header("DataFrame 2 (PCL code)")
            st.table(df2)

            st.header("Records not present in DataFrame 2")
            st.table(df3)

if __name__ == "__main__":
    main()
