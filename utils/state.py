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

def get_all_users():
    """Google Sheet se sara data read karein"""
    return conn.read(spreadsheet=SHEET_URL, ttl="0s")

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
    """Data ko Google Sheet mein save/update karein"""
    df = get_all_users()
    
    # Lists ko string mein convert karein Google Sheets ke liye
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
        df.loc[df['username'] == gs["username"]] = list(new_data.values())
    else:
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    conn.update(spreadsheet=SHEET_URL, data=df)
    st.cache_data.clear()

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