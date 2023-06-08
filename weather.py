from pprint import pprint

import pandas as pd
import plotly.express as px
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook1 = ""
webhook = DiscordWebhook(url=webhook1)
# create embed object for webhook
embed = DiscordEmbed(title='Woodbridge Air Quality',
                     description='The air quality with Canada\'s wildfires', color='eb346b')

weather_link = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=&longitude=&hourly=pm10,pm2_5&timezone=America%2FNew_York"

r = requests.get(weather_link)
# if response type was set to JSON, then you'll automatically have a JSON response here...
df = pd.DataFrame.from_dict(r.json()["hourly"])


fig = px.line(df, x="time", y="pm2_5", title="Woodbridge Weather", labels={
    "pm2_5": "pm"
},)
fig.add_scatter(x=df["time"], y=df["pm10"], mode="lines")

fig.update_traces(showlegend=False)

fig.write_image("fig1.png")
# Set saved local image inside webhook
with open("fig1.png", "rb") as f:
    webhook.add_file(file=f.read(), filename='fig1.png')
embed.set_image(url='attachment://fig1.png')

# add embed object to webhook
webhook.add_embed(embed)

response = webhook.execute()
