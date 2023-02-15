import discord
import time

class unoGame():
    def __init__(self, startMessage: discord.Message, leader: discord.User) -> None:
        self.message = startMessage
        self.leader = leader

async def checkForCategory(client: discord.Client, name: str):
        for guild in client.guilds:
            global exists
            exists = False
            for category in guild.categories:
                if name in category.name:
                    exists = True
            if not exists:
                errorMessages = {
                    'discord.errors.Forbidden': f'Bot in `{guild.name}` requires permission: `MANAGE_CHANNELS`',
                    'discord.errors.HTTPException': f'An Unknown error occurred for Bot in `{guild.name}`'
                }
                try:
                    await guild.create_category(name)
                except Exception as exception:
                    dm = await guild.owner.create_dm()
                    await dm.send(errorMessages[str(exception.__class__)[8:-2]])

