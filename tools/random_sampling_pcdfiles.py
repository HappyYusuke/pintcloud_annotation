import os
import random
import shutil

# --- 設定 ---

# ディレクトリが存在するベースパス
# スクリプトを同じ階層に置く場合は '.' でOK
base_path = '/path/to/your/input/path'

# pcdファイルが保存されているディレクトリ名
dir_name = 'your_dir_name_in_data'

# 抽出したファイルを保存する新しいディレクトリの名前
output_folder = 'your_output_dir_name'

# 各ディレクトリから抽出するファイル数
files_to_sample_per_dir = 85

# --- 設定ここまで ---


def sample_files():
    """
    指定されたディレクトリからランダムにPCDファイルを抽出し、
    新しいディレクトリにコピーするメインの関数。
    """
    # 出力先ディレクトリのフルパスを作成
    output_path = os.path.join(base_path, output_folder)

    # 出力先ディレクトリが既に存在する場合は削除し、再作成する
    if os.path.exists(output_path):
        print(f"既存のディレクトリ '{output_path}' を削除しています...")
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    print(f"出力先ディレクトリ '{output_path}' を作成しました。")
    print("-" * 30)

    total_copied_files = 0
    filenumber = 0
    digit = 10

    # {dir_name}1 から {dir_name}12 までのディレクトリをループ処理
    for i in range(1, 13):
        dir_name_num = f'{dir_name}{i}'
        source_dir = os.path.join(base_path, dir_name_num)

        if not os.path.isdir(source_dir):
            print(f"警告: ディレクトリ '{source_dir}' が見つかりません。スキップします。")
            continue

        print(f"処理中のディレクトリ: '{source_dir}'")

        try:
            # ディレクトリ内の.pcdファイルをすべてリストアップ
            pcd_files = [f for f in os.listdir(source_dir) if f.endswith('.pcd')]
            
            # 抽出するのに十分なファイルがあるかチェック
            if len(pcd_files) < files_to_sample_per_dir:
                print(f"  警告: ファイル数が{files_to_sample_per_dir}個未満です（{len(pcd_files)}個）。存在するすべてのPCDファイルをコピーします。")
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
                    print(f"警告: ファイル数が{filenumber}個あります。999,999個以上あるため、ファイル名を生成できませんでした。")
                destination_filepath_with_prefix = os.path.join(output_path, new_filename+".pcd")

                shutil.copy2(source_filepath, destination_filepath_with_prefix)

                filenumber += 1
            
            print(f"  -> {len(sampled_files)}個のファイルを '{output_folder}' にコピーしました。")
            total_copied_files += len(sampled_files)

        except Exception as e:
            print(f"  エラー: ディレクトリ '{source_dir}' の処理中にエラーが発生しました: {e}")
        
        print("-" * 30)

    print("すべての処理が完了しました。")
    print(f"合計コピーファイル数: {total_copied_files}個")


if __name__ == '__main__':
    sample_files()

