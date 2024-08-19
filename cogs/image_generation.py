import asyncio
import io
import re
import uuid

import discord
import webuiapi
from discord.ext import commands

SD_WEBUI_IP = "192.168.178.33"
SD_WEBUI_PORT = 7860
api = webuiapi.WebUIApi(host=SD_WEBUI_IP, port=SD_WEBUI_PORT)
# TODO: check if server is even online and move code somewhere else


class ImageGeneration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def extract_dimensions(self, resolution_str):
        # Use a regular expression to find numbers around "x"
        match = re.search(r"(\d+)\s*x\s*(\d+)", resolution_str)
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return [width, height]
        else:
            raise ValueError("Invalid resolution format")

    async def get_resolutions(self, ctx: discord.AutocompleteContext):
        orientation = ctx.options["orientation"]
        # width x height
        if orientation == "Landscape":
            return ["1152 x 896 (9:7)", "1216 x 832 (19:13)", "1344 x 768 (7:4)", "1536 x 640 (12:5)"]
        elif orientation == "Portrait":
            return ["896 x 1152 (7:9)", "832 x 1216 (13:19)", "768 x 1344 (4:7)", "640 x 1536 (5:12)"]
        else:
            return ["1024 x 1024 (1:1)"]

    async def txt2img_gen(self, prompt, neg_prompt, resolution):
        result = await api.txt2img(
            prompt=f"score_9, score_8_up, score_7_up, score_6_up, source_anime, {prompt}",
            negative_prompt=f"score_4_up, score_5_up, rating_explicit, ugly, out of frame, bad anatomy, child, loli, nsfw, nude, {neg_prompt}",
            width=resolution[0],
            height=resolution[1],
            seed=-1,
            cfg_scale=8,
            sampler_index="Euler",
            scheduler="SGM Uniform",
            steps=22,
            use_async=True,
        )
        return result

    @discord.slash_command(
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        name="genimg",
        description="Generate an image",
    )
    @discord.option(name="neg_prompt", type=str, required=False)
    @discord.option(
        "orientation",
        type=str,
        choices=["Portrait", "Landscape"],
        description="Ignore for square (1:1)",
        required=False,
    )
    @discord.option(
        "dimensions",
        description="Width x Height (to choose square, leave orientation empty)",
        type=str,
        autocomplete=discord.utils.basic_autocomplete(get_resolutions),
        required=False,
    )
    async def generate_image(
        self, ctx: discord.ApplicationContext, prompt: str, neg_prompt: str, orientation: str, dimensions: str
    ):
        await ctx.respond("Generating...")

        if dimensions == None:
            dimensions = "1024 x 1024 (1:1)"

        resolution = self.extract_dimensions(dimensions)
        generation = asyncio.create_task(self.txt2img_gen(prompt, neg_prompt, resolution))

        while not generation.done():
            progress = api.get_progress()
            if (progress["progress"] * 100) < 90:
                await ctx.interaction.edit_original_response(
                    content=f"Progress: {progress['progress'] * 100:.0f}% {progress['state']['sampling_step']}/{progress['state']['sampling_steps']}"
                )
                await asyncio.sleep(2.5)
            await asyncio.sleep(1)  # probably redundant lol

        gen_result = await generation
        image_buffer = io.BytesIO()
        gen_result.image.save(image_buffer, format="JPEG", quality=95)  # PIL image
        image_buffer.seek(0)  # go back to the start of the BytesIO object

        await ctx.interaction.edit_original_response(
            content=" ", file=discord.File(fp=image_buffer, filename=f"SeaSharkGen_{uuid.uuid4().hex}.jpg")
        )


def setup(bot):
    bot.add_cog(ImageGeneration(bot))
