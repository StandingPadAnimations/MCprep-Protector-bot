import discord
from discord.ext import commands
import json
import datetime
import re

MCPREP_GUILD_ID = 737871405349339232
IDLE_MINER_CHANNEL_ID = 746745594458144809
HELP_CHANNEL = 737872746700079235
STAFF_CHAT_ID = 741151005688987769

DISCORD_HTTPS = (
    "https://discord.com/",
    "https://cdn.discordapp.com/",
    "https://canary.discord.com/",
)


def findWholeWord(w):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search


class MyClient(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self.spam_text = []

        # intents
        intents = discord.Intents.default()
        discord.Bot.__init__(self, intents=intents)

        self.staff_chat = self.get_channel(STAFF_CHAT_ID)

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: discord.Message):
        message_content = message.content
        message_author = message.author
        if message_author.bot:
            return

        elif message.channel.id == IDLE_MINER_CHANNEL_ID:
            return

        helper_role = message.guild.get_role(748895907805790209)
        helpers = helper_role.members

        if (
            message.channel.id == HELP_CHANNEL
            and helper_role not in message.role_mentions
        ):
            for h in helpers:
                if h.mentioned_in(message):
                    await message.channel.send(
                        f"{message_author.mention}, please ping the Helpers role next time, not individual users"
                    )


client = MyClient()


@client.slash_command(name="mcprep_download", guilds=[MCPREP_GUILD_ID])
async def mcprep_download(ctx: commands.Context):
    await ctx.respond(
        "MCprep can be downloaded here: https://github.com/TheDuckCow/MCprep/releases"
    )


@client.slash_command(name="blender_download", guilds=[MCPREP_GUILD_ID])
async def blender_download(ctx: commands.Context):
    await ctx.respond("Blender can be downloaded here: https://www.blender.org/")


@client.slash_command(name="my_hardware_sucks", guilds=[MCPREP_GUILD_ID])
async def my_hardware_sucks(ctx: commands.Context):
    await ctx.respond(
        "Hardware does not matter when starting out, whoever said that to you was lying.\n\nAll you need to get into 3D rendering is a computer, Blender, some time, and imagination."
    )


@client.slash_command(name="older_versions", guilds=[MCPREP_GUILD_ID])
async def older_versions(ctx: commands.Context):
    await ctx.respond(
        "We don't support older versions of MCprep, especially ones with known bugs. You should download the latest version: https://github.com/TheDuckCow/MCprep/releases"
    )


@client.slash_command(name="asset_submission", guilds=[MCPREP_GUILD_ID])
async def asset_submission(ctx: commands.Context):
    await ctx.respond(
        "You can submit mob rigs here: https://github.com/TheDuckCow/MCprep/issues/new?assignees=&labels=enhancement&template=Asset-Submission.yaml"
    )


@client.slash_command(name="bug_report", guilds=[MCPREP_GUILD_ID])
async def bug_report(ctx: commands.Context):
    await ctx.respond(
        "Submit a bug report here: https://github.com/TheDuckCow/MCprep/issues/new?assignees=&labels=user-troubleshoot&template=Bug-Report.yml"
    )


@client.slash_command(name="feature_request", guilds=[MCPREP_GUILD_ID])
async def feature_request(ctx: commands.Context):
    await ctx.respond(
        "Submit a feature request here: https://github.com/TheDuckCow/MCprep/issues/new?assignees=&labels=enhancement&template=Feature-Request.yml"
    )


@client.slash_command(name="mojang_style", guilds=[MCPREP_GUILD_ID])
async def mojang_style(ctx: commands.Context):
    await ctx.respond(
        'The "Mojang Style" is also known as barebones. All you need is the barebones texturepack and practice.'
    )


@client.slash_command(name="why_is_standard_bad", guilds=[MCPREP_GUILD_ID])
async def why_is_standard_bad(ctx: commands.Context):
    images = None
    with open("assets/images.json") as f:
        data = json.load(f)
        images = data["why_not_to_use_standard"]

    RESPONSE_1 = f"Standard was designed a really long time ago, so it's really bad in terms of dynamic range. This makes areas blown out such as the rays of light in the bottom image:\n{images[0]}"
    RESPONSE_2 = f'You should use filmic instead, as it was designed with a higher dynamic range in mind. As you can see, the rays aren\'t blown out:\n {images[1]}\n\nOf course Filmic can look more washed out sometimes, but this can be fixed by setting the "Look" setting to "High Contrast"'
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2)


@client.slash_command(name="why_is_my_cycles_render_so_noisy", guilds=[MCPREP_GUILD_ID])
async def why_is_my_render_griany(ctx: commands.Context):
    images = None
    with open("assets/images.json") as f:
        data = json.load(f)
        images = data["cycles_noise"]

    RESPONSE_1 = f"Cycles is a path tracing engine, so it produces very accurate lighting. A side effect of this is noise. At low samples it looks really bad:\n{images[0]}"
    RESPONSE_2 = f"As the number of samples increase, the clearer the image becomes:\n{images[1]}"
    RESPONSE_3 = f"There is a tool called denoising which helps with this problem (as seen in the bottom image):\n{images[2]}"
    RESPONSE_4 = f"It can be enabled here. It's recommended to use OpenImage Denoise as it preserves detail better:\n{images[3]}"
    RESPONSE_5 = "Remember this piece of advice though: denoisers are not magic. With low sample counts artifacts can appear that look like oil paint smudges."
    await ctx.respond(RESPONSE_1)
    await ctx.respond(RESPONSE_2)
    await ctx.respond(RESPONSE_3)
    await ctx.respond(RESPONSE_4)
    await ctx.respond(RESPONSE_5)


@client.slash_command(name="how_to_make_rtx_like_render", guilds=[MCPREP_GUILD_ID])
async def how_to_make_rtx_like_render(ctx: commands.Context):
    images = None
    with open("assets/images.json") as f:
        data = json.load(f)
        images = data["rtx_like_render"]

    RESPONSE_1 = f"You mean stuff like this?: {images[0]}\n{images[1]}"
    await ctx.respond(RESPONSE_1)
    await ctx.respond(
        "Creating good-looking renders takes time and practice. While there's no magic button, there are plenty of tutorials available to help you learn. Don't be discouraged if the tutorials are for an older version of Blender or not related to Minecraft - the principles are still applicable. Keep practicing and don't give up. Remember, if you want to be good, you have to put in the work."
    )


@client.slash_command(name="cycles_vs_eevee", guilds=[MCPREP_GUILD_ID])
async def cycles_vs_eevee(ctx: commands.Context):
    RESPONSE_1 = "Cycles is a path tracing engine, which means it properly simulates light. As a result, it creates stunning renders, but those renders come at the cost of render time and noise (use the `why_is_my_cycles_render_so_noisy` command for more info)\n\n"
    RESPONSE_2 = "EEVEE is a rasterized engine, which means it uses some crazy math to fake lighting. This means EEVEE has better performance, but the renders don't look as good compared to Cycles. In order to get something comparable, you need to do stuff such as baking indirect lighting, using reflection probes to improve reflections, etc.\n\n"
    RESPONSE_3 = "EEVEE does have one advantage though: NPR rendering such as anime or toon style rendering. Since EEVEE fakes its lighting, it's able to do things such as taking a shader input as a RGB mask, which makes EEVEE very powerful in the NPR world"
    RESPONSE_4 = 'As for which engine is better, it depends. If by that question you meant "Which engine is the best overall?", then Cycles will always be better. If you meant "Which engine is better for my style?", that\'s for you to figure out on your own. If your style uses realistic lighting, then Cycles is your best bet. If your style doesn\'t need realistic lighting, then EEVEE may be a good option\n\n'
    RESPONSE_5 = "Sidenote: Before Blender 3.0, EEVEE was also much better in terms of volumetrics as they looked decent without taking eternity to render. However as of 3.0+, Cycles volumetrics have improved massively and now look much better then EEVEE's volumetrics"
    await ctx.respond(RESPONSE_1 + RESPONSE_2 + RESPONSE_3)
    await ctx.respond(RESPONSE_4 + RESPONSE_5)


@client.slash_command(name="please_use_google_next_time", guilds=[MCPREP_GUILD_ID])
async def please_use_google_next_time(ctx: commands.Context):
    await ctx.respond(
        "We're happy to help with your issues, but have you tried googling for a solution? You might be able to find the answer you're looking for faster that way."
    )


@client.slash_command(name="rig_sucks", guilds=[MCPREP_GUILD_ID])
async def rig_sucks(ctx: commands.Context):
    await ctx.respond(
        f"Thank you for your feedback, but rigs are made and maintained by the community. If you don't like how the rigs are, then we'll gladly take submissions for replacement rigs"
    )


@client.slash_command(name="contribute_to_mcprep", guilds=[MCPREP_GUILD_ID])
async def contribute_to_mcprep(ctx: commands.Context):
    await ctx.respond(
        "Thanks for the feedback, though our hands are pretty much full when it comes to MCPrep (there's really only 2 active maintainers, and both of them are quite busy in real life). If you can implement the feature/changes you want to see in MCprep, please do, and open a pull request on the MCprep GitHub repo!\n\nA guide can be found here: https://github.com/TheDuckCow/MCprep/blob/dev/CONTRIBUTING.md"
    )


@client.slash_command(name="optifine_shaders_in_blender", guilds=[MCPREP_GUILD_ID])
async def optifine_shaders_in_blender(ctx: commands.Context):
    await ctx.respond(
        "Optifine shaders aren't compatible with Blender, but you can create custom materials and use Blender's built-in lighting system to achieve similar effects."
    )


@client.slash_command(name="shaders", guilds=[MCPREP_GUILD_ID])
async def shaders(ctx: commands.Context):
    RESPONSE_1 = "If by shaders you meant Optifine shaders, please use the `optifine_shaders_in_blender` command for info on why that's not possible.\n\n"
    RESPONSE_2 = "From a technical standpoint, a shader is a program that's ran on a CPU or GPU that does anything related to graphics. In fact, vanilla Minecraft uses shaders even with the default lighting, they're just not as fancy."
    await ctx.respond(RESPONSE_1 + RESPONSE_2)


@client.slash_command(name="previewing_animation_slow", guilds=[MCPREP_GUILD_ID])
async def previewing_animation_slow(ctx: commands.Context):
    await ctx.respond(
        "Make sure you're using solid mode and not material or render mode for previewing animation"
    )


@client.slash_command(name="unrealistic_expectations", guilds=[MCPREP_GUILD_ID])
async def unrealistic_expectations(ctx: commands.Context):
    await ctx.respond("Your expectations are too unrealistic")


@client.slash_command(name="world_exporter_issue", guilds=[MCPREP_GUILD_ID])
async def world_exporter_issue(ctx: commands.Context):
    await ctx.respond(
        "That feature would require changes to the world exporter, which is developed separately from MCprep. We depend on their developers to implement the necessary changes. For example, biome colors would need something exported by the world exporter since all biome information is lost during export."
    )


@client.slash_command(name="blender_27x", guilds=[MCPREP_GUILD_ID])
async def blender_27x(ctx: commands.Context):
    await ctx.respond(
        "Please upgrade from Blender 2.7x as soon as possible as it's extremely outdated and MCprep 3.5 will stop supporting it. If you need to transition from 2.7x, then use the latest relase of Blender and set the keybinds to 2.7x"
    )


@client.slash_command(name="bforartists", guilds=[MCPREP_GUILD_ID])
async def bforartists(ctx: commands.Context):
    await ctx.respond(
        "Bforartists is a fork of Blender that focuses on GUI enhancements. It's based of the alpha releases of Blender, and as such may cause compatibility issues."
    )


# @client.slash_command(name="watch_a_tutorial", guilds=[MCPREP_GUILD_ID])
# async def watch_a_tutorial(ctx: commands.Context):
#    await ctx.respond("Learning the basics of Blender is important to get the most out of the software. While we can't teach you everything here, we recommend checking out some tutorials to help you get started. Judo has some great ones that cover the basics: https://www.youtube.com/playlist?list=PLkN2rUqk0BtWVTVZomXYdJPrMnooovMKy. These tutorials were made with an earlier version of Blender, but they still apply to the current version. Good luck!")


@client.slash_command(name="outlines", guilds=[MCPREP_GUILD_ID])
async def outlines(ctx: commands.Context):
    await ctx.respond("""There are a couple of ways, including:
- Photoshop/GIMP (most common for single renders)\n 
- Some bevel node sorcery (though the bevel node is Cycles only)""")


@client.slash_command(name="no_numerical_ratings", guilds=[MCPREP_GUILD_ID])
async def no_numerical_ratings(ctx: commands.Context):
    await ctx.respond("Numerical ratings are not allowed as per server rules")


if __name__ == "__main__":
    token = None
    with open("config.json") as f:
        data = json.load(f)
        token = data["token"]
    client.run(token)
