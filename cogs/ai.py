import discord
from discord.ext import commands
from utils import log
from datetime import datetime, timedelta
import json 
import numpy as np
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #so tf doesnt complain about not having a gpu lol
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import random
import pickle
import asyncio
from db import db

model = keras.models.load_model("./ai/chat_model")

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            context = await self.client.get_context(message)
            if context.command:
                return
                
            if self.client.user.mentioned_in(message):
                with open("./ai/tokenizer.pickle", "rb") as handle:
                    tokenizer = pickle.load(handle)

                with open("./ai/label_encoder.pickle", "rb") as enc:
                    lbl_encoder = pickle.load(enc)

                max_len = 20

                with open("./ai/intents/intents.json") as file:
                    data = json.load(file)
                    inp = message.content
                    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating="post", maxlen=max_len))
                    tag = lbl_encoder.inverse_transform([np.argmax(result)])

                    for i in data["intents"]:
                        if i["tag"] == tag:
                            response = np.random.choice(i["responses"])
                            
                            async with message.channel.typing():
                                await asyncio.sleep(1)
                                await message.reply(response, mention_author=False)

def setup(client):
    client.add_cog(AI(client))