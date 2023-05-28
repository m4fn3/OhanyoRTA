import datetime
import random

from discord.ext import commands
import discord, logging, os
import numpy
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
load_dotenv(join(dirname(__file__), '.env'))

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
emojis = {
    1011692569358499890: "<:chinponta:1021060110547693619>",
    781897166675116042: "<:yosl:802221707942952971>"
}


def format_timedelta(timedelta):
    text = ""
    total_sec = timedelta.total_seconds()
    hours = total_sec // 3600
    remain = total_sec - (hours * 3600)
    minutes = remain // 60
    seconds = remain - (minutes * 60)
    if hours > 0:
        text += f"{int(hours)}時間"
    if minutes > 0 or hours > 0:
        text += f"{int(minutes)}分"
    if seconds > 0 or minutes > 0 or hours > 0:
        text += f"{int(seconds)}秒"
    if hours > 0:
        comments = ["意識低すぎ", "遅すぎワロタ", "寝るな", "目ついてないな", "遅すぎてうんこ漏らしたわ"]
        text += f" - {numpy.random.choice(comments, p=[0.1, 0.1, 0.1, 0.1, 0.6])}"
    elif minutes > 0:
        comments = ["次からは気をつけろよ", "まだいけるやろ", "意識が低い", "甘い", "ちんぽんた", "乗換二―"]
        text += f" - {random.choice(comments)}"
    else:
        comments = ["悪くないね", "ええやん", "ニート乙", "見張ってた？", "素晴らしいと言わざるを得ない", "学校行ってる？"]
        text += f" - {random.choice(comments)}"
    return text


class Bot(commands.Bot):

    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        self.last_ohanyo = {}

    async def on_message(self, message):
        if message.content == ".version":
            await message.channel.send("""
            v1.0.1
            - changelogs
              [v1.0.1] 他人のオハニョに返答した場合のみ反応/時間の表示を修正float->int/意識が上がるように調整
            """)
        elif message.content == "オハニョ":
            self.last_ohanyo[message.guild.id] = {
                "time": datetime.datetime.now(),
                "user": message.author.id
            }
        elif message.content == emojis[message.guild.id]:
            if not self.last_ohanyo[message.guild.id]:
                return
            elif self.last_ohanyo[message.guild.id]["user"] == message.author.id:
                await message.channel.send(f"自分のオハニョに反応するなハゲ <@{message.author.id}>")
                return
            delta = datetime.datetime.now() - self.last_ohanyo[message.guild.id]["time"]
            delta_str = format_timedelta(delta)
            await message.channel.send(delta_str)


if __name__ == '__main__':
    intents = discord.Intents.all()
    bot = Bot(command_prefix="?", intents=intents)
    bot.run(TOKEN)
