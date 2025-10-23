import os
import argparse

# --- 設定項目 ---

# 変換元のASCII PCDファイルが入っているディレクトリまでのパス
# コマンドラインから引数を取得
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="Your input path.")
parser.add_argument("-s", "--savename", type=str, default='convert_results', help="Save directory name.")
args = parser.parse_args()

# (例: x y z intensity tag line timestamp ... というフィールドを持つPCD)
base_path = args.input

# 変換後のPCDファイルを保存するディレクトリ名を指定
# (bat-3dが読み込む x y z intensity のみ、ASCII形式)
output_name = args.savename

# --- スクリプト本体 ---

def read_and_reformat_ascii(filepath):
    """
    ASCII形式のPCDファイルを読み込み、
    bat-3dが要求する形式(x y z intensity)の文字列リストを返す。
    """
    reformatted_points_lines = []
    header_finished = False
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # ヘッダー部分の処理
                if not header_finished:
                    if line.startswith('DATA ascii'):
                        header_finished = True
                    continue
                
                # データ行の処理
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split(' ')
                
                # 少なくともx, y, z, intensityの4つのフィールドがあるか確認
                if len(parts) < 4:
                    continue # 予期しない行はスキップ
                
                try:
                    # (元のファイルに4つ以上フィールドがあっても、最初の4つだけ使う)
                    
                    # データが数値として有効かどうかの簡易チェック
                    float(parts[0])
                    float(parts[1])
                    float(parts[2])
                    float(parts[3])
                    
                    reformatted_line = f"{parts[0]} {parts[1]} {parts[2]} {parts[3]}\n"
                    reformatted_points_lines.append(reformatted_line)
                except ValueError:
                    # floatに変換できない行（不正なデータ）はスキップ
                    print(f"  Warning: Skipped: {line}")
                    continue
                    
    except Exception as e:
        print(f"  Error: Loading failed '{filepath}': {e}")
        return None

    return reformatted_points_lines

def save_ascii_pcd(filepath, points_lines):
    """
    bat-3dが期待するヘッダーと、フィルタリング済みの点群データを
    新しいASCII PCDファイルとして書き込む。
    """
    num_points = len(points_lines)
    
    # bat-3dが期待するヘッダー (x y z intensity, ASCII)
    header = (
        "# .PCD v0.7 - Point Cloud Data file format\n"
        "VERSION 0.7\n"
        "FIELDS x y z intensity\n"
        "SIZE 4 4 4 4\n"
        "TYPE F F F F\n"
        "COUNT 1 1 1 1\n"
        f"WIDTH {num_points}\n"
        "HEIGHT 1\n"
        "VIEWPOINT 0 0 0 1 0 0 0\n"
        f"POINTS {num_points}\n"
        "DATA ascii\n"
    )
    
    try:
        with open(filepath, 'w') as f:
            f.write(header)
            f.writelines(points_lines) # フィルタリング済みの行をすべて書き込む
    except Exception as e:
        print(f"  Error: Failed to write to '{filepath}': {e}")
        return False
        
    return True

def convert_and_filter():
    """
    メインの処理関数。
    """
    if not os.path.exists(base_path):
        print(f"Error: Not found: {base_path}")
        return

    # 保存先のパスを生成
    parent_path = os.path.abspath(os.path.join(base_path, os.pardir))
    output_path = os.path.join(parent_path, output_name)
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Start processing ...")
    print(f"Input (ASCII): {base_path}")
    print(f"Output (bat-3d ASCII): {output_path}")
    print("-" * 30)

    total_files = 0
    success_files = 0

    for filename in sorted(os.listdir(base_path)):
        if filename.endswith(".pcd"):
            total_files += 1
            input_filepath = os.path.join(base_path, filename)
            output_filepath = os.path.join(output_path, filename)
            
            print(f"Processing: {filename}")
            
            # 1. ASCIIで読み込み、フォーマット変換
            formatted_lines = read_and_reformat_ascii(input_filepath)
            
            if formatted_lines is not None:
                # 2. bat-3d形式でASCII保存
                if save_ascii_pcd(output_filepath, formatted_lines):
                    print(f"  -> Success: {len(formatted_lines)} points saved to '{output_filepath}'")
                    success_files += 1
                else:
                    print(f"  -> Failed: Failed to save file.")
            else:
                 print(f"  -> Failed: Failed to load file")

    print("-" * 30)
    print(f"Finished: Success -> {total_files} / {success_files}")

# スクリプトの実行
if __name__ == "__main__":
    convert_and_filter()


