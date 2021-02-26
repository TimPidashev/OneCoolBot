CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer default 0,
    Stars integer default 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS starboard(
  UserID integer PRIMARY KEY,
  Stars integer default 0,
)

--
-- CREATE TABLE IF NOT EXISTS invites(
-- 	UserID integer PRIMARY KEY,
-- 	Invites integer DEFAULT 0
-- )
