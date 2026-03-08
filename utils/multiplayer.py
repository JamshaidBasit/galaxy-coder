"""
Multiplayer Battle System for Galaxy Coder
Converted from JSON to Google Sheets Backend
"""
import streamlit as st
import pandas as pd
import time
import random
import hashlib
from datetime import datetime
from utils.state import conn, SHEET_URL

def _load_lobby_df():
    """Google Sheet se lobbies ka data read karein"""
    try:
        return conn.read(spreadsheet=SHEET_URL, worksheet="lobbies", ttl="0s")
    except:
        return pd.DataFrame()

def _save_lobby_df(df):
    """Google Sheet mein data update karein"""
    try:
        conn.update(spreadsheet=SHEET_URL, worksheet="lobbies", data=df)
        st.cache_data.clear()
        return True
    except:
        return False

def create_battle_room(host_name, host_avatar, difficulty="beginner"):
    """Create a new multiplayer battle room in Google Sheets"""
    # Generate a unique 6-digit room ID
    room_id = hashlib.md5(f"{host_name}{time.time()}".encode()).hexdigest()[:6].upper()
    df = _load_lobby_df()
    
    # Import questions from your data file
    from data.universe import BATTLE_QUESTIONS
    
    # FIX: Handle BATTLE_QUESTIONS structure
    # If it's a dict (e.g. {"beginner": [...]}), get the specific list
    if isinstance(BATTLE_QUESTIONS, dict):
        q_pool = BATTLE_QUESTIONS.get(difficulty, [])
        # If the difficulty list is empty, fallback to the first available category
        if not q_pool:
            q_pool = list(BATTLE_QUESTIONS.values())[0]
    else:
        # If it's already a list of dicts, filter by difficulty
        q_pool = [q for q in BATTLE_QUESTIONS if isinstance(q, dict) and q.get('difficulty') == difficulty]

    # Final safety: if pool is still empty, use whatever is in BATTLE_QUESTIONS
    if not q_pool:
        q_pool = BATTLE_QUESTIONS if isinstance(BATTLE_QUESTIONS, list) else list(BATTLE_QUESTIONS.values())[0]

    # Select 5 random questions
    selected_qs = random.sample(q_pool, min(5, len(q_pool)))
    q_ids = ",".join([str(q['id']) for q in selected_qs])

    # Prepare the new row for Google Sheets
    new_room = {
        "room_id": room_id,
        "host_name": host_name,
        "players": host_name,        # Comma separated string for Sheets
        "status": "waiting",
        "questions": q_ids,
        "scores": "0",               # Initial score for host
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "winner": ""
    }

    # Append to dataframe and save to Sheets
    df = pd.concat([df, pd.DataFrame([new_room])], ignore_index=True)
    _save_lobby_df(df)
    
    return room_id

def join_battle_room(room_id, player_name, player_avatar=None):
    """Join an existing battle room in Google Sheets"""
    df = _load_lobby_df()
    room_id = room_id.upper().strip()
    
    if df.empty or room_id not in df['room_id'].values:
        return False, "Room not found!"
    
    idx = df.index[df['room_id'] == room_id][0]
    
    if df.at[idx, 'status'] != "waiting":
        return False, "Battle already started!"
    
    players = str(df.at[idx, 'players']).split(",")
    if len(players) >= 4:
        return False, "Room is full!"
    
    if player_name not in players:
        players.append(player_name)
        df.at[idx, 'players'] = ",".join(players)
        
        # Scores list mein bhi initial 0 add karein
        scores = str(df.at[idx, 'scores']).split(",")
        scores.append("0")
        df.at[idx, 'scores'] = ",".join(scores)
        
        _save_lobby_df(df)
    
    return True, room_id

def get_room(room_id):
    """Get current room state from Sheets and format it like the old JSON"""
    df = _load_lobby_df()
    room_id = room_id.upper()
    
    if df.empty or room_id not in df['room_id'].values:
        return None
        
    row = df[df['room_id'] == room_id].iloc[0]
    
    # Format conversion: Google Sheet string to Dictionary (taaki app.py na tootey)
    players_list = str(row['players']).split(",")
    scores_list = str(row['scores']).split(",")
    
    formatted_players = {}
    for i, p_name in enumerate(players_list):
        formatted_players[p_name] = {
            "name": p_name,
            "score": int(scores_list[i]) if i < len(scores_list) else 0,
            "ready": True if row['status'] != "waiting" else False
        }

    return {
        "id": row['room_id'],
        "host": row['host_name'],
        "status": row['status'],
        "players": formatted_players,
        "questions": str(row['questions']).split(","),
        "winner": row['winner']
    }

def submit_answer(room_id, player_name, q_index, answer_idx, is_correct):
    """Update score in Google Sheet"""
    if not is_correct: return True
    
    df = _load_lobby_df()
    room_id = room_id.upper()
    
    if room_id in df['room_id'].values:
        idx = df.index[df['room_id'] == room_id][0]
        players = str(df.at[idx, 'players']).split(",")
        scores = str(df.at[idx, 'scores']).split(",")
        
        if player_name in players:
            p_idx = players.index(player_name)
            current_score = int(scores[p_idx]) if p_idx < len(scores) else 0
            scores[p_idx] = str(current_score + 1)
            df.at[idx, 'scores'] = ",".join(scores)
            _save_lobby_df(df)
    return True

def finish_battle(room_id, winner_name=""):
    """Mark battle as finished in Sheets"""
    df = _load_lobby_df()
    room_id = room_id.upper()
    if room_id in df['room_id'].values:
        idx = df.index[df['room_id'] == room_id][0]
        df.at[idx, 'status'] = "finished"
        df.at[idx, 'winner'] = winner_name
        _save_lobby_df(df)

def list_open_rooms():
    """List all waiting rooms from Sheets"""
    df = _load_lobby_df()
    if df.empty: return []
    
    open_rooms = []
    waiting_rooms = df[df['status'] == 'waiting']
    
    for _, row in waiting_rooms.iterrows():
        open_rooms.append({
            "id": row['room_id'],
            "host": row['host_name'],
            "players": len(str(row['players']).split(",")),
            "difficulty": "standard"
        })
    return open_rooms