import sqlite3
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users_events.db")


def get_sequential_funnel_counts():
    """
    Sequential funnel:
    Signup -> View -> Like -> Comment -> Share
    Each step requires the previous step.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Signup
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM users;")
    signup = cur.fetchone()[0]

    # View
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM events
        WHERE event_type='view';
    """)
    view = cur.fetchone()[0]

    # Like must have viewed
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM events
        WHERE event_type='like'
          AND user_id IN (
              SELECT DISTINCT user_id FROM events WHERE event_type='view'
          );
    """)
    like = cur.fetchone()[0]

    # Comment must have liked
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM events
        WHERE event_type='comment'
          AND user_id IN (
              SELECT DISTINCT user_id FROM events WHERE event_type='like'
          );
    """)
    comment = cur.fetchone()[0]

    # Share must have commented
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM events
        WHERE event_type='share'
          AND user_id IN (
              SELECT DISTINCT user_id FROM events WHERE event_type='comment'
          );
    """)
    share = cur.fetchone()[0]

    conn.close()

    steps = ["Signup", "View", "Like", "Comment", "Share"]
    counts = [signup, view, like, comment, share]
    return steps, counts


def main():
    steps, counts = get_sequential_funnel_counts()

    # Print counts (so you can copy into README)
    print("\n=== FUNNEL COUNTS (SEQUENTIAL) ===")
    for s, c in zip(steps, counts):
        print(f"{s}: {c}")

    # Plot
    plt.figure()
    plt.bar(steps, counts)
    plt.title("User Funnel (Signup → View → Like → Comment → Share)")
    plt.xlabel("Funnel step")
    plt.ylabel("Unique users")
    plt.tight_layout()

    # Save PNG for portfolio
    out_path = os.path.join(BASE_DIR, "funnel_chart.png")
    plt.savefig(out_path, dpi=200)
    plt.show()

    print(f"\n✅ Saved chart to: {out_path}")


if __name__ == "__main__":
    main()
