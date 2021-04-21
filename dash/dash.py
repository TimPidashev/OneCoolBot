from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import discord
import os

app = Quart(__name__)
ipc_client = ipc.Client(
    secret_key="OneCoolDash"
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["SECRET_KEY"] = "OneCoolDash"
app.config["DISCORD_CLIENT_ID"] = 790701838164557854 
app.config["DISCORD_CLIENT_SECRET"] = "ZrZCb1oWUsfExfD7_I1QN00e0Kx1rgc2"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:500/login"

dash = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	logged = ""
	if await dash.authorized:
		logged = True
	return await render_template("index.html", logged=logged)

@app.route("/generic")
async def generic():
	return await render_template("generic.html")

@app.route("/elements")
async def elements():
	return await render_template("elements.html")

@app.route("/login/")
async def login():
	return await dash.create_session()

@app.route("/me/")
@requires_authorization
async def me():
	user = await dash.fetch_user()
	return redirect(url_for("home"))

@app.route("/callback")
async def callback():
	await dash.callback()
	try:
		return redirect(bot.url)
	except:
		return redirect(url_for("me"))

@app.route("/dashboard")
async def dashboard():
	guild_count = await ipc_client.request("get_guild_count")
	guild_ids = await ipc_client.request("get_guild_ids")

	try:
		user_guilds = await dash.fetch_guilds()
	except:
		return redirect(url_for("login")) 

	same_guilds = []

	for guild in user_guilds:
		if guild.id in guild_ids:
			same_guilds.append(guild)


	return await render_template("dashboard.html", guild_count = guild_count, matching = same_guilds)

@app.route('/logout')
async def logout():
	dash.revoke()
	return redirect(url_for("home"))

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
	bot.url = request.url
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug=True)