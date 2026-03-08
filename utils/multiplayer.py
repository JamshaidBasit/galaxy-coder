"""
Multiplayer Battle System for Galaxy Coder
Uses a shared JSON file as simple backend (works on Streamlit Cloud too)
For production: replace with a real database
"""
import json
import os
import time
import random
import hashlib
from datetime import datetime

BATTLE_FILE = "multiplayer_battles.json"
LOBBY_FILE = "battle_lobby.json"

def _load(path, default):
    try:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    except:
        pass
    return default

def _save(path, data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def create_battle_room(host_name, host_avatar, difficulty="beginner"):
    """Create a new multiplayer battle room"""
    room_id = hashlib.md5(f"{host_name}{time.time()}".encode()).hexdigest()[:6].upper()
    lobby = _load(LOBBY_FILE, {})
    lobby[room_id] = {
        "id": room_id,
        "host": host_name,
        "host_avatar": host_avatar,
        "difficulty": difficulty,
        "status": "waiting",  # waiting / active / finished
        "players": {
            host_name: {
                "name": host_name,
                "avatar": host_avatar,
                "score": 0,
                "answered": [],
                "ready": False
            }
        },
        "questions": [],
        "current_q": 0,
        "created_at": datetime.now().isoformat(),
        "max_players": 4
    }
    _save(LOBBY_FILE, lobby)
    return room_id

def join_battle_room(room_id, player_name, player_avatar):
    """Join an existing battle room"""
    lobby = _load(LOBBY_FILE, {})
    room_id = room_id.upper().strip()
    if room_id not in lobby:
        return False, "Room not found!"
    room = lobby[room_id]
    if room["status"] != "waiting":
        return False, "Battle already started!"
    if len(room["players"]) >= room["max_players"]:
        return False, "Room is full!"
    if player_name in room["players"]:
        return True, room_id  # Already in room
    room["players"][player_name] = {
        "name": player_name,
        "avatar": player_avatar,
        "score": 0,
        "answered": [],
        "ready": False
    }
    _save(LOBBY_FILE, lobby)
    return True, room_id

def get_room(room_id):
    """Get current room state"""
    lobby = _load(LOBBY_FILE, {})
    return lobby.get(room_id.upper(), None)

def set_player_ready(room_id, player_name, questions=None):
    """Mark player as ready, optionally set questions"""
    lobby = _load(LOBBY_FILE, {})
    room_id = room_id.upper()
    if room_id not in lobby:
        return False
    room = lobby[room_id]
    if player_name in room["players"]:
        room["players"][player_name]["ready"] = True
    # Host sets questions
    if questions and room["host"] == player_name:
        room["questions"] = questions
    # Check if all ready
    all_ready = all(p["ready"] for p in room["players"].values())
    if all_ready and len(room["questions"]) > 0:
        room["status"] = "active"
    _save(LOBBY_FILE, lobby)
    return True

def submit_answer(room_id, player_name, q_index, answer_idx, is_correct):
    """Submit a player's answer"""
    lobby = _load(LOBBY_FILE, {})
    room_id = room_id.upper()
    if room_id not in lobby:
        return False
    room = lobby[room_id]
    if player_name not in room["players"]:
        return False
    player = room["players"][player_name]
    # Only count first answer per question
    if q_index not in player["answered"]:
        player["answered"].append(q_index)
        if is_correct:
            player["score"] += 1
    _save(LOBBY_FILE, lobby)
    return True

def get_battle_results(room_id):
    """Get ranked results"""
    room = get_room(room_id)
    if not room:
        return []
    players = list(room["players"].values())
    players.sort(key=lambda x: x["score"], reverse=True)
    return players

def finish_battle(room_id):
    """Mark battle as finished"""
    lobby = _load(LOBBY_FILE, {})
    room_id = room_id.upper()
    if room_id in lobby:
        lobby[room_id]["status"] = "finished"
        _save(LOBBY_FILE, lobby)

def list_open_rooms():
    """List all open rooms"""
    lobby = _load(LOBBY_FILE, {})
    open_rooms = []
    now = time.time()
    for rid, room in lobby.items():
        if room["status"] == "waiting":
            created = datetime.fromisoformat(room["created_at"]).timestamp()
            # Only show rooms created in last 30 minutes
            if now - created < 1800:
                open_rooms.append({
                    "id": rid,
                    "host": room["host"],
                    "players": len(room["players"]),
                    "difficulty": room["difficulty"]
                })
    return open_rooms

def cleanup_old_rooms():
    """Remove rooms older than 2 hours"""
    lobby = _load(LOBBY_FILE, {})
    now = time.time()
    to_remove = []
    for rid, room in lobby.items():
        try:
            created = datetime.fromisoformat(room["created_at"]).timestamp()
            if now - created > 7200:
                to_remove.append(rid)
        except:
            to_remove.append(rid)
    for rid in to_remove:
        del lobby[rid]
    if to_remove:
        _save(LOBBY_FILE, lobby)
