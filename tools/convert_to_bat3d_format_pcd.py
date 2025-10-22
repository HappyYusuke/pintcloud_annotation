import os

# --- 設定項目 ---

# 変換元のASCII PCDファイルが入っているディレクトリ
# (例: x y z intensity tag line timestamp ... というフィールドを持つPCD)
path_in = f'/path/to/your/input/path'

# 変換後のPCDファイルを保存するディレクトリ
# (bat-3dが読み込む x y z intensity のみ、ASCII形式)
path_out = f'/path/to/your/output/path'

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
                    # Z軸のフィルタリングを削除
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
                    print(f"  警告: スキップされた不正な行: {line}")
                    continue
                    
    except Exception as e:
        print(f"  エラー: ファイル '{filepath}' の読み込み中に失敗: {e}")
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
        print(f"  エラー: ファイル '{filepath}' への書き込み中に失敗: {e}")
        return False
        
    return True

def convert_and_filter():
    """
    メインの処理関数。
    """
    if not os.path.exists(path_in):
        print(f"エラー: 入力ディレクトリが見つかりません: {path_in}")
        return

    os.makedirs(path_out, exist_ok=True)
    
    print(f"処理を開始します...")
    print(f"入力 (ASCII): {path_in}")
    print(f"出力 (bat-3d ASCII): {path_out}")
    print("Z軸フィルタリングは行いません。")
    print("-" * 30)

    total_files = 0
    success_files = 0

    for filename in sorted(os.listdir(path_in)):
        if filename.endswith(".pcd"):
            total_files += 1
            input_filepath = os.path.join(path_in, filename)
            output_filepath = os.path.join(path_out, filename)
            
            print(f"処理中: {filename}")
            
            # 1. ASCIIで読み込み、フォーマット変換
            formatted_lines = read_and_reformat_ascii(input_filepath)
            
            if formatted_lines is not None:
                # 2. bat-3d形式でASCII保存
                if save_ascii_pcd(output_filepath, formatted_lines):
                    print(f"  -> 成功: {len(formatted_lines)} 点を '{output_filepath}' に保存しました。")
                    success_files += 1
                else:
                    print(f"  -> 失敗: ファイルの保存に失敗しました。")
            else:
                 print(f"  -> 失敗: ファイルの読み込みに失敗しました。")

    print("-" * 30)
    print(f"処理完了: {total_files} ファイル中 {success_files} ファイルの処理に成功しました。")

# スクリプトの実行
if __name__ == "__main__":
    convert_and_filter()


