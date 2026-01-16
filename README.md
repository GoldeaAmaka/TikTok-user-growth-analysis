# TikTok User Growth & Retention Analysis

## Project Overview
This project analyses user growth, engagement, and retention for a TikTok-style short-video application. 
The goal is to understand how users move through the product funnel, identify drop-off points, and evaluate the quality of different acquisition channels.

## Key Questions Answered
- How many users progress from signup to meaningful engagement?
- Where do the biggest funnel drop-offs occur?
- Do engaged users retain better over time?
- Which acquisition channels drive higher-quality users?

## Dataset
Synthetic user and event data generated using Python and stored in SQLite.

**Users Table**
- user_id
- signup_date
- acquisition_channel
- device_type
- country

**Events Table**
- event_id
- user_id
- event_type (view, like, comment, share)
- event_time

## Analysis Performed
- Funnel analysis (Signup → View → Like → Comment → Share)
- Day 1 & Day 7 retention analysis
- Engagement vs retention comparison
- Acquisition channel performance analysis
- Data visualisation using Matplotlib

## Tools & Technologies
- Python
- SQLite
- SQL
- Matplotlib
- PyCharm

## Key Insights
- Engagement strongly predicts retention
- Significant drop-off occurs between viewing and liking
- Some acquisition channels deliver fewer users but higher engagement quality

## Why This Matters
These insights can be used by product and growth teams to:
- Improve content recommendation strategies
- Optimise acquisition spend
- Increase long-term user retention

