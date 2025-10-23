# tools
本リポジトリは、点群ファイルからアノテーションするための前処理についてまとめている。
本リポジトリで提供する機能は以下の通りである。

* rosbag2からpcdファイルへ変換
  > pointcloud_to_pcd.sh ([perception_pcl](https://github.com/ros-perception/perception_pcl.git)を使用)

* pcdファイルを、bat-3d用のフォーマットに変換
  > convert_to_bat3d_format_pcd.py

* pcdファイルをランダムに抽出 & ファイル名をbat-3d用に変換
  > random_sampling_pcdfiles.py

* 点群から地面を削除する
  > [bat-3d](https://github.com/walzimmer/bat-3d.git)の[export_pointcloud_without_ground_nuscenes.py](https://github.com/walzimmer/bat-3d/blob/master/scripts/nuscenes_devkit/python-sdk/scripts/export_pointcloud_without_ground_nuscenes.py)を使用


# Installation


# Usage
