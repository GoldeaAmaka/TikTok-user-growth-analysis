import sqlite3
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users_events.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def plot_users_by_channel():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT acquisition_channel, COUNT(*) 
        FROM users
        GROUP BY acquisition_channel;
    """)
    data = cur.fetchall()
    conn.close()

    channels = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure()
    plt.bar(channels, counts)
    plt.title("Users by Acquisition Channel")
    plt.xlabel("Acquisition Channel")
    plt.ylabel("Number of Users")
    plt.tight_layout()
    plt.show()


def plot_engagement_rate_by_channel():
    conn = get_connection()
    cur = conn.cursor()

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
    data = cur.fetchall()
    conn.close()

    channels = []
    engagement_rates = []

    for channel, total, engaged in data:
        rate = (engaged / total) * 100 if total else 0
        channels.append(channel)
        engagement_rates.append(rate)

    plt.figure()
    plt.bar(channels, engagement_rates)
    plt.title("Engagement Rate by Acquisition Channel")
    plt.xlabel("Acquisition Channel")
    plt.ylabel("Engagement Rate (%)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_users_by_channel()
    plot_engagement_rate_by_channel()
