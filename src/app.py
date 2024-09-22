# AstroBin IOTD Discord Bot
from datetime import datetime, time
import discord
from discord.ext import commands, tasks

from utils import *
from data import *

print("===========================")
print("AstroBin IOTD Discord Bot")
print("Version: 1.0.0")
print("Author: Jamie Chang")
print("License: MIT")
print("===========================")

# TOKEN     = "YOUR TOKEN HERE"
BROADCAST = time(0, 0) # fetch IOTD and broadcast at certain time (UTC)

intents = discord.Intents.default()
intents.message_content = True
client  = discord.Client(intents=intents)
tree    = discord.app_commands.CommandTree(client) 

def build_iotd_message():
    iotd_url  = get_iotd_url()
    iotd_info = get_image_info(iotd_url)
    if iotd_info:
        # create embed message
        embed = discord.Embed(
            title=iotd_info['title'],
            description=truncate_text(iotd_info['description'], 100), # Truncate the description to 100 words
            url=iotd_url,
            color=discord.Color.blue()
        )
        embed.set_author(name=iotd_info['author'])
        embed.set_image(url=iotd_info['img'])
        embed.add_field(name="Date", value=iotd_info['date'], inline=True)
        embed.add_field(name="Link", value=iotd_url, inline=False)

        # footer
        current_date = datetime.now().strftime("%m/%d/%Y")
        embed.set_footer(text=f"Unofficial AstroBin IOTD Bot • {current_date} • Jamie Chang")
        return embed
    return None

@client.event
async def on_ready():
    await tree.sync()
    scheduled_job.start()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} INFO     Bot is ready! Logged in as {client.user}")

@tasks.loop(time=BROADCAST)
async def scheduled_job():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} INFO     Broadcasting IOTD... ({datetime.now().strftime('%m/%d/%Y')})")
    for guild in client.guilds:
        server_info = get_server(guild)
        if server_info:
            for channel in guild.text_channels:
                if channel.id == server_info['channel_id']:
                    embed = build_iotd_message()
                    if embed:
                        await channel.send(embed=embed)
                    else:
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WARNING     Unable to retrieve the IOTD. Please try again later.")
                    add_server(guild, channel) # update the server info

@tree.command(name="today", description="Get the image of the day from AstroBin.")
async def today(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = build_iotd_message()
    await interaction.followup.send(embed=embed if embed else "Unable to retrieve the IOTD. Please try again later.")

@tree.command(name="setup", description="Setup the bot.")
async def setup(interaction: discord.Interaction):
    # message = "Welcome to AstroBin IOTD Bot! Please set the channel where you want to receive the IOTD by typing `/setchannel`. After that, the bot will send the IOTD to that channel every day. Also, you can type `/today` to get today's IOTD immediately."
    message = (
    "Welcome to the AstroBin IOTD Bot! Please set the channel where you would like to receive the IOTD by typing `/setchannel`. "
    "After that, the bot will send the IOTD to that channel every day. You can also type `/today` to get today's IOTD right away."
    )
    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name="setchannel", description="Set the channel to receive IOTD.")
async def set_channel(interaction: discord.Interaction):
    guild   = interaction.guild
    channel = interaction.channel
    if isinstance(channel, discord.DMChannel):
        message = "Please run this command in a server channel, not in a DM."
        await interaction.response.send_message(message, ephemeral=True)
        return
    else:
        message = f"Set the channel to {channel.mention}. Now you will receive the IOTD in this channel every day!"
        await interaction.response.send_message(message, ephemeral=True)    
        add_server(guild, channel)

client.run(TOKEN)