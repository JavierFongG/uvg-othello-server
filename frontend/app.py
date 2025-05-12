import streamlit as st
import pandas as pd
import requests 
# from streamlit_autorefresh import st_autorefresh
# Set Streamlit to wide mode

st.set_page_config(layout="wide")

def count_pieces(board):
    black = sum(row.count(-1) for row in board)
    white = sum(row.count(1) for row in board)
    return black, white

def matches_to_dataframe(match_data):
    rows = []
    for match in match_data["matches"]:
        black_name = match["black_player"]["name"]
        white_name = match["white_player"]["name"]
        board = match["board"]
        status = match["status"]
        black_count, white_count = count_pieces(board)

        rows.append({
            "black_player": black_name,
            "white_player": white_name,
            "black_pieces_count": black_count,
            "white_pieces_count": white_count,
            "status": status
        })

    return pd.DataFrame(rows)

BASE_URL = 'https://7b679617-8c6b-4d0f-bb51-0505412c6c17.us-east-1.cloud.genez.io'

# Initialize session state for tournament data
if "tournament_data" not in st.session_state:
    st.session_state.tournament_data = pd.DataFrame(columns=["Player", "Wins", "Losses", "Draws"])

# Title of the app
st.title("Othello Tournament Tracker")

# Input for tournament name
tournament_name = st.text_input("Enter Tournament Name", "")

# Display tournament name
if tournament_name:
    st.header(f"Tournament: {tournament_name}")

req = requests.get(f"{BASE_URL}/tournament/available")

available_tournaments = req.json()['available_tournaments']

if tournament_name:
    if tournament_name not in available_tournaments: 
        req = requests.post("{BASE_URL}/tournament/create", json={"name": tournament_name})

    req = requests.get(f"{BASE_URL}/tournament/players/{tournament_name}")

    # st.json(req.json())
    st.dataframe(pd.DataFrame(req.json()['players']))

    play_button = st.button('Play')

    if play_button: 
        req = requests.post("{BASE_URL}/pair/", params={"tournament_name": tournament_name})
        
        if req.status_code == 200: 
            st.text('Empecemos!!!')
        if req.status_code == 400: 
            st.text('Espera! Aun no ha terminado la partida anterior')

        # Example usage:
    
    
    refresh_button = st.button('Refresh')

    if refresh_button:
        matches = matches_to_dataframe(requests.get(f"{BASE_URL}/tournament/matches/{tournament_name}").json())

        st.subheader('Ongoing Matches')
        st.dataframe(matches[matches['status'] == "ongoing"])

        st.subheader('Ended Matches')
        st.dataframe(matches[matches['status'] == "ended"])


    