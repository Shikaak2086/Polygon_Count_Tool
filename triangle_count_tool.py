import unreal
import time

# アーティストが入力した制限値を取得
try:
    triangle_limit_raw = {triangle_limit}

    if isinstance(triangle_limit_raw, set) and len(triangle_limit_raw) > 0:
        element = next(iter(triangle_limit_raw))
        if isinstance(element, (int, float)):
            triangle_limit = int(element)
        elif hasattr(element, 'value'):
            triangle_limit = int(element.value)
        else:
            triangle_limit = 10000
    elif isinstance(triangle_limit_raw, (int, float)):
        triangle_limit = int(triangle_limit_raw)
    else:
        triangle_limit = 10000
    
    unreal.log(f"三角形数の上限: {triangle_limit}")
except Exception as e:
    triangle_limit = 10000
    unreal.log(f"値の変換に失敗しました。デフォルト値を使用します: {triangle_limit}")

# 選択されたアセットの三角形数をチェック
def check_triangle_count():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    
    if len(selected_assets) == 0:
        unreal.log_warning("アセットが選択されていません。コンテンツブラウザでアセットを選択してください。")
        return
    
    # Static Meshのみをフィルタリング
    static_meshes = [asset for asset in selected_assets if isinstance(asset, unreal.StaticMesh)]
    
    if len(static_meshes) == 0:
        unreal.log_warning("選択されたアセットの中にStatic Meshが見つかりません。")
        return
    
    unreal.log(f"選択された {len(static_meshes)} 個のStatic Meshをチェックしています...")

    over_limit_assets = []
    
    # 各アセットをチェック
    for sm in static_meshes:
        try:
            triangle_count = sm.get_num_triangles(0)
            
            if triangle_count > triangle_limit:
                over_limit_assets.append((sm, triangle_count))
                unreal.log(f"× 制限超過: {sm.get_name()} - {triangle_count} 三角形 (制限より {triangle_count - triangle_limit} 超過)")
            else:
                unreal.log(f"○ OK: {sm.get_name()} - {triangle_count} 三角形")
                
        except Exception as e:
            unreal.log_error(f"エラー: {sm.get_name()} の処理中に問題が発生しました: {e}")

    # 結果サマリーを表示
    if over_limit_assets:
        unreal.log("\n=== 制限超過アセット一覧 ===")
        for asset, count in over_limit_assets:
            unreal.log(f"⚠️ {asset.get_name()} - {count} 三角形 (制限より {count - triangle_limit} 超過)")
        unreal.log(f"\n合計 {len(over_limit_assets)} 個のアセットが制限値 {triangle_limit} を超えています")
    else:
        unreal.log("すべてのアセットが制限内です。")

check_triangle_count()