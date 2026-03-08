import json, os
from datetime import datetime, date
import streamlit as st

SAVE_FILE = "galaxy_coder_save.json"

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

def load_state():
    if "gs" not in st.session_state:
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE) as f:
                    st.session_state.gs = json.load(f)
            except:
                st.session_state.gs = default_state()
        else:
            st.session_state.gs = default_state()
    return st.session_state.gs

def save_state(gs):
    st.session_state.gs = gs
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(gs, f, indent=2)
    except:
        pass

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
    return gs

def award_badge(gs, badge_name):
    new = []
    if badge_name and badge_name not in gs["earned_badges"]:
        gs["earned_badges"].append(badge_name)
        new.append(badge_name)
    # auto-check special badges
    from data.universe import GALAXY
    if gs["battles_won"] >= 1 and "⚔️ Battle Winner" not in gs["earned_badges"]:
        gs["earned_badges"].append("⚔️ Battle Winner")
        new.append("⚔️ Battle Winner")
    if gs.get("win_streak", 0) >= 5 and "🏆 Tournament Champion" not in gs["earned_badges"]:
        gs["earned_badges"].append("🏆 Tournament Champion")
        new.append("🏆 Tournament Champion")
    if gs.get("streak", 0) >= 7 and "🔥 On Fire" not in gs["earned_badges"]:
        gs["earned_badges"].append("🔥 On Fire")
        new.append("🔥 On Fire")
    if gs.get("perfect_missions", 0) >= 10 and "💎 Perfect Coder" not in gs["earned_badges"]:
        gs["earned_badges"].append("💎 Perfect Coder")
        new.append("💎 Perfect Coder")
    planets_visited = set()
    for mid in gs["completed_missions"]:
        for pid, pdata in GALAXY.items():
            for m in pdata["missions"]:
                if m["id"] == mid:
                    planets_visited.add(pid)
    if len(planets_visited) >= 5 and "🌟 Galaxy Explorer" not in gs["earned_badges"]:
        gs["earned_badges"].append("🌟 Galaxy Explorer")
        new.append("🌟 Galaxy Explorer")
    return gs, new

def check_certificates(gs):
    from data.universe import CERTIFICATES
    new_certs = []
    for cert in CERTIFICATES:
        if cert["id"] in gs.get("earned_certs", []):
            continue
        required = cert["required_missions"]
        completed = gs["completed_missions"]
        if all(m in completed for m in required):
            gs.setdefault("earned_certs", []).append(cert["id"])
            new_certs.append(cert)
    return gs, new_certs

def get_leaderboard(gs):
    sample = [
        {"name": "ZaraKhan", "avatar": "👩‍🚀", "xp": 4800, "level": 16, "planet": "♂ Mars"},
        {"name": "AliHero",  "avatar": "🧑‍🚀", "xp": 4200, "level": 14, "planet": "♂ Mars"},
        {"name": "NovaX",    "avatar": "👾",   "xp": 3600, "level": 12, "planet": "🌍 Earth"},
        {"name": "OmarDev",  "avatar": "🤖",   "xp": 2900, "level": 9,  "planet": "🌍 Earth"},
        {"name": "SkyBlue",  "avatar": "💫",   "xp": 1800, "level": 6,  "planet": "♀ Venus"},
    ]
    user = {
        "name": f"⭐ {gs.get('username','You')}",
        "avatar": gs.get("avatar", "🧑‍🚀"),
        "xp": gs["xp"],
        "level": get_level(gs["xp"]),
        "planet": "☿ Mercury"
    }
    all_entries = sample + [user]
    all_entries.sort(key=lambda x: x["xp"], reverse=True)
    for i, e in enumerate(all_entries):
        e["rank"] = i + 1
    return all_entries
