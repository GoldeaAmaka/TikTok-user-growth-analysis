# TikTok User Growth & Retention Analysis

## Project Overview
This project analyzes user growth, engagement, and retention for a TikTok-style short-video platform.  
The goal is to understand how users progress through the product funnel, identify key drop-off points, and evaluate the quality of different acquisition channels based on user engagement behaviour.

The project simulates real-world product analytics work commonly performed by growth and data teams.

---

## Key Questions
- How do users move from signup to meaningful engagement?
- Where are the largest funnel drop-offs?
- Does engagement predict short-term and medium-term retention?
- Which acquisition channels bring higher-quality users?

---

## Dataset
Synthetic user and event-level data generated using Python and stored in SQLite.

### Users Table
- `user_id`
- `signup_date`
- `acquisition_channel` (organic, ads, influencer)
- `device_type`
- `country`

### Events Table
- `event_id`
- `user_id`
- `event_type` (view, like, comment, share)
- `event_time`

Engagement is defined as any **like, comment, or share** action.

Retention is measured using **Day 1** and **Day 7** return activity.

---

## Analysis Performed
- Sequential funnel analysis: Signup → View → Like → Comment → Share
- Engagement vs retention analysis (Day 1 & Day 7)
- Acquisition channel performance comparison (volume vs quality)
- Data visualisation for stakeholder interpretation

---

## Key Insights
- The largest drop-off occurs between passive viewing and active engagement, highlighting an opportunity to improve interaction prompts.
- Users who engage (like, comment, or share) show significantly higher Day 1 and Day 7 retention.
- Organic and influencer acquisition channels generate fewer users than ads but deliver higher engagement quality.
- Optimising solely for install volume can reduce long-term user value.

---

## Tools & Technologies
- Python
- SQL
- SQLite
- Matplotlib
- PyCharm

---

## Visual Outputs
Funnel and acquisition channel charts are included to support insight communication and stakeholder decision-making.


---

## Why This Project Matters
This project demonstrates practical product analytics skills, including funnel analysis, user segmentation, retention measurement, and data storytelling. The workflow reflects how data analysts support growth and product decisions in real organisations.
