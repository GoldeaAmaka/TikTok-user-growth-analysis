import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "users_events.db"
NUM_USERS = 1000

ACQUISITION_CHANNELS = ["organic", "ads", "influencer"]
DEVICE_TYPES = ["Android", "iOS"]
COUNTRIES = ["UK", "US", "India", "Nigeria"]

EVENT_TYPES = ["signup", "view", "like", "comment", "share", "drop_off"]

# --- Helper functions ---

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """Return a random datetime between start_date and end_date."""
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def weighted_choice(choices_with_weights):
    """
    choices_with_weights example: [("organic", 0.5), ("ads", 0.3), ("influencer", 0.2)]
    Returns one item based on weights.
    """
    items = [x[0] for x in choices_with_weights]
    weights = [x[1] for x in choices_with_weights]
    return random.choices(items, weights=weights, k=1)[0]

def engagement_probability(acquisition_channel: str) -> float:
    """Engagement rate varies by how users joined (realistic assumption)."""
    if acquisition_channel == "influencer":
        return 0.45
    if acquisition_channel == "organic":
        return 0.35
    return 0.22  # ads

def retention_probabilities(is_engaged: bool) -> tuple[float, float]:
    """
    Return (day1_prob, day7_prob).
    Engaged users retain more.
    """
    if is_engaged:
        return (0.55, 0.30)
    return (0.25, 0.10)

def add_event(cur, user_id: int, event_time: datetime, event_type: str):
    cur.execute(
        """
        INSERT INTO events (user_id, event_time, event_type)
        VALUES (?, ?, ?)
        """,
        (user_id, event_time.isoformat(timespec="seconds"), event_type),
    )

# --- Main generation logic ---

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Optional: clear old data so re-running doesn't duplicate
    cur.execute("DELETE FROM events;")
    cur.execute("DELETE FROM users;")
    conn.commit()

    # Define signup window (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    for user_id in range(1, NUM_USERS + 1):
        signup_dt = random_date(start_date, end_date)
        acquisition_channel = weighted_choice([
            ("organic", 0.50),
            ("ads", 0.30),
            ("influencer", 0.20),
        ])
        device_type = random.choice(DEVICE_TYPES)
        country = random.choice(COUNTRIES)

        # Insert user
        cur.execute(
            """
            INSERT INTO users (user_id, signup_date, acquisition_channel, device_type, country)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                signup_dt.date().isoformat(),
                acquisition_channel,
                device_type,
                country,
            ),
        )

        # Every user signs up (also logged as an event)
        add_event(cur, user_id, signup_dt, "signup")

        # Views: most users view multiple times on signup day
        num_views = random.randint(1, 12)
        for _ in range(num_views):
            view_time = signup_dt + timedelta(minutes=random.randint(1, 600))
            add_event(cur, user_id, view_time, "view")

        # Engagement: like/comment/share based on acquisition channel
        engaged = random.random() < engagement_probability(acquisition_channel)

        if engaged:
            # Decide how many engagement actions
            engagement_actions = []
            # At least 1 engagement action
            engagement_actions.append(random.choice(["like", "comment", "share"]))

            # Maybe add more engagement actions
            if random.random() < 0.60:
                engagement_actions.append(random.choice(["like", "comment", "share"]))
            if random.random() < 0.35:
                engagement_actions.append(random.choice(["like", "comment", "share"]))

            for action in engagement_actions:
                action_time = signup_dt + timedelta(minutes=random.randint(5, 720))
                add_event(cur, user_id, action_time, action)

        # Retention: Day 1 and Day 7
        day1_prob, day7_prob = retention_probabilities(engaged)

        # Day 1 return
        if random.random() < day1_prob:
            d1_time = signup_dt + timedelta(days=1, minutes=random.randint(10, 600))
            # returning can include views (and sometimes engagement)
            add_event(cur, user_id, d1_time, "view")
            if engaged and random.random() < 0.25:
                add_event(cur, user_id, d1_time + timedelta(minutes=5), random.choice(["like", "comment", "share"]))

        # Day 7 return
        if random.random() < day7_prob:
            d7_time = signup_dt + timedelta(days=7, minutes=random.randint(10, 600))
            add_event(cur, user_id, d7_time, "view")
            if engaged and random.random() < 0.20:
                add_event(cur, user_id, d7_time + timedelta(minutes=5), random.choice(["like", "comment", "share"]))

        # Drop off event (optional marker)
        # We'll add drop_off for a portion of users who do NOT return on day 7
        if random.random() < 0.60 and random.random() > day7_prob:
            drop_time = signup_dt + timedelta(days=random.randint(2, 10), minutes=random.randint(10, 600))
            add_event(cur, user_id, drop_time, "drop_off")

    conn.commit()
    conn.close()
    print(f"✅ Generated {NUM_USERS} users and inserted events into {DB_NAME}.")

if __name__ == "__main__":
    main()
