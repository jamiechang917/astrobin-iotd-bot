
import pandas as pd
import discord

def add_server(guild: discord.Guild, channel: discord.TextChannel):
    """
    Add the server to the servers.csv file when executing the /setchannel command.
    """
    server = {
        "server":     guild.name,
        "members":    guild.member_count,
        "channel":    channel.name,
        "server_id":  guild.id,
        "channel_id": channel.id,
    }
    try:
        df = pd.read_csv("../data/servers.csv")
    except:
        df = pd.DataFrame(columns=["server", "members", "channel", "server_id", "channel_id"])

    if guild.id in df["server_id"].values: # if server already exists, update the channel and member count
        df.loc[df["server_id"] == guild.id, ["channel", "channel_id", "members"]] = [channel.name, channel.id, guild.member_count]
    else:
        df = pd.concat([df, pd.DataFrame([server])], ignore_index=True)
    
    df.to_csv("../data/servers.csv", index=False)

def get_server(guild: discord.Guild):
    """
    Get the server information from the servers.csv file.
    """
    df = pd.read_csv("../data/servers.csv")
    if guild.id not in df["server_id"].values:
        return None
    else:
        return df[df["server_id"] == guild.id].to_dict(orient="records")[0]