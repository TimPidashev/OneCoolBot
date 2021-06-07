import discord
from discord.ext import commands
from db import db
from io import BytesIO
from typing import Optional
from discord import Member, Embed
from PIL import Image, ImageDraw, ImageFont
from utils import data, log
import asyncio
import aiohttp

db.connect("./data/database.db")

class rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass


    @commands.command(aliases=["rnk"])
    async def rank(self, context, target: Optional[Member]):
        await log.cog_command(self, context)
        target = target or context.author
        if target is not None:
            exp, level = db.record(f"SELECT XP, Level FROM users WHERE (guildID, UserID) = (?, ?)",
                target.guild.id,
                target.id
            )
            ids = db.column(f"SELECT UserID FROM users WHERE GuildID = {target.guild.id} ORDER BY XP DESC")
            message_count = db.record(f"SELECT GlobalMessageCount FROM users WHERE UserID = {context.author.id} and GuildID = {context.guild.id}")[0]

        if exp or level is not None:
            async with context.typing():
                await asyncio.sleep(1)

                rank = f"{ids.index(target.id)+1}"
                xp = exp
                user_name = str(target.name)
                discriminator = f"#{target.discriminator}"

                final_xp_calc = int((level + 1) ** (20 / 11) * 42)
                final_xp = final_xp_calc + xp  

                background = Image.new("RGB", (1000, 240))
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(target.avatar_url)) as response:
                        image = await response.read()
                        icon = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
                        bigsize = (icon.size[0] * 3, icon.size[1] * 3)
                        mask = Image.new("L", bigsize, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + bigsize, 255)
                        mask = mask.resize(icon.size, Image.ANTIALIAS)
                        icon.putalpha(mask)
                        background.paste(icon, (20, 20), mask=icon)
                        draw = ImageDraw.Draw(background, "RGB")
                        big_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 60, encoding="utf-8")
                        medium_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 40, encoding="utf-8")
                        small_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 30, encoding="utf-8")

                        text_size = draw.textsize(str(level), font=big_font)
                        offset_x = 1000 - 15 - text_size[0]
                        offset_y = 10
                        draw.text((offset_x, offset_y), str(level), font=big_font, fill="#9B59B6")
                        text_size = draw.textsize("LEVEL", font=small_font)
                        offset_x -= text_size[0] + 5
                        draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#fff")

                        text_size = draw.textsize(f"#{rank}", font=big_font)
                        offset_x -= text_size[0] + 15
                        draw.text((offset_x, offset_y), f"{rank}", font=big_font, fill="#9B59B6")
                        text_size = draw.textsize("RANK", font=small_font)
                        offset_x -= text_size[0] + 5
                        draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")
                        
                        text_size = draw.textsize(f"{message_count}", font=big_font)
                        offset_x -= text_size[0] + 50
                        draw.text((offset_x, offset_y), f"{message_count}", font=big_font, fill="#9B59B6")
                        text_size = draw.textsize("KARMA", font=small_font)
                        offset_x -= text_size[0] + 10
                        draw.text((offset_x, offset_y + 27), "KARMA", font=small_font, fill="#fff")

                        bar_offset_x = 320
                        bar_offset_y = 160
                        bar_offset_x_1 = 950
                        bar_offset_y_1 = 200
                        circle_size = bar_offset_y_1 - bar_offset_y
                        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")
                        draw.ellipse(
                            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#9B59B6"
                        )
                        draw.ellipse(
                            (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
                        )
                        bar_length = bar_offset_x_1 - bar_offset_x
                        progress = (final_xp - xp) * 100 / final_xp
                        progress = 100 - progress
                        progress_bar_length = round(bar_length * progress / 100)
                        bar_offset_x_1 = bar_offset_x + progress_bar_length
                        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#9B59B6")
                        draw.ellipse(
                            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#9B59B6"
                        )
                        draw.ellipse(
                            (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#9B59B6"
                        )
                        text_size = draw.textsize(f"/ {final_xp} XP", font=small_font)
                        offset_x = 950 - text_size[0]
                        offset_y = bar_offset_y - text_size[1] - 10
                        draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")
                        text_size = draw.textsize(f"{xp:,}", font=small_font)
                        offset_x -= text_size[0] + 8
                        draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")
                        text_size = draw.textsize(user_name, font=medium_font)
                        offset_x = bar_offset_x
                        offset_y = bar_offset_y - text_size[1] - 5
                        draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")
                        offset_x += text_size[0] + 5
                        offset_y += 10
                        draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
                        background.show()

                        background.save("./data/img/imgswap.png")
                        ffile = discord.File("./data/img/imgswap.png")
                        await context.reply(file=ffile, mention_author=False)

        else:
            await context.reply("You are not in the database :(\nDon't worry though, you were just added! Try running the command again.", mention_author=False)


def setup(client):
    client.add_cog(rank(client))