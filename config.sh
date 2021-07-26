#!/bin/bash

echo "Welcome! Please answer all prompts properly to configure the bot." && sleep 2

#ask for the the client id
read -p "Please enter the client id(https://discord.com/developers/applications): " CLIENT_ID

#ask for the statcord id
read -p "Please enter the statcord id(https://statcord.com/profile): " STATCORD_ID

#ask for the admin ids
read -p "Please enter the admin ids(Your discord ID. Add a comma between ids for multiple admins): " ADMIN_IDS

#ask for the primary color
read -p "Please enter the primary color: " PRIMARY_COLOR

#ask for the secondary color
read -p "Please enter the secondary color: " SECONDARY_COLOR

#ask for the third color
read -p "Please enter the third color: " THIRD_COLOR
