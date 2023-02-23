import discord
import functions
import random

UNOGameCount = 0
currentGames = {}

async def drawCard(game: functions.unoGame, participant: functions.unoGame.participant, amt: int, drawCommand: bool = False):
    rangee = range(amt)
    for draw in rangee:
        cardDrawn = random.choice(game.deck)
        participant.hand.append(cardDrawn)
        game.deck.remove(cardDrawn)
        cards = ''
        for card in game.currentPlayer.hand:
            cards += '<a:back:1075645084583866368>'
        if drawCommand:
            async for message in game.channel.history():
                message: discord.Message
                if '<a:back:1075645084583866368>' in message.content and message.author.bot:
                    await message.edit(content=cards)
                    break
    
async def showHand(client: discord.Client, participant, thread, emojis: dict):
    message = f'Cards in user `{participant.user.display_name}`s Hand:'
    message2 = ''
    for card in participant.hand:
        emoji = functions.getCardEmoji(card.color, card.type, card.number, emojis)
        message2 += str(emoji)
    await thread.send(message)
    await thread.send(message2)

async def playCard(type: int, client: discord.Client, unoGame: functions.unoGame, card: functions.unoGame.card, specifiedCard: functions.unoGame.card, player: functions.unoGame.participant, emojis: dict, color: str = ''):
    unoGame.currentCard = specifiedCard
    player.hand.remove(card)
    if type == 5:
        unoGame.participants.reverse()
        playOrderMessage = 'Current Play Order:'
        a = 0
    try:
        unoGame.currentPlayer = unoGame.participants[unoGame.participants.index(unoGame.currentPlayer)+1]
    except IndexError:
        unoGame.currentPlayer = unoGame.participants[0]
    if type == 2 or type == 3 or type == 4:
        if type == 2:
            await drawCard(unoGame, unoGame.currentPlayer, 4)
            message2 = f'{unoGame.currentPlayer.user.display_name} drew 4'
            cards = ''
            for card in unoGame.currentPlayer.hand:
                cards += '<a:back:1075645084583866368>'
        elif type == 3:
            await drawCard(unoGame, unoGame.currentPlayer, 2)
            message2 = f'{unoGame.currentPlayer.user.display_name} drew 2'
            cards = ''
            for card in unoGame.currentPlayer.hand:
                cards += '<a:back:1075645084583866368>'
        elif type == 4:
            message2 = f'{unoGame.currentPlayer.user.display_name} was Skipped'
        try:
            unoGame.currentPlayer = unoGame.participants[unoGame.participants.index(unoGame.currentPlayer)+1]
        except IndexError:
            unoGame.currentPlayer = unoGame.participants[0]
    for participant in unoGame.participants:
        participant: functions.unoGame.participant
        if not participant.user.bot:
            for guild in client.guilds:
                for category in guild.categories:
                    if category.name == 'UNO':
                        for channel in category.text_channels:
                            for thread in channel.threads:
                                if thread.name == participant.user.display_name:
                                    await showHand(client, participant, thread, emojis)
                                    if type == 5:
                                        a += 1
                                        if participant == unoGame.currentPlayer:
                                            playOrderMessage += f'\n{a}: **{participant.user.display_name}**'
                                            unoGame.currentPlayer = participant
                                        else: playOrderMessage += f'\n{a}: {participant.user.display_name}'
    if type == 5:
        await unoGame.channel.send(playOrderMessage)
    await unoGame.channel.send(f'Current Card:')
    await unoGame.channel.send(functions.getCardEmoji(unoGame.currentCard.color, unoGame.currentCard.type, unoGame.currentCard.number, emojis))
    if type == 1 or type == 2 or type == 3 or type == 4:
        if type == 2 or type == 3 or type == 4:
            await unoGame.channel.send(message2)
            if type == 2 or type == 3:
                await unoGame.channel.send(cards)
        if type == 1 or type == 2:
            unoGame.currentCard.color = color
            unoGame.currentCard.number = 11
            await unoGame.channel.send(f'Color is now **{color}**')
    await unoGame.channel.send(f'**It is now {unoGame.currentPlayer.user.mention}\'s Turn**')
    cards = ''
    for card in unoGame.currentPlayer.hand:
        cards += '<a:back:1075645084583866368>'
    await unoGame.channel.send(cards)
    currentGames[f'uno-game-{UNOGameCount}'] = unoGame

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
                        playOrderMessage = 'Current Play Order:'
                        a = 0
                        for participant in unoGame.participants:
                            participant: functions.unoGame.participant
                            if not participant.user.bot:
                                thread = await gameChannel.create_thread(name=participant.user.name, type=discord.ChannelType.private_thread)
                                await thread.send(participant.user.mention)
                                await showHand(client, participant, thread, emojis)
                                a += 1
                                if a == 1:
                                    playOrderMessage += f'\n{a}: **{participant.user.display_name}**'
                                    unoGame.currentPlayer = participant
                                else: playOrderMessage += f'\n{a}: {participant.user.display_name}'
                        await gameChannel.send(playOrderMessage)
                        await gameChannel.send(f'Current Card:')
                        await gameChannel.send(functions.getCardEmoji(unoGame.currentCard.color, unoGame.currentCard.type, unoGame.currentCard.number, emojis))
                        await gameChannel.send(f'**It is now {unoGame.currentPlayer.user.mention}\'s Turn**')
                        cards = ''
                        for card in unoGame.currentPlayer.hand:
                            cards += '<a:back:1075645084583866368>'
                        await unoGame.channel.send(cards)
                        currentGames[f'uno-game-{UNOGameCount}'] = unoGame

async def play(client: discord.Client, channel: discord.TextChannel, message: discord.Message, emojis: dict):
    unoGame: functions.unoGame = currentGames[channel.name]
    colors = [
            'wild',
            'red',
            'yellow',
            'blue',
            'green'
    ]
    specialCards = [
            'skip',
            'reverse',
            'draw',
            'pick'
    ]
    global found
    found = False
    ''' Check if using Draw Command '''
    if message.content.lower() == 'draw':
        for participant in unoGame.participants:
            participant: functions.unoGame.participant
            if message.author == participant.user and participant == unoGame.currentPlayer:
                await drawCard(unoGame, participant, 1, True)
                for guild in client.guilds:
                    for category in guild.categories:
                        if category.name == 'UNO':
                            for channel in category.text_channels:
                                for thread in channel.threads:
                                    if thread.name == participant.user.display_name:
                                        await showHand(client, participant, thread, emojis)
    else:
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
                                if participant == unoGame.currentPlayer:
                                    for card in participant.hand:
                                        card: functions.unoGame.card
                                        if card.color == specifiedCard.color and card.number == specifiedCard.number and card.type == specifiedCard.type:
                                            if specifiedCard.color == unoGame.currentCard.color or specifiedCard.number == unoGame.currentCard.number or specifiedCard.color == 'wild':
                                                # Generic Cards
                                                if specifiedCard.number != 10:
                                                    await playCard(0, client, unoGame, card, specifiedCard, participant, emojis)
                                                    found2 = True
                                                # Special Cards
                                                elif specifiedCard.color == unoGame.currentCard.color or specifiedCard.type == unoGame.currentCard.type or specifiedCard.color == 'wild':
                                                    # Pick Cards
                                                    if specifiedCard.type == 'pick':
                                                        for color in colors:
                                                            if message.content.endswith(color):
                                                                await playCard(1, client, unoGame, card, specifiedCard, participant, emojis, color)
                                                                found2 = True
                                                    # Draw Cards
                                                    elif specifiedCard.type == 'draw':
                                                        print('draw')
                                                        # Wild Draw Four
                                                        if specifiedCard.color == 'wild':
                                                            for color in colors:
                                                                if message.content.endswith(color):
                                                                    await playCard(2, client, unoGame, card, specifiedCard, participant, emojis, color)
                                                                    found2 = True
                                                        else:
                                                            # Normal Draw Two
                                                            await playCard(3, client, unoGame, card, specifiedCard, participant, emojis)
                                                            found2 = True
                                                    # Skip Cards
                                                    elif specifiedCard.type == 'skip':
                                                        await playCard(4, client, unoGame, card, specifiedCard, participant, emojis)
                                                        found2 = True
                                                    # Reverse Cards
                                                    elif specifiedCard.type == 'reverse':
                                                        await playCard(5, client, unoGame, card, specifiedCard, participant, emojis)
                                                        found2 = True
                                            # If Wild Card Is Current Card
                                            elif specifiedCard.color == unoGame.currentCard.color and unoGame.currentCard.number == 11:
                                                # Generic Cards
                                                if specifiedCard.number != 10:
                                                    await playCard(0, client, unoGame, card, specifiedCard, participant, emojis)
                                                    found2 = True
                                                # Special Cards
                                                elif specifiedCard.color == unoGame.currentCard.color or specifiedCard.type == unoGame.currentCard.type or specifiedCard.color == 'wild':
                                                    # Pick Cards
                                                    if specifiedCard.type == 'pick':
                                                        for color in colors:
                                                            if message.content.endswith(color):
                                                                await playCard(1, client, unoGame, card, specifiedCard, participant, emojis, color)
                                                                found2 = True
                                                    # Draw Cards
                                                    elif specifiedCard.type == 'draw':
                                                        print('draw')
                                                        # Wild Draw Four
                                                        if specifiedCard.color == 'wild':
                                                            for color in colors:
                                                                if message.content.endswith(color):
                                                                    await playCard(2, client, unoGame, card, specifiedCard, participant, emojis, color)
                                                                    found2 = True
                                                        else:
                                                            # Normal Draw Two
                                                            await playCard(3, client, unoGame, card, specifiedCard, participant, emojis)
                                                            found2 = True
                                                    # Skip Cards
                                                    elif specifiedCard.type == 'skip':
                                                        await playCard(4, client, unoGame, card, specifiedCard, participant, emojis)
                                                        found2 = True
                                                    # Reverse Cards
                                                    elif specifiedCard.type == 'reverse':
                                                        await playCard(5, client, unoGame, card, specifiedCard, participant, emojis)
                                                        found2 = True
                                            else:
                                                await message.channel.send('You Cannot Play That Card')
                                                found2 = True
                                        if found2: break
                                else:
                                    await message.channel.send('WAIT YOUR TURN')
                                    found2 = True
                                if found2: break
                    if found: break
                if found: break
            if found: break

        if not found:
            await message.channel.send('not a card')

        if not found2:
            await message.channel.send('you dont have this card')




