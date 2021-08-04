import discord
import os
import json
from discord.ext import commands

with open('bot/config.json') as infile:
    config = json.load(infile)

with open('data/units.json') as infile:
    units = json.load(infile)

with open('data/courses.json') as infile:
    courses = json.load(infile)

client = commands.Bot(command_prefix=config['prefix'])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def info(ctx, *, args):
    for arg in args.split():
        unitcode = arg.upper()
        if unitcode in units:
            unitinfo = units[unitcode]
            embedVar = discord.Embed(
                title=unitcode,
                description=unitinfo['description'],
                color=0xf52c40
            )
            learningoutcomes = ''
            for outcome in unitinfo['outcomes'].values():
                learningoutcomes += '• ' + outcome + '\n'
            embedVar.add_field(
                name="Learning Outcomes",
                value=learningoutcomes.strip()
            )
            offerings = set()
            for offering in unitinfo['offerings'].values():
                offerings.add(offering['period'])
            offeredperiods = ''
            for offering in sorted(offerings):
                offeredperiods += '• ' + offering + '\n'
            embedVar.add_field(
                name="Offering Periods",
                value=offeredperiods.strip()
            )
            await ctx.send(embed=embedVar)

@info.error
async def info_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Put course or unit code(s) after command")

client.run(config['discord'])