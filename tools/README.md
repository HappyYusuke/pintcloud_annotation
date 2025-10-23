# tools
本リポジトリは、点群ファイルからアノテーションするための前処理についてまとめている。<br>
本リポジトリで提供する機能は以下の通りである。

* rosbag2からpcdファイルへ変換
  > pointcloud_to_pcd.sh ([perception_pcl](https://github.com/ros-perception/perception_pcl.git)の[pointcloud_to_pcd]([pcl_ros/tools/pointcloud_to_pcd.cpp](https://github.com/ros-perception/perception_pcl/blob/humble/pcl_ros/tools/pointcloud_to_pcd.cpp))を使用)

* pcdファイルを、bat-3d用のフォーマットに変換
  > convert_to_bat3d_format_pcd.py

* pcdファイルをランダムに抽出 & ファイル名をbat-3d用に変換 (6桁の数字で構成、例: `000000.pcd`)
  > random_sampling_pcdfiles.py

* 点群から地面を削除する
  > [bat-3d](https://github.com/walzimmer/bat-3d.git)の[export_pointcloud_without_ground_nuscenes.py](https://github.com/walzimmer/bat-3d/blob/master/scripts/nuscenes_devkit/python-sdk/scripts/export_pointcloud_without_ground_nuscenes.py)を使用

動作確認した環境は以下の通りである。

* Ubuntu22.04
* Python3.10.12
* ros2 humble

# Installation
本リポジトリをクローン
```bash
cd ~/
git clone https://github.com/HappyYusuke/pointcloud_annotation.git
```

## perception_pcl
[perception_pcl](https://github.com/ros-perception/perception_pcl.git)にはInstallationが書かれておらず、主はHumbleでビルドエラーが発生したので、ここにインストール方法を残す。<br>

> [!WARNING]
> ここでは`pointcloud_to_pcd`のみ使用したいため、ビルドエラーの箇所をコメントアウトした`CMakeLists.txt`に置換します。

`ros2`ブランチのリポジトリをros2ワークスペースにクローン
```bash
cd ~/ros2_ws/src
git clone -b ros2 https://github.com/ros-perception/perception_pcl.git
```

依存関係をインストール
```bash
cd ~/ros2_ws
rosdep install -i --from-path src --rosdistro humble -y
```

`pcl_ros`の`CMakeLists.txt`を置換
```bash
rm ~/ros2_ws/src/perception_pcl/pcl_ros/CMakeLists.txt
mv ~/pointcloud_annotation/tools/CMakeLists.txt ~/ros2_ws/src/perception_pcl/pcl_ros
```

ビルド
```bash
colcon build --symlink-install
source install/setup.bash
```

# Usage
## rosbag2 to pcd
`pointcloud_to_pcd.sh`を使用する。
`pointcloud_to_pcd.sh`を開く。
```bash
cd ~/pointcloud_annotation
vim pointcloud_to_pcd.sh
```

各引数を変更する
```sh
#!/bin/bash

ros2 run pcl_ros pointcloud_to_pcd --ros-args \
    -r input:=/livox/lidar \      # トピック名
    -p fixed_frame:=livox_frame \ # 座標系の基準
    -p prefix:=/path/to/your/output/dir/path/filename_  # pcdファイルの保存先
```

`pointcloud_to_pcd.sh`を実行する
```bash
./pointcloud_to_pcd.sh
```

rosbag2を再生する
```bash
ros2 bag play yourbag
```

## Convert pcd files to bat-3d format
`convert_to_bat3d_format_pcd.py`を使用する。

引数は以下の通り。
| 引数 | 初期値 | 内容 |
| --- | --- | --- |
| `-i` or `--input` | - | pcdファイルが格納されているディレクトリまでのパスを指定。 |
| `-s` or `--savename` | `convert_results` | 保存するディレクトリ名を指定。 |

引数を指定して`convert_to_bat3d_format_pcd.py`を実行。
```bash
python3 convert_to_bat3d_format_pcd.py -i /path/to/your/pcd 
```

実行結果は、指定したディレクトリと同じ階層に保存される。

## Random sampling pcd & Convert filename
`random_sampling_pcdfiles.py`を使用する。

引数は以下の通り。
| 引数 | 初期値 | 内容 |
| --- | --- | --- |
| `-i` or `--input` | - | 親ディレクトリまでのパスを指定。 |
| `-s` or `--savename` | `random_results` | 保存するディレクトリ名を指定。 |
| `-n` or `--num` | `85` | 各子ディレクトリからのサンプリング数 |

ファイルツリーを以下のようにする。
```
parent_directory   # 親ディレクトリ
├── child1         # 子ディレクトリ
│   ├── hogehoge.pcd # pcdファイル
│   ├── hogehoge.pcd
│   └── hogehoge.pcd
├── child2
└── child3
```

引数を指定して`convert_to_bat3d_format_pcd.py`を実行。<br>
パスの指定は親ディレクトリを指定する。
```bash
python3 random_sampling_pcdfiles.py -i /path/to/your/parent_directory -n 100
```

実行結果は、指定したディレクトリと同じ階層に保存される。

## Remove the ground
`export_pointcloud_without_ground_nuscenes.py`を使用する。<br>
`export_pointcloud_without_ground_nuscenes.py`を開く。
```bash
cd ~/bat-3d/scripts/nuscenes_devkit/python-sdk/scripts
vim export_pointcloud_without_ground_nuscenes.py
```

3〜4行目の`path_in`と`path_out`を変更する。<br>

16行目の`z_value`の閾値を自分の環境に合わせて変更する。
```py
for file in sorted(os.listdir(path_in)):
    lines = []
    pointcloud_without_ground = []
    with open(path_in + file) as file_reader:
        print(file_reader)
        lines = file_reader.readlines()
    for i in range(len(lines)):
        if i < 11:
            continue
        point_array = lines[i].split(" ")
        z_value = float(point_array[2])
        if z_value > -1.7:  # <--ここを変更する
            pointcloud_without_ground.append(lines[i])
```

スクリプトを実行する。
```bash
python3 export_pointcloud_without_ground_nuscenes.py
```
