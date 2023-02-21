import discord
import functions
import random

UNOGameCount = 0
currentGames = {}

async def showHand(client: discord.Client, participant, thread, emojis: dict):
    message = f'Cards in user `{participant.user.display_name}`s Hand:'
    message2 = ''
    for card in participant.hand:
        emoji = functions.getCardEmoji(card.color, card.type, card.number, emojis)
        message2 += str(emoji)
    await thread.send(message)
    await thread.send(message2)

async def startGame(client: discord.Client, reaction: discord.Reaction, game: functions.unoGame.pending, emojis: dict):
    for guild in client.guilds:
        global exists
        exists = False
        for category in guild.categories:
            if 'UNO' in category.name:
                exists = True
                global UNOGameCount
                UNOGameCount += 1
                gameChannel = await category.create_text_channel(f'uno-game-{UNOGameCount}')
                for reactions in reaction.message.reactions:
                    if reactions.emoji == '✅':
                        users = []
                        async for user in reactions.users():
                            if not user.bot:
                                users.append(user)
                        unoGame = functions.unoGame(gameChannel,game.leader,users)
                        for participant in unoGame.participants:
                            participant: functions.unoGame.participant
                            if not participant.user.bot:
                                thread = await gameChannel.create_thread(name=participant.user.name, type=discord.ChannelType.private_thread)
                                await thread.send(participant.user.mention)
                                await showHand(client, participant, thread, emojis)
                        await gameChannel.send(f'Current Card:')
                        await gameChannel.send(functions.getCardEmoji(unoGame.currentCard.color, unoGame.currentCard.type, unoGame.currentCard.number, emojis))
                        currentGames[f'uno-game-{UNOGameCount}'] = unoGame

async def play(channel: discord.TextChannel, message: discord.Message, emojis: dict):
    unoGame: functions.unoGame = currentGames[channel.name]
    colors = [
            'red',
            'yellow',
            'blue',
            'green',
            'wild'
    ]
    specialCards = [
            'skip',
            'reverse',
            'draw',
            'pick'
    ]
    global found
    found = False

    ''' Check If Command represents a Valid Card'''
    for color in colors:
        print(color)
        rangee = range(10)
        for number in rangee:
            print(number)
            for specialCard in specialCards:
                if color in message.content.lower() and str(number) in message.content.lower() or color in message.content.lower() and specialCard in message.content.lower():
                    if color in message.content.lower() and specialCard in message.content.lower():
                        specifiedCard = functions.unoGame.card(color,number,specialCard)
                    else:
                        specifiedCard = functions.unoGame.card(color,number)
                    found = True
                    global found2
                    found2 = False
                    for participant in unoGame.participants:
                        participant: functions.unoGame.participant
                        if message.author == participant.user:
                            for card in participant.hand:
                                card: functions.unoGame.card
                                if card.color == specifiedCard.color and card.number == specifiedCard.number and card.type == specifiedCard.type:
                                    print('you have this card')
                                    if specifiedCard.color == unoGame.currentCard.color or specifiedCard.number == unoGame.currentCard.number or specifiedCard.color == 'wild':
                                        print('card valid')
                                        await message.channel.send('you can play that card')
                                        found2 = True
                                    else:
                                        print('card invalid')
                                        await message.channel.send('you cannot play that card')
                                        found2 = True
                                else:
                                    print('you dont have this card')
                                    await message.channel.send('you dont have this card')
                                    found2 = True
                                if found2: break
                        if found2: break
                if found: break
            if found: break
        if found: break

    if not found:
        await message.channel.send('not a card')




