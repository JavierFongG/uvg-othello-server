import streamlit as st 
import requests
from dotenv import load_dotenv
import pandas as pd 


# Load environment variables from .env file
load_dotenv()

# Get the BASE_URL from the .env file
# BASE_URL = os.getenv("BASE_URL")
BASE_URL = "http://localhost:8000"


st.set_page_config(layout="wide")

st.title("Admin")

st.header("Finish Match")

tournaments_req = requests.get(f"{BASE_URL}/tournament/list")
tournaments = tournaments_req.json().get("tournaments", [])
open_tournaments = [x for x in tournaments if x['status'] == "available"]

col1, col2 = st.columns(2)

with col1: 
    selected_tournament = st.selectbox("Select a tournament:", ["None"] + [t['name'] for t in open_tournaments])

with col2:
    players = []
    
    if selected_tournament != 'None':
        players_req = requests.get(f"{BASE_URL}/tournament/players/{selected_tournament}")   
        players_req = players_req.json()['players']
        players = [x['name'] for x in players_req]
    
    winner = st.selectbox("Select a winner:", players + ['None'])

finish_match = st.button('Finish')

if finish_match: 

    if selected_tournament and winner: 
        response = requests.post(f"{BASE_URL}/match/set-winner", json={
            "tournament_name": selected_tournament,
            "username": winner
        })

        if response.status_code == 200:
            st.success("Winner has been set successfully!")
        else:
            st.error(f"Failed to set winner: {response.text}")
        

st.header("Set player values")

tournaments_update_req = requests.get(f"{BASE_URL}/tournament/list")
tournaments_list = tournaments_update_req.json().get("tournaments", [])
open_tournaments_list = [x for x in tournaments_list if x['status'] == "available"]

col1, col2 = st.columns(2)

with col1: 
    selected_tournament_update = st.selectbox(key = "tournament_update", label = "Select a tournament:", options = ["None"] + [t['name'] for t in open_tournaments_list])

with col2:
    players_update_list = []
    
    if selected_tournament_update != 'None':
        players_update = requests.get(f"{BASE_URL}/tournament/players/{selected_tournament_update}")   
        players_update = players_update.json()['players']
        players_update_list = [x['name'] for x in players_update]
    
    player_update = st.selectbox("Select a player:", players_update_list + ['None'])

player_wins = st.slider("wins:", min_value=0, max_value=10, value=0)
player_draws = st.slider("draws:", min_value=0, max_value=10, value=0)
player_losses = st.slider("losses:", min_value=0, max_value=10, value=0)


update_player = st.button('Update')

if update_player: 
    if selected_tournament_update and player_update: 
        response = requests.post(f"{BASE_URL}/tournament/update-player-stats", json={
            "tournament_name": selected_tournament_update,
            "player_name": player_update,
            "wins" : player_wins, 
            "draws" : player_draws, 
            "losses" : player_losses
        })

        if response.status_code == 200:
            st.success("Winner has been set successfully!")
        else:
            st.error(f"Failed to set winner: {response.text}")