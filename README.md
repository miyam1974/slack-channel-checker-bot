[日本語へ(Go to Japanese)](#スラックチャンネルチェッカーボット)
# SLACK CHANNEL CHECKER BOT
# Overview
Post the number of posts for the specified period on all channels.  

# Function
1. Check the __number of posts__ in the specified period on all channels and __post to the specified channel__.  
1. Specify the __check target period__ with a combination of __"day, hour, minute"__.  
1. Specify the __channels, users, and subtypes__ to be __excluded__ (join, leave, bot message, etc.).  
1. Depending on the argument, you can execute __only join channel or leave channel__.  

# Slack settings
## Using API Methods

    https://api.slack.com/methods/conversations.list
    https://api.slack.com/methods/conversations.join
    https://api.slack.com/methods/conversations.leave
    https://api.slack.com/methods/conversations.history
    https://api.slack.com/methods/chat.postMessage

(Under Writing)

# Installation
Place script and configuration file in the environment where python3 can be used.  
Please rewrite the configuration file with appropriate values.  
If you want to execute this script periodically, use cron or task scheduler.  

# File list
Script file name can be changed to any name.  
Configuration file name should be the same name of the script file with "-config" added.  

    slack-channel-checker-bot.py
    slack-channel-checker-bot-config.py

# Environmental requirements
python 3

# Execution method
Prints to stdout the same content that is posted to the channel.  

    $ /path/to/python3 /path/to/slack-channel-checker-bot.py

# Config sample
    # ------------------------------------------------------------------------------
    # CONFIG (Change propriately)
    # ------------------------------------------------------------------------------
    # Required
    token              = "please input"
    post_channel_id    = "please input"
    target_days        = 1 # The target range is the sum of days, hours, and minutes. If all zero, 1 day is set as default.
    target_hours       = 0 # The target range is the sum of days, hours, and minutes. If all zero, 1 day is set as default.
    target_minutes     = 0 # The target range is the sum of days, hours, and minutes. If all zero, 1 day is set as default.
    tz_hours           = +9
    tz_name            = "JST"
    
    # Not Required
    exclude_channel_id      = ["if needed, please input"] # When two or more, like this ["one", "tow"]
    exclude_users_id        = ["if needed, please input"] # When two or more, like this ["one", "tow"]
    exclude_message_subtype = ["if needed, please input"] # When two or more, like this ["channel_join", "channel_leave", "bot_message"]
    # ------------------------------------------------------------------------------

# Operation mode
The operation mode can be specified by the command line argument.  
The bot can only join the channel or leave the channel.  

## Operation mode and arguments matrix
| mode | command line argument |
|:---|:---|
|normal||
|channel join|join|
|channel leave|leave|
|dry run|dry-run|

## script action and Operation mode matrix
|script action \ mode|normal|channel join|channel leave|dry run|
|:---|:---|:---|:---|:---|
|1. Get channel list|do|do|do|do|
|2. Join channel|do|do|--|do|
|3. Leave channel|--|--|do|--|
|4. Get channel posts|do|--|--|do|
|5. Posts result|do|--|--|--|

# License
MIT License  

---
[Go To English (英語へ)](#slack-channel-checker-bot)

# スラックチャンネルチェッカーボット
# 概要
全チャンネルの指定期間の投稿数を投稿します。  

# 機能
1. 全チャンネルの指定期間の投稿数をチェックして指定のチャンネルに投稿します。
1. チェック対象期間を「日、時間、分」の組み合わせで指定できます。
1. 対象外にするチャンネル、ユーザー、サブタイプ（参加、退出、ボットメッセージなど）を指定できます。
1. 引数により、チャンネル参加のみ、チャンネル退出のみを実行できます。

# Slack設定
## Using API Methods

    https://api.slack.com/methods/conversations.list
    https://api.slack.com/methods/conversations.join
    https://api.slack.com/methods/conversations.leave
    https://api.slack.com/methods/conversations.history
    https://api.slack.com/methods/chat.postMessage

## Create App
以下のURLでCreate New Appを選択します。

    https://api.slack.com/apps

App Nameを入力し、Workspaceを選択します。

## Scope
以下のメニューをたどります。

    > Features
      > OAuth & Permissions
        > Scopes
          > Bot Token Scopes

「Add an OAuth Scope」ボタンから以下のScopeを追加します。

    channels:read
    channels:history
    channels:join
    channels:manage 
    chat:write

## App Display Name
以下のメニューをたどります。

    > Features
      > App Home
        > Your App's Presence in Slack
          > App Display Name

「Edit」を選択し、以下を入力します。

    Display Name (Bot Name)
    Default username

## Install
以下のメニューをたどります。

    > Features
      > OAuth & Permissions
        > OAuth Tokens & Redirect URLs

「Install App to Workspace」ボタンを選択し、リクエストされた権限を確認の上、「許可する」を選択します。

### Token
以下のメニューをたどります。

    > Features
      > OAuth & Permissions
        > OAuth Tokens & Redirect URLs
        
「Bot User OAuth Access Token」をコピーして、このスクリプトの設定ファイルのtokenに設定します。

# 設置方法
スクリプトと設定ファイルをpython3が利用できる環境に配置してください。  
設定ファイルを適切な内容で書き換えてください。  
定期的に実行する場合は、cronやタスクスケジューラなど定期実行機能で実行してください。  

# ファイル構成
スクリプトファイル名は、任意の名称に変更できます。  
設定ファイルは、スクリプトファイル名に「-config」を付けた名称にします。  

    slack-channel-checker-bot.py
    slack-channel-checker-bot-config.py

# 動作要件
Python3 

# 実行方法
チャンネルに投稿する内容と同じ内容を標準出力に表示します。  

    $ /path/to/python3 /path/to/slack-channel-checker-bot.py
    Posts after 2020/8/9 12:01 JST
    #random 5 posts
    #main 1 posts
    #times_aaa 12 posts
    #times_bbb 25 posts
    Posted from: hostname (xxx.xxx.xxx.xxx):slack-channel-checker-bot.py
    
    $

# エラー処理
標準エラー出力に内容を表示し、終了コード1で終了します。  

# 投稿イメージ
    channel_chacker [アプリ]  12:02
    #random に参加しました。
    
    channel_chacker [アプリ]  12:02
    Posts after 2020/8/9 12:01 JST
    #random 5 posts
    #main 1 posts
    #times_aaa 12 posts
    #times_bbb 25 posts
    Posted from: hostname (xxx.xxx.xxx.xxx):slack-channel-checker-bot.py

# 設定ファイルサンプル（v1.4.1）
    # ------------------------------------------------------------------------------
    # CONFIG (Change propriately)
    # ------------------------------------------------------------------------------
    # Required
    token              = "please input"
    post_channel_id    = "please input"
    target_days        = 1 # The target range is the sum of days, hours, and minutes. If all zero, 1 day is set as default.
    target_hours       = 0 # The target range is the sum of days, hours, and minutes. If all zero, 1 day is set as default.
    target_minutes     = 0 # The target range is the sum of days, hours, and minutes. If all zero, 1 day is set as default.
    tz_hours           = +9
    tz_name            = "JST"
    
    # Not Required
    exclude_channel_id      = ["if needed, please input"] # When two or more, like this ["one", "tow"]
    exclude_users_id        = ["if needed, please input"] # When two or more, like this ["one", "tow"]
    exclude_message_subtype = ["if needed, please input"] # When two or more, like this ["channel_join", "channel_leave", "bot_message"]
    # ------------------------------------------------------------------------------

# 動作モード
コマンドライン引数により、動作モードを指定できます。
ボットがチャンネルに参加だけしたり、使用をやめる際にチャンネルから退出だけ行うことができます。

    # 例
    $ /path/to/python3 /path/to/slack-channel-checker-bot.py join
    $ /path/to/python3 /path/to/slack-channel-checker-bot.py leave

## 動作モードと引数のマトリクス
| モード | コマンドライン引数 |
|:---|:---|
|ノーマル||
|チャンネル参加|join|
|チャンネル退出|leave|
|ドライラン（ダミー実行）|dry-run|

## アクションと動作モードのマトリクス
|アクション＼モード|ノーマル|チャンネル参加|チャンネル退出|ドライラン（ダミー実行）|
|:---|:---|:---|:---|:---|
|1. チャンネルリスト取得|do|do|do|do|
|2. チャンネル参加|do|do|--|do|
|3. チャンネル退出|--|--|do|--|
|4. チャンネル投稿取得|do|--|--|do|
|5. チェック結果投稿|do|--|--|--|

# ライセンス
MIT Licenseです。  
