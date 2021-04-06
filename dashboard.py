from quart import Quart
from discord.ext import ipc

app = Quart(__name__)
ipc_client = ipc.Client(
    secret_key="my_secret_key"
)

@app.route("/")
async def index():
    member_count = await ipc_client.request(
        "get_member_count", guild_id=791160100567384094
    )

    return str(member_count)

if __name__ == "__main__":
    app.run()