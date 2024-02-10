import nextcord
from nextcord.ext import commands
from nextcord import Interaction
class basics(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx: Interaction, message: str):
        await ctx.response.send_message(message)

    #@commands.Cog.listener()