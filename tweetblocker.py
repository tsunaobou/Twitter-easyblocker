import json
import config
from requests_oauthlib import OAuth1Session



#config.pyからアクセストークンなど４種類の認証に必要なものを取得してくる
Consumer_key = config.CONSUMER_KEY
Consumer_secret = config.CONSUMER_SECRET
Access_token = config.ACCESS_TOKEN
Access_token_secret = config.ACCESS_TOKEN_SECRET
#認証を行う
twitter = OAuth1Session(Consumer_key, Consumer_secret, Access_token, Access_token_secret)


#メンバー取得用の動作
url = "https://api.twitter.com/1.1/lists/members.json"
#リスト名とリスト参加人数取得用のURL準備
list_get_url = "https://api.twitter.com/1.1/lists/show.json"


#ブロックかブロック時解除かを選択させる
select = int(input("ブロックなら1を、ブロック解除なら2を入力してください>>"))

#ブロックかブロック解除するリストのIDを入力させる
blockID = int(input("ブロックまたはブロック解除したいリストのURLの末尾の数字を入力してください。>>"))

#リストをGETする
parameter={'list_id' : blockID} #GET用に必要なパラメータの整備
listget = twitter.get(list_get_url, params=parameter)   #GETリクエスト


if listget.status_code == 200 and select==1:
    #GETに成功したらJSONをパースしてリスト名と参加人数を取得し、整数型と文字列に変換
    json_list = json.loads(listget.content)
    count = int(json_list['member_count'])
    list_name = str(json_list['name'])  #ここをUTF-8にしておかないと文字化けした際にログ表示がおかしくなる
    print(list_name)
    print(f"リスト「{list_name}」のブロックを開始します...")
elif listget.status_code == 200 and select==2:  #ここもうちょっと賢く書けない？
    json_list = json.loads(listget.content)
    count = int(json_list['member_count'])
    list_name = str(json_list['name'])  
    print(list_name)
    print(f"リスト「{list_name}」のブロック解除を開始します...")

else:
    print("ステータスコード%dで失敗しました。" % listget.status_code)
    pass


#URLにparamsのパラメータを代入して二回目のGETリクエスト
params ={'list_id' : blockID,'count':count} #GET用に必要なパラメータの整備
res = twitter.get(url, params=params)   #GETリクエスト

if res.status_code == 200:
    #レスポンスをJSONとしてパース
    usejson = json.loads(res.text)

    for i in range(0,count):    #0からcountまでの範囲を指定。実際はcount-1の数までしかないので一個前までで止めるrangeが丁度よく使える。
        #ブロックするIDをJSONから取得
        #なぜかJSONに書かれているユーザー数とcountのユーザー数が一致しなくてバグることがたまにあるので例外処理をしておく
        #この例外が発生したときにはすでにリスト内ユーザーは全ブロックされてるので機能上には支障なし
        try:
             ready_blockid = usejson['users'][i]['id']
        except IndexError:
            break

        #ブロックかブロック解除かでアクセス先URLを選択する
        if select == 1:
            url2 = "https://api.twitter.com/1.1/blocks/create.json"
        elif select == 2:
            url2 = "https://api.twitter.com/1.1/blocks/destroy.json"
        else:
            break
    
        #URLにparams2のパラメータを代入してPOSTリクエスト
        params2 = {'user_id': ready_blockid}    #ブロックするIDを指定するuser_idにはJSONから取得したIDを入れる
        res2 = twitter.post(url2,params=params2)    #POSTリクエスト

        if res2.status_code == 200 and select == 1:
            #書き込み用のファイルパス指定 ファイル名はリストID_リスト名.txt
            path = f'{blockID}_{list_name}.txt'
            #ブロックの場合にだけファイルを作成してブロックしたIDを改行して書き込み モードはaなので末尾追記モード
            with open(path,mode='a') as f:
                print("ID:%dのユーザーをブロックしました。現在%d個中%d個目"%(ready_blockid,count,i+1))
                f.write(str(ready_blockid)+"\n")
        elif res2.status_code == 200 and select == 2:
            print("ID:%dのユーザーをブロック解除しました。現在%d個中%d個目"%(ready_blockid,count,i+1))
        else:
            print("ステータスコード%dで失敗しました。" % res2.status_code)
            
    #終了時の動作
    if select==1:
        print(f"リスト「{list_name}」のブロックが完了しました...")
    
    elif select==2:
        print(f"リスト「{list_name}」のブロック解除が完了しました...")
    else:
        pass

else:
    print("ステータスコード%dで失敗しました。" %res.status_code)