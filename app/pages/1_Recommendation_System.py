import folium
from folium import plugins
import streamlit as st
import pandas as pd
from datetime import datetime, time

@st.cache_data
def load_data():
    df = pd.read_csv('Final.csv')
    return df

df = load_data()

st.title("Alternative Recommendation System")

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []
if 'selected_neighbor' not in st.session_state:
    st.session_state.selected_neighbor = {}
if 'processed_results' not in st.session_state:
    st.session_state.processed_results = []

day_order = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

def add_place():
    hour = st.session_state.hour
    day = st.session_state.day
    place = st.session_state.place
    st.session_state.itinerary.append((hour, day, place))
    st.session_state.itinerary.sort(key=lambda x: (day_order[x[1]], x[0]))

def remove_place(index):
    st.session_state.itinerary.pop(index)

with st.form(key='itinerary_form'):
    col1, col2, col3 = st.columns(3)
    with col1:
        hour = st.time_input("Select hour", value=time(9, 0), key='hour')
    with col2:
        day = st.selectbox("Select day", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], key='day')
    with col3:
        place = st.selectbox("Select place", df['name'].unique(), key='place')
    add_button = st.form_submit_button("Add to Itinerary")

if add_button:
    add_place()

if st.button("Clear Itinerary"):
    st.session_state.itinerary = []
    st.session_state.selected_neighbor = {}
    st.session_state.processed_results = []
    st.rerun()

st.subheader("Itinerary")
for i, (hour, day, place) in enumerate(st.session_state.itinerary):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"{day} {hour.strftime('%H:%M')} - {place}")
    with col2:
        if st.button(f"Remove {place}", key=f"remove_{i}"):
            remove_place(i)
            st.rerun()

def is_place_open(row, day, hour):
    column_name = f"{day}_{hour:02d}"
    return row[column_name] > 0

def get_nearest_neighbors(place, day, hour):
    place_data = df[df['name'] == place].iloc[0]
    neighbors = place_data['nearest_neighbors'].split(', ')
    neighbor_details = []
    for neighbor in neighbors[:5]:
        name, distance = neighbor.split(':')
        neighbor_data = df[df['name'] == name].iloc[0]
        is_open = is_place_open(neighbor_data, day, int(hour.strftime('%H')))
        classification = neighbor_data[f"{day}_{hour.strftime('%H')}_category"]
        predicted_rating_category = neighbor_data['predicted_rating_category']
        neighbor_details.append((name, float(distance[:-2]), is_open, classification, predicted_rating_category))
    
    return neighbor_details

if st.button("Process Itinerary"):
    st.session_state.processed_results = []
    for hour, day, place in st.session_state.itinerary:
        place_data = df[df['name'] == place].iloc[0]
        column_name = f"{day}_{hour.strftime('%H')}_category"
        classification = place_data[column_name]
        is_open = is_place_open(place_data, day, int(hour.strftime('%H')))
        predicted_rating_category = place_data['predicted_rating_category']
        
        neighbors = []
        if classification == 'high' or not is_open or predicted_rating_category == 'Low':
            neighbors = get_nearest_neighbors(place, day, hour)
        
        st.session_state.processed_results.append(
            (place, classification, is_open, predicted_rating_category, neighbors)
        )


st.subheader("Processed Results")
for i, (place, classification, is_open, predicted_rating_category, neighbors) in enumerate(st.session_state.processed_results):
    open_status = "Open Status:**:green[OPEN]**" if is_open else "Open Status:**:red[CLOSED]**"
    rating_status = f" - Rating: **{predicted_rating_category.upper()}**"
    st.write(f"- {place} - Crowd:{classification.capitalize()} - {open_status}{rating_status}")
    
    if neighbors:
        st.write(f" → Nearest neighbors for {place}:")
        options = [
            f"{name} - {distance:.2f}km - Open Status:{'OPEN' if is_open else 'CLOSED'} - Crowd:{classification} - Rating:{predicted_rating_category}"
            for name, distance, is_open, classification, predicted_rating_category in neighbors
        ]
        selected_neighbor = st.radio(
            f"Select a neighbor for {place}", 
            options, 
            key=f"neighbor_{i}"
        )
        st.session_state.selected_neighbor[place] = selected_neighbor.split(' - ')[0]

if st.button("Reprocess with Selected Neighbors"):
    new_itinerary = []
    for hour, day, place in st.session_state.itinerary:
        if place in st.session_state.selected_neighbor:
            new_place = st.session_state.selected_neighbor[place]
            new_itinerary.append((hour, day, new_place))
        else:
            new_itinerary.append((hour, day, place))
    st.session_state.itinerary = new_itinerary
    st.session_state.selected_neighbor = {}
    st.session_state.processed_results = []
    st.rerun()

if st.button("Generate Map"):
    if st.session_state.itinerary:
        m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)
        
        for i, (hour, day, place) in enumerate(st.session_state.itinerary):
            place_data = df[df['name'] == place].iloc[0]
            folium.Marker(
                [place_data['latitude'], place_data['longitude']],
                popup=f"{i+1}. {place}",
                tooltip=f"{i+1}. {place}"
            ).add_to(m)
            
            if i < len(st.session_state.itinerary) - 1:
                next_place = st.session_state.itinerary[i+1][2]
                next_place_data = df[df['name'] == next_place].iloc[0]
                
                folium.plugins.AntPath(
                    locations=[
                        [place_data['latitude'], place_data['longitude']],
                        [next_place_data['latitude'], next_place_data['longitude']]
                    ],
                    popup=f"From {place} to {next_place}",
                    tooltip=f"From {place} to {next_place}",
                    weight=2,
                    color='blue',
                    dash_array=[10, 20]
                ).add_to(m)
        
        st.components.v1.html(m._repr_html_(), height=500)
    else:
        st.warning("Please add places to your itinerary before generating the map.")