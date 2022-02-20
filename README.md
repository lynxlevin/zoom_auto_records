## 機能
以下の流れで操作をし、Zoom会議の概要と音声認識のよる議事録を表示することができます。


1. サーバーを立ち上げ、`http://127.0.0.1:8000/audio`へアクセス
2. ZoomのミーティングIDを入力し、`send`ボタンを押下
3. 表示された過去のミーティングインスタンスのうち、該当するものを選択
4. Zoom会議の録画音声（m4aファイル）をアップロード
5. `send`ボタンを押下
6. 少し待つと、Zoom会議の概要と議事録が表示されます



## 動作の様子
以下のIssueに動画を設置しております。
[Issue](https://github.com/lynxlevin/zoom_auto_records/issues/1)


## 追加予定の機能

### ①Zoom APIの認証方法の変更
Zoom APIの認証方法をJWTからAuthorization Codeへ変換予定
- 現状
  - JWTでの認証のため、デベロッパー本人の会議の情報しか取得することができない
- 改善予定
  - Authorization Codeによる認証へ変更することで、ユーザー自身の会議の情報を取得・表示をできるようにする


### ②ユーザー登録機能による入力の省略
Zoomに登録したメールアドレスやパーソナルミーティングIDを登録してもらうことで、入力を省略
- 現状
  - ユーザーが自分でミーティングIDを入力する必要がある
- 改善予定
  - ユーザー登録されている場合、ユーザーのメールアドレスや登録済みのパーソナルミーティングIDを利用し、自動で過去のミーティング一覧を取得・表示する


### ③音声ファイルをCloud Recordingsから取得
該当のミーティングを選択すると、ユーザーが自分で音声ファイルをアップロードする必要なく、クラウドレコーディングから取得し、議事録を作成する
- 現状
  - ユーザーが自分で音声ファイルをアップロードしなければ、議事録を作成できない
- 追加機能
  - 過去のミーティングを選ぶだけで、該当の音声ファイルをクラウドから取得し、議事録を作成する
- 短所
  - ユーザーがクラウドレコーディングを利用するためにZoomの有料会員になる必要がある


### ④過去のミーティング一覧表示の改善
ミーティングIDを送信した後に表示される過去のミーティング一覧の表示を整備し、よりユーザーにわかりやすい内容にする
- 現状
  - ミーティングのuuidと開始時刻（UTC）しか表示されず、ユーザーにわかりづらい
- 改善予定
  - uuidを表示しない
  - 開始時刻をローカライズする
  - 全てのミーティングについてAPI通信をして詳細を取得・必要な情報を表示する