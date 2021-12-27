import re
import discord
from discord.ext import commands
import json
import os
import random
import praw
import asyncio
import requests
import logging
from urllib import parse
from urllib import request

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

areddit = praw.Reddit(client_id = "G5OFuqZzaInDZn7vJpYQnQ", client_secret = "A6vkaKP9pSdChDTg_CQaBbUr7XBraA", 
                     username = "Average_Botmaker", password = "dangerfluid2005", user_agent = "pythonbot123")

ud_posts = []
ud_requestors = []

BASE = "https://youtube.com/results"
                
class web(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Web imported")
                    
    @commands.command()
    async def reddit(self, ctx, sub = ""):
        """Searches the subreddit on Reddit."""
        colors = [0xe91e63, 0xe74c3c, 0xf1c40f, 0x2ecc71, 0x3498db, 0x9b59b6]
        if sub == "":
            await ctx.channel.send("Specify a subreddit to search")
        else:
            try:
                subreddit = areddit.subreddit(sub)
                allsubs = []
                top = subreddit.hot(limit = 50)
                for submission in top:
                    allsubs.append(submission)
                randomsub = random.choice(allsubs)
                name = randomsub.title
                r_url = randomsub.url
                desc = randomsub.selftext
                if len(name.split()) > 255:
                    await ctx.channel.send('The title of the reddit post is too long for a discord embed, so here\'s the link:')
                    await ctx.channel.send(r_url)
                else:
                    if randomsub.is_self:
                        em = discord.Embed(title = name, url = r_url, description = desc, color = random.choice(colors))
                        if len(em.title) > 255 or len(em.description) > 4095 or len(em) > 5999:
                            await ctx.channel.send('The reddit post is too long for a discord embed, so here\'s the link:\n', r_url)
                        else:
                            await ctx.channel.send(embed = em)
                    else:
                        if r_url.endswith('jpg') or r_url.endswith('png') or r_url.endswith('jpeg'):
                            em = discord.Embed(title = name, ulr = r_url, color = random.choice(colors))
                            em.set_image(url = r_url)
                        else:
                            if r_url.count('gallery') > 0:
                                gallery = []
                                em = discord.Embed(title = name, ulr = r_url, color = random.choice(colors))
                                ncolor = random.choice(colors)
                                for i in randomsub.media_metadata.items():
                                    n_url = i[1]['p'][0]['u']
                                    n_url = n_url.split("?")[0].replace("preview", "i")
                                    gallery.append(n_url)
                                for img in gallery:
                                    em = discord.Embed(title = name, ulr = r_url, color = ncolor)
                                    em.set_image(url = img)
                                    await ctx.channel.send(embed = em)
                            else:
                                em = discord.Embed(title = name, ulr = r_url, description = r_url, color = random.choice(colors))

                        if len(em.title) > 255 or len(em) > 5999:
                            await ctx.channel.send('The reddit post is too long for a discord embed, so here\'s the link:\n', r_url)
                        else:
                            if r_url.count('gallery') == 0:
                                await ctx.channel.send(embed = em)
            except:
                await ctx.channel.send("That is not a valid subreddit.")

    @commands.command(aliases=['ud'])
    async def urban(self, ctx, *msg):
        """Searches the word on Urban Dictionary."""
        i = 0
        word = ' '.join(msg)
        api = "http://api.urbandictionary.com/v0/define"
        # Send request to the Urban Dictionary API and grab info
        response = requests.get(api, params=[("term", word)]).json()
        embed = discord.Embed(description="No results found!", colour=0x1f97f1)
        if len(response["list"]) == 0:
            return await ctx.channel.send(embed=embed)
        # Add results to the embed
        embed = discord.Embed(title=response['list'][0]['word'],url = response['list'][0]['permalink'], description = '**Defenition:**\n' + str(response['list'][0]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
        # if len(str(response['list'][0]['definition'])) > 900:
        #     embed.add_field(name="Top definition:", value=str(response['list'][0]['definition'])[:900].replace("[", "").replace("]","") + "...\n\n" + "Read the rest at https://www.urbandictionary.com/define.php?term=" + word, inline=True)
        # else:
        #     embed.add_field(name="Definition:", value=str(response['list'][0]['definition']).replace("[", "").replace("]",""), inline=True)
        # embed(description = str(response['list'][0]['definition'])[:900].replace("[", "").replace("]","") + "...\n\n" + "Read the rest at https://www.urbandictionary.com/define.php?term=" + word)
        if len(str(response['list'][0]['example'])) > 0:
            if len(str(response['list'][0]['example'])) > 900:
                embed.add_field(name="Examples:", value=str(response['list'][0]['example'])[:900].replace("[", "").replace("]","") + "...\n\n" + "Read the rest at https://www.urbandictionary.com/define.php?term=" + word, inline=False)
            else:
                embed.add_field(name="Examples:", value=str(response['list'][0]['example']).replace("[", "").replace("]",""), inline=False)
        embed.set_footer(text=f"Uploaded by: {str(response['list'][i]['author'])} and Requested by {ctx.author.name}")
        def_msg = await ctx.channel.send(embed=embed)
        ud_posts.append(def_msg.id)
        ud_requestors.append(ctx.message.author.id)
        await def_msg.add_reaction('◀️')
        await def_msg.add_reaction('⏹️')
        await def_msg.add_reaction('▶️')
        acceptable = ['◀️', '⏹️', '▶️']

        def check (reaction, user):
            return str(reaction.emoji) in acceptable and user == ctx.message.author and reaction.message == def_msg

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
                if str(reaction.emoji) == '◀️':
                    try:
                        i -= 1
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Defenition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
                        # if len(str(response['list'][i]['definition'])) > 900:
                        #     embed.add_field(name="Top definition:", value=str(response['list'][i]['definition'])[:900].replace("[", "").replace("]","") + "...\n\n" + "Read the rest at https://www.urbandictionary.com/define.php?term=" + word, inline=True)
                        # else:
                        #     embed.add_field(name="Definition:", value=str(response['list'][i]['definition']).replace("[", "").replace("]",""), inline=True)
                        if len(str(response['list'][i]['example'])) > 0:
                            if len(str(response['list'][i]['example'])) > 900:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example'])[:900].replace("[", "").replace("]","") + "...\n\n" + f"Read the rest at {response['list'][i]['permalink']}", inline=False)
                            else:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example']).replace("[", "").replace("]",""), inline=False)
                        embed.set_footer(text=f"Uploaded by: {str(response['list'][i]['author'])} and Requested by {ctx.author.name}")
                        try:
                            await def_msg.edit(embed = embed)
                        except:
                            return
                    except:
                        i = -1
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Defenition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
                        # if len(str(response['list'][i]['definition'])) > 990:
                        #     embed.add_field(name="Top definition:", value=str(response['list'][i]['definition'])[:955].replace("[", "").replace("]","") + "...\n\n" + "Read the rest at https://www.urbandictionary.com/define.php?term=" + word, inline=True)
                        # else:
                        #     embed.add_field(name="Definition:", value=str(response['list'][i]['definition']).replace("[", "").replace("]",""), inline=True)
                        if len(str(response['list'][i]['example'])) > 0:
                            if len(str(response['list'][i]['example'])) > 990:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example'])[:900].replace("[", "").replace("]","") + "...\n\n" + f"Read the rest at {response['list'][i]['permalink']}", inline=False)
                            else:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example']).replace("[", "").replace("]",""), inline=False)
                        embed.set_footer(text=f"Uploaded by: {str(response['list'][i]['author'])} and Requested by {ctx.author.name}")
                        try:
                            await def_msg.edit(embed = embed)
                        except:
                            return
                    await def_msg.remove_reaction('◀️', user)    
                elif str(reaction.emoji) == '⏹️':
                    await def_msg.remove_reaction('⏹️', user)  
                    raise TimeoutError
                elif str(reaction.emoji) == '▶️':
                    try:
                        i += 1
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Defenition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
                        # if len(str(response['list'][i]['definition'])) > 990:
                        #     embed.add_field(name="Top definition:", value=str(response['list'][i]['definition'])[:955].replace("[", "").replace("]","") + "...\n\n" + f"Read the rest at {response['list'][i]['permalink']}", inline=True)
                        # else:
                        #     embed.add_field(name="Definition:", value=str(response['list'][i]['definition']).replace("[", "").replace("]",""), inline=True)
                        if len(str(response['list'][i]['example'])) > 0:
                            if len(str(response['list'][i]['example'])) > 990:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example'])[:900].replace("[", "").replace("]","") + "...\n\n" + f"Read the rest at {response['list'][i]['permalink']}", inline=False)
                            else:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example']).replace("[", "").replace("]",""), inline=False)
                        embed.set_footer(text=f"Uploaded by: {str(response['list'][i]['author'])} and Requested by {ctx.author.name}")
                        await def_msg.edit(embed = embed)
                    except:
                        i = 0
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Defenition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
                        # if len(str(response['list'][i]['definition'])) > 990:
                        #     embed.add_field(name="Top definition:", value=str(response['list'][i]['definition'])[:955].replace("[", "").replace("]","") + "...\n\n" + f"Read the rest at {response['list'][i]['permalink']}", inline=True)
                        # else:
                        #     embed.add_field(name="Definition:", value=str(response['list'][i]['definition']).replace("[", "").replace("]",""), inline=True)
                        if len(str(response['list'][i]['example'])) > 0:
                            if len(str(response['list'][i]['example'])) > 990:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example'])[:900].replace("[", "").replace("]","") + "...\n\n" + f"Read the rest at {response['list'][i]['permalink']}", inline=False)
                            else:
                                embed.add_field(name="Examples:", value=str(response['list'][i]['example']).replace("[", "").replace("]",""), inline=False)
                        embed.set_footer(text=f"Uploaded by: {str(response['list'][i]['author'])} and Requested by {ctx.author.name}")
                        await def_msg.edit(embed = embed)
                    await def_msg.remove_reaction('▶️', user)
                
            except TimeoutError:
                await def_msg.clear_reactions()
                break

            except asyncio.TimeoutError:
                await def_msg.clear_reactions()
                break

    @commands.command(aliases = ['yt'])
    async def youtube(self, ctx, *, search):
        """Searches the term on Youtube."""

        i = 0
        query_string = parse.urlencode({'search_query': search})
        html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
        search_content= html_content.read().decode()
        search_results = re.findall(r'\/watch\?v=\w+', search_content)
        #print(search_results)
        res_msg = await ctx.send('https://www.youtube.com' + search_results[0])

        await res_msg.add_reaction('◀️')
        await res_msg.add_reaction('⏹️')
        await res_msg.add_reaction('▶️')
        acceptable = ['◀️', '⏹️', '▶️']

        def check (reaction, user):
            return str(reaction.emoji) in acceptable and user == ctx.message.author and reaction.message == res_msg

        while True:
            '''for r in def_msg.reactions:
                if str(r.emoji) not in acceptable:
                    await def_msg.reaction.remove(r)'''
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
                if str(reaction.emoji) == '◀️':
                    try:
                        i -= 1
                        edit = 'https://www.youtube.com' + search_results[i]
                        try:
                            await res_msg.edit(content = edit)
                        except:
                            return
                    except:
                        i = -1
                        edit = 'https://www.youtube.com' + search_results[i]
                        try:
                            await res_msg.edit(content = edit)
                        except:
                            return
                    await res_msg.remove_reaction('◀️', user)
                elif str(reaction.emoji) == '⏹️':
                    await res_msg.remove_reaction('⏹️', user)  
                    raise TimeoutError
                elif str(reaction.emoji) == '▶️':
                    try:
                        i += 1
                        edit = 'https://www.youtube.com' + search_results[i]
                        try:
                            await res_msg.edit(content = edit)
                        except:
                            return
                    except:
                        i = 0
                        edit = 'https://www.youtube.com' + search_results[i]
                        try:
                            await res_msg.edit(content = edit)
                        except:
                            return
                    await res_msg.remove_reaction('▶️', user)
                
            except TimeoutError:
                await res_msg.clear_reactions()
                break

            except asyncio.TimeoutError:
                await res_msg.clear_reactions()
                break




def setup(client):
    client.add_cog(web(client))