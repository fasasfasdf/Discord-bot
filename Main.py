
import discord
from discord.ext import commands
import re
from datetime import timedelta

TOKEN = "MTQ3ODU1MDIzOTk2NjM5NjQ3OQ.G4DzLH.AWQIkuiDoGbN5c2mfmQuS9_qGogjsvrw4i62js"

ALLOWED_CODE = "cvupayqegG"

# Put the channel IDs where you want this enforced
ALLOWED_CHANNEL_IDS = [
    1477786983555403798,  # replace with your channel ID
]

TIMEOUT_DURATION = 120  # seconds (120 = 2 minutes)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # required for timeout

bot = commands.Bot(command_prefix="!", intents=intents)

INVITE_REGEX = re.compile(
    r"(?:https?:\/\/)?(?:www\.)?(?:discord\.gg|discord\.com\/invite)\/([a-zA-Z0-9]+)"
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Only enforce in chosen channels
    if message.channel.id not in ALLOWED_CHANNEL_IDS:
        return

    # Ignore admins and users with Manage Messages permission
    if message.author.guild_permissions.administrator or \
       message.author.guild_permissions.manage_messages:
        return

    matches = INVITE_REGEX.findall(message.content)

    if matches:
        for code in matches:
            if code != ALLOWED_CODE:
                try:
                    await message.delete()

                    # Timeout the user
                    await message.author.timeout(
                        timedelta(seconds=TIMEOUT_DURATION),
                        reason="Unauthorized Discord invite link"
                    )

                    await message.channel.send(
                        f"{message.author.mention} was timed out for posting an unauthorized invite.",
                        delete_after=5
                    )

                except discord.Forbidden:
                    print("Missing permissions to delete or timeout.")
                break

    await bot.process_commands(message)

bot.run(TOKEN)