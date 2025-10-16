# pintcloud_annotation
本リポジトリは、[bat-3d](https://github.com/walzimmer/bat-3d.git)のREADMEに情報が足りないため作成しました。
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
1. 独自データを配置 </br>
   本家のREADME通りにファイルツリーを構成し、独自データを格納します。
   <details>
      <summary>ファイルツリーはこちらを参照</summary>
      <pre>
      input
      └── waymo 👉 自分のプロジェクト
          └── 20251015_waymo  👉 シーケンス
              ├── annotations 👉 アノテーション作業の結果格納用
              ├── images      👉 アノテーション作業中に表示される画像格納用（任意）
              ├── pointclouds 👉 点群データを格納（重要）
              │   ├── 000000.pcd
              │   ├── 000001.pcd
              │   ├── 000002.pcd
              │   ├── 000003.pcd
              │   ├── 000004.pcd
              │   ├── 000005.pcd
              │   ├── 000006.pcd
              │   ├── 000007.pcd
              │   ├── 000008.pcd
              │   └── 000009.pcd
              └── pointclouds_without_ground 👉 地面の点を除去したデータ格納用（任意）
      </pre>
   </details>

   ディレクトリを作成
   ```bash
   # 独自データ用のディレクトリをbat-3dに移動
   mv $HOME/pointcloud_annotation/input $HOME/bat-3d

   # bat-3dに移動
   cd $HOME/bat-3d

   # 独自データ用のディレクトリを作成（例：my_data）
   mkdir input/my_data

   # 独自のシーケンス用ディレクトリを作成
   mkdir input/my_data/20251015_my_data

   # 移動
   cd input/my_data/20251015_my_data
   
   # 本家のREADME通りにディレクトリを作成
   mkdir annotations  images  pointclouds  pointclouds_without_ground
   ```

   独自データを格納（⚠️: 点群データは拡張子が`.pcd`です。）
   
   ```bash
   cp /path/to/your/data_directory/*.pcd input/my_data/20251015_my_data/pointclouds
   ```
   
2. 設定ファイルの編集 </br>
   `bat-3d/config/config.json`の以下の部分を書き換えてください。
   * name: ディレクトリ名（例：my_data）
   * sequences: シーケンス名（例：20251015_my_data）
   * classes: アノテーションするクラス
   * class_colors: バウンディングボックスの色
   ```json
   {
      "name": "waymo",
      "sequences": ["20251015_waymo"],
      "classes": ["Car", "Truck", "Motorcycle", "Bicycle", "Pedestrian"],
      "class_colors": ["#51C38C", "#EBCF36", "#B9A454", "#B18CFF", "#E976F9"]
    }
   ```

   `bat-3d/js/base_label_tool.js`の以下の部分を書き換えてください。
   * CUSTOM_DATASET_NAME: ディレクトリ名（例：my_data）
   * CUSTOM_DATASET_NUM_FRAMES: 点群のデータ数
   ```js
   // ==========================================
   // ユーザー用の変数を追加（by kanazawa）
   // ==========================================
   const CUSTOM_DATASET_NAME = 'waymo';
   const CUSTOM_DATASET_NUM_FRAMES = 5;
   // ==========================================
   ```
   
3. PHP Storm起動 </br>
   設定ファイルの変更を保存したら、PHP Stormを起動します。
   ```bash
   bash $HOME/PhpStorm-252.26830.95/bin/phpstorm.sh
   ```
   
4. bat-3d起動 </br>
   * PHP Stormのウィンドウが立ち上がったら、PHP Stormから`bat-3d`のディレクトリを開いてください。
   * ウィンドウ左側のファイルツリーから`index.html`を右クリックしてください。
   * 「開く」 => 「ブラウザ」 => 「Chrome」の順に選択してください。（ブラウザはChrome以外でもOKです）
   * ブラウザでbat-3dが立ち上がります。
   
5. データの読み込み </br>
   * 画面右側の`Choose dataset`を「NuScenes」から自身で設定したデータセット名にしてください。（例：my_data）
   * １個下の`Choose Sequence`を「ONE」から自身で設定したシーケンス名にしてください。（例：20251015_my_data）
   * データが表示されまず。
   
6.  アノテーション（Comming soon ...）
