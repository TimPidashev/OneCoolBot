import discord
from discord.ext import commands
from utils import data, embed, log
# from datetime import datetime, timedelta
# import json 
# import numpy as np
# from tensorflow import keras
# from sklearn.preprocessing import LabelEncoder
# import random
# import pickle
# import asyncio
# from db import db

class ai(commands.Cog):
    def __init__(self, client):
        self.client = client
        # model = keras.models.load_model('./ai/chat_model')

    async def on_ready(self):
        await log.cog_command(self)
        # db.connect("./data/database.db")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if not message.author.bot:
    #         context = await self.client.get_context(message)
    #         if context.command:
    #             return
                
    #         if not self.client.user.mentioned_in(message):
    #             ailock = db.record("SELECT AILock FROM users WHERE UserID = (?)", message.author.id)[0]
    #             if datetime.utcnow() > datetime.fromisoformat(ailock):
    #                 return

    #             else:
    #                 with open('./ai/tokenizer.pickle', 'rb') as handle:
    #                     tokenizer = pickle.load(handle)

    #                 with open('./ai/label_encoder.pickle', 'rb') as enc:
    #                     lbl_encoder = pickle.load(enc)

    #                 max_len = 20

    #                 with open("./ai/intents/intents.json") as file:
    #                     data = json.load(file)
    #                     model = keras.models.load_model('./ai/chat_model')
    #                     inp = message.content
    #                     result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))
    #                     tag = lbl_encoder.inverse_transform([np.argmax(result)])

    #                     for i in data['intents']:
    #                         if i['tag'] == tag:
    #                             response = np.random.choice(i['responses'])
                                
    #                             async with message.channel.typing():
    #                                 await asyncio.sleep(1)
    #                                 await message.reply(response, mention_author=False)

    #                                 db.execute("UPDATE users SET AILock = ?", (datetime.utcnow() + timedelta(seconds=5)).isoformat())
    #                                 db.commit()

                    
    #         if self.client.user.mentioned_in(message):
    #             ailock = db.record("SELECT AILock FROM users WHERE UserID = (?)", message.author.id)[0]
    #             if datetime.utcnow() > datetime.fromisoformat(ailock):
    #                 db.execute("UPDATE users SET AILock = ?", (datetime.utcnow() + timedelta(seconds=10)).isoformat())
    #                 db.commit()
                    

    #                 with open('./ai/tokenizer.pickle', 'rb') as handle:
    #                     tokenizer = pickle.load(handle)

    #                 with open('./ai/label_encoder.pickle', 'rb') as enc:
    #                     lbl_encoder = pickle.load(enc)

    #                 max_len = 20

    #                 with open("./ai/intents/intents.json") as file:
    #                     data = json.load(file)
    #                     model = keras.models.load_model('./ai/chat_model')
    #                     inp = message.content
    #                     result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))
    #                     tag = lbl_encoder.inverse_transform([np.argmax(result)])

    #                     for i in data['intents']:
    #                         if i['tag'] == tag:
    #                             response = np.random.choice(i['responses'])
                                
    #                             async with message.channel.typing():
    #                                 await asyncio.sleep(1)
    #                                 await message.reply(response, mention_author=False)

def setup(client):
    client.add_cog(ai(client))