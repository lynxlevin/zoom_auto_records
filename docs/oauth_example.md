## Access Token取得の画面フロー


1. `python3 manage.py runserver`コマンドでサーバーを立ち上げる
2. `http://127.0.0.1:8000/user/signup/`にアクセスし、ユーザー登録を行う
![画面画像01](images/oauth_example01.png)
3. `http://127.0.0.1:8000/user/zoom/auth/init`にアクセスし、`Zoomの連携ページへ`のリンクを押下する
![画面画像02](images/oauth_example02.png)
4. 遷移先のページで`連携`または`Authorize`を押下する
![画面画像03](images/oauth_example03.png)
5. `http://127.0.0.1:8000/user/zoom/auth/return`にリダイレクトされ、Access Tokenの取得が完了する
![画面画像04](images/oauth_example04.png)
