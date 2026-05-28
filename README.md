# LeetCode Tracker

---

## 🚀 Features

- 🔄 **Auto-sync solved LeetCode problems** by username (uses LeetCode’s GraphQL)
- 📝 **Add/edit your own notes & patterns** for each problem
- ⭐️ **Set and filter your confidence level**, to plan and focus your revisions
- 🔍 **Powerful filter/search** by title, pattern, or confidence
- 🔗 **Click any problem title** to open the official LeetCode page

---

## 🚦 LeetCode API Limitation

> **Important:**  
> Due to LeetCode's official API restrictions (even via GraphQL), *only your 20 most recent solved problems* are available for syncing.
>
> - This is an official LeetCode limitation—no tool can fetch more than 20 via public API.
> - When you solve more, re-sync to track new solutions.
> - Your notes and confidence for previously tracked problems are always kept unless deleted by you.

---

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
├── .gitignore
├── learning-process.excalidraw
└── README.md
```

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Sync engine:** Uses LeetCode’s GraphQL API under the hood

---

## 🗄️ Database Table Design

### `problems` Table

| Field      | Type     | Details/Constraints                   |
|------------|----------|---------------------------------------|
| id         | INTEGER  | Primary Key, auto-increment           |
| title      | TEXT     | LeetCode problem title                |
| slug       | TEXT     | Unique, for direct linking            |
| pattern    | TEXT     | (Optional) e.g. "array", "dp"         |
| notes      | TEXT     | (Optional) your revision notes        |
| confidence | INTEGER  | [0–5]: revision/proficiency score     |
| username   | TEXT     | For multi-user support                |

- **Slug:** used for problem URLs: `https://leetcode.com/problems/{slug}/`
- **Confidence:** from 0 (no confidence) to 5 (mastered)

---

## 🏃‍♀️ Running Locally

### 1. **Clone the repository**

```bash
git clone https://github.com/Neha-28-fluff/leetcode-tracker.git
cd leetcode-tracker
```

### 2. **Set up the backend**

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Initialize the database (SQLite, done automatically, but you may run to ensure)**

```bash
python database.py
```

### 4. **Run the FastAPI backend**

```bash
uvicorn main:app --reload
```
Backend will be at `http://127.0.0.1:8000`

---

### 5. **Set up and run the frontend**

(Open a new terminal if your backend is running)

```bash
cd ../frontend
python -m venv env
source env/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Frontend will be at the URL shown in your terminal (typically `http://localhost:8501`).

---

## 📝 My Learnings & Journey

This project was a fantastic learning experience in **full-stack development, integration with web APIs, and cloud deployment**. My key learnings:

- 🟦 **FastAPI:** Built a secure backend API, handling authentication, CORS, and clean API design.
- 🟩 **Streamlit for UI:** Leveraged Streamlit for a responsive Python-based frontend, including session state, editing in tables, and dynamic filtering.
- 🟨 **LeetCode GraphQL:** Learned to use the (unofficial) LeetCode GraphQL API for fetching problem data, and robust error handling for public API quirks.
- 🟧 **Integration:** Making sure frontend and backend work together—across `localhost`—was a rewarding debugging + deployment challenge.
- 🟪 **Database design:** Built multi-user support and persistence with SQLite, safely storing user notes and ratings.

---

## 💬 Questions/Feedback

Find a bug or have a suggestion?  
[Open an issue on GitHub](https://github.com/Neha-28-fluff/leetcode-tracker/issues)  
or connect with me [on LinkedIn](https://www.linkedin.com/in/neha-biswas-b15636322)!

---

**Happy Tracking ^^!**
