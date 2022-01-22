import os
import logging

from io import BytesIO
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands
from discord import File
from dotenv import load_dotenv
from ai.gpt.gpt_controller import GPT
from ai.image_predict.predict_image import pretty_print_prediction, predict_image
from lib.utils import get_browser_headers, setup_logging
from lib.image.utils import get_image_from_url


setup_logging(log_level=logging.DEBUG)

load_dotenv()  # Get environment variables from .env.
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GPT_API_KEY = os.getenv('GPT_API_KEY')

if not DISCORD_TOKEN:
    raise RuntimeError('DISCORD_TOKEN is not set. Check if .env file is set up correctly.')

if not GPT_API_KEY:
    raise RuntimeError('GPT_API_KEY is not set. Check if .env file is set up correctly.')


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


@slash.slash(name="summarize", description="Summarize a piece of text.")
async def summarize(ctx: SlashContext, text: str):
    await ctx.defer()  # Use defer since it can take a while to get the response from GPT-3.
    summary = gpt.summarize(text)
    logging.info('Text: %s\nSummary: %s', text, summary)
    await ctx.send('Text: {}\nSummary: {}'.format(text, summary))


@slash.slash(name="QandA", description="Answer a question.")
async def answer_question(ctx: SlashContext, question: str):
    await ctx.defer()  # Use defer since it can take a while to get the response from GPT-3.
    answer = gpt.answer_question(question)
    logging.info('Text: %s\nAnswer: %s', question, answer)
    await ctx.send('Text: {}\nAnswer: {}'.format(question, answer))


@slash.slash(name="this_person_does_not_exist", description="Get a picture of a person who doesn't exist.")
async def this_person_does_not_exist(ctx: SlashContext):
    await ctx.defer()
    headers = get_browser_headers()
    data = get_image_from_url('https://thispersondoesnotexist.com/image', headers=headers)
    # Create a discord.File object from the image data.
    file = File(BytesIO(data), filename="this_person_does_not_exist.png")
    # Send the image as an attachment to the message.
    await ctx.send(file=file)


@bot.event
async def on_message(message):
    if 'predict' in message.content.lower():
        # Get the image from the message.
        data = await message.attachments[0].read(use_cached=True)
        # Predict the image and send the predictions to the channel.
        prediction = predict_image(src=data)
        await message.channel.send(pretty_print_prediction(prediction))


bot.run(DISCORD_TOKEN)
