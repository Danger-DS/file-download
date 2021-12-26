import discord
from discord import message
from discord.colour import Color as Color
from discord.ext import commands
import json
import os
import logging
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont
from io import BytesIO
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionNotLoaded
import numpy as np

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

TOKEN = 'OTExNjAwNzIxMDU1NjAwNjcx.YZjwVA.pBua8V7w4qtamZaRWgzd1PoZU0k'

# os.chdir(r'C:\Users\dange\OneDrive\Desktop\Portfolio\Discord')

prefix = '.'

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ".", intents = intents)

@client.event
async def on_ready():
    print('Function is now online!')
    

@client.event
async def on_member_join(member):
    with open('index.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('index.json', 'w') as f:
        json.dump(users, f)

    await member.send('Welcome to the server! You can use \'.help\' to view my commands. Hope you have a good time! You can invite me to your other servers with:')
    em = discord.Embed(title = 'Invite Link', url = 'https://discord.com/api/oauth2/authorize?client_id=911600721055600671&permissions=8&scope=bot', description = 'Click title to invite Function to a server.')
    em.set_thumbnail(url = client.user.avatar_url)
    await member.send(embed = em)


@client.event
async def on_message(message):
    content = message.content
    user = message.author
    channel = message.channel
    server = message.guild

    print(f'{user}: {content}  (#{channel} in {server})')

    if message.author.bot == False:
        with open('index.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('index.json', 'w') as f:
            json.dump(users, f)

    await client.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {'\n'}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        # font_thick = ImageFont.truetype('Montserrat-SemiBold.otf', 50)
        # font_thin = ImageFont.truetype('Montserrat-Regular.otf', 25)
        # font_level = ImageFont.truetype('Montserrat-SemiBold.otf', 15)

        # if user.color == discord.Color(0):
        #     bordColor = 'white'
        # else:
        #     bordColor = str(user.color)

        # img = Image.new("RGB", (1000, 200), 'black')
        # img = ImageOps.expand(img, border = 10, fill = bordColor)
        # asset = user.avatar_url_as(size = 256)
        # data = BytesIO(await asset.read())
        # face = Image.open(data)
        # face = face.resize((190, 190))

        # lum_img = Image.new('L',[190, 190] ,0) 
        # draw = ImageDraw.Draw(lum_img)
        # draw.pieslice([(10, 10),(180,180)],0,360,fill=255)
        # lum_img = lum_img.filter(ImageFilter.GaussianBlur(7))
        # img_arr = np.array(face)
        # lum_img_arr = np.array(lum_img)
        # output = np.dstack((img_arr, lum_img_arr))
        # try:
        #     face = Image.fromarray(output)
        # except:
        #     print('didnt work')
        # face = face.filter(ImageFilter.GaussianBlur(10))
        

        # img.paste(face, (810, 15), lum_img)

        # img_edit = ImageDraw.Draw(img)
        # name = f'{user.name[:14]}#{user.discriminator}..' if len(user.name) > 15 else f'{user}'
        # nick = f'AKA - {user.display_name[:18]}..' if len(user.display_name) > 18 else f'AKA - {user.display_name}'
        # if user.color == discord.Color(0):
        #     color = 'white'
        # else:
        #     color = discord.Colour.to_rgb(user.color)
        # img_edit.text((30, 15), name, color, font = font_thick)
        # img_edit.text((30, 77), nick, color, font = font_thin)

        # img_edit.text((45, 124), f"Lvl. {int(users[f'{user.id}']['level']) + 1}", color, font = font_level)
        # img_edit.text((725, 124), f"Lvl. {int(users[f'{user.id}']['level']) + 2}", color, font = font_level)
        # img_edit.rounded_rectangle([(30, 148), (775, 188)], fill = '#D3D3D3', radius = 10)

        # img_edit.text((400, 124), f"0%", color, font = font_level)

        # img.save("lvl_info.png")
        # await message.channel.send(f'Congratulations {user.mention}! You are now on level {lvl_end}.', file = discord.File("lvl_info.png"))
        await message.channel.send(f'Congratulations {user.mention}! You are now on level {lvl_end}. Use \'.rank\' to view your progess.')
        users[f'{user.id}']['level'] = lvl_end


#functions
@client.command(aliases = ['import'], hidden = True)
async def load(ctx, ext):
    if ctx.author.id == 485123430010585101:
        if str(ext) == "all":
            for filename in os.listdir('./cogs'):
                try: 
                    if filename.endswith(".py"):
                        client.load_extension(f'cogs.{filename[:-3]}')
                except:
                    continue
            await ctx.channel.send(f'Loaded all!')
        else:
            try:
                client.load_extension(f'cogs.{ext}')
                await ctx.channel.send(f'{str(ext).title()} has been loaded!')
            except ExtensionNotFound:
                await ctx.channel.send("Extension not found.")
            except ExtensionAlreadyLoaded:
                await ctx.channel.send("Extension already loaded.")

@client.command(aliases = ['remove'], hidden = True)
async def unload(ctx, ext):
    if ctx.author.id == 485123430010585101:
        if str(ext) == "all":
            for filename in os.listdir('./cogs'):
                try:
                    if filename.endswith(".py"):
                        client.unload_extension(f'cogs.{filename[:-3]}')
                except:
                    continue
            await ctx.channel.send(f'Unloaded all!')
        else:
            try:
                client.unload_extension(f'cogs.{ext}')
                await ctx.channel.send(f'{str(ext).title()} has been unloaded!')
            except ExtensionNotLoaded:
                await ctx.channel.send("Extension not loaded.")
                

@client.command(aliases = ['reboot'], hidden = True)
async def reload(ctx, ext):
    if ctx.author.id == 485123430010585101:
        if str(ext) == "all":
            for filename in os.listdir('./cogs'):
                try:
                    if filename.endswith(".py"):
                        client.unload_extension(f'cogs.{filename[:-3]}')
                        client.load_extension(f'cogs.{filename[:-3]}')
                except:
                    continue
            await ctx.channel.send(f'Reloaded all!')
        else:
            try:
                client.unload_extension(f'cogs.{ext}')
                client.load_extension(f'cogs.{ext}')
                await ctx.channel.send(f'{str(ext).title()} has been reloaded!')
            except ExtensionNotFound:
                await ctx.channel.send("Extension not found.")
            except ExtensionNotLoaded:
                await ctx.channel.send("Extension not loaded.")

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(TOKEN)