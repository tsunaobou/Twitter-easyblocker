# Twitter-easyblocker
Twitterのユーザーを簡単にブロックすることができるツールです。 
## JustNow
現在可能な操作一覧です。  
1.リスト内のメンバーを全ブロック/全ブロック解除できます。  
(製作中)2.スクリーンネームや自己紹介欄に書かれている単語を用いてブロック/ブロック解除します。  
(製作中)3.ブロックしたIDをテキストファイルに書き出します。 
## Usage
1.まずpipでパッケージをインストール 
```
pip install requests requests-oauthlib
```
2.Twitter Developer PortalでTwitter Appを作り、アクセストークンなどの4種類の認証に必要な情報を取得する(ここらへんは調べれば出てきます)  
3.このスクリプトと同じディレクトリにあるconfig.pyのXXXの部分に2で取得したトークン類を入れる  
4.tweetblocker.pyを動かし、指示通りに進む  
