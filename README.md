# pintcloud_annotation
本リポジトリは、[bat-3d](https://github.com/walzimmer/bat-3d.git)のREADMEに情報が足りないため作成されたものです。
最初に[3d-bat](https://github.com/walzimmer/3d-bat.git)を試しましたが、動作しなかったのでbat-3dの使い方を説明します。
本リポジトリで想定している使用方法は以下の通りですが、本家のREADMEによるとWindowsでも使用できるようです。
* Ubuntu 22.04
* Google Chrome
* 点群のみのアノテーション

# Installation
1. bat-3dと本リポジトリをクローン
   ```bash
   # bat-3d
   git clone https://github.com/walzimmer/bat-3d.git

   # 本リポジトリ
   git clone https://github.com/HappyYusuke/pintcloud_annotation.git
   ```
   
2. npmをインストール
   ```bash
   sudo apt install npm
   ```
   
3. PHP Stormをダウンロード</br>
   以下URLからダウンロード（ウィンドウが立ち上がります）</br>
   https://www.jetbrains.com/phpstorm/download/download-thanks.html
   
5. ファイルを解凍
   ```bash
   # ダウンロード先に移動
   cd $HOME/Downloads
   
   # 解凍
   tar -zxvf PhpStorm-2025.2.3.tar.gz

   # ホームディレクトリに移動
   mv PhpStorm-252.26830.95 $HOME
   ```
   
6. 本リポジトリのファイルと置換
   ```bash
   # ホームディレクトリに移動
   cd $HOME/pointcloud_annotation

   # 元のファイルを削除
   rm bat-3d/js/base_label_tool.js bat-3d/config/config.json

   # 本リポジトリのファイルを移動
   mv pointcloud_annotation/base_label_tool.js bat-3d/js
   mv pointcloud_annotation/config.json bat-3d/config
   ```
   
7. npmで必要なパッケージをインストール
   ```bash
   # bat-3dに移動
   cd $HOME/bat-3d

   # パッケージをインストール
   npm install
   ```

# Usage
