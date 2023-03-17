# 再現パッケージ

## 環境
* `Docker 20.10.8(Client), 20.20.12(Server)`

Docker内
* `Python 2.7`
* `Java JDK1.8` ← 手法の実行
* `Java JDK11` ← git-steinの実行

## ディレクトリ説明
* `/analysis`　Bench4BLに元々入っていたもの(なんだか不明)
* `/Docker`　再現をDockerで行うための全て
  * `/Docker/newscripts`　Dockerで再現するために修正した起動・評価用スクリプト
* `/scripts`　Bench4BLに搭載されていた起動・評価用スクリプト
  * 手を加えていないBench4BLそのままのもの
* `/techniques`　jarなど
  * `/techniques/method_jar`　本実験用で用いたメソッド手法のjar
  * `/techniques/file_jar`　本実験のために修正したファイル手法のjar

## 実験手順

### 準備
1. 本リポジトリの`Clone`

```
$ git clone リポジトリの名前
```
2. 手法を実行する場所を作る。`Docker`ディレクトリを実験対象(`Bench4BL`の46プロジェクト)のグループごとに分けたので、実験したいグループのディレクトリに移動する
  + `Apache/CAMEL`
  + `Apache/HBASE_HIVE`
  + `Commons`
  + `JBoss`
  + `Wildfly`
  + `Spring`

3. ディレクトリに移動したら`build.sh` を実行する。この時のコンテナ名やイメージ名は自由に設定して良い
```
$ chmod +x build.sh
$ ./build.sh -c {コンテナ名} -i {イメージ名}

// (例) Commonsのコンテナを作る場合
$ cd tsumita-bthesis/exp/Docker/Commons
$ ./build.sh -c commons-container -i commons-image
```

4. 無事にDockerコンテナがビルドされたらコンテナの中に入っているはず
```
root@7205559fe31c:/Bench4BL#  のようになれば成功
```

5. `Bench4BL/scripts`に移動し`launcher.sh`を実行する。これでgit-steinを実行し、メソッドリポジトリを生成・メソッドBL手法に対する正解データセットを作成する
```
$ cd scripts/
$ chmod +x launcher.sh
$ ./launcher.sh
```
6. `launcher.sh`の最後にJavaのバージョンをどうするかを聞かれるのでJDK1.8を選択する

### 実験
実行する。
メソッドで先に実験、分析までやりきってからファイルの実験を行わないとCounting.pyの結果が変わるので先にメソッドで全プロジェクトの実験を仕切った方が良い。

メソッドレベルの実行時間は結構なもの。特にMATHが大きいかも
```
$ cd /Bench4BL
$ timeout -sKILL 40000 python ./scripts/launcher_Tool.py -w ExpCommons -g Commons -p CODEC
```
`-w`は出力するディレクトリを指定、
`-g`は実験対象のグループ、
`-p`は実験対象のプロジェクト、
`-t`は実験対象のBL手法。

`-g`,`-p`,`-t`は指定しないと全手法を全プロジェクトに対して実行する。

詳細は`https://github.com/exatoa/Bench4BL`

### 分析
#### 分析するためのxlsxファイルを生成
```
$ cd /Bench4BL/scripts/results
$ vi XLSResultsAll.py
// 449行目のname="test"を出力したファイル名に変更する
// 例 ExpCommonsに結果を出力した場合
// name = "ExpCommons"にする
$ python XLSResultsAll.py
```
expresultsにResult_ExpCommons.xlsxのように結果のxlsxファイルが生成される
（LOCを計算しているため重いグループだと結構時間がかかる。Commonsだけで2、3時間...?）

#### ファイルレベルの結果を出す
1. 先にメソッドレベルでの結果を出し切る
  * でないとファイル数やバグレポートの数が変わる
2. `gitrepo`を`gitrepo_method`に`rename`し、元の`gitrepo_file`を`gitrepo`に`rename`する
```
$ cd Bench4BL/data/
$ find . -name 'gitrepo' | xargs rename 's/gitrepo/gitrepo_method/'
$ find . -name 'gitrepo_file' | xargs rename 's/gitrepo_file/gitrepo/'
```
3. `sources`->`sources_method`に変換
```
$ cd Bench4BL/data/
$ find . -name 'sources' | xargs rename 's/sources/sources_method/'
```
4. GitInfratorをかけてバージョン毎にsrcを分ける
```
$ cd Bench4BL/scripts
$ python scripts/launcher_GitInflator.py
```
5. バグの正解をファイルレベルに合わせる
```
$ cd Bench4BL/scripts
$ python scripts/launcher_repoMaker.py -p {PROJECT} -g {GROUP}
$ python scripts/launcher_DupRepo.py
```
6. バグ・ファイル数を再計算
```
$ cd /Bench4BL/scripts
$ python Counting.py
```
7. 分析するためのxlsxファイルを生成
```
$ cd /Bench4BL/scripts/results
$ vi XLSResultsAll.py -f
// -fオプションをつけないとファイルレベルのLOCを等しい条件下で計測できない
// 449行目のname="test"を出力したファイル名に変更する
// 例 ExpCommonsに結果を出力した場合
// name = "ExpCommons"にする
$ python XLSResultsAll.py
```

### build.shの説明
build.shでは以下の処理が行われている

```
# {IMAGE} -> Docker のイメージ名 (任意)
# {CONTAINER} -> Docker のコンテナ名 (任意)
# {DOCKERFILE_PATH} -> Apache/CAMEL, Apache/HBASE_HIVE, Commons, JBoss, Wildfly, Spring の6通り
# {GROUP} -> Apache, Commons, JBoss, Wildfly, Spring の5通り

$ cd ~
// 1. Dockerfile がある場所に移動
$ cd hoge/Docker/{DOCKERFILE_PATH}
// (例) Commons の場合
$ cd hoge/Docker/Commons
```

Bench4BLから更新した`launcher_Tool.py`、`laucher_gitrepoMaker.py`の起動スクリプトや`Items.py`など評価用に変更したスクリプトを`/Docker/newscripts`に置いてある。

また、メソッドレベルの評価のために更新、及び修正したファイルレベルの手法のjarファイルを`/techniques/releases/{method, file}_jar`のなかに置いてある。

これらをDockerコンテナに持っていくため、`copy.sh`を用いてDockerfileがある場所にコピーを行う

```
./copy.sh
```
Dockerfileがある場所にjarファイル、pyスクリプトがコピーされたのを確認してコンテナを作成する。

```
// 2. Docker イメージの作成
$ docker build -t {IMAGE} --force-rm .
// (例) Commons の場合
$ docker build -t commons-image --force-rm .

// 3. Docker コンテナを作成し，コンテナ内に移動
// -vをつけると結果がコンテナの外に共有される
// ⅰ) Commons, JBoss, Wildfly, Spring の場合
$ docker run -it -v `pwd`/expresults:/Bench4BL/expresults --name {CONTAINER} {IMAGE} /bin/bash
// ⅰⅰ) Apache/CAMEL, Apache/HBASE_HIVE の場合
$ docker run -it -v `pwd`/../expresults:/Bench4BL/expresults --name {CONTAINER} {IMAGE} /bin/bash
// (例) Commons の場合
$ docker run -it -v `pwd`/expresults:/Bench4BL/expresults --name commons-container commons-image /bin/bash

// 共有する必要がなく、ただ実行したいときは以下
$ docker build -t {IMAGE} --force-rm .
$ docker run -it --name {CONTAINER} {IMAGE} /bin/bash
```

### launcher.shの説明
launcher.shでは以下の処理が行われている

1. `git-stein`を使ってメソッドリポジトリを生成する

```
# {PROJECT} -> プロジェクト名 例)CODEC,COMPRESS
# {GROUP} -> グループ名 例)Commons,Apache

$ cd Bench4BL/scripts
$ launcher_gitrepoMaker.py -p {PROJECT} -g {GROUP}
// (例) CommonsのCODECに対してメソッドリポジトリを作りたい場合
$ launcher_gitrepoMaker.py -p CODEC -g Commons
// (例2) -p,-gオプションを省くとコンテナ内の全プロジェクトに対して動く
$ launcher_gitrepoMaker.py

```
Commons/MATHのように引数が長すぎて縮める必要がある場合
(該当なのはCommons/Math, Wildfly/ELY,WFLY,WFCORE, Spring/AMQP,DATAREST,ROO,SPR)
```
// filename too longで後々困るので適宜オプションをつけて実行し直す

$ cd Bench4BL/data/{GROUP}/{PROJECT}/

// できてしまったメソッドリポジトリを削除
$ rm gitrepo
// gitrepo_fileが残っている状態で以下を実行
$ cd Bench4BL/scripts
$ java -jar ../../gitstein/build/libs/git-stein-all.jar Historage -o ../data/{GROUP}/{PROJECT}/gitrepo --no-classes --no-fields --no-original --method-ext='.java' --parsable --unqualify --digest-params ../data/{GROUP}/{PROJECT}/gitrepo_file
// さらに該当のgitrepoに行ってcheckoutする
$ cd Bench4BL/data/{GROUP}/{PROJECT}/gitrepo
$ git checkout master
```

参考`https://scrapbox.io/salab/メソッドリポジトリを作ってBench4BLを騙す`

2. バージョン毎にBLを行うため、BL手法の検索対象となるバージョン毎のsrcフォルダもメソッドレベルのリポジトリにすり替える

```
$ cd Bench4BL/scripts
$ python launcher_GitInflator.py
```

3. 各バグに対してメソッドリポジトリに準拠した正解ファイルを設定し直す

```
$ cd /Bench4BL/scripts
$ python launcher_repoMaker.py -p {PROJECT} -g {GROUP}
// -p,-gの省略で全プロジェクト動作
$ python launcher_DupRepo.py

// data/{GROUP}/{PROJECT}/bugrepo/repository.xml
// がメソッドファイルに対応づけられていれば成功
```

4. バグの個数やファイル数を再計算

```
$ cd /Bench4BL/scripts
$ python Counting.py
```

5. BL手法を動作させるためにJavaのバージョンを戻す

```
java -version
javac -version
// バージョンを確かめる

update-alternatives --config java
// selectionと言って選べるようになるので番号を入力すると変わる
// java-8に変える

update-alternatives --config javac
// 同様(やる必要ないかも)
```

