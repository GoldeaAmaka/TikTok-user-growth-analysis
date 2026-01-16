import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users_events.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def acquisition_summary():
    conn = get_connection()
    cur = conn.cursor()

    print("\n=== USER ACQUISITION SUMMARY ===")

    cur.execute("""
        SELECT acquisition_channel, COUNT(*) 
        FROM users
        GROUP BY acquisition_channel
        ORDER BY COUNT(*) DESC;
    """)

    rows = cur.fetchall()
    for channel, count in rows:
        print(f"{channel}: {count} users")

    conn.close()


def acquisition_engagement():
    conn = get_connection()
    cur = conn.cursor()

    print("\n=== ENGAGEMENT BY ACQUISITION CHANNEL ===")

    cur.execute("""
        SELECT 
            u.acquisition_channel,
            COUNT(DISTINCT u.user_id) AS total_users,
            COUNT(DISTINCT e.user_id) AS engaged_users
        FROM users u
        LEFT JOIN events e
            ON u.user_id = e.user_id
           AND e.event_type IN ('like', 'comment', 'share')
        GROUP BY u.acquisition_channel;
    """)

    rows = cur.fetchall()
    for channel, total, engaged in rows:
        rate = (engaged / total) * 100 if total else 0
        print(f"{channel}: {engaged}/{total} engaged ({rate:.1f}%)")

    conn.close()


if __name__ == "__main__":
    acquisition_summary()
    acquisition_engagement()
