import json
import config
from requests_oauthlib import OAuth1Session

#config.pyからアクセストークンなど４種類の認証に必要なものを取得してくる
Consumer_key = config.CONSUMER_KEY
Consumer_secret = config.CONSUMER_SECRET
Access_token = config.ACCESS_TOKEN
Access_token_secret = config.ACCESS_TOKEN_SECRET

twitter = OAuth1Session(Consumer_key, Consumer_secret, Access_token, Access_token_secret)

#メンバー取得用の動作
url = "https://api.twitter.com/1.1/lists/members.json"

#ブロックかブロック時解除かを選択させる
select = int(input("ブロックなら1を、ブロック解除なら2を入力してください"))


blockID = int(input("ブロックまたはブロック解除したいリストのURLの末尾の数字を入力してください。"))
count = int(input("ブロックまたはブロック解除したいリストの参加人数を入力してください。"))

params ={'list_id' : blockID,'count':count}
#URLにparamsのパラメータを代入してGETリクエスト
res = twitter.get(url, params=params)

if res.status_code == 200:
    #レスポンスをJSONとしてパース
    usejson = json.loads(res.text)
    for i in range(0,count):
        #ブロックするIDをJSONから取得
        ready_blockid = usejson['users'][i]['id']

        #ブロックかブロック解除かでアクセス先URLを選択する
        if select == 1:
            url2 = "https://api.twitter.com/1.1/blocks/create.json"
        elif select == 2:
            url2 = "https://api.twitter.com/1.1/blocks/destroy.json"
        else:
            break
        params2 = {'user_id': ready_blockid}    #ブロックするIDを指定するuser_idにはJSONから取得したIDを入れる
        
        #URLにparams2のパラメータを代入してPOSTリクエスト
        res2 = twitter.post(url2,params=params2)

        if res2.status_code == 200 and select == 1:
            print("ID:%dのユーザーをブロックしました。現在%d個中%d個目"%(ready_blockid,count,i+1))
        elif res2.status_code == 200 and select == 2:
            print("ID:%dのユーザーをブロック解除しました。現在%d個中%d個目"%(ready_blockid,count,i+1))
        else:
            print("ステータスコード%dで失敗しました。" % res2.status_code)


else:
    print("ステータスコード%dで失敗しました。" %res.status_code)