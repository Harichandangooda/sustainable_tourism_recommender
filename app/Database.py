import streamlit as st
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import ast

DB_HOST = "34.55.113.234"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "dicproject"
DB_PORT = 5432

@st.cache_resource
def get_connection():
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return engine.connect()

from sqlalchemy import text

def run_query(query, params=None):
    conn = get_connection()
    with conn.begin():
        if params:
            result = conn.execute(text(query), params)
        else:
            result = conn.execute(text(query))
    return result

st.title("Similar Places Recommendation System - Database Manager")

menu = ["View Data", "Add Entry", "Modify Entry", "Remove Entry"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Data":
    st.subheader("View Data")
    query = "SELECT s_no, name, popular_times, latitude, longitude, working_hours, city, us_state, rating FROM attractions ORDER BY s_no ASC;"
    result = run_query(query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    st.dataframe(df, hide_index=True)

elif choice == "Add Entry":
    st.subheader("Add New Entry")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        popular_times = st.text_area("Popular Times")
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
        working_hours = st.text_input("Working Hours")
    with col2:
        city = st.text_input("City")
        us_state = st.text_input("US State")
        rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1)
    
    if st.button("Add Entry"):
        try:
            query_max_sno = "SELECT MAX(s_no) FROM attractions;"
            result = run_query(query_max_sno)
            max_sno = result.fetchone()[0] 
            new_sno = max_sno + 1 if max_sno is not None else 1 
            
            query = """
                INSERT INTO attractions 
                (s_no, name, popular_times, latitude, longitude, working_hours, city, us_state, rating) 
                VALUES (:s_no, :name, :popular_times, :latitude, :longitude, :working_hours, :city, :us_state, :rating)
            """

            params = {
                "s_no": new_sno,
                "name": name,
                "popular_times": popular_times,
                "latitude": latitude,
                "longitude": longitude,
                "working_hours": working_hours,
                "city": city,
                "us_state": us_state,
                "rating": rating
            }

            print("Query:", query)
            print("Params:", params)

            run_query(query, params)
            st.success("Entry added successfully!")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Modify Entry":
    st.subheader("Modify Existing Entry")
    
    s_no_to_update = st.number_input("s_no to Update", step=1, min_value=1)
    
    column_to_update = st.selectbox(
        "Column to Update", 
        ["name", "popular_times", "latitude", "longitude", "working_hours", "city", "us_state", "rating"]
    )
    
    new_value = st.text_input("New Value")
    
    if st.button("Update Entry"):
        try:
            if column_to_update in ["latitude", "longitude", "rating"]:
                new_value = float(new_value)
            elif column_to_update == "s_no":
                new_value = int(new_value)
            
            query = f"UPDATE attractions SET {column_to_update} = :value WHERE s_no = :id"
            params = {"value": new_value, "id": s_no_to_update}
            
            run_query(query, params)
            
            st.success(f"Entry with s_no {s_no_to_update} updated successfully!")
        
        except ValueError:
            st.error("Invalid data type for the selected column. Please enter the correct value.")
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Remove Entry":
    st.subheader("Remove Entry")
    
    s_no_to_delete = st.number_input("s_no to Delete", step=1)
    
    if st.button("Delete Entry"):
        try:
            query = "DELETE FROM attractions WHERE s_no = :s_no"
            
            params = {"s_no": s_no_to_delete}
            
            print("Query:", query)
            print("Params:", params)
            
            run_query(query, params)
            st.success("Entry removed successfully!")
        except Exception as e:
            st.error(f"Error: {e}")