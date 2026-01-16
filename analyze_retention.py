import sqlite3

DB_NAME = "users_events.db"

ENGAGEMENT_EVENTS = ("like", "comment", "share")

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 1) Total users
    cur.execute("SELECT COUNT(*) FROM users;")
    total_users = cur.fetchone()[0]

    # 2) Engaged users (any like/comment/share at any time)
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM events
        WHERE event_type IN ('like', 'comment', 'share');
    """)
    engaged_users = cur.fetchone()[0]
    not_engaged_users = total_users - engaged_users

    print("\n==== BASIC COUNTS ====")
    print(f"Total users: {total_users}")
    print(f"Engaged users (like/comment/share): {engaged_users}")
    print(f"Not engaged users: {not_engaged_users}")

    # 3) Day 1 retention: user has ANY event exactly 1 day after signup_date
    # We use users.signup_date (date) and compare to date(events.event_time)
    cur.execute("""
        WITH user_return_day1 AS (
            SELECT u.user_id
            FROM users u
            JOIN events e ON e.user_id = u.user_id
            WHERE date(e.event_time) = date(u.signup_date, '+1 day')
            GROUP BY u.user_id
        ),
        engaged AS (
            SELECT DISTINCT user_id
            FROM events
            WHERE event_type IN ('like','comment','share')
        )
        SELECT
            (SELECT COUNT(*) FROM user_return_day1) AS day1_returners,
            (SELECT COUNT(*) FROM user_return_day1 WHERE user_id IN (SELECT user_id FROM engaged)) AS day1_engaged_returners,
            (SELECT COUNT(*) FROM user_return_day1 WHERE user_id NOT IN (SELECT user_id FROM engaged)) AS day1_not_engaged_returners;
    """)
    day1_returners, day1_engaged_returners, day1_not_engaged_returners = cur.fetchone()

    # 4) Day 7 retention
    cur.execute("""
        WITH user_return_day7 AS (
            SELECT u.user_id
            FROM users u
            JOIN events e ON e.user_id = u.user_id
            WHERE date(e.event_time) = date(u.signup_date, '+7 day')
            GROUP BY u.user_id
        ),
        engaged AS (
            SELECT DISTINCT user_id
            FROM events
            WHERE event_type IN ('like','comment','share')
        )
        SELECT
            (SELECT COUNT(*) FROM user_return_day7) AS day7_returners,
            (SELECT COUNT(*) FROM user_return_day7 WHERE user_id IN (SELECT user_id FROM engaged)) AS day7_engaged_returners,
            (SELECT COUNT(*) FROM user_return_day7 WHERE user_id NOT IN (SELECT user_id FROM engaged)) AS day7_not_engaged_returners;
    """)
    day7_returners, day7_engaged_returners, day7_not_engaged_returners = cur.fetchone()

    conn.close()

    # Helper for safe rate calculation
    def rate(part, whole):
        return (part / whole * 100) if whole else 0

    print("\n==== DAY 1 RETENTION ====")
    print(f"Day 1 returners: {day1_returners} ({rate(day1_returners, total_users):.1f}%)")
    print(f" - Engaged returners: {day1_engaged_returners} ({rate(day1_engaged_returners, engaged_users):.1f}% of engaged)")
    print(f" - Not engaged returners: {day1_not_engaged_returners} ({rate(day1_not_engaged_returners, not_engaged_users):.1f}% of not engaged)")

    print("\n==== DAY 7 RETENTION ====")
    print(f"Day 7 returners: {day7_returners} ({rate(day7_returners, total_users):.1f}%)")
    print(f" - Engaged returners: {day7_engaged_returners} ({rate(day7_engaged_returners, engaged_users):.1f}% of engaged)")
    print(f" - Not engaged returners: {day7_not_engaged_returners} ({rate(day7_not_engaged_returners, not_engaged_users):.1f}% of not engaged)")


if __name__ == "__main__":
    main()
