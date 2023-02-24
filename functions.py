import discord
import time
import random







class unoGame():
    class participant():
        def __init__(self, member, deck: list) -> None:
            self.user = member
            hand = []
            rangee = range(7)
            for draw in rangee:
                cardDrawn = random.choice(deck)
                hand.append(cardDrawn)
                deck.remove(cardDrawn)
            self.hand = hand
            self.uno = False
     
    class card():
        def __init__(self, color, number: int, type: str = 'generic') -> None:
            self.color = color
            self.number = number
            self.type = type
            if type != 'generic':
                self.number = 10

    class pending():
        def __init__(self, message, leader) -> None:
            self.message: discord.Message = message
            self.leader: discord.Member = leader

    def __init__(self, channel, leader, members) -> None:
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
        self.channel: discord.TextChannel = channel
        self.leader: discord.Member = leader
        deck = []
        rangee = range(10)
        for number in rangee:
            if number == 0:
                for color in colors:
                    if color != 'wild':
                        deck.append(unoGame.card(color, number))
            else:
                for color in colors:
                    if color != 'wild':
                        deck.append(unoGame.card(color, number))
                        deck.append(unoGame.card(color, number))
        for card in specialCards:
            for color in colors:
                if color == 'wild':
                    if card == 'draw':
                        deck.append(unoGame.card(color, 10, card))
                        deck.append(unoGame.card(color, 10, card))
                        deck.append(unoGame.card(color, 10, card))
                        deck.append(unoGame.card(color, 10, card))
                    else:
                        if card == 'pick':
                            deck.append(unoGame.card(color, 10, card))
                            deck.append(unoGame.card(color, 10, card))
                            deck.append(unoGame.card(color, 10, card))
                            deck.append(unoGame.card(color, 10, card))

                elif card != 'pick':
                    deck.append(unoGame.card(color, 10, card))
                    deck.append(unoGame.card(color, 10, card))
        
                    
        self.deck = deck
        participants = []
        for participant in members:
            participantObj = unoGame.participant(participant,deck.copy())
            participants.append(participantObj)
            for card in participantObj.hand:
                self.deck.remove(card)

        self.participants = participants
        self.currentPlayer: unoGame.participant

        drawnCard = random.choice(self.deck)
        self.currentCard: unoGame.card = drawnCard
        self.deck.remove(drawnCard)

# testGame = unoGame(None,None,None)
# for card in testGame.deck:
#     print(f'{card.color} {card.type} {card.number}')
# print(f'{len(testGame.deck)} total cards')


async def checkPerms(guild: discord.Guild):
    requiredPermissions = [
        ('manage_channels', True),
        ('manage_messages', True),
        ('manage_roles', True),
    ]
    returnn = True
    for permission in requiredPermissions:
        permissions = iter(guild.self_role.permissions)
        if permission not in permissions:
            dm = await guild.owner.create_dm()
            await dm.send(f'Bot in `{guild.name}` requires permission: `{permission[0]}`')
            returnn = False
    return returnn

async def checkForCategory(client: discord.Client, name: str):
    exists = False
    for guild in client.guilds:
        for category in guild.categories:
            if category.name == name:
                exists = True

        if not exists:
            category = await guild.create_category(name)
            if name == 'UNO-ARCHIVE':
                permissions = discord.PermissionOverwrite()
                permissions.send_messages = False
                permissions.send_messages_in_threads = False
                permissions.create_private_threads = False
                permissions.create_public_threads = False
                await category.set_permissions(guild.default_role, overwrite=permissions)

def getCardEmoji(color, type, number, emojis: dict):
    emoji: discord.Emoji = emojis[f':{color}_{type}_{number}:']
    if emoji.animated:
        return f'<a:{emoji.name}:{emoji.id}>'
    else:
        return f'<:{emoji.name}:{emoji.id}>'