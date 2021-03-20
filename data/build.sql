CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer default 0,
    Stars integer default 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
)

