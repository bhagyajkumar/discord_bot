from discord import app_commands
import aiohttp
import discord

API_URL = "https://api.tinyurl.com/create?api_token=nwHHb7Y6jIZYqRbvrexxGbHzWjLw6CrvP0Zvun6PGXw69PQHqeTG07YJoPW3"
MY_GUILD = discord.Object(811637862134972467)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
@app_commands.describe(url="the url to shorten")
async def shorten(interaction: discord.Interaction, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data={"url": url, "domain": "tiny.one"}) as resp:
            data = await resp.json()
            print(data)
            await interaction.response.send_message(f'Your URL has been shortened `{data["data"]["tiny_url"]}`')

client.run("NzM5MTA4MjE2NTQ1NDc2NjQ4.GrvpJm.KxJ4XeJBfTa5bDoDbHgu9amUmYBoWWpVaxXTYk")
