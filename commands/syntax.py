import bot
import discord


def import_command():
        # Create Command Group
    syntaxCommands = discord.app_commands.Group(
        name='syntax',
        description='Get the syntax for the respective game'
    )

    # Add Command Group to Tree
    bot.commands.add_command(syntaxCommands)

    # Main Command
    @syntaxCommands.command(
        name="uno",
        description="Get UNO In-Game Syntax"
    )
    async def self(Interaction:discord.Interaction):
        embed = discord.Embed(title='UNO Game Syntax', description='{card color} {card type / number}')
        embed.add_field(name='Card Names', value='Red, Yellow, Green, Blue, Wild', inline=False)
        embed.add_field(name='Type Names', value='Skip, Reverse, Draw, Pick', inline=False)
        embed.add_field(name='Examples', value='Red 7\nBlue Skip\nWild Pick\nGreen Draw\nYellow Reverse', inline=False)
        await Interaction.response.send_message(embed=embed)
