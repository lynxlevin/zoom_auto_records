# アプリケーション概要

## 主な機能
- Zoom APIに通信し、必要な情報を取得する機能
  - ユーザー登録を行い、OAuthでZoomに連携し、Access Tokenを取得する機能
  - `Access Token`または`JWT`を利用してZoom APIを利用する機能
    - ミーティングIDを元に過去の会議の一覧を取得する機能
    - 過去の会議のuuidを元に会議の詳細情報を取得する機能
  - [Access Token取得のシーケンス図](docs/zoom_authentication_sequence.md)
- 音声ファイルを文字起こしする機能
  - 音声ファイル（m4a）のアップロードする機能
  - 音声ファイルをflac形式に変換する機能
  - 音声認識APIを利用し、文字起こしする機能


## 使用したライブラリ
- [jiaaro/pydub](https://github.com/jiaaro/pydub1)
  - 依存ライブラリ：[FFmpeg](http://www.ffmpeg.org)
  - 音声ファイルの変換（m4a → flac）のため
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
  - 音声認識し、文字起こしをするため
- [environ](https://pypi.org/project/environ/)
  - 環境変数でClient Secretなどの機密情報を扱うため

## アプリ作成の目的
- Pythonの学習
- Djangoの学習
- OAuthの実装の体験
  - JWTによる連携
  - access tokenによる連携
- API連携の実装の体験
- 音声認識による自動文字起こしの実装の体験
- サーバーサイドの実装経験を積むこと



## 動作確認方法

### 環境構築
1. リポジトリをクローンする
2. 以下のライブラリをインストールする
   1. Django
   2. pydub
   3. ffmpeg
   4. SpeechRecognition
   5. environ
3. `python3 manage.py migrate`コマンドを入力し、マイグレーションを行う
4. Zoomのデベロッパーアカウントに登録し、JWTとOAuthのアプリの登録を行う
5. プロジェクトディレクトリに`.env`ファイルを作成し、以下の内容を記述する
   1. ZOOM_API_KEY
   2. ZOOM_API_SECRET
   3. ZOOM_CLIENT_ID
   4. ZOOM_CLIENT_SECRET

 ※5-1と5-2はJWTのアプリ情報、5-3と5-4はOAuthのアプリ情報
### Access Token取得（OAuth）の方法

1. `python3 manage.py runserver`コマンドでサーバーを立ち上げる
2. `http://127.0.0.1:8000/user/signup/`にアクセスし、ユーザー登録を行う
3. `http://127.0.0.1:8000/user/zoom/auth/init`にアクセスし、`Zoomの連携ページへ`のリンクを押下する
4. 遷移先のページで`連携`または`Authorize`を押下する
5. `http://127.0.0.1:8000/user/zoom/auth/return`にリダイレクトされ、Access Tokenの取得が完了する

[Access Token取得の画面フロー](docs/oauth_example.md)


### 議事録作成の方法
1. `python3 manage.py runserver`コマンドでサーバーを立ち上げる
2. `http://127.0.0.1:8000/audio/`にアクセスする
3. 自分のZoomのミーティングIDを入力し、`send`を押下する
4. start_timeを元に会議を選択する
5. 会議の音声ファイル(m4a形式)をアップロードする
6. `send`を押下する
7. 処理完了後、会議の概要と文字起こしされた議事録が表示される

[議事録作成の画面フロー](docs/speech_recognition_example.md)

 ※Zoom API連携に関しては、ログイン状態に応じて以下のように行う
- `ログイン状態`かつ`Access Token取得済み`：
  - Access Tokenを利用したOAuthによりAPI連携
- `未ログイン状態`または`Access Token未取得`：
  - JWTを利用したAPI連携




## 省略した実装
アプリ作成の目的から外れた以下の機能は実装を行わなかった
- 使いやすい画面フロー・UIの実装
- 使いやすいサービスにするためにより適したZoom APIの選定
  - クラウド録画の利用
  - 過去の会議一覧表示の改善

## できなかった実装
以下の機能は時間が足りず実装できなかった
- 期限切れトークンの更新機能
- ユニットテストの実装
- エラーの際の分岐処理