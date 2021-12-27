import discord
from discord.ext import commands
import random
import logging
from PIL import Image, ImageDraw
from colour import Color
from discord.ext.commands.core import command
import requests
import asyncio
from io import BytesIO

logger = logging.getLogger('discord')

class fun(commands.Cog):
    

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun imported")

    @commands.command(pass_context = True, aliases = ['random'])
    async def randomnumber(self, ctx, num = "Please specify a range.", *, times=1):
        """Provides a random number in specified range."""
        try:
            if ':' in str(num):
                test = int(str(num).split(':')[0])-1
                test = int(str(num).split(':')[1])-1
            else:
                test = int(num)-1
        except:
            await ctx.channel.send('Enter a valid range.')
            return

        try:
            test = int(times) - 1
        except:
            await ctx.channel.send('\'Times\' has to be an integer value.')
            return
            
        if times > 100:
            await ctx.channel.send("Please request a lower number of results.")
        elif times < 1:
            await ctx.channel.send(f"Cannot pick random {times} times")
        else:
            answer = ""
            for i in range(times):
                if ':' in str(num):
                    try:
                        result = random.randrange(int(str(num).split(':')[0])-1, int(str(num).split(':')[1]))
                    except:
                        await ctx.channel.send("Enter range in ascending order.")
                        break
                else:
                    if int(num) < 0:
                        result = random.randrange(int(num), 0)
                    else:
                        result = random.randrange(int(num))
                answer += f'Random: {result + 1}\n'
            if answer != "":
                await ctx.channel.send(answer)

    @commands.command()
    async def coinflip(self, ctx, check = ""):
        """Heads or Tails"""
        result = ['Heads', 'Tails']
        if check != "":
            await ctx.channel.send("No parameters required after '.coinflip'")
        else:
            await ctx.channel.send(random.choice(result))

    @commands.command(aliases = ['choice'])
    async def choose(self, ctx, *, options = ""):
        """Chooses between options provided randomly."""
        if options == '':
            await ctx.channel.send("Please give options to choose from.")
        else:
            print(options)
            options_list = options.split(',')
            print(options_list)
            await ctx.channel.send(f"Your random choice: {str(random.choice(options_list)).strip()}")

    @commands.command(name = "8ball")
    async def eight_ball(self, ctx, question = ""):
        """Gives a random answer to a Yes/No question"""
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        if question == "":
            await ctx.channel.send("Please ask a Yes/No question.")
        else:
            await ctx.channel.send(random.choice(responses))

    @commands.command(aliases = ['colour'])
    async def color(self, ctx, color = ""):
        """Sends info on the color requested."""
        if color == "":
            await ctx.channel.send("Please state a color name.")
        else:
            try:
                c = Color(str(color))
                #col = discord.Embed(title = str(color).title(), color = discord.Color(0xffff00))
                red = int(str((c.get_red()/1) * 255).split('.')[0])
                green = int(str((c.get_green()/1) * 255).split('.')[0])
                blue = int(str((c.get_blue()/1) * 255).split('.')[0])
                print((c.get_red()/1) * 255, (c.get_green()/1) * 255, (c.get_blue()/1) * 255)
                col = discord.Embed(title = str(c).upper(), color = discord.Color.from_rgb(red, green, blue))
                col.add_field(name = 'HEX', value = str(c.hex).upper(), inline = False)
                col.add_field(name = 'RGB', value = f'({red}, {green}, {blue})', inline = False)
                #img = Image.new("RGB", (200,50), str(color))
                img = Image.new("RGB", (200,50), str(color))
                img.save(r"cogs\media\blank.png")
                file = discord.File(r"cogs\media\blank.png", filename="blank.png")
                col.set_image(url = "attachment://blank.png")
                await ctx.channel.send(file = file, embed = col)
            except:
                await ctx.channel.send("That is not a valid color.")

    @commands.command()
    async def insult(self, ctx, *, user:discord.Member = None):
        """Says something mean about you."""
        if user == None:
            user = ctx.message.author
        insults = ["If laughter is the best medicine, your face must be curing the world.", "It's better to let someone think you are an idiot than to open your mouth and prove it.", "If I had a face like yours, I'd sue my parents.", "You're so ugly, when your mom dropped you off at school she got a fine for littering.", "If I wanted to kill myself I'd climb your ego and jump down to your IQ.", "Brains aren't everything. In your case they're nothing.", "Are you always this stupid or is today a special occasion?", "Don't you have a terribly empty feeling - in your skull?", "How did you get here? Did someone leave your cage open?", "I'd like to see things from your point of view but I can't seem to get my head that far up my ass.", "Have you been shopping lately? They're selling lives, you should go get one.", "The last time I saw something like you, I flushed it.", "If ugliness was measured in bricks, you would be the Great Wall of China.", "You want an insult? Look in the mirror!", "The story of your life is more insulting than anything I have to say.", "Did a thought cross your mind? It must have been a long and lonely journey...", "You'd better hide; the garbage man is coming.", "Roses are red, violets are blue, I have five fingers, the middle one's for you.", "I have a text file bigger than your brain in my database. It's 0KB in size.", "You're old enough to remember when emojis were called 'hieroglyphics.'", "I don't engage in mental combat with the unarmed.", "Is your ass jealous of the amount of shit that comes out of your mouth?", "Your face looks like it caught fire and someone tried to put it out with a fork.", "Hey, you have something on your third chin.", "I thought a little girl from Kansas dropped a house on you…", "I'm jealous of people that don't know you.", "You bring everyone a lot of joy, when you leave the room.", "If you are going to be two faced, at least make one of them pretty.", "If you're going to be a smartarse, first you have to be smart. Otherwise you're just an arse.", "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. I think you owe it an apology.", "I don't exactly hate you, but if you were on fire and I had water, I'd drink it.", "If you were on TV, I would change the channel.", "You have Diarrhea of the mouth; constipation of the ideas.", "If ugly were a crime, you'd get a life sentence.", "There is no vaccine for stupidity.", "Did your parents ever ask you to run away from home?", "Any similarity between you and a human is purely coincidental.", "Keep talking – someday you’ll say something intelligent.", "Don’t you love nature, despite what it did to you?", "I'm sure if you studied harder you could get enough qualifications to work as a McDonalds' cleaner.", "If I knew you were a cock I would have fed you corn.", "I shouldn't say anything to upset you, I know it's your time of the month.", "Has your existence been verified by science yet?", "I don't understand how they could cram so much ugly into one physical form.", "you are a classic example of the inverse ratio between the size of the mouth and the size of the brain.", "You're about as much use as a condom machine in the Vatican."]
        await ctx.send(str(user.display_name).split('#')[0] + " " + random.choice(insults))

    @commands.command(aliases=["fancy"])
    async def fancify(self, ctx, *, text:str = None):
        """Makes text look fancy."""
        try:
            def strip_non_ascii(string):
                """Returns the string without non ASCII characters."""
                stripped = (c for c in string if 0 < ord(c) < 127)
                return ''.join(stripped)

            text = strip_non_ascii(text)
            if len(text.strip()) < 1:
                await ctx.channel.send("Input ASCII characters only.")
            output = ""
            for letter in text:
                if 65 <= ord(letter) <= 90:
                    output += chr(ord(letter) + 119951)
                elif 97 <= ord(letter) <= 122:
                    output += chr(ord(letter) + 119919)
                elif letter == " ":
                    output += " "
            await ctx.send(output)

        except:
            await ctx.channel.send("Provide text to fancify.")
            return

    @commands.command()
    async def animalfact(self, ctx):
        """Gives you a random fact about a random animal."""
        #making a GET request to the endpoint.
        try:
            links = ['https://some-random-api.ml/animal/dog', 'https://some-random-api.ml/animal/panda', 'https://some-random-api.ml/animal/cat', 'https://some-random-api.ml/animal/fox', 'https://some-random-api.ml/animal/red_panda', 'https://some-random-api.ml/animal/koala', 'https://some-random-api.ml/animal/birb', 'https://some-random-api.ml/animal/raccoon', 'https://some-random-api.ml/animal/kangaroo']
            link = random.choice(links)
            resp = requests.get(link)
            content = resp.json() #We have a dict now.
            em = discord.Embed(title = link.split('/')[-1].title().replace('_', ' '), description = content['fact'], url = content['image'])
            em.set_image(url = content['image'])
            await ctx.channel.send(embed = em)
        except:
            await ctx.channel.send(f"Recieved a bad status code of {resp.status_code}.")

    @commands.command(aliases = ['ttt'])
    async def tictactoe(self, ctx, user:discord.Member = None):
        """Play tictactoe with anyone"""
        if user == None:
            await ctx.channel.send('Specify a user to play with.')
        elif user == ctx.author:
            await ctx.channel.send('You cannot play with yourself. (That\'s sad btw)')
        else:
            players = [ctx.author.id, user.id]

            img = Image.new("RGBA", (900, 900), (0, 0, 0, 255))

            # x = Image.new("RGBA", (292, 292), (255, 255, 255, 0))
            # o = Image.new("RGBA", (292, 292), (255, 255, 255, 0))
            # img_x = ImageDraw.Draw(x)
            # img_x.line([(30, 30), (262, 262)], fill = 'red', width = 15)
            # img_x.line([(262, 30), (30, 262)], fill = 'red', width = 15)
            # img_o = ImageDraw.Draw(o)
            # img_o.arc([(30, 30), (262, 262)], 0, 360, fill = 'blue', width = 15)

            img_edit = ImageDraw.Draw(img)
            img_edit.rectangle([(296, 4), (304, 896)], fill = 'white')
            img_edit.rectangle([(596, 4), (604, 896)], fill = 'white')
            img_edit.rectangle([(4, 296), (896, 304)], fill = 'white')
            img_edit.rectangle([(4, 596), (896, 604)], fill = 'white')
            # img.paste(o, (4, 4), o)
            # img.paste(x, (304, 304), x)
            
            img.save(r'cogs/media/tictactoe.png')
            x = Image.open(r'cogs/media/x.png')
            o = Image.open(r'cogs/media/o.png')
            # x.save(r'C:\Users\dange\OneDrive\Desktop\Portfolio\Discord\tictactoe\x.png')
            # o.save(r'C:\Users\dange\OneDrive\Desktop\Portfolio\Discord\tictactoe\o.png')
            # await ctx.channel.send('saved.')
            player1 = user.id #random.choice(players)
            players.remove(player1)#
            player2 = ctx.author.id #players[0]
            players = [player1, player2]
            print(player1, player2)
            emb = discord.Embed(title = f'{ctx.author.display_name} started a game of tictactoe against {user.display_name}!', description = f'<@{player1}> goes first! (X)')
            imag = discord.File(r'cogs/media/tictactoe.png', filename = 'imag.png')
            emb.set_image(url = 'attachment://imag.png')
            # await ctx.channel.send(f'{ctx.author.display_name} started a game of tictactoe!')
            ticMsg = await ctx.channel.send(file = imag, embed = emb)

            places = [(4, 4), (304, 4), (604, 4), (4, 304), (304, 304), (604, 304), (4, 604), (304, 604), (604, 604)]
            spaces = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
            wins = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3'], ['c1', 'c2', 'c3'], ['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'], ['a3', 'b3', 'c3'], ['a1', 'b2', 'c3'], ['a3', 'b2', 'c1']]
            board = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']

            self.client.tictacstart = 1
            print(players)

            def check (message):
                print(str(message.content) in spaces and message.author.id in players)
                return str(message.content) in spaces and message.author.id in players
            
            turn = 1
            gameOver = False
            pOnePlays = []
            pTwoPlays = []
            totalPlays = []
            while gameOver == False:
                try:
                    msg = await self.client.wait_for('message', check = check, timeout = 30)

                    if msg.content in totalPlays:
                        await ctx.channel.send('You can\'t play there.')
                        continue

                    totalPlays.append(msg.content)

                    if turn % 2 == 1:
                        rightPlayer = player1
                        pOnePlays.append(msg.content)
                    else:
                        rightPlayer = player2
                        pTwoPlays.append(msg.content)

                    if msg.author.id != rightPlayer:
                        notTurn = await ctx.channel.send('Not your turn.')
                        await asyncio.sleep(1)
                        await msg.delete()
                        await notTurn.delete()
                    elif msg.author.id == rightPlayer:
                        print('right player')
                        index = spaces.index(msg.content)
                        loc = places[index]
                        if turn % 2 == 1:
                            img.paste(x, loc, x)
                        else:
                            img.paste(o, loc, o)
                        img.save('cogs/media/tictactoe.png', as_attachment = True)
                        em = discord.Embed(title = f'{ctx.author.display_name} started a game of tictactoe against {user.display_name}!', description = f'<@{player1}> went first! (X)')
                        image = discord.File(r'cogs/media/tictactoe.png', filename = 'image.png')
                        em.set_image(url = 'attachment://image.png')
                        await ticMsg.delete()
                        ticMsg = await ctx.channel.send(file = image, embed = em)
                        await msg.delete()
                        
                        for set in wins:
                            count = 0
                            for spot in set:
                                if turn % 2 == 1:
                                    if spot in pOnePlays:
                                        count += 1
                                        continue
                                else:
                                    if spot in pTwoPlays:
                                        count += 1
                                        continue
                            if count == 3:
                                break
                            count = 0

                        if count == 3:
                            winner = rightPlayer
                            gameOver = True
                        
                        print(totalPlays)
                        if sorted(totalPlays) == board:
                            winner = None
                            gameOver = True

                        turn += 1
                except TimeoutError:
                    if turn == 1:
                        winner = player2
                    else:
                        winner = rightPlayer
                        gameOver = True
                except asyncio.TimeoutError:
                    if turn == 1:
                        winner = player2
                    else:
                        winner = rightPlayer
                        gameOver = True

            if winner == None:
                winMsg = 'It was a draw!'
            else:
                winMsg = f'<@{winner}> won the game!'
            embe = discord.Embed(title = f'{ctx.author.display_name} started a game of tictactoe against {user.display_name}!', description = f'<@{player1}> went first! (X)\n\n{winMsg}')
            imge = discord.File(r'cogs/media/tictactoe.png', filename = 'imge.png')
            embe.set_image(url = 'attachment://imge.png')
            await ticMsg.delete()
            await ctx.channel.send(file = imge, embed = embe)

    @commands.command(aliases = ['profilepic', 'pfp'])
    async def profilepicture(self, ctx, user:discord.Member = None):
        if user == None:
            user = ctx.author

        pfp = user.avatar_url
        # pfp = BytesIO(await asset.read())
        # await ctx.channel.send(file = discord.File(pfp))
        await ctx.channel.send(pfp)

    @commands.command(hidden = True)
    async def send(self, ctx, channel:int, *, msg:str):
        if ctx.author.id == 485123430010585101:
            '''for server in self.client.guilds:
                print(server, server.id)'''
            try:
                sChannel = self.client.get_channel(channel)
                await sChannel.send(msg)
            except:
                user = (self.client.get_user(int(channel)))
                sChannel = await user.create_dm()
                await sChannel.send(msg)
        else:
            await ctx.channel.send('You are not the owner of this bot.')


def setup(client):
    client.add_cog(fun(client))
    
    
    '''@commands.command(aliases = ['userbanner', 'profilebanner', 'usercard', 'profilecard'])
    async def banner(self, ctx, user:discord.Member = None):
        if user == None:
            user = ctx.author
        userid = user.id

        req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{userid}/{banner_id}?size=1024"
        try:
            await ctx.channel.send(banner_url)
        except:
            await ctx.channel.send('No Banner')'''