import streamlit as st
import requests

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_BASE = "https://leetcode-tracker-7as7.onrender.com"  # CHANGE THIS to your backend URL (e.g. http://localhost:8000 if running locally)

st.set_page_config(
    page_title="LeetCode Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:      #0d0f14;
    --surf:    #13161e;
    --border:  #1e2330;
    --accent:  #f0b429;
    --text:    #e8eaf0;
    --muted:   #6b7280;
    --green:   #22c55e;
    --blue:    #3b82f6;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stMain"],
section.main > div { background-color: var(--bg) !important; color: var(--text) !important; font-family: 'Syne', sans-serif !important; }

#MainMenu, footer, header, [data-testid="stDecoration"],
[data-testid="stSidebarNav"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; }

[data-testid="stSidebar"] { display: none !important; }

/* ── inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #0a0c10 !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 7px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(240,180,41,0.12) !important;
}
div[data-testid="stTextArea"] textarea {
    background: #0a0c10 !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 7px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important;
    resize: vertical !important;
}
.stSelectbox > div > div { background: #0a0c10 !important; border: 1px solid var(--border) !important; border-radius: 7px !important; }
.stSelectbox > div > div > div { color: var(--text) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem !important; }

/* ── slider ── */
.stSlider > div > div > div > div { background: var(--accent) !important; }

/* ── buttons ── */
.stButton > button {
    background: var(--accent) !important; color: #0d0f14 !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    border: none !important; border-radius: 7px !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
    background: transparent !important; color: var(--muted) !important;
    border: 1px solid var(--border) !important;
}

/* ── labels ── */
label, [data-testid="stWidgetLabel"] {
    color: var(--muted) !important; font-size: 0.72rem !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--muted) !important; border: none !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; letter-spacing: 1px; padding: 10px 18px !important; }
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom: 2px solid var(--accent) !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── expander ── */
[data-testid="stExpander"] {
    background: #0f121a !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; margin-top: -1px !important;
}
[data-testid="stExpander"] summary { color: var(--muted) !important; font-size: 0.78rem !important; }

/* ── divider ── */
hr { border-color: var(--border) !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── stat cards ── */
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 28px; }
.stat-card {
    background: var(--surf); border: 1px solid var(--border); border-radius: 10px;
    padding: 20px 24px; position: relative; overflow: hidden;
}
.stat-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--accent);
}
.stat-card.blue::after { background: var(--blue); }
.stat-label { font-size: 0.68rem; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
.stat-value { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 700; color: var(--text); line-height: 1; }

/* ── table ── */
.tbl-head {
    display: grid;
    grid-template-columns: 40px 2.5fr 1.4fr 2fr 100px 70px;
    gap: 8px; padding: 10px 14px;
    font-size: 0.65rem; color: var(--muted); letter-spacing: 2px; text-transform: uppercase;
    border-bottom: 2px solid var(--border); margin-top: 16px;
}
.tbl-row {
    display: grid;
    grid-template-columns: 40px 2.5fr 1.4fr 2fr 100px 70px;
    gap: 8px; align-items: center;
    padding: 0 14px; min-height: 52px;
    border-bottom: 1px solid var(--border);
    transition: background 0.12s;
}
.tbl-row:hover { background: rgba(240,180,41,0.03); }
.sno { font-family: 'JetBrains Mono', monospace; color: var(--muted); font-size: 0.78rem; }
.prob-link { font-weight: 600; font-size: 0.92rem; }
.prob-link a { color: var(--text) !important; text-decoration: none !important; }
.prob-link a:hover { color: var(--accent) !important; }
.conf-pip { display: flex; gap: 3px; align-items: center; }
.pip { width: 10px; height: 10px; border-radius: 2px; background: var(--border); }
.pip.on-0 { background: var(--muted); }
.pip.on-1 { background: #ef4444; }
.pip.on-2 { background: #f97316; }
.pip.on-3 { background: #eab308; }
.pip.on-4 { background: var(--green); }
.pip.on-5 { background: var(--blue); }

/* ── filter bar ── */
.filter-bar {
    background: var(--surf); border: 1px solid var(--border); border-radius: 10px;
    padding: 16px 20px; margin-bottom: 6px;
}

/* ── auth ── */
.auth-logo {
    text-align: center; padding: 52px 0 8px;
    font-family: 'JetBrains Mono', monospace; font-size: 2.6rem;
    font-weight: 700; color: var(--accent); letter-spacing: -2px;
}
.auth-sub { text-align: center; color: var(--muted); font-size: 0.78rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 36px; }

/* ── toast / banner ── */
.sync-banner {
    background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2);
    border-radius: 8px; padding: 10px 16px; margin-bottom: 18px;
    color: var(--green); font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
}
.page-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 4px 0 20px; border-bottom: 1px solid var(--border); margin-bottom: 20px;
}
.page-logo { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: var(--accent); letter-spacing: -1px; }
.page-user { font-size: 0.75rem; color: var(--muted); letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("token", None), ("username", None), ("lc_username", None), ("synced", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── API HELPERS ──────────────────────────────────────────────────────────────
def ah():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def api_get(path, params=None):
    try:
        return requests.get(f"{API_BASE}{path}", headers=ah(), params=params, timeout=12)
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def api_post(path, json=None, data=None, form=False):
    try:
        if form:
            return requests.post(f"{API_BASE}{path}", data=data, timeout=12)
        return requests.post(f"{API_BASE}{path}", headers=ah(), json=json, timeout=12)
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def api_put(path, json=None):
    try:
        return requests.put(f"{API_BASE}{path}", headers=ah(), json=json, timeout=12)
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def api_delete(path):
    try:
        return requests.delete(f"{API_BASE}{path}", headers=ah(), timeout=12)
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

# ─── HELPERS ──────────────────────────────────────────────────────────────────
CONF_LABEL = {0: "Unseen", 1: "Struggling", 2: "Shaky", 3: "Ok", 4: "Good", 5: "Mastered"}

def pips_html(c):
    colors = {0:"#4b5563",1:"#ef4444",2:"#f97316",3:"#eab308",4:"#22c55e",5:"#3b82f6"}
    html = '<div class="conf-pip">'
    for i in range(1, 6):
        col = colors[c] if i <= c else "#1e2330"
        html += f'<div class="pip" style="background:{col}"></div>'
    html += f'<span style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:{colors[c]};margin-left:5px;">{CONF_LABEL[c]}</span>'
    html += '</div>'
    return html

# ─── AUTO SYNC (runs once per session after login) ────────────────────────────
def auto_sync():
    lc_user = st.session_state.lc_username
    if not lc_user:
        return
    r = api_post("/sync", json={"leetcode_username": lc_user, "limit": 50})
    if r and r.status_code == 200:
        st.session_state.synced = True

# ─── AUTH PAGE ────────────────────────────────────────────────────────────────
def auth_page():
    st.markdown('<div class="auth-logo">⚡ LC Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Track · Review · Master</div>', unsafe_allow_html=True)

    col = st.columns([1, 1.1, 1])[1]
    with col:
        tab_in, tab_up = st.tabs(["SIGN IN", "REGISTER"])

        with tab_in:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            username  = st.text_input("Username", key="li_u", placeholder="your_handle")
            password  = st.text_input("Password", type="password", key="li_p", placeholder="••••••••")
            lc_handle = st.text_input("LeetCode Username", key="li_lc", placeholder="leetcode_handle  (for auto-sync)")

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", key="li_btn", use_container_width=True):
                if not username or not password:
                    st.warning("Fill in username and password.")
                else:
                    r = api_post("/login", data={"username": username, "password": password}, form=True)
                    if r and r.status_code == 200:
                        st.session_state.token       = r.json()["access_token"]
                        st.session_state.username    = username
                        st.session_state.lc_username = lc_handle.strip() if lc_handle.strip() else None
                        st.session_state.synced      = False
                        st.rerun()
                    else:
                        msg = r.json().get("detail", "Login failed.") if r else "Server error."
                        st.error(msg)

        with tab_up:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            new_u = st.text_input("Username", key="reg_u", placeholder="choose_a_handle")
            new_p = st.text_input("Password", type="password", key="reg_p", placeholder="••••••••")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", key="reg_btn", use_container_width=True):
                if not new_u or not new_p:
                    st.warning("Fill in both fields.")
                else:
                    r = requests.post(f"{API_BASE}/register", params={"username": new_u, "password": new_p})
                    if r.status_code == 200:
                        st.success("Account created — sign in above.")
                    else:
                        st.error(r.json().get("detail", "Registration failed."))

# ─── DASHBOARD ────────────────────────────────────────────────────────────────
def dashboard():
    # ── Auto-sync on first load ────────────────────────────────────────────────
    if not st.session_state.synced and st.session_state.lc_username:
        with st.spinner(f"Syncing from LeetCode ({st.session_state.lc_username})…"):
            auto_sync()

    # ── Header ────────────────────────────────────────────────────────────────
    h1, h2 = st.columns([1, 1])
    with h1:
        st.markdown(f"""
        <div class="page-header">
          <div>
            <div class="page-logo">⚡ LC Tracker</div>
            <div class="page-user">Signed in as <b>{st.session_state.username}</b>
              {f'· LC: <b>{st.session_state.lc_username}</b>' if st.session_state.lc_username else ''}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        btnc1, btnc2, _ = st.columns([1, 1, 2])
        with btnc1:
            st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
            if st.button("↺ Re-sync", key="resync"):
                if st.session_state.lc_username:
                    with st.spinner("Syncing…"):
                        auto_sync()
                    st.rerun()
                else:
                    st.warning("No LeetCode username set. Sign out and sign in again with your LC handle.")
        with btnc2:
            st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
            if st.button("Sign Out", key="so"):
                for k in ["token", "username", "lc_username", "synced"]:
                    st.session_state[k] = None if k != "synced" else False
                st.rerun()

    # ── Sync banner ───────────────────────────────────────────────────────────
    if st.session_state.synced:
        st.markdown(f'<div class="sync-banner">✓ Synced latest submissions from <b>{st.session_state.lc_username}</b></div>', unsafe_allow_html=True)

    # ── Fetch problems ────────────────────────────────────────────────────────
    r = api_get("/problems")
    if r is None or r.status_code != 200:
        st.error("Could not load problems.")
        return
    problems = r.json()

    total    = len(problems)
    patterns = len(set(p["pattern"] for p in problems if p.get("pattern")))

    # ── Stat cards ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-label">Total Problems Solved</div>
        <div class="stat-value">{total}</div>
      </div>
      <div class="stat-card blue">
        <div class="stat-label">Unique Patterns</div>
        <div class="stat-value">{patterns}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not problems:
        st.markdown("""
        <div style="text-align:center;padding:60px 0;color:#6b7280;">
          <div style="font-size:3rem;margin-bottom:10px;">📭</div>
          <div style="font-family:'JetBrains Mono',monospace;">No problems yet.</div>
          <div style="font-size:0.8rem;margin-top:6px;">Sign in with your LeetCode username to auto-sync.</div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
        fa, fb, fc = st.columns([2, 2, 2])
        with fa:
            search_title = st.text_input("Search title", placeholder="e.g. Two Sum", key="f_title", label_visibility="visible")
        with fb:
            pattern_opts = ["All patterns"] + sorted(set(p["pattern"] for p in problems if p.get("pattern")))
            filter_pat = st.selectbox("Pattern", pattern_opts, key="f_pat")
        with fc:
            conf_opts = ["Any confidence"] + [f"{i} — {CONF_LABEL[i]}" for i in range(6)]
            filter_conf = st.selectbox("Confidence", conf_opts, key="f_conf")
        st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered = problems[:]
    if search_title:
        filtered = [p for p in filtered if search_title.lower() in p["title"].lower()]
    if filter_pat != "All patterns":
        filtered = [p for p in filtered if p.get("pattern") == filter_pat]
    if filter_conf != "Any confidence":
        cv = int(filter_conf.split(" ")[0])
        filtered = [p for p in filtered if p["confidence"] == cv]

    # Sort newest first by default
    filtered.sort(key=lambda p: p.get("timestamp") or "", reverse=True)

    st.markdown(f'<div style="color:var(--muted);font-size:0.75rem;margin:10px 0 0;letter-spacing:1px;">{len(filtered)} problem(s)</div>', unsafe_allow_html=True)

    # ── Table header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="tbl-head">
      <span>#</span>
      <span>Problem</span>
      <span>Pattern</span>
      <span>Notes</span>
      <span>Confidence</span>
      <span>Save</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Rows ──────────────────────────────────────────────────────────────────
    for idx, p in enumerate(filtered, 1):
        slug  = p["slug"]
        title = p["title"]
        pat   = p.get("pattern") or ""
        notes = p.get("notes") or ""
        conf  = p["confidence"]

        lc_url = f"https://leetcode.com/problems/{slug}/"

        # Static display row (HTML)
        pat_html   = f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:0.78rem;background:rgba(240,180,41,0.1);color:#f0b429;border:1px solid rgba(240,180,41,0.2);border-radius:4px;padding:2px 8px;">{pat}</span>' if pat else '<span style="color:#374151;font-size:0.78rem;">—</span>'
        notes_html = f'<span style="font-size:0.8rem;color:#9ca3af;">{notes}</span>'        if notes else '<span style="color:#374151;font-size:0.78rem;">—</span>'

        st.markdown(f"""
        <div class="tbl-row">
          <div class="sno">{idx}</div>
          <div class="prob-link"><a href="{lc_url}" target="_blank">{title}</a></div>
          <div>{pat_html}</div>
          <div>{notes_html}</div>
          <div>{pips_html(conf)}</div>
          <div></div>
        </div>
        """, unsafe_allow_html=True)

        # Editable controls sit in a thin expander below each row
        with st.expander("edit", expanded=False):
            ec1, ec2, ec3, ec4 = st.columns([2, 2, 1, 0.7])
            with ec1:
                new_pat = st.text_input(
                    "Pattern", value=pat,
                    key=f"p_{slug}", placeholder="e.g. Sliding Window",
                    label_visibility="visible"
                )
            with ec2:
                new_notes = st.text_input(
                    "Notes", value=notes,
                    key=f"n_{slug}", placeholder="Key insight…",
                    label_visibility="visible"
                )
            with ec3:
                new_conf = st.number_input(
                    "Confidence (0–5)", min_value=0, max_value=5,
                    value=conf, step=1,
                    key=f"c_{slug}",
                    label_visibility="visible"
                )
            with ec4:
                st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
                if st.button("Save", key=f"s_{slug}", use_container_width=True):
                    ur = api_put("/update", json={
                        "slug": slug, "pattern": new_pat,
                        "notes": new_notes, "confidence": int(new_conf)
                    })
                    if ur and ur.status_code == 200:
                        st.success("Saved.")
                        st.rerun()
                    else:
                        st.error("Failed to save.")

# ─── ROUTER ───────────────────────────────────────────────────────────────────
if st.session_state.token is None:
    auth_page()
else:
    dashboard()