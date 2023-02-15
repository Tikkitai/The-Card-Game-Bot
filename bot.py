import discord
from dotenv import load_dotenv
from os import getenv, listdir
import functions
import asyncio
import threading

def start():

    ''' Get Token '''
    load_dotenv()
    TOKEN = getenv('TOKEN')
    if TOKEN is None:
        raise NameError('TOKEN is not defined in .env file')

    ''' Bot Intents '''
    botIntents = discord.Intents.default()
    botIntents.guilds = True
    botIntents.members = True

    ''' Client Variables '''
    global client
    global commands
    client = discord.Client(intents=botIntents)
    commands = discord.app_commands.CommandTree(client)

    ''' Dynamic Variables '''
    global commandList
    global pendingUNOgames
    global UNOGameCount
    commandList = []
    pendingUNOgames = []
    UNOGameCount = 0

    ''' Events '''
    @client.event
    async def on_ready():
        print('Running')

        ''' Set Bot Status '''
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="card games"))
        print('Bot Presence changed to \"Playing card games\"')

        ''' Load Commands '''
        for command in listdir('commands'):
            for command in listdir('commands'):
                if command.endswith('py'):
                    if '__init__.py' not in command:
                        if 'template.py' not in command:
                            if command not in commandList:
                                exec(f'import commands.{command[:-3]}')
                                exec(
                                    f'commands.{command[:-3]}.import_command()')
                                commandList.append(command)

        ''' Sync Commands '''
        await commands.sync()

    @client.event
    async def on_interaction(interaction):
        await functions.checkForCategory(client, 'UNO')

    @client.event
    async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
        for game in pendingUNOgames:
            if reaction.message == game.message and user == game.leader and reaction.emoji == '👍':
                pendingUNOgames.remove(game)
                for guild in client.guilds:
                    global exists
                    exists = False
                    for category in guild.categories:
                        if 'UNO' in category.name:
                            exists = True
                            global UNOGameCount
                            UNOGameCount += 1
                            gameChannel = await category.create_text_channel(f'uno-game-{UNOGameCount}')
                            # gameStartMessage = await gameChannel.send('`UNO Game Start`')
                            for reactions in reaction.message.reactions:
                                if reactions.emoji == '✅':
                                    async for participant in reactions.users():
                                        if not participant.bot:
                                            thread = await gameChannel.create_thread(name=participant.name, type=discord.ChannelType.private_thread)
                                            await thread.send(participant.mention)
                        

        

    ''' Deploy Bot '''
    client.run(TOKEN)