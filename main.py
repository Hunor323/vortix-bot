import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLES_FILE = "roles.json"

def load_roles():
    if os.path.exists(ROLES_FILE):
        with open(ROLES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_roles(roles):
    with open(ROLES_FILE, "w") as f:
        json.dump(roles, f, indent=4)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online and running on {len(bot.guilds)} servers!')
    await bot.change_presence(activity=discord.Game(name=f"!setrole | {len(bot.guilds)} servers"))

@bot.command()
@commands.has_permissions(administrator=True)
async def setrole(ctx, role: discord.Role):
    roles = load_roles()
    guild_id = str(ctx.guild.id)
    
    roles[guild_id] = role.id
    save_roles(roles)
    
    await ctx.send(f"✅ **Auto-role configured!** New members will automatically receive the **{role.name}** role.")

@bot.event
async def on_member_join(member):
    roles = load_roles()
    guild_id = str(member.guild.id)
    
    if guild_id in roles:
        role_id = roles[guild_id]
        role = member.guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
                print(f"Added role '{role.name}' to {member.name} in {member.guild.name}")
            except discord.Forbidden:
                print(f"Missing permissions to assign role in {member.guild.name}")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    TOKEN = "MTU1MzgyMjMzNTgxNDA4MjU2MA.GXcl8A.IboTkxa_wB6L8GV_xbOzb2wrflDxmJNJspC_B0"

bot.run(TOKEN)