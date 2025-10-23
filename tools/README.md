# tools
本リポジトリは、点群ファイルからアノテーションするための前処理についてまとめている。<br>
本リポジトリで提供する機能は以下の通りである。

* rosbag2からpcdファイルへ変換
  > pointcloud_to_pcd.sh ([perception_pcl](https://github.com/ros-perception/perception_pcl.git)の[pointcloud_to_pcd]([pcl_ros/tools/pointcloud_to_pcd.cpp](https://github.com/ros-perception/perception_pcl/blob/humble/pcl_ros/tools/pointcloud_to_pcd.cpp))を使用)

* pcdファイルを、bat-3d用のフォーマットに変換
  > convert_to_bat3d_format_pcd.py

* pcdファイルをランダムに抽出 & ファイル名をbat-3d用に変換
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
git clone https://github.com/HappyYusuke/pointcloud_annotation.git
```


## perception_pcl
[perception_pcl](https://github.com/ros-perception/perception_pcl.git)にはInstallationが書かれておらず、主はHumbleでまともに動かなかったので、ここにインストール方法を残しておきます。

`humble`ブランチのリポジトリをros2ワークスペースにクローン
```bash
cd ~/ros2_ws/src
git clone https://github.com/ros-perception/perception_pcl.git -b humble
```

依存関係をインストール
```bash
cd ~/ros2_ws
rosdep install -i --from-path src --rosdistro humble -y
```

ファイルを置換
```bash

```

ビルド
```bash
colcon build --symlink-install
```

# Usage
