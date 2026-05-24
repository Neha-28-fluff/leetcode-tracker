# LeetCode Tracker

![screenshot or demo gif here](screenshots/demo.gif)

A web app to automatically sync your solved LeetCode questions, let you add personal notes and confidence ratings, and view/edit your progress—all in one place.

## 🚀 Features

- 🔄 **Sync solved problems** from LeetCode by username
- 📝 **Add/edit notes** on each problem
- ⭐️ **Set your confidence** per problem for easy revision
- 🔍 **Search/filter** by title or status
- 🔗 **Click problem title** → jump directly to actual LeetCode page

## 🛠️ Tech Stack

- **Python 3.10+**
- [FastAPI](https://fastapi.tiangolo.com/) (backend/API)
- [SQLite](https://docs.python.org/3/library/sqlite3.html) (storage)
- [Streamlit](https://streamlit.io/) (frontend UI)
- [requests](https://docs.python-requests.org/) (for LeetCode syncing)
- Docker for deployment

## 📸 Demo

![tracker UI screenshot](screenshots/screenshot.png)

## ⚡️ Quick Start

### 1. Clone the repo
```bash
git clone [https://github.com/yourusername/leetcode-tracker.git](https://github.com/Neha-28-fluff/leetcode-tracker.git)
cd leetcode-tracker
```

### 2. Install dependencies (ideally in a virtualenv)
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Set up environment (Optional: Create `.env` if needed)
```bash
cp backend/.env.example backend/.env
# Add your config/secrets as needed
```

### 4. Run the backend API (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```
By default, it starts at `http://localhost:8000`

### 5. Run the frontend UI (Streamlit)
```bash
cd frontend
streamlit run app.py
```
By default, opens in your browser.

## 🚦 LeetCode Tracker Data Limitations & Usage

### 🔗 How This Tracker Works
- Enter your LeetCode username and click **Sync**
- Browse/search problems, edit notes/confidence as you solve or review
- Click a problem title to jump to LeetCode for that problem
- Use the app regularly to track progress and prep smart!

### 🚨 API Limitation: Only Last 20 Solved Problems
- **Due to LeetCode public API restrictions, only the 20 most recent accepted submissions are available for syncing for any user.**
- This is a LeetCode global limit—**no app or script can fetch more than your last 20 via their public API.**
- If you solve additional problems, re-run the sync to track your newest ones.
- Previously tracked problems are not overwritten—you can keep/add notes/confidence for your full history (as long as you sync regularly).

## 🏗️ Project Structure

```
leetcode-tracker/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── leetcode_sync.py
│   └── ...
├── frontend/
│   ├── app.py
│   └── ...
├── data/
│   └── leetcode.db
├── scripts/
├── requirements.txt
├── .gitignore
└── README.md
```

---
## Database Table Design
## `problems` Table

| Field      | Type     | Details/Constraints                   |
|------------|----------|---------------------------------------|
| id         | INTEGER  | Primary Key, auto-increment           |
| title      | TEXT     | Not null, LeetCode problem title      |
| slug       | TEXT     | Not null, unique, for direct linking  |
| pattern    | TEXT     | (Optional) e.g. "array", "dp"         |
| notes      | TEXT     | (Optional) revision notes             |
| confidence | INTEGER  | [0–5], revision/proficiency score     |

### Conventions
- `slug` uses LeetCode string for direct URL: `https://leetcode.com/problems/{slug}/`
- Confidence: 0 (no confidence) to 5 (mastered)

### Design Justification
- Unique slug prevents duplicates from API sync
- Simple scale for fast update and UI filtering
- `pattern` is future-proofing for tags

### Questions for the Future
- Should I track date solved? Multiple notes? Multiple users?

---

## 📝 Future Goals / Ideas

- 🚩 Streak and tag support
- 📊 Visualize progress (charts, pie graphs)
- ✅ CSV/JSON export of your log
- 🛡️ Authentication/own hosting
- 📱 Mobile app or PWA

---

## 💬 License

MIT (or your favorite license).

---

### Need help? [Open an issue](https://github.com/Neha-28-fluff/leetcode-tracker/issues) or ping me on LinkedIn!
