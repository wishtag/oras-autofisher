from discord_webhook import DiscordWebhook, DiscordEmbed
webhook = DiscordWebhook(url="", username="Sparkles")
embed = DiscordEmbed(title=f"Done Capturing Encounters", description=f"I finished lol", color="FCDE3A")
webhook.add_embed(embed)
response = webhook.execute()
