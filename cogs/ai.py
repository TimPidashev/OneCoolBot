import discord
from discord.ext import commands
from utils import data, embed, log
from datetime import datetime
import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import random
import pickle

#test channel
channel_name = "timmy-testin" # default channel name

with open('./ai/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

with open('./ai/label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

max_len = 20

class ai(commands.Cog):
    def __init__(self, client):
        self.client = client
        model = keras.models.load_model('./ai/chat_model')

    async def on_ready(self):
        await log.cog_command(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel == channel_name:
                with open("./ai/intents/intents.json") as file:
                    data = json.load(file)
                inp = message.content()
                result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))
                tag = lbl_encoder.inverse_transform([np.argmax(result)])
                
                # for i in data['intents']:
                #     if i['tag'] == tag:
                #         await message.reply(np.random.choice(i['responses'])

                


def setup(client):
    client.add_cog(ai(client))