CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "."
);

CREATE TABLE IF NOT EXISTS guildconfig(
    GuildID integer PRIMARY KEY,
    ErrorMessages text DEFAULT "YES",
    Levels text DEFAULT "NO",
    Moderation text DEFAULT "NO",
    Music text DEFAULT "NO",
    AI text DEFAULT "NO",
    Memes text DEFAULT "NO"
);

CREATE TABLE IF NOT EXISTS users(
    GuildID integer,
    UserID integer,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer default 0,
    Stars integer default 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("GuildID", "UserID")
)
