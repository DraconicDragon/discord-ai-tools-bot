import discord

# import sd_gen

# ctx.defer https://guide.pycord.dev/extensions/bridge#deferring


KOBOLDCPP_API_URL = "http://192.168.178.33:5001/api/v1/generate"

# TODO: cogs

bot = discord.Bot()


def load_cogs(is_reload=False):
    cogs_list = [
        "image_tagging",
        "image_generation",
        "text_chat_generation",
    ]
    if not is_reload:
        for cog in cogs_list:
            bot.load_extension(f"cogs.{cog}")
    else:
        for cog in cogs_list:
            bot.reload_extension(f"cogs.{cog}")


load_cogs()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.event
async def on_connect():
    if bot.auto_sync_commands:
        await bot.sync_commands()


@bot.slash_command(
    # This command can be used by guild members, but also by users anywhere if they install it as user
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
)
async def reload(ctx: discord.ApplicationContext):
    load_cogs(is_reload=True)
    await ctx.respond(f"Cogs Reloaded!")


bot.run("")
