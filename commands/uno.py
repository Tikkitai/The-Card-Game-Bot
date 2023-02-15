import bot
import functions
import discord

def import_command():

    unoCommands = discord.app_commands.Group(
        name='uno',
        description='uno'
    )
    bot.commands.add_command(unoCommands)

    @unoCommands.command(
        name='start',
        description='Start UNO Game'
    )
    async def self(interaction: discord.Interaction):
        await interaction.response.send_message('React with 👍 to start game',ephemeral=True)
        message = await interaction.channel.send(embed=discord.Embed(title=f'{interaction.user.name} would like to start an UNO Game', description='React Below to join'))
        await message.add_reaction('✅')
        bot.pendingUNOgames.append(functions.unoGame(message, interaction.user))
        print(bot.pendingUNOgames)