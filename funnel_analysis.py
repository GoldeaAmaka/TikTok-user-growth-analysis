# Funnel Analysis for TikTok-style App
# Steps:
# 1. Signup
# 2. View
# 3. Like
# 4. Comment
# 5. Share
#
# Goal:
# - Count unique users at each step (SEQUENTIAL funnel)
# - Calculate conversion rates between steps
# - Identify biggest drop-off points

import sqlite3
import os


def get_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "users_events.db")
    return sqlite3.connect(DB_PATH)


def run_funnel_analysis():
    conn = get_connection()
    cur = conn.cursor()

    # Step 1: Signup (all users)
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM users;")
    signup = cur.fetchone()[0]

    # Step 2: View
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM events
        WHERE event_type = 'view';
    """)
    viewed = cur.fetchone()[0]

    # Step 3: Like (must have viewed)
    cur.execute("""
        SELECT COUNT(DISTINCT e.user_id)
        FROM events e
        WHERE e.event_type = 'like'
          AND e.user_id IN (
              SELECT DISTINCT user_id
              FROM events
              WHERE event_type = 'view'
          );
    """)
    liked = cur.fetchone()[0]

    # Step 4: Comment (must have liked)
    cur.execute("""
        SELECT COUNT(DISTINCT e.user_id)
        FROM events e
        WHERE e.event_type = 'comment'
          AND e.user_id IN (
              SELECT DISTINCT user_id
              FROM events
              WHERE event_type = 'like'
          );
    """)
    commented = cur.fetchone()[0]

    # Step 5: Share (must have commented)
    cur.execute("""
        SELECT COUNT(DISTINCT e.user_id)
        FROM events e
        WHERE e.event_type = 'share'
          AND e.user_id IN (
              SELECT DISTINCT user_id
              FROM events
              WHERE event_type = 'comment'
          );
    """)
    shared = cur.fetchone()[0]

    conn.close()

    return {
        "signup": signup,
        "view": viewed,
        "like": liked,
        "comment": commented,
        "share": shared
    }


def print_funnel_results(results):
    steps = list(results.keys())

    print("\n=== FUNNEL ANALYSIS ===")
    for i, step in enumerate(steps):
        count = results[step]
        if i == 0:
            print(f"{step.capitalize()}: {count}")
        else:
            prev_count = results[steps[i - 1]]
            conversion = (count / prev_count) * 100 if prev_count else 0
            print(f"{step.capitalize()}: {count} ({conversion:.1f}% from previous)")


if __name__ == "__main__":
    results = run_funnel_analysis()
    print_funnel_results(results)
