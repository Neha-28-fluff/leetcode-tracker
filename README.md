# LeetCode Tracker

[![LeetCode Tracker Webapp](https://img.shields.io/badge/Try%20it%20Live-Streamlit%20App-brightgreen)](https://leetcode-review-tracker.streamlit.app/)

> **Try the app here**:  
> 🌐 **[https://leetcode-review-tracker.streamlit.app/](https://leetcode-review-tracker.streamlit.app/)**

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

- **Backend:** FastAPI, deployed on [Render](https://render.com)
- **Frontend:** Streamlit, deployed on [Streamlit Community Cloud](https://streamlit.io/cloud)
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

## 📝 My Learnings & Journey

This project was a fantastic learning experience in **full-stack development, integration with web APIs, and cloud deployment**. My key learnings:

- 🟦 **FastAPI + Cloud:** Built and deployed a secure backend API on Render, handling authentication, CORS, and clean API design.
- 🟩 **Streamlit for UI:** Leveraged Streamlit for a responsive Python-based frontend, including session state, editing in tables, and dynamic filtering.
- 🟨 **LeetCode GraphQL:** Learned to use the (unofficial) LeetCode GraphQL API for fetching problem data, and robust error handling for public API quirks.
- 🟧 **Integration:** Making sure frontend and backend work together—across `localhost` and then “live” on two platforms—was a rewarding debugging + deployment challenge.
- 🟪 **Database design:** Extended SQLite to support multi-user data and real-world persistence in the cloud, plus safely storing user notes and ratings.
- 🟫 **DevOps:** Covered everything from environment variables to troubleshooting deployment errors (like database folder creation and port binding).

> **Biggest challenge:** Adapting to LeetCode’s API rate/data limits, and ensuring a smooth user experience
> despite those constraints.

> **Most fun:** Seeing my LeetCode history, notes, and confidence levels all in one connected, cloud-accessible dashboard!

---

## 🌐 Web App

👉 **Try it live:** [https://leetcode-review-tracker.streamlit.app/](https://leetcode-review-tracker.streamlit.app/)

---

## 💬 Questions/Feedback

Find a bug or have a suggestion?  
[Open an issue on GitHub](https://github.com/Neha-28-fluff/leetcode-tracker/issues)  
or connect with me [on LinkedIn](https://www.linkedin.com/in/neha-biswas-b15636322)!

---

**Happy Trackin ^^!**
