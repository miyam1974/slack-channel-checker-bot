#!/usr/bin/env python3
#
# Slack Channel Checker Bot
#   This bot posts the number of posts on all channels during the target days.
#
# [Slack Setting]
#   (URL)
#     https://api.slack.com/apps
#
#   (Token)
#     Slack App
#       > OAuth & Permissions
#         > Bot User OAuth Access Token
#
#   (Scopes)
#     Slack App
#       > OAuth & Permissions
#         > Scopes
#           > Bot Token Scopes
#               channels:read
#               channels:history
#               channels:join
#               channels:manage 
#               chat:write
#
#   (See Also)
#      https://api.slack.com/methods
#
# [Mode Argument Matrix]
#   +----------------------+
#   |mode    |argument     |
#   +--------+-------------+
#   |normal  |normal or "" |
#   |join    |join         |
#   |leave   |leave        |
#   +----------------------+
#
# [Action Mode Matrix]
#   +---------------------+------+------+------+
#   |action / mode        |normal|join  |leave |
#   +---------------------+------+------+------+
#   |1. get channel list  |  do  |  do  |  do  |
#   |2. join channel      |  do  |  do  |  --  |
#   |3. leave channel     |  --  |  --  |  do  |
#   |4. get channel posts |  do  |  --  |  --  |
#   |5. post result       |  do  |  --  |  --  |
#   +---------------------+------+------+------+
#
# ------------------------------------------------------------------------------
# SETTTING (Change ppropriately)
# ------------------------------------------------------------------------------
token           = "pleease input"
post_channel_id = "pleease input"
target_days     = 1
tz_hours        = +9
tz_name         = "JST"
# ------------------------------------------------------------------------------
# SCRIPT (No changes required)
# ------------------------------------------------------------------------------
url1  = "https://slack.com/api/conversations.list"
url2  = "https://slack.com/api/conversations.join"
url3  = "https://slack.com/api/conversations.leave"
url4  = "https://slack.com/api/conversations.history"
url5  = "https://slack.com/api/chat.postMessage"

normal = "normal"
join   = "join"
leave  = "leave"

import requests
import json
import pprint
import socket
import os
import sys
import pwd
from datetime import datetime,timedelta,timezone

def main():
    host = socket.gethostname()
    ip   = socket.gethostbyname(host)
    file = os.path.basename(__file__)

    # ------------------
    # 0: mode check (normal / join / leave)
    # ------------------ 
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == normal:
            mode = normal
        if sys.argv[1].lower() == join:
            mode = join
        if sys.argv[1].lower() == leave:
            mode = leave
    else:
        mode = normal
    # ------------------
    # 1: get channel list
    # ------------------
    text     = ""
    oldest   = (datetime.now(timezone(timedelta(hours = tz_hours), tz_name)) - timedelta(days = target_days))
    payload1 = {
        "token"           : token,
        "exclude_archived": "true"
    }
    response1  = requests.get(url1, params=payload1)
    json_data1 = response1.json()
    channels   = json_data1["channels"]

    for i in channels:
        # ------------------
        # 2: join channel
        # ------------------
        if mode == normal or mode == join:
            payload2 = {
                "token"   : token,
                "channel" : i["id"]
            }
            response2 = requests.get(url2, params=payload2)
        # ------------------
        # 3: leave channel
        # ------------------
        if mode == leave:
            payload3 = {
                "token"   : token,
                "channel" : i["id"]
            }
            response3 = requests.get(url3, params=payload3)
        # ------------------
        # 4: get channel posts
        # ------------------
        if mode == normal:
            payload4 = {
                "token"   : token,
                "channel" : i["id"],
                "oldest"  : oldest.timestamp()
            }
            response4  = requests.get(url4, params=payload4)
            json_data4 = response4.json()
            if json_data4["ok"] == True and len(json_data4["messages"]) != 0:
                text += "#" + i["name"]  + " " + str(len(json_data4["messages"])) + " posts\n"
    # ------------------
    # 5: post result
    # ------------------
    if mode == normal:
        if text != "":
            text  = "Posts after " + oldest.strftime('%Y/%-m/%-d %-H:%M') + " " + tz_name + "\n" + text + "\n"
            text += "Posted from: %s (%s):%s" % (host, ip, file)+ "\n"
            print(text)
            payload5 = {
                "token"     : token,
                "channel"   : post_channel_id,
                "link_names": "true",
                "text"      : text
            }
            response5 = requests.get(url5, params=payload5)

if __name__ == '__main__':
    main()
# ------------------------------------------------------------------------------
