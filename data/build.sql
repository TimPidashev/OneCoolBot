CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
)

--CREATE TABLE IF NOT EXISTS votes(
	--UserID integer PRIMARY KEY,
	--HAVEVOTED text DEFAULT "no",
	--VoteLock text DEFAULT CURRENT_TIMESTAMP
--)
