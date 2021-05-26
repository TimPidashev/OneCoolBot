CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "."
);

CREATE TABLE IF NOT EXISTS guildconfig(
    GuildID integer PRIMARY KEY,
    Levels text DEFAULT "OFF",
    LevelMessages text DEFAULT "OFF",
    LevelMessage text DEFAULT "This is a level message!",
    LevelMessageChannel integer DEFAULT 0,
    UpdateMessage text DEFAULT "NONE",
    Economy text DEFAULT "OFF",
    Games text Default "OFF",
    Music text DEFAULT "OFF",
    BotAI text DEFAULT "OFF",
    ErrorMessages text DEFAULT "On"
);

CREATE TABLE IF NOT EXISTS users(
    GuildID integer,
    UserID integer,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer default 0,
    Stars integer default 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP,
    AILock text DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("GuildID", "UserID")
)
