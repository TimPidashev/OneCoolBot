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
  Stars integer default 0
);

CREATE TABLE IF NOT EXISTS items(
  ItemID integer NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  ItemName TEXT,
  ItemDescription TEXT
);

CREATE TABLE IF NOT EXISTS inventory(
  UserID integer NOT NULL,
  ItemID integer NOT NULL,
  Count integer NOT NULL DEFAULT 0 CHECK(count>=0),
  FOREIGN KEY("ItemID") REFERENCES "items"("ItemID") ON DELETE CASCADE
);

--add a market TABLE
