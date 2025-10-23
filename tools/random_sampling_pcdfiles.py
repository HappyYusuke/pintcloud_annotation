import os
import random
import shutil
import argparse

# --- 設定 ---

# コマンドラインから引数を取得
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="Your input path.")
parser.add_argument("-s", "--savename", type=str, default='random_results', help="Save directory name.")
args = parser.parse_args()

# ディレクトリが存在するベースパス
# スクリプトを同じ階層に置く場合は '.' でOK
base_path = args.input

# 抽出したファイルを保存する新しいディレクトリの名前
output_dir = args.savename

# 各ディレクトリから抽出するファイル数
files_to_sample_per_dir = 85

# --- 設定ここまで ---


def sample_files():
    """
    指定されたディレクトリからランダムにPCDファイルを抽出し、
    新しいディレクトリにコピーするメインの関数。
    """
    # base_pathの1つ上の階層のディレクトリパスを生成
    parent_path = os.path.abspath(os.path.join(base_path, os.pardir))
    # 出力先ディレクトリのフルパスを作成
    output_path = os.path.join(parent_path, output_dir)

    # 出力先ディレクトリが既に存在する場合は削除し、再作成する
    if os.path.exists(output_path):
        print(f"Removing '{output_path}'")
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    print(f"Created '{output_path}'")
    print("-" * 30)

    total_copied_files = 0
    filenumber = 0
    digit = 10

    # ディレクトリを取得
    data_dirs = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

    # pcdファイルが保存されているディレクトリをループ処理
    for dir_name in data_dirs:
        source_dir = os.path.join(base_path, dir_name)

        print(f"Processing: '{source_dir}'")

        try:
            # ディレクトリ内の.pcdファイルをすべてリストアップ
            pcd_files = [f for f in os.listdir(source_dir) if f.endswith('.pcd')]
            
            # 抽出するのに十分なファイルがあるかチェック
            if len(pcd_files) < files_to_sample_per_dir:
                print(f"  Warning: There are less than {files_to_sample_per_dir} files（{len(pcd_files)}）. Copy all the PCD files that are present.")
                sampled_files = pcd_files
            else:
                # ランダムにファイルを抽出
                sampled_files = random.sample(pcd_files, files_to_sample_per_dir)

            # 抽出したファイルを新しいディレクトリにコピー
            for filename in sampled_files:
                source_filepath = os.path.join(source_dir, filename)
                destination_filepath = os.path.join(output_path, filename)
                
                # ファイル名を生成
                # 例: 000000.pcd
                num_zero = 6 - len(str(int(digit / 10)))
                if filenumber < digit:
                    new_filename = f"{'0'*num_zero}{filenumber}"
                elif filenumber >= digit:
                    new_filename = f"{'0'*(num_zero - 1)}{filenumber}"
                    digit *= 10
                else:
                    print(f"Warning: There are {filenumber} files. File name could not be generated because thre are moure than 999,999 files")
                destination_filepath_with_prefix = os.path.join(output_path, new_filename+".pcd")

                shutil.copy2(source_filepath, destination_filepath_with_prefix)

                filenumber += 1
            
            print(f"  -> The {len(sampled_files)} files were saved to '{output_path}'")
            total_copied_files += len(sampled_files)

        except Exception as e:
            print(f"  Error: An error occurred while processing the '{source_dir}': {e}")
        
        print("-" * 30)

    print("All completed!")
    print(f"Total number of files: {total_copied_files}")


if __name__ == '__main__':
    sample_files()

