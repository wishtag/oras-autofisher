import json
from discord_webhook import DiscordWebhook, DiscordEmbed

def read_json(file):
    f = open (file, "r")
    data = json.loads(f.read())
    f.close()
    return data

def write_json(file, object):
    f = open (file, "w")
    json.dump(object, f)
    f.close()

encounter_names = ["Barboach", "Magikarp", "Goldeen"]

encountered = 1

resets = read_json("resets.json")

seconds = resets["total_seconds_since_last_shiny"]
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60
since_last_shiny_time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

seconds = resets["total_seconds"]
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60
time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

webhook = DiscordWebhook(url="", username="Sparkles")
with open("img/screenshot.png", "rb") as f:
    webhook.add_file(file=f.read(), filename="screenshot.png")
embed = DiscordEmbed(title=f"Shiny {encounter_names[encountered]} Found", description=f"{resets['resets_since_last_shiny']} encounters since last shiny over the span of {since_last_shiny_time_formatted}, with a chain of {resets['chain']}", color="FCDE3A")
embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
embed.set_image(url="attachment://screenshot.png")
embed.add_embed_field(name="Total Encounters", value=resets['resets'])
embed.add_embed_field(name="Total Time", value=time_formatted)
embed.set_footer(text="Alpha Sapphire")
embed.set_timestamp()
webhook.add_embed(embed)
response = webhook.execute()