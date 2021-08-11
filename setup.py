import ez_db as db

#setup db
db = db.DB(db_path="./data/database/database.db", build_path="./data/database/build.sql")

client_token = str(input("Paste your bot token and press enter: "))
statcord_token = str(input("Paste your statcord token and press enter: "))
owner_ids = str(input("Paste the discord ids of trusted people in your server with a comma in between each id: "))
server_id = str(input("Paste the discord id of your server: "))

try:
    db.execute("INSERT INTO botconfig (ClientToken, StatcordToken, OwnerIDS, ServerID) VALUES (?, ?, ?, ?)",
        client_token,
        statcord_token,
        owner_ids,
        server_id   
    )
    db.commit()

except Exception as error:
    print(error)
