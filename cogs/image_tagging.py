import io

import discord
from discord.ext import commands
from PIL import Image

import wd_tagger


class ImageTagging(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    async def tag_image_logic(self, ctx: discord.ApplicationContext, attachment: discord.Attachment):
        await ctx.respond("Processing image... ETA: ±10 seconds")
        char_prob, gen_prob = "", ""

        image_bytes = await attachment.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        general_res, character_res = wd_tagger.predictsimple(image)

        for tag, prob in character_res:
            char_prob += f"{tag}\n"
        for tag, prob in general_res:
            gen_prob += f"{tag}, "
        gen_prob = gen_prob.rstrip(", ")

        if len(gen_prob) > 3950:
            gen_prob = gen_prob[:3950]
        if char_prob == "":
            char_prob = "None"

        # python doesnt like backslashes in f strings, cringe
        escaped_char_prob = char_prob.replace("_", "\\_")
        escaped_gen_prob = gen_prob.replace("_", "\\_")

        # Use the preprocessed strings in the f-string
        await ctx.interaction.edit_original_response(
            content=f"**Character (Probability > 80%):** `{escaped_char_prob}`"
            + f"**General (Probability > 30%):** \n`{escaped_gen_prob}`",
            # file=discord.File(fp=io.BytesIO(image_bytes), filename=f"{attachment.filename}"),
        )

    # Tag Image message command (context menu)
    @discord.message_command(
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        name="Tag First Image",
    )
    async def tag_image_user_command(self, ctx: discord.ApplicationContext, msg: discord.Message):
        if msg.attachments:
            await self.tag_image_logic(ctx, msg.attachments[0])
        else:
            await ctx.respond("No image found in the selected message.")

    # Tag Image Slash command
    @discord.slash_command(
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        name="tag_image",
        description="Tag an image using WaifuDiffusion taggers",
    )
    async def tag_image(self, ctx: discord.ApplicationContext, attachment: discord.Attachment):
        await self.tag_image_logic(ctx, attachment)


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(ImageTagging(bot))  # add the cog to the bot
