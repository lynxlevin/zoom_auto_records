## アプリケーション概要

### 主な機能
- Zoom APIに通信し、必要な情報を取得できる
  - ユーザー登録を行い、OAuthでZoomに連携し、Access Tokenを取得できる
  - `Access Token`または`JWT`を利用してZoom APIを利用できる
    - ミーティングIDを元に過去の会議の一覧を取得できる
    - 過去の会議にuuidを元に会議の詳細情報を取得できる
  - [Access Token取得のシーケンス図](docs/zoom_authentication_sequence.md)
- 音声ファイルを文字起こしできる
  - 音声ファイル(m4a)のアップロードができる
  - 音声ファイルをflac形式に変換できる
  - 音声認識APIを利用し、文字起こしができる


### 使用したライブラリ
- pydub
  - 音声ファイルの変換(m4a -> flac)のため
- SpeechRecognition
  - 音声認識し、文字起こしをするため
- environ
  - 環境変数で機密情報を扱うため


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

### 動作確認方法
#### Access Token取得（OAuth）の方法
1. `python3 manage.py runserver`コマンドでサーバーを立ち上げる
2. `http://localhost:8000/user/signup/`にアクセスし、ユーザー登録を行う
3. `http://localhost:8000/user/zoom/auth/init`にアクセスし、`Zoomの連携ページへ`のリンクを押下する
4. 遷移先のページで`連携`を押下する
5. `http://localhost:8000/user/zoom/auth/return`にリダイレクトされ、Access Tokenの取得が完了する


#### 議事録作成の方法
1. `python3 manage.py runserver`コマンドでサーバーを立ち上げる
2. `http://localhost:8000/audio/`にアクセスする
3. 自分のZoomのミーティングIDを入力し、`send`を押下する
4. start_timeを元に会議を選択する
5. 会議の音声ファイル(m4a形式)をアップロードし、`send`を押下する
6. 処理完了後、会議の概要と文字起こしされた議事録が表示される




 ※Zoom API連携に関しては、ログイン状態に応じて以下のように行います。
- `ログイン状態`かつ`Access Token取得済み`：
  - Access Tokenを利用したOAuthによりAPI連携
- `未ログイン状態`または`Access Token未取得`：
  - JWTを利用したAPI連携

[議事録作成の動作の様子](docs/speech_recognition_example.md)


## このアプリ作成の目的
- Pythonの学習
- Djangoの学習
- OAuth2.0の実装を経験すること
  - JWTによる連携
  - access tokenによる連携
- API連携の実装を経験すること
- 音声認識による自動文字起こしの実装を経験すること


## 省略した実装
目的の本筋から外れた以下の機能は実装を行わなかった
- フロントの実装
- 使いやすい画面フロー・UIの実装
- 使いやすいサービスにするためにより適したZoom APIの選定
  - クラウド録画の利用
  - 過去の会議一覧を見やすくすること
- ユニットテストの実装
- エラーの際の分岐処理