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

blockID = input("ブロックしたいリストの末尾の数字を入力してください。")
count = input("ブロックしたいリストの参加人数を入力してください。")
blockcount = int(count)

params ={'list_id' : blockID,'count':blockcount}
#URLにparamsのパラメータを代入してGETリクエスト
res = twitter.get(url, params=params)

if res.status_code == 200:
    #後々代入するための配列を宣言
    blockidlist = []
    #レスポンスをJSONとしてパース
    usejson = json.loads(res.text)
    for i in range(0,blockcount):
        #ブロックするIDをJSONから取得
        ready_blockid = usejson['users'][i]['id']

        #ブロック動作用のURL
        url2 = "https://api.twitter.com/1.1/blocks/create.json"
        params2 = {'user_id': ready_blockid}    #ブロックするIDを指定するuser_idにはJSONから取得したIDを入れる
        
        #URLにparams2のパラメータを代入してPOSTリクエスト
        res2 = twitter.post(url2,params=params2)

        if res2.status_code == 200:
            print("ID:%dのユーザーをブロックしました"%ready_blockid)
        else:
            print("ステータスコード%dで失敗しました。" % res2.status_code)


else:
    print("ステータスコード%dで失敗しました。" %res.status_code)