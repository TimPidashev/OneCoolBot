CREATE TABLE IF NOT EXISTS users(
    GuildID integer,
    UserID integer,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer DEFAULT 0,
    Stars integer DEFAULT 0,
    GlobalMessageCount integer DEFAULT 0,
    MessagesPerWeek text DEFAULT CURRENT_DATE,
    XPLock text DEFAULT CURRENT_TIMESTAMP,
    AILock text DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("GuildID", "UserID")
);

CREATE TABLE IF NOT EXISTS guildsettings(
    GuildID integer,
    RoleLevel integer,
    LevelRoleID integer,
    LevelCoins integer,
    PRIMARY KEY("GuildID", "LevelRoleID")
);

CREATE TABLE IF NOT EXISTS usersettings(
    UserID integer PRIMARY KEY,
    ColorTheme text DEFAULT "0x71368a",
    RankBackground text DEFAULT "None"
);

CREATE TABLE IF NOT EXISTS userinventory(
    UserID integer,
    ItemID VARCHAR(50) NOT NULL,
    DateBought date NOT NULL,
    Quantity VARCHAR(50) NOT NULL,
    AverageValue VARCHAR(50) NOT NULL

);

CREATE TABLE IF NOT EXISTS globalmarket(
    ItemID integer PRIMARY KEY AUTOINCREMENT,
    ItemName VARCHAR(50) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    DateReleased DEFAULT CURRENT_DATE,
    QuantityLimit VARCHAR(50) NOT NULL,
    QuantityAvailable Varchar(50) NOT NULL,
    Price int NOT NULL,
    WhoBoughtLast TEXT DEFAULT "Nobody"
)

