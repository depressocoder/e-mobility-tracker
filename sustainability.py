#sustainability tracking app

import streamlit as st
import pandas as pd
import numpy as np
import json

#constants

CO2_EMISSION_TRADITIONAL = 400 #grams per kg
CO2_EMISSION_EV = 200 #grams per kg

#load user data
def load_user_data():
    try:
        with open('user_data.json','r') as file:
            return json.load(file)
    except FileNotFoundError:
        return{}
    
#save user data to file

def save_user_data(data):
    with open('user_data.json','w') as file:
        json.dump(data,file,indent=4)
        
#calculate CO2 emissions

def calculate_co2_savings(miles):
    savings = (CO2_EMISSION_TRADITIONAL - CO2_EMISSION_EV) * miles / 1000  #tons of CO2 saved per mile
    return savings


#award badges

def award_badge(savings):
    if savings >= 50:
        return "Eco Warrior"
    elif savings >= 25:
        return "Sustainable Adventurer"
    elif savings >= 10:
        return "Green Thumb"
    else:
        return "No Badge"
    
#Streamlit app

st.title("Sustainability Tracker for EV Users 🌱")
st.sidebar.header("Navigation")
option = st.sidebar.radio('Choose an option',["Track Sustainability", "View Leaderboard", "Visualize Data"])

users=load_user_data()  

if option == 'Track Sustainability':
    st.subheader("Track your carbon savings")
    username= st.text_input("Enter your username", "").strip()
    
    if username:
        if username not in users:
            st.warning('New User detected....Setting up your account')
            users[username]={'miles':0,'co2_saved':0,'badges':[]}
            
        miles=st.number_input('Enter the miles you have driven with your EV:',min_value=0.0, step=0.1)
        savings = 0  # Initialize savings to a default value
         
        if st.button('Track'):
            savings = calculate_co2_savings(miles)
            users[username]['miles']+=miles
            users[username]["co2_saved"] += savings
            
        if savings > 0:            
            badge = award_badge(savings)
            if badge and badge not in users[username]['badges']:
                users[username]['badges'].append(badge)
                st.success(f'congratulations! you have earned the {badge} badge!')
            
        st.write(f"***Total miles driven***{users[username]['miles']:.2f}miles")
        st.write(f"**Total CO₂ Saved**: {users[username]['co2_saved']:.2f} kg")
        st.write(f"**Badges Earned**: {', '.join(users[username]['badges'])if users[username]['badges'] else 'None'}")
        
        save_user_data(users)
        
elif option == 'View Leaderboard':
    st.subheader('View the leaderboard')
    sorted_users = sorted(users.items(), key=lambda x: x[1].get('co2_saved', 0), reverse=True)
    if sorted_users:
        for i, (user, data) in enumerate(sorted_users, 1):
            st.write(f"{i}. **{user}** - {data.get('co2_saved', 0):.2f} kg CO₂ saved")
    else:
        st.write('No user Tracker yet')
            
           
elif option == 'Visualize Data':
    st.subheader('Visualize user data')
    if users:
        # Convert user data to DataFrame
        df = pd.DataFrame([
            {'Username': user,
             'Miles driven': data['miles'],
             'CO2 saved kg': data.get('co2_saved', 0)}
            for user, data in users.items()
        ])
        
        # Show the raw data table
        st.write('Raw Data Table')
        st.dataframe(df)
        
        # Barchart: Total miles driven
        st.write('Total miles driven by user')
        st.bar_chart(df.set_index('Username')['Miles driven'])
        
        # Barchart: Total CO2 saved
        st.write('Total CO₂ saved by user')
        st.bar_chart(df.set_index('Username')['CO2 saved kg'])
        
    else:
        st.write('No user Tracker yet. Track some miles first')
            
         
        
            
