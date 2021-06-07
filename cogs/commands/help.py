import discord
from discord.ext import commands
from utils import data, embed, log
import asyncio

EXCLUDED_COMMANDS = ['help']

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def on_ready(self):
        pass

    @commands.command(aliases=["hlp", "h"])
    async def help(self, context, arg=None):
        await log.cog_command(self, context)
        if arg is None:
            async with context.typing():
                await asyncio.sleep(1)
                message = await context.reply(embed=await embed.help_page_1(context), mention_author=False)
                await message.add_reaction("◀️")
                await message.add_reaction("▶️")
                await message.add_reaction("❌")
                pages = 6
                current_page = 1

                def check(reaction, user):
                    return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

                while True:
                    try:
                        reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                        if str(reaction.emoji) == "▶️" and current_page != pages:
                            current_page += 1

                            if current_page == 2:
                                await message.edit(embed=await embed.help_page_2(context))
                                await message.remove_reaction(reaction, user)
                            
                            elif current_page == 3:
                                await message.edit(embed=await embed.help_page_3(context))
                                await message.remove_reaction(reaction, user)

                            elif current_page == 4:
                                await message.edit(embed=await embed.help_page_4(context))
                                await message.remove_reaction(reaction, user)

                            elif current_page == 5:
                                await message.edit(embed=await embed.help_page_5(context))
                                await message.remove_reaction(reaction, user)

                            elif current_page == 6:
                                await message.edit(embed=await embed.help_page_6(context))
                                await message.remove_reaction(reaction, user)
                        
                        if str(reaction.emoji) == "◀️" and current_page > 1:
                            current_page -= 1
                            
                            if current_page == 1:
                                await message.edit(embed=await embed.help_page_1(context))
                                await message.remove_reaction(reaction, user)

                            elif current_page == 2:
                                await message.edit(embed=await embed.help_page_2(context))
                                await message.remove_reaction(reaction, user)
                            
                            elif current_page == 3:
                                await message.edit(embed=await embed.help_page_3(context))
                                await message.remove_reaction(reaction, user)

                            elif current_page == 4:
                                await message.edit(embed=await embed.help_page_4(context))
                                await message.remove_reaction(reaction, user)

                            elif current_page == 5:
                                await message.edit(embed=await embed.   help_page_5(context))
                                await message.remove_reaction(reaction, user)

                        if str(reaction.emoji) == "❌":
                            await message.delete()
                            await context.message.delete()
                            break

                        else:
                            await message.remove_reaction(reaction, user)
                            
                    except asyncio.TimeoutError:
                        await message.delete()
                        await context.message.delete()
                        break
            
        elif arg is not None:
            if arg == "aliases" or arg == "alias" or arg == "als" or arg == "a":
                await log.client_command(context)
                await context.reply("**help** aliases: `hlp` `h`", mention_author=False)

            else:
                return


    
def setup(client):
    client.add_cog(help(client))