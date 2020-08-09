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
# [Program File and Config File]
#   This program file can be renamed to any file name.
#   Prepare a config file in the same directory with the following name.
#   
#     Program File: /path/to/anyname.py
#     Config File:  /path/to/anyname-config.py
#
# [Mode Argument Matrix]
#   +---------------------+
#   |mode      |argument  |
#   +----------+----------+
#   |normal    |          |
#   |join      |join      |
#   |leave     |leave     |
#   |dry-run   |dry-run   |
#   +---------------------+
#
# [Action Mode Matrix]
#   +---------------------+--------+--------+--------+--------+
#   |action / mode        | normal | join   | leave  | dry-run|
#   +---------------------+--------+--------+--------+--------+
#   |1. get channel list  |   do   |   do   |   do   |   do   |
#   |2. join channel      |   do   |   do   |   --   |   do   |
#   |3. leave channel     |   --   |   --   |   do   |   --   |
#   |4. get channel posts |   do   |   --   |   --   |   do   |
#   |5. post result       |   do   |   --   |   --   |   --   |
#   |6. print result      |   do   |   --   |   --   |   do   |
#   +---------------------+--------+--------+--------+--------+
#
# ------------------------------------------------------------------------------
# SCRIPT (No changes required)
# ------------------------------------------------------------------------------
url1  = "https://slack.com/api/conversations.list"
url2  = "https://slack.com/api/conversations.join"
url3  = "https://slack.com/api/conversations.leave"
url4  = "https://slack.com/api/conversations.history"
url5  = "https://slack.com/api/chat.postMessage"

normal   = "normal"
join     = "join"
leave    = "leave"
dry_run  = "dry-run"

import requests
import json
import pprint
import socket
import os
import sys
import importlib
from datetime import datetime,timedelta,timezone

def main():
    host = socket.gethostname()
    ip   = socket.gethostbyname(host)
    file = os.path.basename(__file__)
    conf = os.path.splitext(os.path.basename(file))[0] + "-config"

    # ------------------
    # 0.1: config check
    # ------------------
    try:
        config = importlib.import_module(conf)
    except ModuleNotFoundError as e:
        print("Error: config file import failed. File: %s Desc: %s\n" % (conf, e.args), file=sys.stderr)
        sys.exit(1)

    try:
        config.token
        config.post_channel_id
        config.tz_hours
        config.target_days
        config.target_hours
        config.target_minutes
        config.tz_name
    except AttributeError as e:
        print("Error: required config not exists. Desc: %s\n" % (e.args), file=sys.stderr)
        sys.exit(1)

    if config.target_days == 0 and config.target_hours == 0 and config.target_minutes == 0:
        config.target_days = 1

    # ------------------
    # 0.2: mode check (normal / join / leave)
    # ------------------
    if len(sys.argv) >= 2: # 1: No Arguments
        if   [a for a in sys.argv if a.lower() == join]:
            mode = join
        elif [a for a in sys.argv if a.lower() == leave]:
            mode = leave
        elif [a for a in sys.argv if a.lower() == dry_run]:
            mode = dry_run
        else:
            mode = normal
    else:
        mode = normal

    # ------------------
    # 1: get channel list
    # ------------------
    oldest   = (datetime.now(timezone(timedelta(hours = config.tz_hours), config.tz_name)) - timedelta(days = config.target_days, hours = config.target_hours, minutes = config.target_minutes))
    payload1 = {
        "token"           : config.token,
        "exclude_archived": "true"
    }
    response1  = requests.get(url1, params=payload1)
    json_data1 = response1.json()
    if json_data1["ok"] == False:
        print("Error: api/conversations.list failed. Desc: %s\n" % (json_data1["error"]), file=sys.stderr)
        sys.exit(1)
    channels   = json_data1["channels"]

    text = ""
    for i in channels:
        try:
            if i["id"] in config.exclude_channel_id:
                continue
        except AttributeError:
            pass

        # ------------------
        # 2: join channel
        # ------------------
        if mode == normal or mode == join or mode == dry_run:
            payload2 = {
                "token"   : config.token,
                "channel" : i["id"]
            }
            response2  = requests.get(url2, params=payload2)
            json_data2 = response2.json()
            if json_data2["ok"] == False:
                print("Error: api/conversations.join failed. Desc: %s\n" % (json_data2["error"]), file=sys.stderr)
                sys.exit(1)

        # ------------------
        # 3: leave channel
        # ------------------
        if mode == leave:
            payload3 = {
                "token"   : config.token,
                "channel" : i["id"]
            }
            response3  = requests.get(url3, params=payload3)
            json_data3 = response3.json()
            if json_data3["ok"] == False:
                print("Error: api/conversations.leave failed. Desc: %s\n" % (json_data3["error"]), file=sys.stderr)
                sys.exit(1)

        # ------------------
        # 4: get channel posts
        # ------------------
        if mode == normal or mode == dry_run:
            payload4 = {
                "token"   : config.token,
                "channel" : i["id"],
                "oldest"  : oldest.timestamp()
            }
            response4  = requests.get(url4, params=payload4)
            json_data4 = response4.json()
            if json_data4["ok"] == False:
                print("Error: api/conversations.history failed. Desc: %s\n" % (json_data4["error"]), file=sys.stderr)
                sys.exit(1)
            json_message4 = json_data4["messages"]

            try:
                if config.exclude_users_id:
                    messages = []
                    for m in json_message4:
                        try:
                            if m["user"] not in config.exclude_users_id:
                                messages.append(m)
                        except KeyError:
                            messages.append(m)
                    json_message4 = messages
            except AttributeError:
                pass

            try:
                if config.exclude_message_subtype:
                    messages = []
                    for m in json_message4:
                        try:
                            if m["subtype"] not in config.exclude_message_subtype:
                                messages.append(m)
                        except KeyError:
                            messages.append(m)
                    json_message4 = messages
            except AttributeError:
                pass

            if len(json_message4) != 0:
                text += "#" + i["name"]  + " " + str(len(json_message4)) + " posts\n"

    # ------------------
    # 5: post result
    # ------------------
    if mode == normal or mode == dry_run:
        if text != "":
            text  = "Posts after " + oldest.strftime("%Y/%-m/%-d %-H:%M") + " " + config.tz_name + "\n" + text
            text += "Posted from: %s (%s):%s" % (host, ip, file)+ "\n"
            payload5 = {
                "token"     : config.token,
                "channel"   : config.post_channel_id,
                "link_names": "true",
                "text"      : text
            }
            if mode == normal:
                response5  = requests.get(url5, params=payload5)
                json_data5 = response5.json()
                if json_data5["ok"] == False:
                    print("Error: api/chat.postMessage failed. Desc: %s\n" % (json_data5["error"]), file=sys.stderr)
                    sys.exit(1)

    if len(sys.argv) >= 2:
        arguments = sys.argv[1:len(sys.argv)]
    else:
        arguments = []
    print("Args: %s" % (arguments))
    print("Mode: %s" % (mode))
    print("\n" + text)

if __name__ == '__main__':
    main()
# ------------------------------------------------------------------------------
