import discord
import os
import asyncio
import random
from discord.ext import tasks, commands
from itertools import cycle



prefix = '!'
bot = commands.Bot(command_prefix = prefix)
bot.remove_command('help')
status = cycle(["!help", "Dev by Gino", "Invite me"])

punch_gifs = ['https://c.tenor.com/UH8Jnl1W3CYAAAAM/anime-punch-anime.gif', 
'https://c.tenor.com/DKMb2QPU7aYAAAAM/rin243109-blue-exorcist.gif',
'https://c.tenor.com/gL_S5CIIhkgAAAAM/yuji-yuji-itadori.gif', 
'https://c.tenor.com/1I0Om7HbUscAAAAM/baki-anime.gif']
punch_names = ['Punches you!']

kiss_gifs = ['https://c.tenor.com/9jB6M6aoW0AAAAAM/val-ally-kiss.gif',
'https://c.tenor.com/4ofp_xCUBxcAAAAM/eden-of-the-east-akira-takizawa.gif',
'https://c.tenor.com/A4D3Mk-Y2h4AAAAM/chuunibyou-anime.gif']
kiss_names = ['Gave you a kiss!']



#|--------------------EVENTS--------------------|
@bot.event
async def on_ready():
    change_status.start()
    print("Bot is ready to use.")


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Oh no! Looks like you have missed out an argument for this command.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Oh no! Looks like you Dont have the permissions for this command.")
    if isinstance(error, commands.MissingRole):
        await context.send("Oh no! Looks like you Dont have the roles for this command.")
    #bot errors
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Oh no! Looks like I Dont have the permissions for this command.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Oh no! Looks like I Dont have the roles for this command.")
    
#|------------------COMMANDS------------------|   
@bot.command()
async def help(message):
    helpC = discord.Embed(title="Moderator Bot \nHelp Guide", description="discord bot built for moderation")
    helpC.set_thumbnail(url='https://cdn.discordapp.com/attachments/980797489315741746/980797514724827136/oie_vlSnWkOjZoe5.png')
    helpC.add_field(name="Clear", value="To use this command type ./clear and the number of messages you would like to delete, the default is 5.", inline=False)
    helpC.add_field(name="Kick/Ban/Unban", value="To use this command type ./kick/ban/unban then mention the user you would like to perform this on, NOTE: user must have permissions to use this command.", inline=False)
    helpC.add_field(name="Fun", value="To use this command type !kiss/!punch then mention the user you would like to perform this on", inline=False)
    helpC.add_field(name="Invite", value="To get the invite type !invite", inline=False)

    await message.channel.send(embed=helpC)
    
@bot.command()

@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'Member {member} kicked')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member} has been banned')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await bot.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} has been unbanned')
    

@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : discord.Member, days, reason=None):
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} has been softbanned')
    await asyncio.sleep(days)
    print("Time to unban")
    await member.unban()
    await context.send(f'{member} softban has finished')

@bot.command()
async def av(ctx, *, member: discord.Member=None): 
    await ctx.message.delete()
    if not member: 
        member = ctx.message.author 
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

@bot.command()
async def punch(ctx):
  embed = discord.Embed(
      colour=(discord.Colour.dark_gray()),
      description = f'{ctx.author.mention} {(random.choice(punch_names))}'
  )
  embed.set_image(url=(random.choice(punch_gifs)))

  await ctx.send(embed = embed)

@bot.command()
async def kiss(ctx):
  embed = discord.Embed(
      colour=(discord.Colour.dark_gray()),
      description = f'{ctx.author.mention} {(random.choice(kiss_names))}'
  )
  embed.set_image(url=(random.choice(kiss_gifs)))

  await ctx.send(embed = embed)


@bot.command()
async def invite(message):
    invite = discord.Embed(title="Invite", description="https://discord.com/api/oauth2/authorize?client_id=980788754811858964&permissions=8&scope=bot")
    await message.channel.send(embed=invite)


#|------------------TASKS------------------| 

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run('OTk1NzYyNjU1MjkxNzg1MjQ4.GnFFE4.3Y7aSCT0UHMCEQkhkzQqb3hKl1ls4ORSjVvJTM')
