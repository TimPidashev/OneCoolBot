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
    LevelChannel integer,
    PRIMARY KEY("GuildID", "LevelRoleID")
);

CREATE TABLE IF NOT EXISTS usersettings(
    UserID integer PRIMARY KEY,
    ColorTheme text DEFAULT "0x71368a",
    RankBackground text DEFAULT "None"
);

CREATE TABLE IF NOT EXISTS userinventory(
    UserID integer PRIMARY KEY,
    ItemID VARCHAR(50) NOT NULL,
    DateBought DEFAULT CURRENT_DATE,
    Quantity VARCHAR(50) NOT NULL,
    AverageValue VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets(
    TicketID integer PRIMARY KEY AUTOINCREMENT,
    UserID integer NOT NULL,
    ProjectName VARCHAR(50) NOT NULL,
    ProjectDescription text NOT NULL,
    DateOpened DEFAULT CURRENT_DATE,
    DateClosed DEFAULT CURRENT_DATE,
    AdminVotes integer DEFAULT 0,
    Status VARCHAR(50) DEFAULT "Open"
);

CREATE TABLE IF NOT EXISTS globalmarket(
    ItemID integer PRIMARY KEY AUTOINCREMENT,
    ItemName VARCHAR(50) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    DateReleased DEFAULT CURRENT_DATE,
    QuantityAvailable Varchar(50) NOT NULL,
    QuantityLimit VARCHAR(50) NOT NULL,
    Price int NOT NULL,
    Popularity integer DEFAULT 0,
    WhoBoughtLast TEXT DEFAULT "Nobody"
);

CREATE TABLE IF NOT EXISTS botconfig(
    ClientToken VARCHAR(100) NOT NULL,
    StatcordToken VARCHAR(50) NOT NULL,
    OwnerIDS TEXT DEFAULT "0",
    ServerID TEXT DEFAULT "0"
);

CREATE TABLE IF NOT EXISTS commands(
    Name VARCHAR(20) NOT NULL,
    Status TEXT DEFAULT "OFF"
);

CREATE TABLE IF NOT EXISTS modules(
    Name VARCHAR(20) NOT NULL,
    Status TEXT DEFAULT "OFF"
)

-- CREATE TABLE IF NOT EXISTS usershop(
--     UserID integer PRIMARY KEY,
--     ShopName VARCHAR(50) NOT NULL,
--     DateOpened DEFAULT CURRENT_DATE
-- );

-- CREATE TABLE IF NOT EXISTS usershopinventory(
--     UserID integer PRIMARY KEY
--     ItemID VARCHAR(50) NOT NULL,
--     Quantity VARCHAR(50) NOT NULL,
--     DatePosted DEFAULT CURRENT_DATE
-- );
