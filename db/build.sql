CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "."
);

CREATE TABLE IF NOT EXISTS guildconfig(
    GuildID integer PRIMARY KEY,
    Levels text DEFAULT "off",
    LevelMessageCheck text DEFAULT "off",
    LevelMessage text DEFAULT "This is a level message!",
    LevelMessageChannel integer DEFAULT 0,
    LevelMessageChannelDirect text DEFAULT "off"
);

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
)