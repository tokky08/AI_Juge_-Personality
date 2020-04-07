import json
import sys
import glob
import os
import pprint
import api
from requests_oauthlib import OAuth1Session

API_key = api.API_key
API_secret_key = api.API_secret_key
Access_token = api.Access_token
Access_token_secret = api.Access_token_secret

session = OAuth1Session(API_key, API_secret_key, Access_token, Access_token_secret)



def screen_name_list(file):
    #読み込み用データとして、fileを開いて読み込む
    f = open(file, "r", encoding="utf-8").read()
    #改行コード（\n）で区切ってリスト化（配列化）する
    screen_name = f.split("\n")
    #screen_nameリストを返却する
    return screen_name

# メンヘラ・非メンヘラリストのファイル名を設定
train_list = glob.glob('list/*.txt')

# 取得したツイートデータを保存するフォルダを作成
os.makedirs("data", exist_ok=True)


# メンヘラ・非メンヘラリストを順番に呼び出す
for train in train_list:
    # 先ほど作成したscreen_name_list関数を実行
    screen_names = screen_name_list(train)

    # パラメータ（スクリーンネーム、1回に取得するツイートの件数）を設定し、ツイートを取得する
    for screen_name in screen_names:

        # ユーザーのタイムラインを取得するTwitter　APIのURLを設定する
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        
        # パラメータ（スクリーンネーム、1回に取得するツイートの件数）を設定する
        params = {'screen_name':screen_name, 'count':200}

        # Twitter APIにアクセスし、データを読み込む
        response = session.get(url, params = params)
        response_text = json.loads(response.text)
        
        # Twitter APIから読み込んだデータを格納するリストを用意
        texts = []
        
        # 読み込んだデータの中からツイートのテキスト部分に該当するものをtextsに格納する
        for data in response_text:
            texts.append(data['text'])

        # メンヘラ・非メンヘラのツイートデータを保存するために、リストディレクトリ名を書き換える
        data_name = str(train).replace('list', 'data', 1)

        # ツイートデータを保存するファイルを開く
        with open(data_name, "a") as f:
            for text in texts:
                # ツイートのテキストを書き込む
                f.write(str(text) + "\n")

