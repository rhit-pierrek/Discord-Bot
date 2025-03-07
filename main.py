import discord
import os
import requests
import json
import random
import firebase_admin
from firebase_admin import credentials, firestore
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
cred = credentials.Certificate("discordbotmessages-firebase-adminsdk-fbsvc-d964f02bf9.json")  # Ensure this file is in your project folder
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Bot with Command Prefix
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Required for welcome/goodbye messages

bot = commands.Bot(command_prefix="!", intents=intents)

# Encouragement & Filtered Words
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "kms", "kill myself"] 
bad_words = ["fuck", "shit", "nigga", "nigger", "bitch", "slut", "hoe", "cunt", "asshole", "faggot"]  

starter_encouragements = [
    "You got this!", "You are a great person!", "You are amazing!", 
    "DONT STOPPPP BELIEVING!", "Lock in!", "That's not very sigma of you"
]

# 🔹 Function to Log Moderator Actions to Firestore
def log_mod_action(action, mod, target, reason):
    db.collection("mod_logs").add({
        "action": action,
        "moderator": mod,
        "target": target,
        "reason": reason,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

# 🔹 Get a Quote from ZenQuotes API
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return json_data[0]['q'] + " -" + json_data[0]['a']

# ✅ BOT READY MESSAGE
@bot.event 
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')

# ✅ AUTO-MODERATION: Delete Offensive Words
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

    if any(word in msg for word in bad_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, your message was removed for violating rules.")

    await bot.process_commands(message)  # Process other bot commands

# ✅ GREET NEW MEMBERS
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")  # Change to your welcome channel
    if channel:
        await channel.send(f"🎉 Welcome {member.mention} to {member.guild.name}! Read the rules and have fun.")

# ✅ FAREWELL MESSAGE WHEN MEMBERS LEAVE
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")  # Change to your goodbye channel
    if channel:
        await channel.send(f"😢 {member.mention} has left the server.")

# ✅ KICK COMMAND (LOGGED TO FIREBASE)
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    log_mod_action("Kick", ctx.author.name, member.name, reason)
    await ctx.send(f"👢 {member.mention} has been kicked. Reason: {reason}")

# ✅ BAN COMMAND (LOGGED TO FIREBASE)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    log_mod_action("Ban", ctx.author.name, member.name, reason)
    await ctx.send(f"⛔ {member.mention} has been banned. Reason: {reason}")

# ✅ UNBAN COMMAND
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    banned_users = await ctx.guild.bans()
    user = discord.utils.get(banned_users, user__id=user_id)

    if user:
        await ctx.guild.unban(user.user)
        log_mod_action("Unban", ctx.author.name, user.user.name, "User unbanned")
        await ctx.send(f"✅ {user.user.mention} has been unbanned.")
    else:
        await ctx.send(f"User with ID {user_id} is not banned.")

# ✅ MUTE COMMAND (LOGGED TO FIREBASE)
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not role:
        role = await ctx.guild.create_role(name="Muted")

    for channel in ctx.guild.channels:
        await channel.set_permissions(role, send_messages=False)

    await member.add_roles(role)
    log_mod_action("Mute", ctx.author.name, member.name, reason)
    await ctx.send(f"🔇 {member.mention} has been muted. Reason: {reason}")

# ✅ UNMUTE COMMAND
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role and role in member.roles:
        await member.remove_roles(role)
        log_mod_action("Unmute", ctx.author.name, member.name, "User unmuted")
        await ctx.send(f"🔊 {member.mention} has been unmuted.")
    else:
        await ctx.send(f"{member.mention} is not muted.")

# ✅ RETRIEVE MOD LOGS
@bot.command()
@commands.has_permissions(administrator=True)
async def modlogs(ctx):
    logs = db.collection("mod_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()
    
    log_messages = []
    for log in logs:
        data = log.to_dict()
        log_messages.append(f"**{data['action']}**: {data['target']} by {data['moderator']} - {data['reason']}")

    if log_messages:
        await ctx.send("\n".join(log_messages))
    else:
        await ctx.send("No moderation actions recorded.")

# ✅ RUN THE BOT
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("❌ Error: Discord bot token not found. Make sure it's in the .env file.")
    exit(1)

bot.run(TOKEN)
