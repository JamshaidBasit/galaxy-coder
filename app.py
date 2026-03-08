import streamlit as st
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.universe import GALAXY, ACHIEVEMENTS, CERTIFICATES, BATTLE_QUESTIONS, XP_PER_LEVEL
from utils.state import (load_user, save_user_progress, default_state, 
                          get_level, get_level_progress, add_xp, check_streak, 
                          award_badge, check_certificates, get_all_users_leaderboard)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Galaxy Coder — Zero to AI Hero",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Dark Space Theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;900&family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

:root {
  --space: #020817;
  --nebula: #0D1B2A;
  --panel: #0F2336;
  --panel2: #132C41;
  --border: rgba(56,189,248,0.12);
  --cyan: #38BDF8;
  --gold: #FBBF24;
  --purple: #A78BFA;
  --green: #34D399;
  --red: #F87171;
  --orange: #FB923C;
  --text: #E2E8F0;
  --muted: #64748B;
  --glow-c: 0 0 24px rgba(56,189,248,0.35);
  --glow-g: 0 0 24px rgba(251,191,36,0.35);
  --glow-p: 0 0 24px rgba(167,139,250,0.35);
}

html, body, .stApp { background: var(--space) !important; color: var(--text) !important;
  font-family: 'Exo 2', sans-serif !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton { display:none !important; }

/* Sidebar — multiple selectors for Streamlit version compatibility */
[data-testid="stSidebar"],
section[data-testid="stSidebar"],
.css-1d391kg, .css-hxt7ib, .css-6qob1r {
  background: var(--nebula) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Force sidebar visible */
[data-testid="stSidebarContent"] { display: block !important; visibility: visible !important; }
[data-testid="collapsedControl"] { display: flex !important; }

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, #0C4A6E, #1E3A5F) !important;
  color: var(--cyan) !important; border: 1px solid rgba(56,189,248,0.3) !important;
  font-family: 'Exo 2', sans-serif !important; font-weight: 700 !important;
  border-radius: 8px !important; transition: all 0.25s !important; letter-spacing: 0.5px !important;
}
.stButton > button:hover { background: linear-gradient(135deg,#0EA5E9,#7C3AED) !important;
  color: white !important; box-shadow: var(--glow-c) !important; transform: translateY(-1px) !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
  background: var(--panel) !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 8px !important;
  font-family: 'Exo 2', sans-serif !important; }
.stTextArea textarea { font-family: 'Share Tech Mono', monospace !important; font-size: 13px !important; }

/* Progress bars */
.stProgress > div > div > div { background: linear-gradient(90deg, #38BDF8, #A78BFA) !important; border-radius: 999px !important; }

/* Metrics */
[data-testid="stMetric"] { background: var(--panel) !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important; padding: 12px !important; }
[data-testid="stMetricValue"] { color: var(--cyan) !important; font-family: 'Orbitron', sans-serif !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: var(--panel) !important; border-radius: 10px !important; padding: 3px !important; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Exo 2', sans-serif !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg,rgba(56,189,248,0.2),rgba(167,139,250,0.2)) !important;
  color: var(--cyan) !important; border-radius: 7px !important; }

/* Alerts */
.stSuccess > div { background: rgba(52,211,153,0.08) !important; border-color: rgba(52,211,153,0.4) !important; }
.stError > div { background: rgba(248,113,113,0.08) !important; border-color: rgba(248,113,113,0.4) !important; }
.stWarning > div { background: rgba(251,191,36,0.08) !important; border-color: rgba(251,191,36,0.4) !important; }
.stInfo > div { background: rgba(56,189,248,0.08) !important; border-color: rgba(56,189,248,0.3) !important; }

/* Headings */
h1 { font-family: 'Orbitron', sans-serif !important; color: var(--cyan) !important; letter-spacing: 2px !important; }
h2, h3 { font-family: 'Exo 2', sans-serif !important; color: var(--text) !important; }
h4 { color: var(--muted) !important; }
code, pre { font-family: 'Share Tech Mono', monospace !important;
  background: rgba(2,8,23,0.8) !important; border: 1px solid rgba(56,189,248,0.15) !important; border-radius: 6px !important; }
hr { border-color: var(--border) !important; }

/* ── Custom Components ── */
.planet-card {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 16px; padding: 20px; text-align: center;
  transition: all 0.3s; position: relative; overflow: hidden; cursor: pointer;
}
.planet-card.unlocked:hover { transform: translateY(-4px); border-color: rgba(56,189,248,0.4); }
.planet-card.locked { opacity: 0.45; cursor: not-allowed; }
.planet-card::after { content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 50% 0%, rgba(56,189,248,0.06), transparent 60%); }

.mission-row {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;
  transition: all 0.25s; cursor: pointer; display: flex; align-items: center; gap: 14px;
}
.mission-row.done { border-color: rgba(52,211,153,0.3); background: rgba(52,211,153,0.04); }
.mission-row:hover:not(.done) { border-color: rgba(56,189,248,0.35); transform: translateX(4px); }

.hud-bar {
  background: var(--nebula); border: 1px solid var(--border);
  border-radius: 12px; padding: 12px 20px;
  display: flex; align-items: center; gap: 20px; margin-bottom: 16px;
}

.xp-fill { height: 8px; border-radius: 999px;
  background: linear-gradient(90deg, #38BDF8, #A78BFA);
  box-shadow: 0 0 8px rgba(56,189,248,0.5); transition: width 0.8s; }
.xp-track { background: rgba(255,255,255,0.06); border-radius: 999px; height: 8px; overflow: hidden; }

.step-card { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.step-card.active { border-color: rgba(56,189,248,0.4); box-shadow: var(--glow-c); }

.battle-opt { background: var(--panel); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 18px; margin-bottom: 8px;
  cursor: pointer; transition: all 0.2s; font-size: 15px; }
.battle-opt:hover { border-color: var(--cyan); background: rgba(56,189,248,0.08); }
.battle-opt.correct { border-color: var(--green); background: rgba(52,211,153,0.1); }
.battle-opt.wrong { border-color: var(--red); background: rgba(248,113,113,0.1); }

.cert-card { border-radius: 16px; padding: 28px; text-align: center;
  border: 2px solid; position: relative; overflow: hidden; }

.badge-pill { display: inline-block; padding: 4px 12px; border-radius: 999px;
  font-size: 12px; font-weight: 700; margin: 3px; }

.stat-box { background: var(--panel); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px; text-align: center; }

.lb-row { background: var(--panel); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 16px; margin-bottom: 6px;
  display: flex; align-items: center; gap: 14px; }
.lb-row.gold { border-color: rgba(251,191,36,0.4); background: rgba(251,191,36,0.04); }
.lb-row.silver { border-color: rgba(148,163,184,0.4); }
.lb-row.bronze { border-color: rgba(180,120,60,0.4); }
.lb-row.me { border-color: rgba(56,189,248,0.4); background: rgba(56,189,248,0.04); }

.quiz-option { background: var(--panel); border: 1px solid var(--border);
  border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;
  cursor: pointer; transition: all 0.2s; text-align: left; width: 100%; }
.quiz-option:hover { border-color: var(--cyan); }
.quiz-option.correct { border-color: var(--green) !important; background: rgba(52,211,153,0.1) !important; }
.quiz-option.wrong { border-color: var(--red) !important; background: rgba(248,113,113,0.1) !important; }

/* Stars background */
.stars-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none; z-index: 0; overflow: hidden; }

/* Onboarding */
.onboard-container { max-width: 680px; margin: 0 auto; padding: 60px 20px; text-align: center; }
</style>

<div class="stars-bg">
  <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
    <defs><radialGradient id="g1" cx="50%" cy="30%"><stop offset="0%" stop-color="#0D1B2A"/><stop offset="100%" stop-color="#020817"/></radialGradient></defs>
    <rect width="100%" height="100%" fill="url(#g1)"/>
  </svg>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION INIT
# ══════════════════════════════════════════════════════════════════════════════
def init():
    defaults = {
        "page": "galaxy",
        "active_planet": None,
        "active_mission": None,
        "mission_step": 0,
        "code_output": {},
        "quiz_answered": {},
        "battle_q_idx": 0,
        "battle_score": 0,
        "battle_active": False,
        "battle_difficulty": "beginner",
        "battle_answered": None,
        "chat": [],
        "notifications": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
# ✅ Naya Code:
if "gs" not in st.session_state:
    st.session_state.gs = default_state()
gs = st.session_state.gs
if st.session_state.get("authenticated", False):
    pass

level, level_xp, level_max, level_pct = get_level_progress(gs["xp"])


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def nav(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()

def show_notification(msg, type_="success"):
    if type_ == "success":
        st.success(msg)
    elif type_ == "error":
        st.error(msg)
    elif type_ == "info":
        st.info(msg)
    else:
        st.warning(msg)

def xp_bar(pct, label=""):
    st.markdown(f"""
    <div style="margin-bottom:4px;">
      <div class="xp-track">
        <div class="xp-fill" style="width:{min(pct,100):.1f}%;"></div>
      </div>
      {f'<div style="font-size:11px;color:var(--muted);margin-top:3px;">{label}</div>' if label else ''}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONBOARDING
# ══════════════════════════════════════════════════════════════════════════════
def page_onboard():
    st.markdown("""
    <div class="onboard-container">
      <div style="font-size:72px; margin-bottom:16px; animation: none;">🚀</div>
      <div style="font-family:'Orbitron',sans-serif; font-size:38px; font-weight:900;
                  background:linear-gradient(135deg,#38BDF8,#A78BFA,#FBBF24);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  margin-bottom:12px; letter-spacing:2px;">GALAXY CODER</div>
      <div style="font-size:17px; color:#94A3B8; margin-bottom:8px;">Zero to AI Hero</div>
      <div style="font-size:14px; color:#64748B; margin-bottom:40px;">
        Travel the galaxy. Complete missions. Learn Python, ML & AI.<br>
        From absolute zero to building AI agents — as a game.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    features = [
        ("🪐", "5 Planets", "Each planet = new skill level. Unlock as you grow."),
        ("🤖", "ARIA Mentor", "Your AI robot guide. Step-by-step. Always there."),
        ("⚔️", "Code Battles", "Challenge others. Tournaments. Leaderboard glory."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], features):
        with col:
            st.markdown(f"""
            <div class="planet-card unlocked" style="margin-bottom:24px;">
              <div style="font-size:36px; margin-bottom:10px;">{icon}</div>
              <div style="font-weight:700; font-size:15px; margin-bottom:6px;">{title}</div>
              <div style="font-size:12px; color:#64748B;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        avatars = ["🧑‍🚀", "👩‍🚀", "👨‍🚀", "🤖", "👾", "💫", "⭐", "🌟"]
        st.markdown("<div style='text-align:center; margin-bottom:12px; font-size:13px; color:#64748B;'>Choose your avatar:</div>", unsafe_allow_html=True)
        av_cols = st.columns(len(avatars))
        selected_av = st.session_state.get("picked_av", "🧑‍🚀")
        for i, (av, col) in enumerate(zip(avatars, av_cols)):
            with col:
                border = "2px solid #38BDF8" if av == selected_av else "2px solid transparent"
                if st.button(av, key=f"av_{i}"):
                    st.session_state.picked_av = av
                    st.rerun()

        uname = st.text_input("", placeholder="Enter your commander name...", key="ob_name")
        if st.button("🚀 LAUNCH MY MISSION", use_container_width=True, key="ob_launch"):
            if uname.strip():
                gs["username"] = uname.strip()
                gs["avatar"] = st.session_state.get("picked_av", "🧑‍🚀")
                save_user_progress(gs)
                nav("galaxy")
            else:
                st.warning("Commander needs a name!")


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        # If not logged in, show minimal sidebar
        if not gs.get("username"):
            st.markdown("""
            <div style="text-align:center; padding:30px 10px;">
              <div style="font-family:'Orbitron',sans-serif; font-size:18px; font-weight:900;
                          background:linear-gradient(135deg,#38BDF8,#A78BFA);
                          -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                🚀 GALAXY CODER
              </div>
              <div style="font-size:10px; color:#475569; letter-spacing:3px; margin-top:4px;">ZERO TO AI HERO</div>
              <div style="margin-top:24px; font-size:13px; color:#64748B; line-height:1.8;">
                🪐 5 Planets to explore<br>
                🤖 AI Mentor ARIA<br>
                ⚔️ Battle Arena<br>
                👥 Multiplayer battles<br>
                📜 Earn certificates<br>
                🏗️ Build real projects
              </div>
            </div>
            """, unsafe_allow_html=True)
            return
        st.markdown(f"""
        <div style="text-align:center; padding:18px 0 12px;">
          <div style="font-family:'Orbitron',sans-serif; font-size:22px; font-weight:900;
                      background:linear-gradient(135deg,#38BDF8,#A78BFA);
                      -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:3px;">
            🚀 GALAXY CODER
          </div>
          <div style="font-size:10px; color:#475569; letter-spacing:3px; margin-top:3px;">ZERO TO AI HERO</div>
        </div>
        """, unsafe_allow_html=True)

        # Commander HUD
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(56,189,248,0.08),rgba(167,139,250,0.08));
                    border:1px solid rgba(56,189,248,0.15); border-radius:12px; padding:14px; margin-bottom:14px;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <span style="font-size:28px;">{gs.get('avatar','🧑‍🚀')}</span>
            <div>
              <div style="font-weight:700; font-size:15px;">{gs.get('username','Commander')}</div>
              <div style="font-size:11px; color:#A78BFA;">Level {level} Commander</div>
            </div>
          </div>
          <div style="font-size:11px; color:#64748B; display:flex; justify-content:space-between; margin-bottom:5px;">
            <span>Level {level} → {level+1}</span><span>{level_xp}/{level_max} XP</span>
          </div>
          <div class="xp-track"><div class="xp-fill" style="width:{level_pct:.1f}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

        # Quick stats
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("⚡", f"{gs['xp']:,}", label_visibility="collapsed")
            st.caption("XP")
        with c2:
            st.metric("✅", len(gs["completed_missions"]), label_visibility="collapsed")
            st.caption("Done")
        with c3:
            st.metric("🔥", gs["streak"], label_visibility="collapsed")
            st.caption("Streak")

        st.divider()

        # Nav
        nav_items = [
            ("🪐", "Galaxy Map", "galaxy"),
            ("🎯", "Active Mission", "mission"),
            ("⚔️", "Solo Battle", "battle"),
            ("👥", "Multiplayer", "multiplayer"),
            ("🏗️", "Projects", "projects"),
            ("🤖", "ARIA Mentor", "aria"),
            ("🏆", "Achievements", "achievements"),
            ("📜", "Certificates", "certificates"),
            ("📊", "Leaderboard", "leaderboard"),
            ("⚙️", "Settings", "settings"),
        ]
        st.markdown("<div style='font-size:10px; color:#475569; letter-spacing:2px; margin-bottom:8px;'>NAVIGATION</div>", unsafe_allow_html=True)
        for icon, label, key in nav_items:
            is_active = st.session_state.page == key
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True, type=btn_type):
                nav(key)

        st.divider()

        # Total progress
        total = sum(len(p["missions"]) for p in GALAXY.values())
        done = len(gs["completed_missions"])
        pct = int(done / total * 100) if total else 0
        st.markdown(f"""
        <div style="font-size:11px; color:#475569; text-align:center;">
          Galaxy Progress: {pct}% ({done}/{total} missions)
        </div>
        """, unsafe_allow_html=True)
        xp_bar(pct)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: GALAXY MAP
# ══════════════════════════════════════════════════════════════════════════════
def page_galaxy():
    st.markdown("""
    <h1 style="text-align:center; margin-bottom:4px;">🪐 GALAXY MAP</h1>
    <p style="text-align:center; color:#64748B; margin-bottom:32px;">Your cosmic learning journey — unlock planets, complete missions, become the hero.</p>
    """, unsafe_allow_html=True)

    planets = list(GALAXY.items())
    rows = [planets[:3], planets[3:]]

    for row in rows:
        if not row:
            continue
        cols = st.columns(len(row))
        for col, (pid, pdata) in zip(cols, row):
            unlocked = gs["xp"] >= pdata["xp_required"]
            done_count = sum(1 for m in pdata["missions"] if m["id"] in gs["completed_missions"])
            total_m = len(pdata["missions"])
            pct = int(done_count / total_m * 100) if total_m else 0

            with col:
                lock_icon = "" if unlocked else "🔒"
                req_txt = f"Requires {pdata['xp_required']:,} XP" if not unlocked else f"{done_count}/{total_m} missions"
                color = pdata["color"]
                glow = pdata["glow"]

                st.markdown(f"""
                <div class="planet-card {'unlocked' if unlocked else 'locked'}"
                     style="border-color:{'rgba(56,189,248,0.2)' if unlocked else 'rgba(255,255,255,0.04)'};
                            {'box-shadow: 0 0 30px ' + color + '22;' if unlocked else ''}">
                  <div style="font-size:52px; margin-bottom:6px;">{pdata['icon']}</div>
                  <div style="font-family:'Orbitron',sans-serif; font-size:16px; font-weight:700;
                              color:{color if unlocked else '#475569'}; margin-bottom:4px;">{pdata['name']}</div>
                  <div style="font-size:11px; color:#475569; margin-bottom:12px;">{pdata['subtitle']}</div>
                  <div style="font-size:12px; color:#64748B; margin-bottom:12px; line-height:1.5;">{pdata['description'][:70]}...</div>
                  {'<div class="xp-track" style="margin-bottom:8px;"><div class="xp-fill" style="width:'+str(pct)+'%; background:linear-gradient(90deg,'+color+','+glow+');"></div></div>' if unlocked else ''}
                  <div style="font-size:12px; color:{color if unlocked else '#475569'}; font-weight:600;">
                    {'✅ ' if pct==100 else ''}{req_txt if unlocked else lock_icon + ' ' + req_txt}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if unlocked:
                    if st.button(f"{'✅ Review' if pct==100 else '▶ Explore'} {pdata['name']}", 
                                  key=f"planet_{pid}", use_container_width=True):
                        nav("planet", active_planet=pid)

        st.markdown("<br>", unsafe_allow_html=True)

    # Next mission suggestion
    st.divider()
    st.markdown("### 🎯 Continue Your Journey")
    for pid, pdata in GALAXY.items():
        if gs["xp"] < pdata["xp_required"]:
            continue
        for m in pdata["missions"]:
            if m["id"] not in gs["completed_missions"]:
                diff_stars = m["difficulty"]
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"""
                    <div class="mission-row" style="border-color:rgba(56,189,248,0.3);">
                      <span style="font-size:28px;">{pdata['icon']}</span>
                      <div>
                        <div style="font-size:11px; color:#475569; letter-spacing:1px;">{pdata['name'].upper()}</div>
                        <div style="font-weight:700; font-size:16px;">{m['title']}</div>
                        <div style="font-size:12px; color:#64748B; margin-top:2px;">
                          {diff_stars} · ⚡ {m['xp']} XP · {m['concept']}
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("▶ Launch", key=f"next_{m['id']}", use_container_width=True):
                        nav("mission", active_planet=pid, active_mission=m["id"], mission_step=0)
                return


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PLANET VIEW
# ══════════════════════════════════════════════════════════════════════════════
def page_planet():
    pid = st.session_state.get("active_planet", "mercury")
    if pid not in GALAXY:
        nav("galaxy")
        return

    pdata = GALAXY[pid]
    color = pdata["color"]

    c_back, c_title = st.columns([1, 5])
    with c_back:
        if st.button("← Galaxy", key="back_galaxy"):
            nav("galaxy")
    with c_title:
        st.markdown(f"<h2>{pdata['icon']} {pdata['name']} — {pdata['subtitle']}</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color:#64748B;'>{pdata['description']}</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("### 📋 Missions")
    for i, m in enumerate(pdata["missions"]):
        done = m["id"] in gs["completed_missions"]
        diff = m["difficulty"]
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f"""
            <div class="mission-row {'done' if done else ''}">
              <div style="font-size:22px; min-width:36px; text-align:center;">
                {'✅' if done else str(i+1)}
              </div>
              <div>
                <div style="font-weight:700; font-size:15px;">{m['title']}</div>
                <div style="font-size:12px; color:#64748B; margin-top:2px;">
                  {diff} · ⚡{m['xp']} XP · {m['concept']}
                  {'· 🏅 ' + m['reward']['badge'] if m['reward'].get('badge') else ''}
                </div>
              </div>
              {'<span style="margin-left:auto; font-size:18px;">🏆</span>' if done else ''}
            </div>
            """, unsafe_allow_html=True)
        with c2:
            label = "↩ Review" if done else "▶ Start"
            if st.button(label, key=f"m_btn_{m['id']}", use_container_width=True):
                nav("mission", active_planet=pid, active_mission=m["id"], mission_step=0)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MISSION (the core interactive experience)
# ══════════════════════════════════════════════════════════════════════════════
def page_mission():
    pid = st.session_state.get("active_planet")
    mid = st.session_state.get("active_mission")

    if not pid or not mid:
        nav("galaxy")
        return

    pdata = GALAXY[pid]
    mission = next((m for m in pdata["missions"] if m["id"] == mid), None)
    if not mission:
        nav("galaxy")
        return

    step_idx = st.session_state.mission_step
    steps = mission["steps"]
    total_steps = len(steps)
    already_done = mid in gs["completed_missions"]

    # Header
    cb, ct, cp = st.columns([1, 4, 1])
    with cb:
        if st.button("← Planet", key="back_planet"):
            nav("planet", active_planet=pid)
    with ct:
        st.markdown(f"""
        <div>
          <div style="font-size:11px; color:#475569; letter-spacing:1px;">{pdata['name'].upper()} · {mission['concept']}</div>
          <h2 style="margin:4px 0;">{mission['title']}</h2>
          <div style="font-size:13px; color:#64748B;">⚡ {mission['xp']} XP · {mission['difficulty']}</div>
        </div>
        """, unsafe_allow_html=True)
    with cp:
        if already_done:
            st.success("✅ Completed!")

    # Progress dots
    dots = ""
    for i in range(total_steps):
        if i < step_idx:
            dots += '<span style="color:#34D399; font-size:16px;">●</span> '
        elif i == step_idx:
            dots += '<span style="color:#38BDF8; font-size:20px;">●</span> '
        else:
            dots += '<span style="color:#1E3A5F; font-size:16px;">●</span> '
    st.markdown(f"<div style='text-align:center; margin:12px 0;'>{dots}</div>", unsafe_allow_html=True)

    progress_pct = ((step_idx) / total_steps) * 100
    xp_bar(progress_pct, f"Step {step_idx + 1} of {total_steps}")

    # ARIA story banner
    st.markdown(f"""
    <div style="background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.15);
                border-radius:10px; padding:14px 18px; margin-bottom:16px; display:flex; gap:12px; align-items:flex-start;">
      <span style="font-size:24px;">🤖</span>
      <div style="font-size:14px; color:#94A3B8; font-style:italic; line-height:1.5;">{mission['story']}</div>
    </div>
    """, unsafe_allow_html=True)

    if step_idx >= total_steps:
        # Mission complete!
        st.markdown(f"""
        <div style="text-align:center; padding:40px; background:linear-gradient(135deg,rgba(52,211,153,0.1),rgba(56,189,248,0.1));
                    border:2px solid rgba(52,211,153,0.4); border-radius:20px;">
          <div style="font-size:64px; margin-bottom:12px;">🎉</div>
          <div style="font-family:'Orbitron',sans-serif; font-size:28px; font-weight:900; color:#34D399;">MISSION COMPLETE!</div>
          <div style="font-size:16px; color:#94A3B8; margin-top:8px;">{mission['title']} — {mission['xp']} XP earned</div>
        </div>
        """, unsafe_allow_html=True)

        if not already_done:
            updated_gs, leveled_up, new_level = add_xp(gs, mission["xp"], mid)
            badge = mission["reward"].get("badge")
            updated_gs, new_badges = award_badge(updated_gs, badge)
            updated_gs, new_certs = check_certificates(updated_gs)
            save_state(updated_gs)

            if leveled_up:
                st.balloons()
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,rgba(251,191,36,0.15),rgba(56,189,248,0.15));
                            border:2px solid #FBBF24; border-radius:16px; padding:20px; margin-top:16px;">
                  <div style="font-size:40px;">⬆️</div>
                  <div style="font-family:'Orbitron',sans-serif; font-size:24px; color:#FBBF24;">LEVEL UP!</div>
                  <div style="color:#94A3B8;">You reached Level {new_level}!</div>
                </div>
                """, unsafe_allow_html=True)
            for b in new_badges:
                st.success(f"🏅 Badge Unlocked: **{b}**")
            for c in new_certs:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(251,191,36,0.08); border:2px solid #FBBF24;
                            border-radius:12px; padding:16px; margin-top:8px;">
                  📜 Certificate Earned: <strong>{c['title']}</strong>
                </div>
                """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔄 Replay Mission", use_container_width=True, key="replay"):
                st.session_state.mission_step = 0
                st.session_state.quiz_answered = {}
                st.session_state.code_output = {}
                st.rerun()
        with c2:
            if st.button("← Back to Planet", use_container_width=True, key="back_p2"):
                nav("planet", active_planet=pid)
        with c3:
            if st.button("🪐 Galaxy Map", use_container_width=True, key="go_galaxy2"):
                nav("galaxy")
        return

    # Current step
    step = steps[step_idx]
    step_type = step["type"]

    # ── STORY step ──
    if step_type == "story":
        st.markdown(f"""
        <div class="step-card active">
          <div style="display:flex; gap:10px; align-items:flex-start; margin-bottom:12px;">
            <span style="font-size:20px;">📖</span>
            <span style="font-size:13px; color:#475569; letter-spacing:1px; text-transform:uppercase; font-weight:700;">Theory</span>
          </div>
          <div style="color:#E2E8F0; line-height:1.7;">{step['content']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✅ Got it! Next →", key=f"next_story_{step_idx}", use_container_width=True):
            st.session_state.mission_step += 1
            st.rerun()

    # ── VISUAL step ──
    elif step_type == "visual":
        visual_type = step.get("content", "")
        caption = step.get("caption", "")
        render_visual(visual_type, caption)

        if st.button("👁 Understood! Next →", key=f"next_vis_{step_idx}", use_container_width=True):
            st.session_state.mission_step += 1
            st.rerun()

    # ── QUIZ step ──
    elif step_type == "quiz":
        q = step["question"]
        options = step["options"]
        correct = step["answer"]
        explanation = step.get("explanation", "")
        q_key = f"quiz_{mid}_{step_idx}"
        answered = st.session_state.quiz_answered.get(q_key)

        st.markdown(f"""
        <div class="step-card active">
          <div style="display:flex; gap:10px; align-items:flex-start; margin-bottom:16px;">
            <span style="font-size:20px;">🧩</span>
            <span style="font-size:13px; color:#475569; letter-spacing:1px; text-transform:uppercase; font-weight:700;">Quiz Challenge</span>
          </div>
          <div style="font-size:17px; font-weight:600; margin-bottom:20px; line-height:1.5;">{q}</div>
        </div>
        """, unsafe_allow_html=True)

        for i, opt in enumerate(options):
            if answered is not None:
                cls = "correct" if i == correct else ("wrong" if i == answered else "quiz-option")
                icon = "✅ " if i == correct else ("❌ " if i == answered else "")
                st.markdown(f'<div class="quiz-option {cls}">{icon}{opt}</div>', unsafe_allow_html=True)
            else:
                if st.button(f"  {opt}", key=f"quiz_opt_{step_idx}_{i}", use_container_width=True):
                    st.session_state.quiz_answered[q_key] = i
                    st.rerun()

        if answered is not None:
            if answered == correct:
                st.success(f"✅ Correct! {explanation}")
            else:
                st.error(f"❌ Not quite. {explanation}")

            if st.button("Next →", key=f"next_quiz_{step_idx}", use_container_width=True):
                st.session_state.mission_step += 1
                st.rerun()

    # ── CODE step ──
    elif step_type == "code":
        instruction = step["instruction"]
        starter = step.get("starter", "# Write your solution here\n")
        solution = step.get("solution", "")
        hints = step.get("hints", [])
        check_contains = step.get("check", [])

        st.markdown(f"""
        <div class="step-card active">
          <div style="display:flex; gap:10px; align-items:flex-start; margin-bottom:12px;">
            <span style="font-size:20px;">💻</span>
            <span style="font-size:13px; color:#475569; letter-spacing:1px; text-transform:uppercase; font-weight:700;">Coding Challenge</span>
          </div>
          <div style="font-size:15px; line-height:1.6; color:#CBD5E1;">{instruction}</div>
        </div>
        """, unsafe_allow_html=True)

        code_key = f"code_{mid}_{step_idx}"
        if code_key not in st.session_state:
            st.session_state[code_key] = starter

        c_left, c_right = st.columns([3, 2])
        with c_left:
            user_code = st.text_area(
                "Code:", value=st.session_state[code_key],
                height=280, key=f"editor_{mid}_{step_idx}",
                label_visibility="collapsed"
            )
            st.session_state[code_key] = user_code

            c1, c2, c3 = st.columns(3)
            with c1:
                run_btn = st.button("▶ Run", key=f"run_{mid}_{step_idx}", use_container_width=True)
            with c2:
                submit_btn = st.button("✅ Submit", key=f"sub_{mid}_{step_idx}", use_container_width=True)
            with c3:
                aria_btn = st.button("🤖 Ask ARIA", key=f"aria_{mid}_{step_idx}", use_container_width=True)

            if run_btn:
                from utils.runner import run_code
                out, err, t = run_code(user_code)
                st.session_state.code_output[code_key] = (out, err, t, False)
                st.rerun()

            if submit_btn:
                from utils.runner import check_output
                passed, out, err, t = check_output(user_code, check_contains)
                st.session_state.code_output[code_key] = (out, err, t, True)
                if passed:
                    st.session_state[f"passed_{mid}_{step_idx}"] = True
                st.rerun()

            if aria_btn:
                from utils.aria import aria_review_code
                with st.spinner("🤖 ARIA analyzing..."):
                    review = aria_review_code(user_code, mission["title"], instruction)
                st.session_state[f"aria_review_{mid}_{step_idx}"] = review
                st.rerun()

        with c_right:
            # Output panel
            out_data = st.session_state.code_output.get(code_key)
            if out_data:
                out, err, t, was_submit = out_data
                st.markdown("**📤 Output:**")
                if out:
                    st.code(out.strip() or "(no output)", language=None)
                if err:
                    st.markdown(f'<div style="background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.3); border-radius:6px; padding:10px; font-family:monospace; font-size:12px; color:#F87171;">{err}</div>', unsafe_allow_html=True)
                    # ARIA error help
                    if "Error" in err:
                        from utils.aria import aria_explain_error
                        hint = aria_explain_error(err, user_code)
                        st.info(f"🤖 ARIA: {hint}")
                if t:
                    st.caption(f"⏱ {t}s")

                if was_submit:
                    passed_flag = not (err and "Error" in err)
                    if check_contains:
                        passed_flag = all(c.lower() in (out+err).lower() for c in check_contains)
                    if passed_flag:
                        st.success("🎯 Challenge Passed!")
                    else:
                        st.error("Not quite — check the requirements!")
            else:
                st.markdown("""
                <div style="background:rgba(2,8,23,0.5); border:1px solid rgba(56,189,248,0.1);
                            border-radius:8px; padding:24px; text-align:center; color:#475569; min-height:120px;
                            display:flex; align-items:center; justify-content:center;">
                  <div>💻<br>Output appears here</div>
                </div>
                """, unsafe_allow_html=True)

            # ARIA review
            aria_rev = st.session_state.get(f"aria_review_{mid}_{step_idx}")
            if aria_rev:
                st.markdown("**🤖 ARIA Review:**")
                st.markdown(aria_rev)

            # Hints
            if hints:
                with st.expander("💡 Hints"):
                    for i, h in enumerate(hints, 1):
                        st.markdown(f"**Hint {i}:** {h}")

            # Solution
            with st.expander("👁 View Solution"):
                st.warning("Try first! Understanding > Copying")
                st.code(solution, language="python")

        # Next button
        passed_this = st.session_state.get(f"passed_{mid}_{step_idx}", False)
        if passed_this or already_done:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Complete Mission Step →", key=f"next_code_{step_idx}", use_container_width=True):
                st.session_state.mission_step += 1
                st.rerun()
        else:
            st.info("💡 Submit correct code to advance to the next step!")


def render_visual(visual_type, caption):
    """Render interactive visual diagrams"""
    visuals = {
        "print_visual": """
<div style="background:#020817; border:1px solid rgba(56,189,248,0.2); border-radius:12px; padding:20px; font-family:'Share Tech Mono',monospace; margin-bottom:12px;">
  <div style="color:#38BDF8; margin-bottom:12px;">print("Hello, Earth!")</div>
  <div style="display:flex; align-items:center; gap:12px; margin:12px 0;">
    <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); padding:10px 16px; border-radius:8px; color:#38BDF8;">📝 print()</div>
    <div style="font-size:24px; color:#A78BFA;">→</div>
    <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:10px 16px; border-radius:8px; color:#34D399;">📺 Screen Output</div>
    <div style="font-size:24px; color:#A78BFA;">→</div>
    <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3); padding:10px 16px; border-radius:8px; color:#FBBF24;">Hello, Earth!</div>
  </div>
  <div style="color:#64748B; font-size:12px;">print() function sends text to the output console</div>
</div>""",
        "variables_visual": """
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:10px; margin-bottom:12px;">
  <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); border-radius:10px; padding:14px; text-align:center;">
    <div style="font-size:24px; margin-bottom:6px;">📦</div>
    <div style="color:#38BDF8; font-size:12px; font-weight:700;">str</div>
    <div style="font-family:monospace; font-size:13px; margin-top:4px; color:#E2E8F0;">name = "Alex"</div>
  </div>
  <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); border-radius:10px; padding:14px; text-align:center;">
    <div style="font-size:24px; margin-bottom:6px;">🔢</div>
    <div style="color:#34D399; font-size:12px; font-weight:700;">int</div>
    <div style="font-family:monospace; font-size:13px; margin-top:4px; color:#E2E8F0;">age = 25</div>
  </div>
  <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3); border-radius:10px; padding:14px; text-align:center;">
    <div style="font-size:24px; margin-bottom:6px;">🌡️</div>
    <div style="color:#FBBF24; font-size:12px; font-weight:700;">float</div>
    <div style="font-family:monospace; font-size:13px; margin-top:4px; color:#E2E8F0;">temp = 9.8</div>
  </div>
  <div style="background:rgba(167,139,250,0.1); border:1px solid rgba(167,139,250,0.3); border-radius:10px; padding:14px; text-align:center;">
    <div style="font-size:24px; margin-bottom:6px;">💡</div>
    <div style="color:#A78BFA; font-size:12px; font-weight:700;">bool</div>
    <div style="font-family:monospace; font-size:13px; margin-top:4px; color:#E2E8F0;">on = True</div>
  </div>
</div>""",
        "condition_visual": """
<div style="background:#020817; border:1px solid rgba(56,189,248,0.15); border-radius:12px; padding:20px; font-family:'Share Tech Mono',monospace; margin-bottom:12px;">
  <div style="text-align:center; margin-bottom:16px;">
    <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); display:inline-block; padding:10px 20px; border-radius:8px; color:#38BDF8;">❓ Condition Check</div>
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
    <div style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.3); border-radius:8px; padding:14px; text-align:center;">
      <div style="color:#34D399; font-size:18px; margin-bottom:6px;">✅ True</div>
      <div style="color:#94A3B8; font-size:12px;">Execute if block</div>
    </div>
    <div style="background:rgba(248,113,113,0.08); border:1px solid rgba(248,113,113,0.3); border-radius:8px; padding:14px; text-align:center;">
      <div style="color:#F87171; font-size:18px; margin-bottom:6px;">❌ False</div>
      <div style="color:#94A3B8; font-size:12px;">Skip to else</div>
    </div>
  </div>
</div>""",
        "loop_visual": """
<div style="background:#020817; border:1px solid rgba(167,139,250,0.2); border-radius:12px; padding:20px; font-family:'Share Tech Mono',monospace; margin-bottom:12px;">
  <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; justify-content:center;">
    <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); padding:10px; border-radius:8px; color:#38BDF8; text-align:center; min-width:80px;">▶ Start<br><small>i=0</small></div>
    <span style="color:#A78BFA; font-size:20px;">→</span>
    <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3); padding:10px; border-radius:8px; color:#FBBF24; text-align:center; min-width:80px;">❓ Check<br><small>i &lt; 5?</small></div>
    <span style="color:#34D399; font-size:20px;">→</span>
    <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:10px; border-radius:8px; color:#34D399; text-align:center; min-width:80px;">⚙️ Execute<br><small>print(i)</small></div>
    <span style="color:#A78BFA; font-size:20px;">→</span>
    <div style="background:rgba(167,139,250,0.1); border:1px solid rgba(167,139,250,0.3); padding:10px; border-radius:8px; color:#A78BFA; text-align:center; min-width:80px;">🔁 Update<br><small>i += 1</small></div>
    <span style="color:#F87171; font-size:16px;">↩ loop back</span>
  </div>
</div>""",
        "collections_visual": """
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:12px;">
  <div style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25); border-radius:10px; padding:14px;">
    <div style="color:#38BDF8; font-weight:700; margin-bottom:8px;">📋 List</div>
    <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:2;">
      [0] "Alex"<br>[1] "Zara"<br>[2] "Omar"<br><span style="color:#34D399;">✅ Changeable</span>
    </div>
  </div>
  <div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.25); border-radius:10px; padding:14px;">
    <div style="color:#FBBF24; font-weight:700; margin-bottom:8px;">🗂️ Dict</div>
    <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:2;">
      "name":"Alex"<br>"age": 25<br>"xp": 1500<br><span style="color:#34D399;">✅ Key:Value</span>
    </div>
  </div>
  <div style="background:rgba(167,139,250,0.08); border:1px solid rgba(167,139,250,0.25); border-radius:10px; padding:14px;">
    <div style="color:#A78BFA; font-weight:700; margin-bottom:8px;">🔒 Tuple</div>
    <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:2;">
      (0) 40.7128<br>(1) -74.0060<br>(2) "NYC"<br><span style="color:#F87171;">🔒 Immutable</span>
    </div>
  </div>
</div>""",
        "function_visual": """
<div style="background:#020817; border:1px solid rgba(52,211,153,0.2); border-radius:12px; padding:20px; font-family:'Share Tech Mono',monospace; margin-bottom:12px;">
  <div style="display:flex; align-items:center; gap:10px; justify-content:center; flex-wrap:wrap;">
    <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); padding:12px 16px; border-radius:8px; text-align:center;">
      <div style="color:#38BDF8; font-size:11px; font-weight:700;">INPUT</div>
      <div style="color:#E2E8F0; font-size:13px; margin-top:4px;">distance=1000<br>time=5</div>
    </div>
    <span style="color:#A78BFA; font-size:24px;">→</span>
    <div style="background:rgba(167,139,250,0.1); border:2px solid rgba(167,139,250,0.4); padding:12px 20px; border-radius:8px; text-align:center;">
      <div style="color:#A78BFA; font-size:11px; font-weight:700;">FUNCTION</div>
      <div style="color:#E2E8F0; font-size:12px; margin-top:4px;">def warp_speed()<br>speed = dist/time</div>
    </div>
    <span style="color:#A78BFA; font-size:24px;">→</span>
    <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:12px 16px; border-radius:8px; text-align:center;">
      <div style="color:#34D399; font-size:11px; font-weight:700;">OUTPUT</div>
      <div style="color:#E2E8F0; font-size:13px; margin-top:4px;">return 200<br>ly/hr</div>
    </div>
  </div>
</div>""",
        "class_visual": """
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:12px;">
  <div style="background:rgba(56,189,248,0.08); border:2px dashed rgba(56,189,248,0.3); border-radius:12px; padding:16px;">
    <div style="color:#38BDF8; font-weight:700; margin-bottom:8px;">🏗️ CLASS (Blueprint)</div>
    <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:1.8;">
      class Spaceship:<br>
      &nbsp;&nbsp;name = ?<br>
      &nbsp;&nbsp;fuel = ?<br>
      &nbsp;&nbsp;def fly(): ...<br>
    </div>
  </div>
  <div style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.3); border-radius:12px; padding:16px;">
    <div style="color:#34D399; font-weight:700; margin-bottom:8px;">🚀 OBJECTS (Ships)</div>
    <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:1.8;">
      eagle = Spaceship("Eagle", 100)<br>
      falcon = Spaceship("Falcon", 85)<br>
      eagle.fly() → "Eagle flying!"<br>
    </div>
  </div>
</div>""",
        "numpy_visual": """
<div style="background:#020817; border:1px solid rgba(56,189,248,0.15); border-radius:12px; padding:20px; margin-bottom:12px;">
  <div style="text-align:center; margin-bottom:14px; color:#64748B; font-size:12px;">Python List vs NumPy Array</div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
    <div style="background:rgba(248,113,113,0.08); border:1px solid rgba(248,113,113,0.25); border-radius:8px; padding:12px;">
      <div style="color:#F87171; font-weight:700; margin-bottom:6px; font-size:12px;">❌ Python List (slow)</div>
      <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:1.8;">
        nums = [1,2,3,4,5]<br>result = []<br>for n in nums:<br>&nbsp;&nbsp;result.append(n*2)<br><span style="color:#F87171;">→ loop required</span>
      </div>
    </div>
    <div style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.3); border-radius:8px; padding:12px;">
      <div style="color:#34D399; font-weight:700; margin-bottom:6px; font-size:12px;">✅ NumPy Array (fast)</div>
      <div style="font-family:monospace; font-size:11px; color:#94A3B8; line-height:1.8;">
        arr = np.array([1,2,3,4,5])<br>result = arr * 2<br>&nbsp;<br><span style="color:#34D399;">→ instant! no loop!</span>
      </div>
    </div>
  </div>
</div>""",
        "ml_visual": """
<div style="background:#020817; border:1px solid rgba(167,139,250,0.2); border-radius:12px; padding:20px; margin-bottom:12px;">
  <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; flex-wrap:wrap;">
    <div style="text-align:center; min-width:80px;"><div style="font-size:20px;">📊</div><div style="font-size:10px; color:#38BDF8; font-weight:700; margin-top:4px;">DATA</div></div>
    <div style="color:#A78BFA; font-size:18px;">→</div>
    <div style="text-align:center; min-width:80px;"><div style="font-size:20px;">✂️</div><div style="font-size:10px; color:#38BDF8; font-weight:700; margin-top:4px;">SPLIT</div><div style="font-size:9px; color:#64748B;">train/test</div></div>
    <div style="color:#A78BFA; font-size:18px;">→</div>
    <div style="text-align:center; min-width:80px;"><div style="font-size:20px;">⚖️</div><div style="font-size:10px; color:#38BDF8; font-weight:700; margin-top:4px;">SCALE</div></div>
    <div style="color:#A78BFA; font-size:18px;">→</div>
    <div style="text-align:center; min-width:80px;"><div style="font-size:20px;">🎓</div><div style="font-size:10px; color:#38BDF8; font-weight:700; margin-top:4px;">TRAIN</div></div>
    <div style="color:#A78BFA; font-size:18px;">→</div>
    <div style="text-align:center; min-width:80px;"><div style="font-size:20px;">📈</div><div style="font-size:10px; color:#34D399; font-weight:700; margin-top:4px;">EVALUATE</div></div>
  </div>
</div>""",
        "langchain_visual": """
<div style="background:#020817; border:1px solid rgba(251,191,36,0.2); border-radius:12px; padding:20px; margin-bottom:12px;">
  <div style="display:flex; align-items:center; gap:10px; justify-content:center; flex-wrap:wrap;">
    <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); padding:10px 14px; border-radius:8px; text-align:center;">
      <div style="color:#38BDF8; font-size:11px; font-weight:700;">PROMPT</div>
      <div style="font-size:10px; color:#64748B; margin-top:2px;">Template</div>
    </div>
    <span style="color:#FBBF24; font-size:20px; font-weight:900;">|</span>
    <div style="background:rgba(167,139,250,0.1); border:1px solid rgba(167,139,250,0.3); padding:10px 14px; border-radius:8px; text-align:center;">
      <div style="color:#A78BFA; font-size:11px; font-weight:700;">LLM</div>
      <div style="font-size:10px; color:#64748B; margin-top:2px;">Claude / GPT</div>
    </div>
    <span style="color:#FBBF24; font-size:20px; font-weight:900;">|</span>
    <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:10px 14px; border-radius:8px; text-align:center;">
      <div style="color:#34D399; font-size:11px; font-weight:700;">PARSER</div>
      <div style="font-size:10px; color:#64748B; margin-top:2px;">StrOutput</div>
    </div>
    <span style="color:#38BDF8; font-size:20px;">→</span>
    <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3); padding:10px 14px; border-radius:8px; text-align:center;">
      <div style="color:#FBBF24; font-size:11px; font-weight:700;">OUTPUT</div>
      <div style="font-size:10px; color:#64748B; margin-top:2px;">AI Response</div>
    </div>
  </div>
  <div style="text-align:center; color:#64748B; font-size:11px; margin-top:10px;">The | pipe operator connects chain steps</div>
</div>""",
        "langgraph_visual": """
<div style="background:#020817; border:1px solid rgba(251,191,36,0.2); border-radius:12px; padding:20px; margin-bottom:12px;">
  <div style="display:flex; align-items:center; gap:8px; justify-content:center; flex-wrap:wrap;">
    <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); padding:12px 16px; border-radius:8px; text-align:center;">
      <div style="font-size:18px;">🔍</div>
      <div style="color:#38BDF8; font-size:11px; font-weight:700; margin-top:4px;">PLANNER</div>
    </div>
    <div style="color:#A78BFA; font-size:20px;">→</div>
    <div style="background:rgba(167,139,250,0.1); border:1px solid rgba(167,139,250,0.3); padding:12px 16px; border-radius:8px; text-align:center;">
      <div style="font-size:18px;">⚙️</div>
      <div style="color:#A78BFA; font-size:11px; font-weight:700; margin-top:4px;">EXECUTOR</div>
    </div>
    <div style="color:#A78BFA; font-size:20px;">→</div>
    <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:12px 16px; border-radius:8px; text-align:center;">
      <div style="font-size:18px;">✅</div>
      <div style="color:#34D399; font-size:11px; font-weight:700; margin-top:4px;">REVIEWER</div>
    </div>
    <div style="color:#A78BFA; font-size:20px;">→</div>
    <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3); padding:12px 16px; border-radius:8px; text-align:center;">
      <div style="font-size:18px;">🏁</div>
      <div style="color:#FBBF24; font-size:11px; font-weight:700; margin-top:4px;">END</div>
    </div>
  </div>
  <div style="text-align:center; color:#64748B; font-size:11px; margin-top:10px;">Stateful workflow — each node processes and passes state forward</div>
</div>""",
        "inheritance_visual": """
<div style="background:#020817; border:1px solid rgba(248,113,113,0.2); border-radius:12px; padding:20px; margin-bottom:12px; text-align:center; font-family:'Share Tech Mono',monospace; font-size:12px;">
  <div style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); display:inline-block; padding:10px 20px; border-radius:8px; color:#38BDF8; margin-bottom:8px;">🚗 Vehicle<br><small style="color:#64748B;">name, speed, move()</small></div>
  <div style="color:#64748B; margin:4px 0;">inherits ↓</div>
  <div style="display:flex; gap:20px; justify-content:center;">
    <div style="background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:10px 16px; border-radius:8px; color:#34D399;">🚀 Spaceship<br><small style="color:#64748B;">+warp, move()</small></div>
    <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3); padding:10px 16px; border-radius:8px; color:#FBBF24;">✈️ Fighter<br><small style="color:#64748B;">+weapons, fire()</small></div>
  </div>
</div>""",
        "pandas_visual": """
<div style="background:#020817; border:1px solid rgba(52,211,153,0.2); border-radius:12px; padding:16px; margin-bottom:12px; overflow-x:auto;">
  <div style="color:#34D399; font-size:11px; font-weight:700; margin-bottom:8px;">📊 DataFrame — Programmable Spreadsheet</div>
  <table style="width:100%; border-collapse:collapse; font-family:monospace; font-size:11px;">
    <tr style="background:rgba(56,189,248,0.1);">
      <th style="padding:6px 10px; color:#38BDF8; border:1px solid rgba(56,189,248,0.2);">name</th>
      <th style="padding:6px 10px; color:#38BDF8; border:1px solid rgba(56,189,248,0.2);">size</th>
      <th style="padding:6px 10px; color:#38BDF8; border:1px solid rgba(56,189,248,0.2);">temp</th>
      <th style="padding:6px 10px; color:#38BDF8; border:1px solid rgba(56,189,248,0.2);">moons</th>
    </tr>
    <tr><td style="padding:5px 10px; color:#E2E8F0; border:1px solid rgba(255,255,255,0.06);">Earth</td><td style="padding:5px 10px; color:#94A3B8; border:1px solid rgba(255,255,255,0.06);">12742</td><td style="padding:5px 10px; color:#34D399; border:1px solid rgba(255,255,255,0.06);">15</td><td style="padding:5px 10px; color:#94A3B8; border:1px solid rgba(255,255,255,0.06);">1</td></tr>
    <tr style="background:rgba(255,255,255,0.02);"><td style="padding:5px 10px; color:#E2E8F0; border:1px solid rgba(255,255,255,0.06);">Mars</td><td style="padding:5px 10px; color:#94A3B8; border:1px solid rgba(255,255,255,0.06);">6779</td><td style="padding:5px 10px; color:#F87171; border:1px solid rgba(255,255,255,0.06);">-60</td><td style="padding:5px 10px; color:#94A3B8; border:1px solid rgba(255,255,255,0.06);">2</td></tr>
    <tr><td style="padding:5px 10px; color:#E2E8F0; border:1px solid rgba(255,255,255,0.06);">Jupiter</td><td style="padding:5px 10px; color:#94A3B8; border:1px solid rgba(255,255,255,0.06);">139820</td><td style="padding:5px 10px; color:#F87171; border:1px solid rgba(255,255,255,0.06);">-145</td><td style="padding:5px 10px; color:#94A3B8; border:1px solid rgba(255,255,255,0.06);">95</td></tr>
  </table>
</div>""",
    }
    html = visuals.get(visual_type, f'<div style="padding:20px; text-align:center; color:#64748B;">Visual: {visual_type}</div>')
    st.markdown(f"""
    <div class="step-card active">
      <div style="display:flex; gap:10px; align-items:center; margin-bottom:12px;">
        <span style="font-size:20px;">👁</span>
        <span style="font-size:13px; color:#475569; letter-spacing:1px; text-transform:uppercase; font-weight:700;">Visual Concept</span>
      </div>
      {html}
      <div style="text-align:center; font-size:12px; color:#64748B; font-style:italic;">{caption}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BATTLE ARENA
# ══════════════════════════════════════════════════════════════════════════════
def page_battle():
    st.markdown("""
    <h1 style="text-align:center;">⚔️ BATTLE ARENA</h1>
    <p style="text-align:center; color:#64748B; margin-bottom:24px;">Test your skills. Compete. Climb the ranks.</p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("⚔️ Battles Won", gs.get("battles_won", 0))
    with c2: st.metric("🏆 Win Rate", f"{int(gs.get('battles_won',0)/max(gs.get('battles_played',1),1)*100)}%")
    with c3: st.metric("🔥 Win Streak", gs.get("win_streak", 0))

    st.divider()

    if not st.session_state.battle_active:
        # Battle lobby
        st.markdown("### ⚔️ Choose Your Battle")
        diff_info = {
            "beginner": ("☿ Cadet", "#A8A8A8", "Python basics, syntax, data types"),
            "intermediate": ("🌍 Officer", "#4ECDC4", "OOP, comprehensions, advanced functions"),
            "advanced": ("♃ Commander", "#F59E0B", "ML concepts, algorithms, decorators"),
        }
        cols = st.columns(3)
        for (diff, (rank, color, desc)), col in zip(diff_info.items(), cols):
            with col:
                st.markdown(f"""
                <div class="planet-card unlocked" style="border-color:rgba(56,189,248,0.15); margin-bottom:12px;">
                  <div style="font-size:32px; margin-bottom:8px;">{rank.split()[0]}</div>
                  <div style="font-weight:700; color:{color}; margin-bottom:4px;">{rank}</div>
                  <div style="font-size:11px; color:#64748B;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"⚔️ {diff.title()} Battle", key=f"start_battle_{diff}", use_container_width=True):
                    from utils.aria import aria_generate_battle_questions
                    with st.spinner(f"🤖 ARIA generating fresh {diff} questions..."):
                        ai_qs = aria_generate_battle_questions(
                            diff, diff, gs["completed_missions"], count=8
                        )
                    if ai_qs and len(ai_qs) >= 4:
                        pool = ai_qs
                        st.toast("🤖 ARIA generated fresh questions — never seen before!", icon="🚀")
                    else:
                        pool = BATTLE_QUESTIONS.get(diff, []).copy()
                        import random as _r
                        _r.shuffle(pool)
                        pool = pool[:8]
                        st.toast("⚡ Using backup questions (AI offline)", icon="⚠️")
                    st.session_state.battle_pool = pool
                    st.session_state.battle_q_idx = 0
                    st.session_state.battle_score = 0
                    st.session_state.battle_active = True
                    st.session_state.battle_difficulty = diff
                    st.session_state.battle_answered = None
                    st.rerun()

        # Practice mode
        st.divider()
        st.markdown("### 🎯 Quick Practice — AI Random Question")
        st.caption("🤖 Every question is freshly generated by ARIA — never repeats!")

        if "practice_q" not in st.session_state:
            st.session_state.practice_q = random.choice([q for qs in BATTLE_QUESTIONS.values() for q in qs])
            st.session_state.practice_ans = None
            st.session_state.practice_ai = False

        if st.button("🤖 Generate AI Question", key="gen_prac_ai", use_container_width=False):
            from utils.aria import aria_generate_battle_questions
            with st.spinner("ARIA generating..."):
                ai_qs = aria_generate_battle_questions("beginner", "beginner", gs["completed_missions"], count=1)
            if ai_qs:
                st.session_state.practice_q = ai_qs[0]
                st.session_state.practice_ans = None
                st.session_state.practice_ai = True
                st.rerun()

        pq = st.session_state.practice_q
        st.markdown(f"**{pq['q']}**")
        for i, opt in enumerate(pq["options"]):
            ans = st.session_state.practice_ans
            if ans is not None:
                cls = "correct" if i == pq["answer"] else ("wrong" if i == ans else "")
                icon = "✅ " if i == pq["answer"] else ("❌ " if i == ans else "")
                st.markdown(f'<div class="quiz-option {cls}">{icon}{opt}</div>', unsafe_allow_html=True)
            else:
                if st.button(opt, key=f"prac_{i}", use_container_width=True):
                    st.session_state.practice_ans = i
                    st.rerun()

        if st.session_state.practice_ans is not None:
            c_np1, c_np2 = st.columns(2)
            with c_np1:
                if st.button("🔄 Random Question", use_container_width=True, key="new_prac"):
                    all_qs = [q for qs in BATTLE_QUESTIONS.values() for q in qs]
                    st.session_state.practice_q = random.choice(all_qs)
                    st.session_state.practice_ans = None
                    st.session_state.practice_ai = False
                    st.rerun()
            with c_np2:
                if st.button("🤖 AI Question", use_container_width=True, key="ai_prac_next"):
                    from utils.aria import aria_generate_battle_questions
                    with st.spinner("ARIA generating..."):
                        ai_qs = aria_generate_battle_questions("beginner", "beginner", gs["completed_missions"], count=1)
                    if ai_qs:
                        st.session_state.practice_q = ai_qs[0]
                        st.session_state.practice_ans = None
                        st.session_state.practice_ai = True
                        st.rerun()
    else:
        # Active battle
        pool = st.session_state.get("battle_pool", [])
        idx = st.session_state.battle_q_idx
        score = st.session_state.battle_score
        total = len(pool)

        if idx >= total:
            # Battle finished
            pct = int(score / total * 100)
            won = score >= total * 0.6

            if won:
                st.success(f"🏆 VICTORY! Score: {score}/{total} ({pct}%)")
                st.balloons()
                gs["battles_won"] = gs.get("battles_won", 0) + 1
                gs["win_streak"] = gs.get("win_streak", 0) + 1
                xp_gain = score * 20
                updated, _, _ = add_xp(gs, xp_gain)
                updated, new_badges = award_badge(updated, None)
                save_state(updated)
                st.markdown(f"⚡ +{xp_gain} XP earned!")
                for b in new_badges:
                    st.success(f"🏅 {b}")
            else:
                st.error(f"❌ Defeated. Score: {score}/{total} ({pct}%). Train harder, Commander!")
                gs["win_streak"] = 0
                gs["battles_played"] = gs.get("battles_played", 0) + 1
                save_user_progress(gs)

            if st.button("🔄 Battle Again", use_container_width=True, key="battle_again"):
                st.session_state.battle_active = False
                st.rerun()
            return

        q = pool[idx]
        # Header
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; 
                    background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:12px 20px; margin-bottom:20px;">
          <div style="color:#64748B; font-size:13px;">Question {idx+1}/{total}</div>
          <div style="font-weight:700; color:#FBBF24;">Score: {score}/{idx}</div>
          <div style="color:#64748B; font-size:12px; background:rgba(56,189,248,0.1); padding:4px 10px; border-radius:20px;">
            {q.get('topic','').upper()}
          </div>
        </div>
        """, unsafe_allow_html=True)

        xp_bar((idx / total) * 100)
        st.markdown(f"### {q['q']}")
        st.markdown("<br>", unsafe_allow_html=True)

        answered = st.session_state.battle_answered
        for i, opt in enumerate(q["options"]):
            if answered is not None:
                cls = "correct" if i == q["answer"] else ("wrong" if i == answered else "")
                icon = "✅ " if i == q["answer"] else ("❌ " if i == answered else "   ")
                st.markdown(f'<div class="quiz-option {cls}">{icon} {opt}</div>', unsafe_allow_html=True)
            else:
                if st.button(f"  {opt}", key=f"battle_opt_{i}", use_container_width=True):
                    st.session_state.battle_answered = i
                    if i == q["answer"]:
                        st.session_state.battle_score += 1
                    st.rerun()

        if answered is not None:
            if answered == q["answer"]:
                st.success("⚡ Correct!")
            else:
                st.error(f"❌ Wrong. Answer: **{q['options'][q['answer']]}**")

            if st.button("Next Question →", use_container_width=True, key="battle_next"):
                st.session_state.battle_q_idx += 1
                st.session_state.battle_answered = None
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ARIA MENTOR
# ══════════════════════════════════════════════════════════════════════════════
def page_aria():
    st.markdown("""
    <h1>🤖 ARIA — Your AI Mentor</h1>
    <p style='color:#64748B;'>Your personal robot tutor. Available 24/7. Ask anything!</p>
    """, unsafe_allow_html=True)

    c_chat, c_side = st.columns([3, 2])

    with c_chat:
        # Chat history
        if not st.session_state.chat:
            st.markdown("""
            <div style="background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.15);
                        border-radius:16px; padding:32px; text-align:center; margin-bottom:24px;">
              <div style="font-size:48px; margin-bottom:12px;">🤖</div>
              <div style="font-size:18px; font-weight:700; margin-bottom:8px;">ARIA Online!</div>
              <div style="color:#64748B; font-size:13px; line-height:1.6;">
                Greetings Commander! I am ARIA — your AI co-pilot for the coding galaxy.<br>
                Ask me anything: Python errors, concepts, career advice, code review!
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; margin-bottom:12px;">
                      <div style="background:linear-gradient(135deg,#1E40AF,#4C1D95); border-radius:16px 16px 4px 16px;
                                  padding:12px 16px; max-width:75%; font-size:14px; line-height:1.5;">
                        {msg['content']}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display:flex; gap:10px; margin-bottom:12px; align-items:flex-start;">
                      <span style="font-size:22px; min-width:32px;">🤖</span>
                      <div style="background:var(--panel); border:1px solid var(--border);
                                  border-radius:4px 16px 16px 16px; padding:12px 16px;
                                  max-width:82%; font-size:14px; line-height:1.6;">
                        {msg['content']}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Input
        c_inp, c_btn = st.columns([5, 1])
        with c_inp:
            user_msg = st.text_input("", placeholder="Ask ARIA anything about Python, errors, concepts...",
                                      key="aria_input", label_visibility="collapsed")
        with c_btn:
            send = st.button("Send", key="aria_send", use_container_width=True)

        if send and user_msg:
            from utils.aria import aria_chat
            st.session_state.chat.append({"role": "user", "content": user_msg})
            hist = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat[:-1]]
            with st.spinner("🤖 ARIA calculating..."):
                resp = aria_chat(user_msg, history=hist)
            st.session_state.chat.append({"role": "assistant", "content": resp})
            st.rerun()

        # Quick questions
        if len(st.session_state.chat) == 0:
            st.markdown("**⚡ Quick Questions:**")
            quick = [
                "What's the difference between a list and a dictionary?",
                "How do I fix an IndentationError?",
                "Explain classes and objects simply",
                "What is machine learning in simple terms?",
                "How do f-strings work?",
                "What is LangChain and why use it?",
            ]
            qc = st.columns(2)
            for i, q in enumerate(quick):
                with qc[i % 2]:
                    if st.button(q, key=f"quick_{i}", use_container_width=True):
                        from utils.aria import aria_chat
                        st.session_state.chat.append({"role": "user", "content": q})
                        with st.spinner("🤖 ARIA..."):
                            r = aria_chat(q)
                        st.session_state.chat.append({"role": "assistant", "content": r})
                        st.rerun()

        if st.session_state.chat:
            if st.button("🗑 Clear Chat", key="clear_aria"):
                st.session_state.chat = []
                st.rerun()

    with c_side:
        st.markdown("### 🎲 Generate Mission")
        topics = ["Python Basics", "Functions", "Lists", "OOP", "NumPy", "Pandas", "ML", "APIs", "LangChain"]
        diff_lvl = st.select_slider("Difficulty:", options=[1,2,3,4,5], value=2, key="gen_diff")
        topic = st.selectbox("Topic:", topics, key="gen_topic")
        if st.button("🎲 Generate Challenge!", use_container_width=True, key="gen_ch"):
            from utils.aria import aria_generate_challenge
            with st.spinner("ARIA generating..."):
                ch = aria_generate_challenge(topic, diff_lvl, len(gs["completed_missions"]))
            if ch:
                st.session_state.generated_ch = ch
                st.rerun()

        if st.session_state.get("generated_ch"):
            st.markdown(f"""
            <div style="background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.2);
                        border-radius:10px; padding:14px; font-size:13px; line-height:1.6;">
              {st.session_state.generated_ch}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📚 ARIA Can Help With")
        helps = ["🐛 Debug errors", "📖 Explain concepts", "🔍 Code review", "🎯 Practice challenges",
                 "🚀 Career guidance", "⚡ Best practices", "🏗️ System design", "🤖 AI/ML questions"]
        for h in helps:
            st.markdown(f"<div style='padding:6px 0; font-size:13px; color:#94A3B8;'>{h}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ACHIEVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
def page_achievements():
    st.markdown("<h1>🏆 Achievements</h1>", unsafe_allow_html=True)
    earned = gs.get("earned_badges", [])
    c1, c2, c3 = st.columns(3)
    c1.metric("🏅 Earned", f"{len(earned)}/{len(ACHIEVEMENTS)}")
    c2.metric("⚡ Total XP", f"{gs['xp']:,}")
    c3.metric("✅ Missions", len(gs["completed_missions"]))
    st.divider()

    cols = st.columns(3)
    for i, (name, info) in enumerate(ACHIEVEMENTS.items()):
        is_earned = name in earned
        emoji = name.split()[0]
        title = " ".join(name.split()[1:])
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:{'rgba(251,191,36,0.08)' if is_earned else 'rgba(255,255,255,0.02)'};
                        border:1px solid {'rgba(251,191,36,0.35)' if is_earned else 'rgba(255,255,255,0.06)'};
                        border-radius:12px; padding:18px; text-align:center; margin-bottom:12px;
                        {'box-shadow:0 0 16px rgba(251,191,36,0.15);' if is_earned else 'opacity:0.4; filter:grayscale(80%);'}">
              <div style="font-size:32px; margin-bottom:8px;">{'🔓' if not is_earned else emoji}</div>
              <div style="font-weight:700; font-size:13px; margin-bottom:4px;">{title}</div>
              <div style="font-size:11px; color:#64748B; margin-bottom:6px;">{info['desc']}</div>
              <div style="font-size:11px; color:{'#FBBF24' if is_earned else '#475569'}; font-weight:700;">
                {'✓ EARNED' if is_earned else ('+' + str(info['xp']) + ' XP to earn')}
              </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CERTIFICATES
# ══════════════════════════════════════════════════════════════════════════════
def page_certificates():
    st.markdown("<h1>📜 Certificates</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B;'>Complete all missions in a track to earn your official certificate.</p>", unsafe_allow_html=True)

    earned_certs = gs.get("earned_certs", [])
    cols = st.columns(2)
    for i, cert in enumerate(CERTIFICATES):
        is_earned = cert["id"] in earned_certs
        req = cert["required_missions"]
        done = sum(1 for m in req if m in gs["completed_missions"])
        total = len(req)
        pct = int(done / total * 100) if total else 0
        color = cert["color"]

        with cols[i % 2]:
            if is_earned:
                st.markdown(f"""
                <div class="cert-card" style="border-color:{color}; background:linear-gradient(135deg,rgba(0,0,0,0.6),rgba(0,0,0,0.3));
                            box-shadow:0 0 30px {color}33; margin-bottom:16px;">
                  <div style="font-size:48px; margin-bottom:8px;">{cert['icon']}</div>
                  <div style="font-family:'Orbitron',sans-serif; font-size:11px; letter-spacing:3px; color:{color}; margin-bottom:8px;">CERTIFICATE OF COMPLETION</div>
                  <div style="font-size:20px; font-weight:700; margin-bottom:4px;">{cert['title']}</div>
                  <div style="font-size:13px; color:#94A3B8; margin-bottom:16px; font-style:italic;">{cert['subtitle']}</div>
                  <div style="background:{color}22; border:1px solid {color}44; border-radius:20px; padding:6px 16px; display:inline-block;">
                    <span style="color:{color}; font-size:12px; font-weight:700;">✓ CERTIFIED COMMANDER</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="cert-card" style="border-color:rgba(255,255,255,0.08); opacity:0.6; margin-bottom:16px;">
                  <div style="font-size:36px; margin-bottom:8px; filter:grayscale(80%);">🔒</div>
                  <div style="font-size:18px; font-weight:700; margin-bottom:4px; color:#64748B;">{cert['title']}</div>
                  <div style="font-size:12px; color:#475569; margin-bottom:12px;">{cert['subtitle']}</div>
                  <div style="font-size:12px; color:#64748B; margin-bottom:8px;">Progress: {done}/{total} missions</div>
                  <div class="xp-track" style="margin:8px auto; max-width:200px;">
                    <div class="xp-fill" style="width:{pct}%; background:linear-gradient(90deg,{color},{color}88);"></div>
                  </div>
                  <div style="font-size:11px; color:#475569; margin-top:6px;">{pct}% complete</div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LEADERBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_leaderboard():
    st.title("🏆 Galactic Leaderboard")
    st.subheader("Top Space Cadets in the Universe")
    
    # Humne utils/state.py mein jo naya function banaya hai usay use karenge
    leaderboard_data = get_all_users_leaderboard()
    
    if leaderboard_data:
        import pandas as pd
        df_lb = pd.DataFrame(leaderboard_data)
        
        # Table ko thora pyara dikhane ke liye
        st.table(df_lb[['rank', 'avatar', 'username', 'level', 'xp']].set_index('rank'))
        
        # User ki apni rank highlight karna
        try:
            my_username = st.session_state.gs['username']
            # Check if user is in the list
            my_info = next((item for item in leaderboard_data if item["username"] == my_username), None)
            if my_info:
                st.info(f"🚀 Commander **{my_username}**, aapki current rank **#{my_info['rank']}** hai!")
        except:
            pass
    else:
        st.write("🌌 Galaxy khali hai... pehla kadam aap uthayein!")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
def page_settings():
    st.markdown("<h1>⚙️ Settings</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 👾 Commander Profile")
        new_name = st.text_input("Name:", value=gs.get("username", ""), key="set_name")
        avatars = ["🧑‍🚀","👩‍🚀","👨‍🚀","🤖","👾","💫","⭐","🌟"]
        av_cols = st.columns(8)
        current_av = gs.get("avatar", "🧑‍🚀")
        for a, c in zip(avatars, av_cols):
            with c:
                border = "2px solid #38BDF8" if a == current_av else "none"
                if st.button(a, key=f"set_av_{a}"):
                    gs["avatar"] = a
                    save_user_progress(gs)
                    st.rerun()

        if st.button("💾 Save Profile", use_container_width=True, key="save_profile"):
            gs["username"] = new_name
            save_user_progress(gs)
            st.success("✅ Profile saved!")

        st.divider()
        st.markdown("### 📊 Your Stats")
        stats = [
            ("Total XP", f"{gs['xp']:,}"),
            ("Level", get_level(gs["xp"])),
            ("Missions Done", len(gs["completed_missions"])),
            ("Badges", len(gs.get("earned_badges", []))),
            ("Certs", len(gs.get("earned_certs", []))),
            ("Streak", f"{gs['streak']} days"),
            ("Battles Won", gs.get("battles_won", 0)),
            ("Joined", gs.get("joined", "Today")),
        ]
        for k, v in stats:
            sc1, sc2 = st.columns([2, 1])
            sc1.markdown(f"<span style='color:#64748B;'>{k}</span>", unsafe_allow_html=True)
            sc2.markdown(f"**{v}**")

    with c2:
        st.markdown("### ℹ️ About Galaxy Coder")
        st.markdown("""
        <div style="background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:20px; color:#94A3B8; line-height:1.8; font-size:13px;">
          <strong style="color:#E2E8F0;">Galaxy Coder v1.0</strong><br>
          The world's first gamified space-themed Python learning platform.<br><br>
          <strong style="color:#38BDF8;">🪐 5 Planets:</strong><br>
          ☿ Mercury — Python Basics<br>
          ♀ Venus — OOP & Design<br>
          🌍 Earth — Data Science<br>
          ♂ Mars — Machine Learning<br>
          ♃ Jupiter — AI & LangGraph<br><br>
          <strong style="color:#FBBF24;">Powered by:</strong> Claude AI, Streamlit, Python
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.warning("⚠️ Danger Zone")
        if st.button("🔄 Reset All Progress", key="reset_all"):
            st.session_state.confirm_reset = True
        if st.session_state.get("confirm_reset"):
            st.error("This deletes EVERYTHING. Are you sure?")
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("✅ Yes, Reset", key="confirm_y"):
                    import os
                    new_gs = {"username": gs["username"], "avatar": gs.get("avatar","🧑‍🚀"),
                              "xp": 0, "level": 1, "completed_missions": [], "earned_badges": [],
                              "earned_certs": [], "streak": 0, "last_active": "", "battles_won": 0,
                              "battles_played": 0, "perfect_missions": 0, "hints_used": 0,
                              "current_planet": "mercury", "daily_xp": 0, "win_streak": 0,
                              "joined": gs.get("joined", "")}
                    save_state(new_gs)
                    st.session_state.confirm_reset = False
                    st.rerun()
            with rc2:
                if st.button("❌ Cancel", key="cancel_r"):
                    st.session_state.confirm_reset = False
                    st.rerun()





# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MULTIPLAYER BATTLE
# ══════════════════════════════════════════════════════════════════════════════
def page_multiplayer():
    st.markdown("""
    <h1 style="text-align:center;">👥 MULTIPLAYER ARENA</h1>
    <p style="text-align:center; color:#64748B; margin-bottom:24px;">Challenge friends. Battle live. Prove you're the best coder in the galaxy.</p>
    """, unsafe_allow_html=True)

    from utils.multiplayer import (create_battle_room, join_battle_room, get_room,
                                    set_player_ready, submit_answer, get_battle_results,
                                    finish_battle, list_open_rooms, cleanup_old_rooms)
    from utils.aria import aria_generate_battle_questions
    from data.universe import BATTLE_QUESTIONS
    import random

    cleanup_old_rooms()

    username = gs.get("username", "Commander")
    avatar = gs.get("avatar", "🧑‍🚀")

    # State
    if "mp_room_id" not in st.session_state:
        st.session_state.mp_room_id = None
    if "mp_q_idx" not in st.session_state:
        st.session_state.mp_q_idx = 0
    if "mp_answered" not in st.session_state:
        st.session_state.mp_answered = None

    room_id = st.session_state.mp_room_id

    # ── Not in a room ──
    if not room_id:
        tab_host, tab_join, tab_browse = st.tabs(["🏠 Host Battle", "🔗 Join Battle", "🌐 Open Rooms"])

        with tab_host:
            st.markdown("### Create Your Battle Room")
            diff = st.selectbox("Difficulty:", ["beginner", "intermediate", "advanced"], key="mp_diff")
            st.markdown(f"""
            <div style="background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.15);
                        border-radius:10px; padding:14px; margin:12px 0; font-size:13px; color:#94A3B8;">
              🤖 Questions will be <strong>AI-generated by ARIA</strong> — unique every battle!<br>
              👥 Up to 4 players can join your room<br>
              ⚔️ 8 questions per battle
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Create Room", use_container_width=True, key="mp_create"):
                new_id = create_battle_room(username, avatar, diff)
                st.session_state.mp_room_id = new_id
                st.session_state.mp_q_idx = 0
                st.session_state.mp_answered = None
                st.rerun()

        with tab_join:
            st.markdown("### Join a Battle")
            code = st.text_input("Enter Room Code:", placeholder="ABC123", key="mp_code").upper().strip()
            if st.button("⚔️ Join Room", use_container_width=True, key="mp_join"):
                if code:
                    ok, result = join_battle_room(code, username, avatar)
                    if ok:
                        st.session_state.mp_room_id = result
                        st.session_state.mp_q_idx = 0
                        st.session_state.mp_answered = None
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.warning("Enter a room code!")

        with tab_browse:
            st.markdown("### Open Battle Rooms")
            open_rooms = list_open_rooms()
            if open_rooms:
                for room in open_rooms:
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"""
                        <div style="background:var(--panel); border:1px solid var(--border);
                                    border-radius:10px; padding:12px 16px;">
                          <strong>{room['id']}</strong> · hosted by {room['host']} ·
                          {room['players']}/4 players · {room['difficulty'].title()}
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        if st.button("Join →", key=f"join_{room['id']}", use_container_width=True):
                            ok, result = join_battle_room(room['id'], username, avatar)
                            if ok:
                                st.session_state.mp_room_id = result
                                st.rerun()
            else:
                st.info("No open rooms right now. Create one and invite friends!")
        return

    # ── In a room ──
    room = get_room(room_id)
    if not room:
        st.error("Room not found!")
        st.session_state.mp_room_id = None
        st.rerun()
        return

    is_host = room["host"] == username

    # Room header
    col_code, col_status, col_leave = st.columns([2, 2, 1])
    with col_code:
        st.markdown(f"""
        <div style="background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.3);
                    border-radius:8px; padding:10px 16px; text-align:center;">
          <div style="font-size:11px; color:#64748B; letter-spacing:2px;">ROOM CODE</div>
          <div style="font-family:'Orbitron',sans-serif; font-size:28px; font-weight:900; color:#FBBF24;">{room_id}</div>
          <div style="font-size:11px; color:#64748B;">Share this with friends!</div>
        </div>
        """, unsafe_allow_html=True)
    with col_status:
        status_color = {"waiting": "#FBBF24", "active": "#34D399", "finished": "#F87171"}
        sc = status_color.get(room["status"], "#64748B")
        st.markdown(f"""
        <div style="background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.15);
                    border-radius:8px; padding:10px 16px; text-align:center;">
          <div style="font-size:11px; color:#64748B; letter-spacing:2px;">STATUS</div>
          <div style="font-size:20px; font-weight:700; color:{sc}; margin:4px 0;">
            {'⏳ Waiting' if room['status']=='waiting' else '⚔️ Battle Active!' if room['status']=='active' else '🏁 Finished'}
          </div>
          <div style="font-size:11px; color:#64748B;">{room['difficulty'].title()} difficulty</div>
        </div>
        """, unsafe_allow_html=True)
    with col_leave:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Leave", use_container_width=True, key="mp_leave"):
            st.session_state.mp_room_id = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Players list
    st.markdown("### 👥 Players")
    player_cols = st.columns(min(len(room["players"]), 4))
    for i, (pname, pdata) in enumerate(room["players"].items()):
        with player_cols[i % 4]:
            is_me = pname == username
            ready = pdata.get("ready", False)
            st.markdown(f"""
            <div style="background:{'rgba(52,211,153,0.08)' if ready else 'var(--panel)'};
                        border:1px solid {'rgba(52,211,153,0.3)' if ready else 'var(--border)'};
                        border-radius:10px; padding:14px; text-align:center;">
              <div style="font-size:28px;">{pdata['avatar']}</div>
              <div style="font-weight:700; font-size:13px; color:{'#38BDF8' if is_me else '#E2E8F0'};">{pname}{'  (You)' if is_me else ''}</div>
              <div style="font-size:11px; margin-top:4px; color:{'#34D399' if ready else '#64748B'};">{'✅ Ready!' if ready else '⏳ Waiting...'}</div>
              {f'<div style="font-size:20px; font-weight:900; color:#FBBF24; margin-top:4px;">{pdata["score"]} pts</div>' if room["status"]=="active" else ''}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── WAITING ROOM ──
    if room["status"] == "waiting":
        me = room["players"].get(username, {})
        if not me.get("ready", False):
            if is_host:
                st.markdown("### 🚀 Start Battle")
                st.info(f"👑 You are the HOST. Generate questions and start when everyone is ready!")
                if st.button("🤖 Generate Questions & Ready Up!", use_container_width=True, key="mp_gen_start"):
                    with st.spinner("ARIA generating battle questions..."):
                        ai_qs = aria_generate_battle_questions(
                            room["difficulty"], room["difficulty"],
                            gs["completed_missions"], count=8
                        )
                    if not ai_qs:
                        qs = BATTLE_QUESTIONS.get(room["difficulty"], list(BATTLE_QUESTIONS.values())[0]).copy()
                        random.shuffle(qs)
                        ai_qs = qs[:8]
                    set_player_ready(room_id, username, ai_qs)
                    st.success("✅ Questions ready! Waiting for others...")
                    st.rerun()
            else:
                if st.button("✅ I'm Ready!", use_container_width=True, key="mp_ready"):
                    set_player_ready(room_id, username)
                    st.rerun()
        else:
            st.success("✅ You're ready! Waiting for others...")

        if st.button("🔄 Refresh", use_container_width=True, key="mp_refresh"):
            st.rerun()

    # ── ACTIVE BATTLE ──
    elif room["status"] == "active":
        questions = room.get("questions", [])
        if not questions:
            st.error("No questions found!")
            return

        q_idx = st.session_state.mp_q_idx
        if q_idx >= len(questions):
            # Show waiting for others / results
            my_score = room["players"].get(username, {}).get("score", 0)
            st.success(f"✅ You finished! Score: {my_score}/{len(questions)}")
            st.info("Waiting for other players...")
            results = get_battle_results(room_id)
            st.markdown("### 📊 Current Standings")
            for i, p in enumerate(results):
                medal = ["🥇","🥈","🥉"][i] if i < 3 else f"#{i+1}"
                st.markdown(f"**{medal} {p['avatar']} {p['name']}** — {p['score']} pts")
            if st.button("🔄 Refresh Results", use_container_width=True, key="mp_ref_res"):
                st.rerun()
            return

        q = questions[q_idx]
        # Progress
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; background:var(--panel);
                    border:1px solid var(--border); border-radius:8px; padding:10px 16px; margin-bottom:16px;">
          <span style="color:#64748B;">Question {q_idx+1}/{len(questions)}</span>
          <span style="color:#FBBF24; font-weight:700;">Your Score: {room['players'].get(username,{}).get('score',0)}</span>
          <span style="font-size:11px; background:rgba(56,189,248,0.1); padding:3px 10px; border-radius:20px; color:#38BDF8;">{q.get('topic','')}</span>
        </div>
        """, unsafe_allow_html=True)

        xp_bar((q_idx / len(questions)) * 100)
        st.markdown(f"### {q['q']}")

        answered = st.session_state.mp_answered
        for i, opt in enumerate(q["options"]):
            if answered is not None:
                cls = "correct" if i == q["answer"] else ("wrong" if i == answered else "")
                icon = "✅ " if i == q["answer"] else ("❌ " if i == answered else "   ")
                st.markdown(f'<div class="quiz-option {cls}">{icon}{opt}</div>', unsafe_allow_html=True)
            else:
                if st.button(f"  {opt}", key=f"mp_opt_{q_idx}_{i}", use_container_width=True):
                    correct = (i == q["answer"])
                    submit_answer(room_id, username, q_idx, i, correct)
                    st.session_state.mp_answered = i
                    st.rerun()

        if answered is not None:
            if answered == q["answer"]:
                st.success("⚡ Correct! +1 point")
            else:
                exp = q.get("explanation", "")
                st.error(f"❌ Wrong. {exp}")
            if st.button("Next →", use_container_width=True, key=f"mp_next_{q_idx}"):
                st.session_state.mp_q_idx += 1
                st.session_state.mp_answered = None
                st.rerun()

    # ── FINISHED ──
    elif room["status"] == "finished":
        st.markdown("## 🏁 Battle Complete!")
        results = get_battle_results(room_id)
        medals = ["🥇","🥈","🥉"]
        for i, p in enumerate(results):
            medal = medals[i] if i < 3 else f"#{i+1}"
            is_me = p["name"] == username
            st.markdown(f"""
            <div style="background:{'rgba(251,191,36,0.08)' if i==0 else 'var(--panel)'};
                        border:1px solid {'rgba(251,191,36,0.3)' if i==0 else 'var(--border)'};
                        border-radius:10px; padding:14px 20px; margin-bottom:8px;
                        display:flex; align-items:center; gap:16px;">
              <span style="font-size:28px;">{medal}</span>
              <span style="font-size:22px;">{p['avatar']}</span>
              <div style="flex:1;">
                <div style="font-weight:700; color:{'#38BDF8' if is_me else '#E2E8F0'};">
                  {p['name']}{'  ← You' if is_me else ''}
                </div>
              </div>
              <div style="font-family:'Orbitron',sans-serif; font-size:24px; font-weight:900;
                          color:{'#FBBF24' if i==0 else '#94A3B8'};">{p['score']} pts</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔄 New Battle", use_container_width=True, key="mp_new"):
            st.session_state.mp_room_id = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PORTFOLIO PROJECTS
# ══════════════════════════════════════════════════════════════════════════════
def page_projects():
    st.markdown("""
    <h1>🏗️ Portfolio Projects</h1>
    <p style='color:#64748B;'>Real projects. Real code. Real portfolio. Build these and show the world what you can do.</p>
    """, unsafe_allow_html=True)

    try:
        from data.extra_content import PORTFOLIO_PROJECTS
    except:
        st.error("Projects not loaded yet.")
        return

    diff_colors = {"Intermediate": "#34D399", "Advanced": "#FBBF24", "Expert": "#F87171"}

    # Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Projects Available", len(PORTFOLIO_PROJECTS))
    completed_projs = len([p for p in PORTFOLIO_PROJECTS if f"proj_{p['id']}" in gs.get("completed_missions", [])])
    c2.metric("✅ Completed", completed_projs)
    total_proj_xp = sum(p["xp"] for p in PORTFOLIO_PROJECTS)
    c3.metric("⚡ Total XP Available", f"{total_proj_xp:,}")

    st.divider()

    for proj in PORTFOLIO_PROJECTS:
        color = proj.get("color", "#38BDF8")
        diff = proj["difficulty"]
        dc = diff_colors.get(diff, "#64748B")

        with st.expander(f"{proj['title']}  ·  {diff}  ·  ⚡{proj['xp']} XP  ·  ⏱ {proj['time']}", expanded=False):
            c_left, c_right = st.columns([3, 2])

            with c_left:
                st.markdown(f"""
                <div style="background:rgba(0,0,0,0.2); border-left:3px solid {color};
                            border-radius:0 10px 10px 0; padding:16px; margin-bottom:16px;">
                  <p style="color:#CBD5E1; margin:0; line-height:1.6;">{proj['description']}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**🎯 What You'll Learn:**")
                for item in proj["what_you_learn"]:
                    st.markdown(f"- {item}")

                st.markdown("**📋 Build Steps:**")
                for i, step in enumerate(proj["steps"], 1):
                    st.markdown(f"{i}. {step}")

            with c_right:
                # Tech stack
                st.markdown("**🛠️ Tech Stack:**")
                tech_html = " ".join([
                    f'<span class="badge-pill" style="background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); color:#38BDF8;">{t}</span>'
                    for t in proj["tech"]
                ])
                st.markdown(f"<div>{tech_html}</div>", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # GitHub topics
                st.markdown("**🏷️ GitHub Topics:**")
                gt_html = " ".join([
                    f'<span class="badge-pill" style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.2); color:#34D399; font-size:11px;">{t}</span>'
                    for t in proj.get("github_topics", [])
                ])
                st.markdown(f"<div>{gt_html}</div>", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"📋 Get Starter Code", key=f"proj_code_{proj['id']}", use_container_width=True):
                    st.session_state[f"show_proj_{proj['id']}"] = True

            if st.session_state.get(f"show_proj_{proj['id']}"):
                st.markdown("**🚀 Starter Code:**")
                st.code(proj.get("starter_code", "# Coming soon!"), language="python")
                st.info("💡 Copy this to your local environment and build the full project. When done, add to GitHub and your portfolio!")

                if st.button(f"✅ Mark as Complete (+{proj['xp']} XP)", key=f"proj_done_{proj['id']}", use_container_width=True):
                    if proj["id"] not in gs.get("completed_missions", []):
                        updated, leveled_up, new_level = add_xp(gs, proj["xp"], proj["id"])
                        save_state(updated)
                        st.balloons()
                        st.success(f"🎉 +{proj['xp']} XP! Project marked complete!")
                        if leveled_up:
                            st.markdown(f"""
                            <div style="text-align:center; background:rgba(251,191,36,0.1); border:2px solid #FBBF24;
                                        border-radius:12px; padding:16px; margin-top:8px;">
                              ⬆️ <strong>LEVEL UP! Level {new_level}!</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.info("Already completed!")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

# 1. Authentication Check (Check karein ke kya user login hai)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 2. Agar login nahi hai, toh sirf Onboarding/Login screen dikhayein
if not st.session_state.authenticated:
    st.title("🚀 Galaxy Coder: System Access")
    st.subheader("Welcome Cadet! Identify yourself to enter the universe.")
    
    # Login aur Sign Up ke liye do Tabs
    tab1, tab2 = st.tabs(["🔐 Commander Login", "🌟 New Cadet Sign-Up"])
    
    with tab1:
        u_login = st.text_input("Enter your Registered Name", key="login_name")
        if st.button("Resume Mission"):
            user_data = load_user(u_login) # Google Sheets se data check hoga
            if user_data:
                st.session_state.gs = user_data
                st.session_state.authenticated = True
                st.success(f"Welcome back, Commander {u_login}!")
                st.rerun()
            else:
                st.error("Access Denied! Name not found in database.")

    with tab2:
        u_signup = st.text_input("Choose a Unique Name", key="signup_name")
        if st.button("Initialize Profile"):
            if u_signup:
                if load_user(u_signup): # Check karein ke naam pehle se toh nahi hai
                    st.error("This name is already claimed! Choose another identifier.")
                else:
                    new_gs = default_state()
                    new_gs["username"] = u_signup
                    save_user_progress(new_gs) # Pehli baar Google Sheet mein save
                    st.session_state.gs = new_gs
                    st.session_state.authenticated = True
                    st.success(f"Profile Created! Welcome to the Galaxy, {u_signup}!")
                    st.rerun()
            else:
                st.warning("Please provide a name to initialize your systems.")
    
    # Jab tak login na ho, app ka baqi hissa load nahi hoga
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATED AREA (Sirf login ke baad dikhega)
# ══════════════════════════════════════════════════════════════════════════════

# Sidebar hamesha dikhayen taaki user pages badal sakay
render_sidebar()

page = st.session_state.page

if page == "galaxy":         page_galaxy()
elif page == "planet":       page_planet()
elif page == "mission":      page_mission()
elif page == "battle":       page_battle()
elif page == "multiplayer":  page_multiplayer()
elif page == "projects":     page_projects()
elif page == "aria":         page_aria()
elif page == "achievements": page_achievements()
elif page == "certificates": page_certificates()
elif page == "leaderboard":  page_leaderboard()
elif page == "settings":     page_settings()
else:                        page_galaxy()
