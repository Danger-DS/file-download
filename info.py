from os import name
from re import T
import discord
from discord import user
from discord.ext import commands
import time
import logging
from discord.ext.commands.core import after_invoke
import requests
import datetime
import json
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import numpy as np
import math
import random

logger = logging.getLogger('discord')

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info imported")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        with open('stats.json', 'r') as f:
            statistics = json.load(f)

        # print(self.client.command.qualified_name)
        if not ctx.command.qualified_name in statistics:
            statistics[f'{ctx.command.qualified_name}'] = {}
            statistics[f'{ctx.command.qualified_name}']['usageCount'] = 1
        else:
            statistics[f'{ctx.command.qualified_name}']['usageCount'] += 1
        statistics['total']['usageCount'] += 1

        with open('stats.json', 'w') as f:
            json.dump(statistics, f)


    @commands.command(aliases = ['link'])
    async def invite(self, ctx):
        """Provides invite link to the bot."""
        em = discord.Embed(title = 'Invite Link', url = 'https://discord.com/api/oauth2/authorize?client_id=911600721055600671&permissions=8&scope=bot', description = 'Click title to invite Function to a server.')
        em.set_thumbnail(url = self.client.user.avatar_url)
        await ctx.channel.send(embed = em)

    @commands.command(aliases = ['user'])
    async def userinfo(self, ctx,member: discord.Member = None):
        """Provides discord info of specified user"""
        if member == None:
            member = ctx.author
        try:
            roles = [role for role in member.roles[1:]]
            embed = discord.Embed(
                color = member.color,
                title = f"User Profile: {member}")
            embed.add_field(name="Name:", value=member.name, inline=True)
            embed.add_field(name="Nickname:", value=member.display_name, inline=True)
            embed.add_field(name="**ID:**", value=f"{member.id}", inline=False)
            embed.set_thumbnail(url=f"{member.avatar_url}")
            #embed.add_field(name=f"**Roles ({len(ctx.author.roles) - 1})**", value='• '.join([role.mention for role in roles]), inline=False)
            embed.add_field(name="Highest role:", value=member.top_role.mention, inline=False)
            embed.add_field(name="**Account Created At:**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
            embed.add_field(name="**Joined Server At:**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        except:
            roles = [role for role in member.roles[1:]]
            embed = discord.Embed(
                color = member.color,
                title = f"User Profile: {member}")
            embed.add_field(name="Name:", value=member.name, inline=True)
            embed.add_field(name="Nickname:", value=member.display_name, inline=True)
            embed.add_field(name="**ID:**", value=f"{member.id}", inline=False)
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.add_field(name="Highest role:", value=member.top_role.mention, inline=False)
            embed.add_field(name="**Account Created At:**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
            embed.add_field(name="**Joined Server At:**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Gets bot ping."""
        try:
            pingtime = time.time()
            pingms = await ctx.channel.send("*Pinging...*")
            ping = (time.time() - pingtime) * 1000
            await pingms.edit(content = " " + pingms.content + " **Pong!** :ping_pong:  The ping time is `%dms`" % ping)
        except:
            await ctx.channel.send("Could not perform action")

    @commands.command(aliases = ['servercount', 'membercount', 'commandcount'], hidden = True)
    async def botinfo(self, ctx):
        """Provides statistical information on Function."""
        servers = []
        memberCount = 0
        commandCount = 0
        fullCommands = list(self.client.commands)
        for guild in self.client.guilds:
            for member in guild.members:
                if not member.bot:
                    memberCount += 1
            servers.append(guild.name)
        commandsS = self.client.all_commands
        for com in commandsS:
            if commandsS[com] in fullCommands:
                commandCount += 1
                fullCommands.remove(commandsS[com])
        with open('stats.json', 'r') as f:
            statistics = json.load(f)
        totalComCount = statistics['total']['usageCount']
        with open('stats.json', 'w') as f:
            json.dump(statistics, f)
        em = discord.Embed(title = 'Bot Info', url = 'https://discord.com/api/oauth2/authorize?client_id=911600721055600671&permissions=8&scope=bot')
        em.add_field(name = 'Server Count', value = f'{len(servers)}', inline = True)
        em.add_field(name = 'Member Count', value = f'{memberCount}', inline = True)
        em.add_field(name = chr(173), value = chr(173), inline = True)
        em.add_field(name = 'Command Count', value = f'{commandCount}', inline = True)
        em.add_field(name = 'Command Usage Count', value = f'{totalComCount}', inline = True)
        em.add_field(name = chr(173), value = chr(173), inline = True)
        em.set_thumbnail(url = self.client.user.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.channel.send(embed = em)
        print(servers)
        # servers = list(self.client.servers)

    @commands.command()
    async def weather(self, ctx, *, city = 'dubai'):
        """Sends weather report of specified city"""
        api_key = "df21c66d6dea311d1bacd0e446baa6a6"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        response = requests.get(complete_url).json()
        print(complete_url)

        if response["cod"] != "404":
            main = response["main"]
            sys = response["sys"]
            current_temperature = main["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = main["pressure"]
            current_humidity = main["humidity"]
            weather = response["weather"]
            name = response["name"]
            country = sys["country"]
            weather_description = weather[0]["description"]
            embed = discord.Embed(title=f"Weather in {str(name)} ({country})", color = discord.Color(0x1abc9c), timestamp = ctx.message.created_at)
            embed.add_field(name="Description", value=f"{weather_description}", inline=False)
            embed.add_field(name="Temperature(C)", value=f"{current_temperature_celsiuis}°C", inline=False)
            embed.add_field(name="Humidity(%)", value=f"{current_humidity}%", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"{current_pressure}hPa", inline=False)
            embed.set_thumbnail(url="https://image.winudf.com/v2/image1/Y29tLmhhbmRtYXJrLmV4cHJlc3N3ZWF0aGVyX2ljb25fMTU4ODYyNjMzNV8wMTQ/icon.png?w=&fakeurl=1")
            # https://cdn.iconscout.com/icon/free/png-256/weather-rain-season-cloud-rainy-1-28907.png
            # https://i.ibb.co/CMrsxdX/weather.png
            # https://store-images.s-microsoft.com/image/apps.10595.14397430983184912.cfdf6f70-0a34-4999-b494-936559d822c3.7355576f-baf9-4be3-8b34-27bdc6ac1bd2
            # https://image.winudf.com/v2/image1/b3JnLmFuZHJvd29ya3Mua2xhcmFfaWNvbl8xNjExMzc2NDc2XzAzMQ/icon.png?w=&fakeurl=1
            # https://image.winudf.com/v2/image1/Y29tLmhhbmRtYXJrLmV4cHJlc3N3ZWF0aGVyX2ljb25fMTU4ODYyNjMzNV8wMTQ/icon.png?w=&fakeurl=1
            # https://icons-for-free.com/iconfiles/png/512/cloud+sunny+weather+icon-1320136426457332725.png
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("City not found.")
        
    @commands.command(aliases = ['rank'])
    async def level(self, ctx, user : discord.Member = None):
        """Displays level and global rank of user"""
        rickChance = random.randint(0, 1000)
        # rickChance = 10
        if user == None:
            user = ctx.author

        with open('index.json', 'r') as f:
            users = json.load(f)

        font_thick = ImageFont.truetype('Montserrat-SemiBold.otf', 50)
        smaller_font_thick = ImageFont.truetype('Montserrat-SemiBold.otf', 42)
        font_thin = ImageFont.truetype('Montserrat-Regular.otf', 25)
        font_level = ImageFont.truetype('Montserrat-SemiBold.otf', 15)

        if user.color == discord.Color(0):
            bordColor = 'white'
        else:
            bordColor = str(user.color)

        img = Image.new("RGB", (1000, 200), 'black')
        img = ImageOps.expand(img, border = 10, fill = bordColor)
        asset = user.avatar_url_as(size = 256)
        data = BytesIO(await asset.read())
        face = Image.open(data)
        face = face.resize((190, 190))

        if rickChance == 10:
            face = Image.open(r'cogs\media\rickroll.jpg')
        else:
            face = Image.open(data)

        face = face.resize((190, 190))

        lum_img = Image.new('L',[190, 190] ,0) 
        draw = ImageDraw.Draw(lum_img)
        draw.pieslice([(10, 10),(180,180)],0,360,fill=255)
        lum_img = lum_img.filter(ImageFilter.GaussianBlur(7))
        img_arr = np.array(face)
        lum_img_arr = np.array(lum_img)
        output = np.dstack((img_arr, lum_img_arr))
        # print(output)
        output_list = list(output)
        output_list[2] = 3
        output = np.array(output_list)
        # print(output)
        try:
            face = Image.fromarray(output)
        except:
            print('didnt work')

        # face = face.filter(ImageFilter.GaussianBlur(10))
        

        # img.paste(face, (810, 20))
        img.paste(face, (810, 15), lum_img)

        img_edit = ImageDraw.Draw(img)

        if rickChance == 10:
            name = 'Get Rick Rolled'
            nick = 'AKA - idiot'
        else:
            name = f'{user.name[:14]}#{user.discriminator}..' if len(user.name) > 15 else f'{user}'
            nick = f'AKA - {user.display_name[:35]}..' if len(user.display_name) > 35 else f'AKA - {user.display_name}'

        if user.color == discord.Color(0):
            color = 'white'
        else:
            color = discord.Colour.to_rgb(user.color)
        img_edit.text((30, 15), name, color, font = font_thick)
        img_edit.text((30, 77), nick, color, font = font_thin)

        img_edit.text((45, 124), f"Lvl. {int(users[f'{user.id}']['level']) }", color, font = font_level)
        img_edit.text((725, 124), f"Lvl. {int(users[f'{user.id}']['level']) + 1}", color, font = font_level)
        img_edit.rounded_rectangle([(30, 145), (775, 190)], fill = '#D3D3D3', radius = 13, outline = 'black', width = 5)
        # img_edit.text((30, 140), f"Level - {int(users[f'{user.id}']['level']) + 1}", discord.Color.to_rgb(user.color), font = font_level)

        level = int(users[f'{user.id}']['level']) + 1
        last_exp = int(users[f'{user.id}']['level']) ** 4
        last_exp += (5 - (last_exp % 5))
        exp_req = level ** 4
        exp_req += (5 - (exp_req % 5))
        exp_req -= last_exp
        exp_cur = int(users[f'{user.id}']['experience']) - last_exp
        percentage = (exp_cur / exp_req) * 100
        width = (745 * percentage)/100
        img_edit.rounded_rectangle([(30, 145), (width + 30, 190)], fill = color, radius = 13, outline = 'black', width = 5)
        img_edit.text((400, 124), f"{int(percentage)}%", color, font = font_level)

        scores = []
        for username in users:
            scores.append(users[username]['experience'])
        scores.sort(reverse = True)
        rank = scores.index(users[f'{user.id}']['experience']) + 1
        img_edit.text((500, 60), f'Rank: #{rank}', color, font = smaller_font_thick)



        img.save(r'cogs\media\lvl_info.png')
        await ctx.channel.send(file = discord.File('cogs\media\lvl_info.png'))

        with open('index.json', 'w') as f:
            json.dump(users, f)

    @commands.command(aliases = ['ranklist', 'scoreboard', 'ranking', 'rankings'])
    async def leaderboard(self, ctx):
        with open('index.json', 'r') as f:
            users = json.load(f)
        scores = []
        for userid in users:
            scores.append(users[userid]['experience'])
        scores.sort(reverse = True)
        rankingid = []
        for score in scores:
            for username in users:
                if users[username]['experience'] == score and username not in rankingid:
                    rankingid.append(username)
        print(rankingid)
        ranking = []
        for id in rankingid:
            ranking.append(f'{(self.client.get_user(int(id)))}')
        print(scores)
        print(ranking)

        img = Image.new("RGB", (750, 1000), 'black')
        img = ImageOps.expand(img, border = 10, fill = 'white')



def setup(client):
    client.add_cog(info(client))



    