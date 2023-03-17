# DockerFileセット

## 内容物
- build.sh
  - Dockerコンテナを起動させる包括スクリプト
- copy.sh
  - コンテナを起動させたあと手法を実行させたりするのに必要なものをここにコピーするスクリプト
  - build.sh内で呼び出される
- download.sh launcher.sh Subjects.py
  - コンテナ内で実行したい、各プロジェクトごとに内容が異なるスクリプト
  - ここでは実行しない、DockerFile内でこれらをコンテナ内にコピーすることになっている

## ここでやること
ここでは`build.sh`を実行してコンテナを作成・コンテナに入ります

`copy.sh`がここにコピーするものはnewscripts内にある全ファイルです
コンテナに入れ込みたい変更済スクリプトをコピーします

* pyファイル
  * BugRepositoryMaker.py
    * BugRepoを再生成するように引数変更
  * Counting.py
    * ソースファイル数を再計算するように変更
  * launcher_gitrepoMaker.py
    * 新ファイル。git-steinでgitrepoをメソッド化するためのスクリプト
  * launcher_Tool.py
    * ツール全体の改造。実行時間の取得や〇〇 on BLIAのconfigを設定するように変更
  * Subjects.py
    * Techniquesで使用手法を変更。Group等で上手くやりたい実験対象を選べる。適宜変更されている
  * XLSResultsAll.py
    * Singleの結果がみれる。あんまり活用性はないかも。
* jarファイル
  * 手法実行のために変更したjarファイルをコンテナに輸送する必要がある
