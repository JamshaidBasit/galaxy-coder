import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date
import json

# Google Sheets Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)
SHEET_URL = st.secrets["gsheets_url"]

def default_state():
    return {
        "username": "",
        "avatar": "🧑‍🚀",
        "xp": 0,
        "level": 1,
        "completed_missions": [],
        "earned_badges": [],
        "earned_certs": [],
        "streak": 0,
        "last_active": "",
        "battles_won": 0,
        "battles_played": 0,
        "perfect_missions": 0,
        "hints_used": 0,
        "current_planet": "mercury",
        "daily_xp": 0,
        "win_streak": 0,
        "joined": str(date.today()),
    }

@st.cache_data(ttl=60) # 1 minute tak data cache rahega, baar baar read nahi hoga
def get_all_users():
    try:
        df = conn.read(spreadsheet=SHEET_URL, ttl="0s")
        if not df.empty:
            # Username aur mission columns ko string mein convert karein taaki error na aaye
            for col in ['username', 'completed_missions', 'earned_badges', 'earned_certs']:
                if col in df.columns:
                    df[col] = df[col].astype(str).replace('nan', '')
        return df
    except Exception as e:
        return pd.DataFrame()

def load_user(username):
    """Specific user ka record load karein"""
    df = get_all_users()
    if not df.empty and username in df['username'].values:
        user_row = df[df['username'] == username].iloc[0]
        
        # String data ko wapas list mein badalna
        def to_list(val):
            if pd.isna(val) or val == "": return []
            return str(val).split(",")

        return {
            "username": str(user_row['username']),
            "avatar": str(user_row.get('avatar', '🧑‍🚀')),
            "xp": int(user_row['xp']),
            "level": int(user_row['level']),
            "completed_missions": to_list(user_row.get('completed_missions', "")),
            "earned_badges": to_list(user_row.get('earned_badges', "")),
            "earned_certs": to_list(user_row.get('earned_certs', "")),
            "streak": int(user_row.get('streak', 0)),
            "last_active": str(user_row.get('last_active', "")),
            "battles_won": int(user_row.get('battles_won', 0)),
            "battles_played": int(user_row.get('battles_played', 0)),
            "perfect_missions": int(user_row.get('perfect_missions', 0)),
            "hints_used": int(user_row.get('hints_used', 0)),
            "current_planet": str(user_row.get('current_planet', 'mercury')),
            "daily_xp": int(user_row.get('daily_xp', 0)),
            "win_streak": int(user_row.get('win_streak', 0)),
            "joined": str(user_row.get('joined', date.today())),
        }
    return None

def save_user_progress(gs):
    """Data ko Google Sheet mein save karein - with safety check"""
    # 1. Check karein ke kya username maujood hai
    if not gs.get("username"):
        return

    # 2. Rate limiting: Ek hi session mein baar baar save karne se bachne ke liye
    # Hum checks laga sakte hain ya simply caching use kar sakte hain
    try:
        df = get_all_users()
        
        def to_str(lst):
            return ",".join(map(str, lst)) if isinstance(lst, list) else ""

        new_data = {
            "username": gs["username"],
            "avatar": gs["avatar"],
            "xp": gs["xp"],
            "level": gs["level"],
            "completed_missions": to_str(gs["completed_missions"]),
            "earned_badges": to_str(gs["earned_badges"]),
            "earned_certs": to_str(gs["earned_certs"]),
            "streak": gs["streak"],
            "last_active": gs["last_active"],
            "battles_won": gs["battles_won"],
            "battles_played": gs["battles_played"],
            "perfect_missions": gs["perfect_missions"],
            "hints_used": gs["hints_used"],
            "current_planet": gs["current_planet"],
            "daily_xp": gs["daily_xp"],
            "win_streak": gs["win_streak"],
            "joined": gs["joined"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if not df.empty and gs["username"] in df['username'].values:
            # Sirf us bande ki row update karein
            df.loc[df['username'] == gs["username"]] = list(new_data.values())
        else:
            # Naya user add karein
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        conn.update(spreadsheet=SHEET_URL, data=df)
        # Save karne ke baad cache clear karein taaki agli baar naya data dikhe
        st.cache_data.clear()
        
    except Exception as e:
        if "429" in str(e):
            st.warning("🚀 Galaxy systems are busy saving data. Progress is cached locally!")
        else:
            st.error(f"Error saving to cloud: {e}")
# --- Baki logic (XP, Levels, Badges) hamesha ki tarah ---

def get_level(xp):
    from data.universe import XP_PER_LEVEL
    return max(1, xp // XP_PER_LEVEL + 1)

def get_level_progress(xp):
    from data.universe import XP_PER_LEVEL
    level = get_level(xp)
    level_start = (level - 1) * XP_PER_LEVEL
    level_xp = xp - level_start
    pct = (level_xp / XP_PER_LEVEL) * 100
    return level, level_xp, XP_PER_LEVEL, pct

def add_xp(gs, amount, mission_id=None):
    old_level = get_level(gs["xp"])
    gs["xp"] += amount
    gs["daily_xp"] = gs.get("daily_xp", 0) + amount
    if mission_id and mission_id not in gs["completed_missions"]:
        gs["completed_missions"].append(mission_id)
    new_level = get_level(gs["xp"])
    leveled_up = new_level > old_level
    # XP update hone par foran save karein
    save_user_progress(gs)
    return gs, leveled_up, new_level

def check_streak(gs):
    today = str(date.today())
    last = gs.get("last_active", "")
    if last == today:
        return gs
    yesterday = str(date.fromordinal(date.today().toordinal() - 1))
    gs["streak"] = gs.get("streak", 0) + 1 if last == yesterday else 1
    gs["last_active"] = today
    gs["daily_xp"] = 0
    save_user_progress(gs)
    return gs

def award_badge(gs, badge_name):
    new = []
    if badge_name and badge_name not in gs["earned_badges"]:
        gs["earned_badges"].append(badge_name)
        new.append(badge_name)
    
    from data.universe import GALAXY
    # Special badge logic
    if gs["battles_won"] >= 1 and "⚔️ Battle Winner" not in gs["earned_badges"]:
        gs["earned_badges"].append("⚔️ Battle Winner")
        new.append("⚔️ Battle Winner")
    
    if len(new) > 0:
        save_user_progress(gs)
    return gs, new

def check_certificates(gs):
    from data.universe import CERTIFICATES
    new_certs = []
    for cert in CERTIFICATES:
        if cert["id"] in gs.get("earned_certs", []):
            continue
        if all(m in gs["completed_missions"] for m in cert["required_missions"]):
            gs.setdefault("earned_certs", []).append(cert["id"])
            new_certs.append(cert)
    
    if new_certs:
        save_user_progress(gs)
    return gs, new_certs

def get_all_users_leaderboard():
    """Asli users ka leaderboard"""
    df = get_all_users()
    if df.empty: return []
    
    lb = df[['username', 'avatar', 'xp', 'level']].sort_values(by="xp", ascending=False).head(10)
    records = lb.to_dict('records')
    for i, r in enumerate(records):
        r["rank"] = i + 1
    return records

# ══════════════════════════════════════════════════════════════════════════════
# MULTIPLAYER LOBBY SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

def get_all_lobbies():
    """Lobbies wali sheet se sara data read karein"""
    try:
        # worksheet="lobbies" lazmi likhna hai jo aapne Sheet mein banayi hai
        return conn.read(spreadsheet=SHEET_URL, worksheet="lobbies", ttl="0s")
    except Exception:
        return pd.DataFrame()

def create_lobby(room_id, host_name):
    """Naya multiplayer room banayein"""
    df = get_all_lobbies()
    
    # Question selection (Randomly 5 questions pick karein)
    from data.universe import BATTLE_QUESTIONS
    selected_q = random.sample(BATTLE_QUESTIONS, 5)
    q_ids = ",".join([str(q['id']) for q in selected_q])

    new_lobby = {
        "room_id": str(room_id),
        "host_name": host_name,
        "players": host_name, # Shuru mein sirf host hoga
        "status": "waiting",
        "questions": q_ids,
        "scores": "0", # Initial score
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "winner": ""
    }

    if df.empty:
        df = pd.DataFrame([new_lobby])
    else:
        df = pd.concat([df, pd.DataFrame([new_lobby])], ignore_index=True)
    
    conn.update(spreadsheet=SHEET_URL, worksheet="lobbies", data=df)
    st.cache_data.clear()

def join_lobby(room_id, username):
    """Maujooda room mein join karein (Max 4 players)"""
    df = get_all_lobbies()
    if df.empty: return False
    
    room_id = str(room_id)
    if room_id in df['room_id'].values:
        idx = df.index[df['room_id'] == room_id][0]
        players = str(df.at[idx, 'players']).split(",")
        
        # Check if room is full or user already in
        if len(players) < 4 and username not in players:
            players.append(username)
            df.at[idx, 'players'] = ",".join(players)
            
            # Scores list ko bhi update karein (Initial 0 add karein)
            scores = str(df.at[idx, 'scores']).split(",")
            scores.append("0")
            df.at[idx, 'scores'] = ",".join(scores)
            
            conn.update(spreadsheet=SHEET_URL, worksheet="lobbies", data=df)
            st.cache_data.clear()
            return True
    return False

def get_lobby_status(room_id):
    """Room ka live data lein (Players, Status etc.)"""
    df = get_all_lobbies()
    if not df.empty and str(room_id) in df['room_id'].values:
        return df[df['room_id'] == str(room_id)].iloc[0].to_dict()
    return None

def start_lobby_battle(room_id):
    """Host jab 'Start' click kare toh status badal dein"""
    df = get_all_lobbies()
    if str(room_id) in df['room_id'].values:
        idx = df.index[df['room_id'] == str(room_id)][0]
        df.at[idx, 'status'] = 'active'
        conn.update(spreadsheet=SHEET_URL, worksheet="lobbies", data=df)
        st.cache_data.clear()