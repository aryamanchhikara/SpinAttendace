import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime


page_title = "SRC Spin Class Check in "
page_icon = ":sports_medal:"
layout = "centered"

# Set the Streamlit page configuration
st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title + " " + page_icon)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('students_attendance.db')
c = conn.cursor()

# Create the attendance table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        name TEXT,
        attendance_count INTEGER,
        last_attendance_date TEXT
    )
''')
conn.commit()


# Initialize session state variables
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'count' not in st.session_state:
    st.session_state.count = None

# Input form
with st.form(key='attendance_form'):
    name = st.text_input(label='Please Enter Full Name', value=st.session_state.name)
    submit_button = st.form_submit_button(label='Submit')


if submit_button:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Check if the name already exists in the database
    c.execute('SELECT * FROM attendance WHERE name = ?', (name,))
    record = c.fetchone()
    
    if record:
        # Update the existing record
        new_count = record[1] + 1
        c.execute('''
            UPDATE attendance
            SET attendance_count = ?, last_attendance_date = ?
            WHERE name = ?
        ''', (new_count, current_date, name))
        st.session_state.count = new_count
    else:
        # Add a new record
        c.execute('''
            INSERT INTO attendance (name, attendance_count, last_attendance_date)
            VALUES (?, ?, ?)
        ''', (name, 1, current_date))
        st.session_state.count = 1
    
    conn.commit()
    st.success('Attendance recorded')
    
    # Clear the text field by resetting session state
    st.session_state.name = ''

# Display the entered name and count
if st.session_state.count is not None:
    st.subheader(f'Name: {name}')
    st.subheader(f'Classes Attended: {st.session_state.count}')

# Fetch the data from the database to display
#df = pd.read_sql('SELECT * FROM attendance', conn)
#st.subheader('Current Attendance Data')
#st.dataframe(df)

# Close the database connection 
conn.close()

# ------- navigation Links ----------

