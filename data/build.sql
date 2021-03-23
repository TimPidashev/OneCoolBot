CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer default 0,
    Stars integer default 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items(
    ItemId bigserial NOT NULL,
    ItemName text NULL,
    ItemDescription text NULL, 
    ItemRarity int2 NULL,
    Emoji text NULL,
    CONSTRAINT "items-primarykey" PRIMARY KEY (ItemId)
);

CREATE TABLE IF NOT EXISTS inventory(
    UserID int8 NOT NULL,  
    ItemId int8 NOT NULL,
    CONSTRAINT useritems_unique UNIQUE (UserID),
    CONSTRAINT useritems_fk FOREIGN KEY (ItemID) REFERENCES items(itemid)
)