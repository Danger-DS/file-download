import re
import discord
from discord.ext import commands
import json
import os
import random
import praw
import socialblade
from aiotube import Channel
import youtube_comment_scraper_python
import youtubesearchpython
from youtube_easy_api.easy_wrapper import *
from youtube_comment_scraper_python import *
# import instagram_explore
from better_instagram import better_instagram as bi
# from bs4 import BeautifulSoup
import snscrape.modules.twitter as sntwitter
import pandas
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
    async def reddit(self, ctx, sub = "", filter = 'hot'):
        """Searches the subreddit on Reddit."""
        colors = [0xe91e63, 0xe74c3c, 0xf1c40f, 0x2ecc71, 0x3498db, 0x9b59b6]
        if sub == "":
            await ctx.channel.send("Specify a subreddit to search")
        else:
            try:
                subreddit = areddit.subreddit(sub)
                allsubs = []
                if str(filter).lower() == 'hot':
                    top = subreddit.hot(limit = 50)
                elif str(filter).lower() == 'top':
                    top = subreddit.top(limit = 50)
                else:
                    await ctx.channel.send('Valid filters are \'top\' and \'hot\'.')
                    return
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
                        if r_url.endswith('jpg') or r_url.endswith('png') or r_url.endswith('jpeg') or r_url.endswith('gif'):
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
        embed = discord.Embed(title=response['list'][0]['word'],url = response['list'][0]['permalink'], description = '**Definition:**\n' + str(response['list'][0]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
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
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Definition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
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
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Definition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
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
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Definition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
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
                        embed = discord.Embed(title=response['list'][i]['word'],url = response['list'][i]['permalink'], description = '**Definition:**\n' + str(response['list'][i]['definition']).replace("[", "").replace("]",""), colour=embed.colour)
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
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def youtube(self, ctx, mode:str, *, search):
        """Searches the term on Youtube."""
        # easy_wrapper = YoutubeEasyWrapper()
        # easy_wrapper.initialize(api_key = 'AIzaSyDwLbUjyfoYF-3chjbYBnsSQDcJRMTeU04')
        # results = easy_wrapper.search_videos(search_keyword = search, order = 'relevance')

        if mode.lower() == 'search':
            i = 0
            query_string = parse.urlencode({'search_query': search})
            print(query_string)
            html_content = request.urlopen('http://www.youtube.com/results?' + query_string + '&sp=CAASAhAB')
            search_content= html_content.read().decode()
            search_results = re.findall(r'\/watch\?v=\w+', search_content)
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
        elif mode.lower() == 'comments':
            videosSearch = youtubesearchpython.VideosSearch(search, limit = 1)
            search_result = videosSearch.result()
            print(str(search_result))
            youtube_comment_scraper_python.youtube.open(search)
            # totalData = []
            for i in range(1):
                response = youtube_comment_scraper_python.youtube.video_comments()
                print(youtube)
                data = response['body']
                # totalData.extend(data)
            for comment in list(data):
                print(str(comment))
            title = search_result['result'][0]['title']
            if len(list(data)) == 0:
                em = discord.Embed(title = title, description = 'No comments.', color = 0xff0000)
            else:
                i = 0
                while True:
                    try:
                        comment = data[i]['Comment']
                        username = data[i]['user']
                        time = data[i]['Time']
                        likes = data[i]['Likes']
                    except:
                        i += 1
                    else:
                        break
                em = discord.Embed(title = title, description = f'{comment}\n\nLikes: {likes}', color = 0xff0000)
                em.set_footer(text = f'Posted by {username} {time}\nComments 1-20')
            await ctx.channel.send(embed = em)
            # print(vid_id)
            # metadata = easy_wrapper.get_metadata(video_id = vid_id)
            # vid_title = metadata['title']
            # if metadata['comments'] == None:
            #     em_des = 'The video has disabled comments.'
            #     em = discord.Embed(description = em_des, color = 0xff0000)
            # elif metadata['statistics']['commentCount'] == 0:
            #     em_des = 'The video has no comments.'
            #     em = discord.Embed(description = em_des, color = 0xff0000)
            # else:
            #     comment_count = metadata['statistics']['commentCount']
            #     em = discord.Embed(title = vid_title, description = f'This video has {comment_count} comments.', color = 0xff0000)
            # await ctx.channel.send(embed = em)
            

    @commands.command(aliases = ['sb'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def socialblade(seld, ctx, platform, *, search):
        if str(platform).lower() == 'yt' or str(platform).lower() == 'youtube':
            channelSearch = youtubesearchpython.ChannelsSearch(search, limit = 1)
            
            # print(str(channelSearch.result()["result"][0]))
            channelId = channelSearch.result()["result"][0]['id']
            channelName = channelSearch.result()["result"][0]['title']
            channelLink = channelSearch.result()["result"][0]['link']
            subCount = channelSearch.result()["result"][0]['subscribers']
            channelDesc = ''
            channelSearchd = Channel(channelId)
            if channelSearch.result()["result"][0]['descriptionSnippet'] == None:
                channelDesc = 'No channel description.'
            else:
                channelDesc = channelSearchd.description
                # for i in channelSearch.result()["result"][0]['descriptionSnippet']:
                #     channelDesc += i['text']
            vidCount = channelSearch.result()["result"][0]['videoCount']
            viewCount = channelSearchd.views
            channelPfp = channelSearch.result()["result"][0]['thumbnails'][-1]['url']
            # print(f'{channelId}\n{channelDesc}\n{channelLink}\n{channelName}\n{subCount}\n{vidCount}\n{channelPfp}')

            em = discord.Embed(title = channelName, description = channelDesc, url = channelLink, color = 0xff0000)
            em.add_field(name = 'Channel ID', value = channelId, inline = False)
            em.add_field(name = 'Subscriber Count', value = subCount, inline = False)
            # em.add_field(name = '\u200b', value = '\u200b')
            em.add_field(name = 'Video Count', value = vidCount, inline = False)
            em.add_field(name = 'Total Views', value = viewCount, inline = False)
            em.add_field(name = 'Channel Link', value = channelLink, inline = False)
            # em.add_field(name = '\u200b', value = '\u200b')
            thumbnail_url = f'https:{channelPfp}' if not channelPfp.startswith('http') else channelPfp
            em.set_thumbnail(url = f'{thumbnail_url}')
            em.set_image(url = channelSearchd.banner)
            print(f'http:{channelPfp}')
            print('poo')
            await ctx.channel.send(embed = em)
            # bladeChannel = socialblade.YouTubeChannel(f'{channelId}')
            # print(bladeChannel)
            # for sub in bladeChannel.live_subscriber_count_generator():
            #     print(sub)
            # print(channelId)
            
            # query_string = parse.urlencode({'search_query': search})
            # # html_content = request.urlopen('http://www.youtube.com/c/' + query_string)
            # link = 'http://www.youtube.com/c/' + search
            # # search_content= html_content.read().decode()
            # # search_results = re.findall(r'\/watch\?v=\w+', search_content)
            # #print(search_results)
            # # res_msg = 'https://www.youtube.com' + search_results[0]

            # # try:
            # #     url = 'http://www.youtube.com/c/' + search
            # #     response_object = request.urlopen(url)
            # # except:
            # #     url = 'http://www.youtube.com/user/' + search
            # #     response_object = request.urlopen(url)

            # url = 'http://www.youtube.com/' + search
            # response_object = request.urlopen(url)

            # # # Print the contents line by line 
            # count = 0
            # iter= 1
            # for line in response_object:
            #     # print(f'{line}')
            #     if f'{line}'.count('www.youtube.com/channel/UC') > 0 and count == 0:
            #         indexStart = f'{line}'.index('www.youtube.com/channel/UC')
            #         # print(indexStart)
            #         mainline = f'{line}'[indexStart:indexStart+48]
            #         count = 1
            #         print(iter)
            #     iter += 1

            # await ctx.channel.send(mainline)

            # channel = socialblade.YouTubeChannel('search')
            # print(channel.get_subscriber_count())

        elif str(platform).lower() == 'ig' or str(platform).lower() == 'instagram':
            if len(search.split()) > 1:
                print('invalid account name')
            else:
                bi.login(username = 'danger._.l', password = 'dangerfluid2005')
                metaData = bi.getuser(f'{search}')
                print(metaData)
                em = discord.Embed(title = metaData['username'], description = metaData['biography'], url = metaData['url'], color = 0xFF1493)
                em.add_field(name = 'Name', value = metaData['name'], inline = False)
                em.add_field(name = 'Followers', value = metaData['followers'], inline = False)
                em.add_field(name = 'Following', value = metaData['following'], inline = False)
                em.add_field(name = 'Posts', value = metaData['posts'], inline = False)
                em.add_field(name = 'Verified', value = metaData['is_verified'], inline = False)
                if metaData['website'] != None:
                    em.add_field(name = 'Website', value = metaData['website'], inline = False)
                em.add_field(name = 'Account Link', value = metaData['url'], inline = False)
                em.set_thumbnail(url = metaData['pfp'])
                await ctx.channel.send(embed = em)

                # searchResult = instagram_explore.user(f'{search}')
                # print(searchResult.data)

                # URL = f'https://instagram.com/{search}/'
                # r = requests.get(URL.format(search))
                # s = BeautifulSoup(r.text, "html.parser")
                # meta = s.find("meta", property = "og:description")
                # content = meta.attrs['content']
                # data = {}
                # s_ = content.split("-")[0]
                # s_ = s_.split(" ")
                # data['followers'] = s_[0]
                # data['following'] = s_[2]
                # data['posts'] = s_[4]
                # print(str(data))

        elif str(platform).lower() == 'tt' or str(platform).lower() == 'twitter':
            tweetInfo = []
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{search}').get_items()):
                if i > 0:
                    break
                content = tweet.content
                if len(tweet.content.split('/')[-1]) == 10:
                    content = tweet.content[:-23]
                tweetInfo.append([tweet.user.username, tweet.user.displayname, tweet.user.id, tweet.user.description, tweet.user.followersCount, tweet.user.profileImageUrl, tweet.user.profileBannerUrl, tweet.user.verified, f'{tweet.user.created}'[:10], tweet.user.friendsCount, f'{tweet.date}'[:10], content, tweet.url, tweet.user.statusesCount])
            em = discord.Embed(title = tweetInfo[0][0], description = tweetInfo[0][3], url = f'https://twitter.com/{tweetInfo[0][0]}/', color = 0x00acee)
            em.add_field(name = 'Display Name', value = tweetInfo[0][1])
            em.add_field(name = 'User ID', value = tweetInfo[0][2])
            em.add_field(name = 'Created', value = tweetInfo[0][8])
            em.add_field(name = 'Followers', value = tweetInfo[0][4])
            em.add_field(name = 'Following', value = tweetInfo[0][9])
            em.add_field(name = 'Verified', value = tweetInfo[0][7])
            em.add_field(name = 'Account Link', value = f'https://twitter.com/{tweetInfo[0][0]}/')
            em.add_field(name = 'Tweets', value = tweetInfo[0][-1])
            em.add_field(name = 'Last Tweet Date', value = tweetInfo[0][-4])
            em.add_field(name = 'Last Tweet', value = f'\n{tweetInfo[0][-2]}\n\n{tweetInfo[0][-3]}', inline = False)
            em.set_thumbnail(url = tweetInfo[0][5])
            # em.set_image(url = f'https://{tweetInfo[0][6]}')
            print(f'{tweetInfo}')
            await ctx.channel.send(embed = em)

            # twitAcc = socialblade.TwitterUser('realdonaldtrump').initalize()
            # await ctx.channel.send(twitAcc.get_follower_count())
        
        




def setup(client):
    client.add_cog(web(client))