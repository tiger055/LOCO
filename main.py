  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'fetch' # change to what you need
#BOT_OWNER_ROLE_ID = "597332392637890571"
  
 

 
oot_channel_id_list = [
    "593990608914219008", #loco galaxy
	"607613349491900436", #loco IQ
    "569420128794443776", #loco unt
    "569502072945377290", #indian loco
	"595635734904307742", #tf loco
	"612177236107460618",#sani loco
	"591498350562377741",#planet loco
	"605443517069656084", #tf confetti
	"593990638916075520", #galaxy confett
	"590583414541910018",# confetti IQ
	"591294134564683809", #indian confetti
	"588070986554015764",#unt confetti
	"609405529575653387",# kingdom confetti
	"612177284471717894",#sani confetti
	"591498756562878475",#planet confetti
	"595639586726740049",#tf hq
	"591068955523809328",#hq galaxy
	"580198028950896640",#HQ tribe
        "459842150323060736",#hq dimensions
        "513818250652680213",#hq world
        "569420198717816852",#hq unt
	"568617830258442255"#hq revolution
	"598669844983840779",#cashquiz dimension
	"446448458090545172",#cashquiz tribe
	"610713322509303809",#cashquiz galaxy
	"595639664300392472",#cashquiz tf
	"596527077402869770",#theq tf
	"501220538518077440",#theq dimensions
	"446448458090545172",#theq tribe
	"513818839008673833",#theq world
	"569420278006808586",#theq unt
	"580208596139245601",#theq revolution
	"535675285211971584",#swagIQ world
	"595639769904447502",#swagIQ tf
	"446448437119025154",#swagIQ tribe
	"501220306128601098",#swagIQ dimension
	"570794448808837131",#swagIQ revolution
	"514915010955313153",#confeti vietnam world
	"595640787933331466",#confetti vietnam tf
	"501219307477532674",#confeti vietnam dimension
	"571241319658291200",#confeti vietnam unt
	"609003338675126272",#confetti vietnam pride
	"611439844996153375",#confetti mexico pride
	"611980037243273220",#confettimexico pride
	"611751492054941696",#confetti mexico
]


answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 500
nomarkscore = 300
markscore = 200

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="**__TRIVIA SAVAGE | PRO__**", description="**Web Searching** :spy:")
        self.embed.set_author(name ='',url=' ',icon_url='https://images-ext-2.discordapp.net/external/aMZ8_Dhu3Cib5U1l--xzP6QVgEV6bzjPDLMC-gNawWY/https/cdn.discordapp.com/attachments/577373201164795904/585046581506605076/ezgif-2-2f5a82b8174f.gif?width=225&height=225')
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/595713706411819033/604679180201754674/image0.png")
        self.embed.add_field(name="Option I", value="0", inline=False)
        self.embed.add_field(name="Option II", value="0", inline=False)
        self.embed.add_field(name="Option III", value="0", inline=False)
        self.embed.set_footer(text=f"CAPTAIN COOL#0044",\
            icon_url="https://cdn.discordapp.com/attachments/595713706411819033/604679180201754674/image0.png")
        self.embed.add_field(name="Suggested Answer!:", value="0", inline=True)

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        best_answer = ' :hourglass: '
        

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        best_answer = ' :hourglass: '
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = "<:white_check_mark:601397380507500549>"
                best_answer = ':one:'
            else:
                one_check = "<:x:600303220417626120>"

            if answer == 2:
                two_check = "<:white_check_mark:601397380507500549>"
                best_answer = ':two:'
            else:
                two_check = "<:x:600303220417626120>"

            if answer == 3:
                three_check = "<:white_check_mark:601397380507500549>"
                best_answer = ':three:'
            else:
                three_check = "<:x:600303220417626120>"

            

        #if lowest < 0:
            #if answer == 1:
                #one_cross = ":x:"
            #if answer == 2:
                #two_cross = ":x:"
            #if answer == 3:
                #three_cross = ":x:"            
 
        self.embed.set_field_at(0, name="Option I", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="Option II", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="Option III", value="**{0}**{1}".format(lst_scores[2], three_check))
        self.embed.set_field_at(3, name="Suggested Answer!:", value=best_answer, inline=True)


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Game(name='Trivia with Captain Cool||*help'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "*":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                #await self.embed_msg.add_reaction("✔️")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return

        if message.content.startswith('*help'):
          await message.delete()
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="Help Commands", description="**How Run Bot**", color=0x00ff00)
           embed.add_field(name="Support Game", value="**Loco\nConfetti-India\nFlipkart\nJeetoh\nHQ Trivia\nCashquiz\nSwag IQ\nThe Q\nConfetti Vietnam\nConfetti mexico**", inline=False)
           embed.add_field(name="when Question come put command", value=" `*` **is command work for all support game except**\n**`*j` is command of jeetoh**\n**`*f` is command for filpkart**\n\n**use cmd! in particular channels**\n\n**FOR MORE INFO CONTACT TO CAPTAIN COOL#0044**", inline=False)
           await message.channel.send(embed=embed)
          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('bot_token_here'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('self_token_here',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
