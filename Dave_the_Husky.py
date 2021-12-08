from urllib.request import urlopen, Request

import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

with open('key.txt') as key:
    discordKey = key.readline()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

# Background Image
back = Image.open("Background.png")

# Initialize the text
font = ImageFont.truetype("ERASBD.TTF", 72)


# When Bot is read to start
@client.event
async def on_ready():
    print('Woof Woof!')
    # channel = client.get_channel(481183685421301763)
    # await channel.send('Ruff!')


# When User Joins a Server
@client.event
async def on_member_join(member):
    global back
    global font
    for channel in member.guild.channels:
        if channel.name == 'general':
            # await channel.send("")
            # Gets the Profile Picture
            req = Request(str(member.avatar_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req)
            fore = Image.open(page)

            fore = fore.convert('RGBA').resize((150, 150))

            # Make fore a circle
            circMask = Image.open("Mask.png").convert('L')
            fore.putalpha(circMask)

            # Layering of Images
            back.paste(fore, (120, 20), mask=fore)

            # Add Text
            # Make a blank image for the text
            txt = Image.new("RGBA", back.size, (255, 255, 255, 0))
            image = ImageDraw.Draw(txt)
            image.text((25, 235), str(member.name), font=font, fill=(255, 255, 255, 255))
            finalImg = Image.alpha_composite(back, txt)
            finalImg.save("temp.png")

            await channel.send(file=discord.File("temp.png"))


# When a Message is Received on a Server
@client.event
async def on_message(message):
    global back
    global font
    if message.content.startswith('!display'):
        # Gets the Profile Picture
        req = Request(str(message.author.avatar_url), headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        fore = Image.open(page)

        fore = fore.convert('RGBA').resize((150, 150))

        # Make fore a circle
        circMask = Image.open("Mask.png").convert('L')
        fore.putalpha(circMask)

        # Layering of Images
        back.paste(fore, (120, 20), mask=fore)

        # Add Text
        # Make a blank image for the text
        txt = Image.new("RGBA", back.size, (255, 255, 255, 0))
        image = ImageDraw.Draw(txt)
        image.text((25, 235), str(message.author.name), font=font, fill=(255, 255, 255, 255))
        finalImg = Image.alpha_composite(back, txt)
        finalImg.save("temp.png")

        await message.channel.send(file=discord.File("temp.png"))

client.run(discordKey)
