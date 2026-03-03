import streamlit as st
import pandas as pd
import sqlite3  # Replace with your DB-API library

# Replace with your database credentials
database = 'DEPI1.db' 
conn = sqlite3.connect(database) 

def execute_query(query):
    df = pd.read_sql(query, conn)
    return df

def main():
    st.set_page_config(page_title="Hospital Depi Executor", layout="wide")
    st.title("Hospital Depi Executor")

    st.sidebar.header("Show the tables in the database")
    if st.sidebar.button("show tables") : 
        df = pd.read_sql("""SELECT * FROM sqlite_master WHERE type='table';""", conn); 
        st.dataframe(df)

    st.sidebar.header("show the metadata of the tables in the database")
    tables_names = 0 
    tables_df = pd.read_sql("""SELECT name FROM sqlite_master WHERE type='table';""", conn)
    tables_names = tables_df['name'].tolist()

    def extract_table_metaData(tables_names, conn):
        tables_data = {}
        for t in tables_names: 
            qry = f"""SELECT * FROM {t} WHERE 1=0;"""  # Changed to 1=0 to avoid fetching data
            tbl = pd.read_sql(qry, conn) 
            tables_data[t] = tbl.columns 
        
        return tables_data 

    if tables_names:
        selected_table = st.sidebar.selectbox("Select a table", [""] + tables_names)
    
        if selected_table:
            table_metadata = extract_table_metaData([selected_table], conn)
            st.write(f"Metadata for table {selected_table}:")
            st.write(table_metadata[selected_table])
        else:
            st.write(" ")
    else:
        st.write("No tables found in the database.")

    st.sidebar.header("Enter SQL Query")
    query = st.sidebar.text_area("SQL Query", height=200)

    if st.sidebar.button("Execute Query"):
        if query.strip():
            try:
                with st.spinner("Executing query..."):
                    df = execute_query(query)
                st.success("Query executed successfully!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
        else:
            st.warning("Please enter a valid SQL query.")

if __name__ == "__main__":
    main()