#!/usr/bin/python3
import discord
from discord.ext import commands
from discord import app_commands
import discord.ext
from gemini import ask_to_gemini
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
bot = discord.ext.commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name="word",description="word")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.defer()  # Etkileşimi hemen yanıtlama (defer)
    rsp = ask_to_gemini(isDefTrigerrefFromOutside=True)
    embed = discord.Embed(title="Herkes Çok dikkatli olabilir mi? Sanırım birileri düğmeye bastı..",description="Random English Word",color=0xf27107)
    embed.add_field(name="word", value=rsp[0], inline=False)
    embed.add_field(name="meaning of the word", value=rsp[1], inline=False)
    embed.add_field(name="etymological origin", value=rsp[2], inline=False)
    for cümle in rsp[4:7]:
        embed.add_field(name="example sentences", value=cümle, inline=False)
    embed.set_footer(text="developed by Geniousoft")
    await interaction.followup.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
           
# Todo: dışardan yeni command alacak.     
# systemctl --user restart discordBot.service    