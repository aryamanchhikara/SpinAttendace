import streamlit as st
import pandas as pd
from datetime import datetime

EXCEL_FILE = 'students_attendance.xlsx'

# Try to read the Excel file, if it does not exist create an empty DataFrame
try:
    df = pd.read_excel(EXCEL_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Name', 'Attendance Count', 'Last Attendance Date'])

st.title('SRC Spin Class Check in: ')

# Input form
with st.form(key='attendance_form'):
    name = st.text_input(label='Name')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Check if the name already exists in the DataFrame
    if name in df['Name'].values:
        # Update the existing record
        df.loc[df['Name'] == name, 'Attendance Count'] += 1
        df.loc[df['Name'] == name, 'Last Attendance Date'] = current_date
    else:
        # Add a new record
        new_data = pd.DataFrame({'Name': [name], 'Attendance Count': [1], 'Last Attendance Date': [current_date]})
        df = pd.concat([df, new_data], ignore_index=True)
    
    df.to_excel(EXCEL_FILE, index=False)
    st.success('Attendance recorded')

# Display the data
st.subheader('Current Attendance Data')
st.dataframe(df)

