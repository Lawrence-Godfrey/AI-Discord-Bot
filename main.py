import os
import discord
from discord import Client, Intents
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands
from dotenv import load_dotenv
from gpt_controller import GPT
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()  # Get environment variables from .env.
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GPT_API_KEY = os.getenv('GPT_API_KEY')

bot = commands.Bot(command_prefix='-')
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

gpt = GPT(GPT_API_KEY)

@slash.slash(name="clue", description="Get a crossword answer given a clue.")
async def crossword_answer(ctx: SlashContext, clue: str, length: int):
    await ctx.defer()  # Use defer since it can take a while to get the response from GPT-3.
    answer = gpt.crossword_answer(clue, answer_length=length)
    logging.info('Clue: %s (%s) \nAnswer: %s', clue, length, answer)
    await ctx.send('Clue: {} ({}) \nAnswer: {}'.format(clue, length, answer))


@slash.slash(name="chat", description="Have a conversation with an AI.")
async def crossword_answer(ctx: SlashContext, prompt: str):
    await ctx.defer()  # Use defer since it can take a while to get the response from GPT-3.
    answer = gpt.chat(prompt)
    logging.info('You: %s\nMe: %s', prompt, answer)
    await ctx.send('You: {}\nMe: {}'.format(prompt, answer))


@slash.slash(name="test")
async def test(ctx: SlashContext):
    await ctx.defer()
    await ctx.send('Test')

bot.run(DISCORD_TOKEN)
