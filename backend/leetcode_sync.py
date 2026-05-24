import requests
from database import add_problem, problem_exists, initialize_db

def get_recent_ac_submissions(username, limit=50):
    url = "https://leetcode.com/graphql/"
    query = '''
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
    '''
    variables = {"username": username, "limit": limit}
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        resp = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"Failed to fetch data from LeetCode! Status: {resp.status_code}")
            print("Raw response:", resp.text)
            return []
        data = resp.json()
        if "errors" in data:
            print("LeetCode API error:", data["errors"])
            return []
        return data["data"]["recentAcSubmissionList"]
    except Exception as e:
        print("Exception while contacting LeetCode API:", e)
        return []

def sync_user_problems(username, limit=50):
    problems = get_recent_ac_submissions(username, limit)
    if not problems:
        print("Nothing to sync (user not found or API error).")
        return
    print(f"Fetched {len(problems)} recent submissions for {username}.")

    added = 0
    for p in problems:
        slug = p['titleSlug']
        if not problem_exists(slug):
            did_add = add_problem(
                title=p['title'],
                slug=slug,
                problem_id=p['id'],
                timestamp=p.get('timestamp', None),
                notes="",
                confidence=0
            )
            if did_add:
                print(f"Added: {p['id']} {p['title']}")
                added += 1
    print(f"Sync complete: {added} new problems added.")

if __name__ == "__main__":
    initialize_db()  # Create table if doesn't exist
    username = input("Enter LeetCode username: ").strip()
    limit = 20
    sync_user_problems(username, limit)