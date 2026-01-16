-- This file creates the database tables for the project

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  signup_date TEXT NOT NULL,
  acquisition_channel TEXT NOT NULL,
  device_type TEXT NOT NULL,
  country TEXT NOT NULL
);

CREATE TABLE events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  event_time TEXT NOT NULL,
  event_type TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
