import discord
from discord.ext import commands


class TextChatGeneration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def gentxt(ctx: discord.ApplicationContext, prompt: str):
        await ctx.respond(f"Not implemented")
        # sd_gen.chat_session = sd_gen.KoboldCppChat(sd_gen.KOBOLDCPP_API_URL)
        # await ctx.interaction.edit_original_response(content=sd_gen.chat_session.chat(prompt))


def setup(bot):
    bot.add_cog(TextChatGeneration(bot))
