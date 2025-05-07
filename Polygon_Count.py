import unreal
import time

# 入力した制限値を取得
try:
    triangle_limit_raw = {triangle_limit}
    
    # 整数へ変換
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
    
    unreal.log(f"ポリゴン数の上限: {triangle_limit}")
except Exception as e:
    triangle_limit = 10000
    unreal.log(f"値の変換に失敗しました。デフォルト値を使用します: {triangle_limit}")

def check_triangle_count():
    # 選択されているアセットを取得
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

    for sm in static_meshes:
        try:
            # ポリゴン数を取得 (LOD 0)
            triangle_count = sm.get_num_triangles(0)
            
            # 結果を表示
            if triangle_count > triangle_limit:
                over_limit_assets.append((sm, triangle_count))
                unreal.log(f"❌ 制限超過: {sm.get_name()} - {triangle_count} ポリゴン数 (制限より {triangle_count - triangle_limit} 超過)")
            else:
                unreal.log(f"✅ OK: {sm.get_name()} - {triangle_count} ポリゴン数")
                
        except Exception as e:
            unreal.log_error(f"エラー: {sm.get_name()} の処理中に問題が発生しました: {e}")

    # 結果サマリーを表示
    if over_limit_assets:
        unreal.log("\n=== 制限超過アセット一覧 ===")
        for asset, count in over_limit_assets:
            unreal.log(f"⚠️ {asset.get_name()} - {count} ポリゴン数 (制限より {count - triangle_limit} 超過)")
        unreal.log(f"\n合計 {len(over_limit_assets)} 個のアセットが制限値 {triangle_limit} を超えています")
    else:
        unreal.log("すべてのアセットが制限内です。")

check_triangle_count()