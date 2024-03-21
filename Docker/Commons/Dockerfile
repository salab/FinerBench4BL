FROM ubuntu:16.04

# 実行のためのpathを設定
RUN ln -s / /mnt/exp \
# gitコマンドのインストール
	&& apt-get update && apt-get clean && apt-get install -y --no-install-recommends git \
# Python 2.7のインストール
	&& apt-get install -y --no-install-recommends software-properties-common \
	&& add-apt-repository ppa:deadsnakes/ppa \
	&& apt-get update && apt-get clean \
	&& apt-get install -y --no-install-recommends python2.7 python \
	&& apt-get install -y --no-install-recommends python-pip \
	&& apt-get install -y curl \
	&& curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py \
	&& python get-pip.py \
# 依存ライブラリのインストール
	&& apt-get install -y python-subprocess32 \
	&& pip install --upgrade setuptools \
	&& pip install wheel \
	&& pip install numpy==1.13.3 scipy==0.19.1 matplotlib==2.0.1 pytz==2017.3 GitPython==2.1.15 bs4==0.0.1 XlsxWriter==0.9.8 python-dateutil==2.6.1 \
# Javaのインストール
	&& apt-get install -y --no-install-recommends python-software-properties \
	&& add-apt-repository ppa:webupd8team/java \
	&& echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections \
	&& apt-get update && apt-get clean \
	&& apt-get install -y openjdk-8-jre-headless \
# Java11のインストール
	&& add-apt-repository ppa:openjdk-r/ppa \
	&& apt update \
	&& apt install -y openjdk-11-jdk \
# vimのインストール
	&& apt-get -y install vim \
	&& apt-get update && apt-get install -y wget

# Bench4BLのクローン
RUN git clone https://github.com/exatoa/Bench4BL.git
RUN git clone https://github.com/sh5i/git-stein.git

WORKDIR /git-stein

# Historage
RUN  ./gradlew executableJar

# 作業ディレクトリの変更
WORKDIR /Bench4BL

# diff制限の解除
RUN git config --global diff.renameLimit 9999

# mkdir
RUN mkdir _archives data expresults
RUN mkdir ./techniques/releases/bluir_properties
RUN mkdir ./techniques/releases/amalgam_properties
RUN mkdir ./techniques/releases/brtracer_properties

# ダウンロード
COPY downloads.sh .
RUN chmod +x downloads.sh \
	&& ./downloads.sh

# 展開
RUN	chmod +x unpacking.sh \
	&& ./unpacking.sh _archives data \
# `_acheives/`の削除
	&& rm -r -f _archives

# 変更したjar の追加
COPY BLIA.jar ./techniques/releases/
COPY AmaLgam.jar ./techniques/releases/
COPY BLUiR.jar ./techniques/releases/
COPY BRTracer.jar ./techniques/releases/
COPY BugLocator.jar ./techniques/releases/

# 改造後script追加
COPY launcher_Tool.py ./scripts/
COPY Subjects.py ./scripts/commons/
COPY Counting.py ./scripts/
COPY Items.py ./scripts/results/
COPY Evaluator.py ./scripts/results/
COPY launcher_gitrepoMaker.py ./scripts/
COPY XLSResultsAll.py ./scripts/results/
COPY BugRepositoryMaker.py ./scripts/repository/
COPY launcher.sh ./scripts/

# file版jarの追加
COPY file_jar/BLIA.jar ./techniques/releases/file_jar
COPY file_jar/AmaLgam.jar ./techniques/releases/file_jar
COPY file_jar/BLUiR.jar ./techniques/releases/file_jar
COPY file_jar/BRTracer.jar ./techniques/releases/file_jar
COPY file_jar/BugLocator.jar ./techniques/releases/file_jar
