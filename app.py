import random
import streamlit as st
import os
# ページの基本設定
st.set_page_config(page_title="惑星進化シミュレーター", page_icon="🧬", layout="centered")

# --- 定数データ（画像マッピングを追加） ---
# 見た目に対応する画像パス（ローカルファイルまたはURL）
# --- 定数データと画像マッピング用リスト ---
APPEARANCES = ["外骨格", "発光器官", "翼膜", "触手", "機械生命体"] # 6種
ATTRIBUTES = ["炎熱", "極寒", "電撃", "猛毒", "光子", "暗黒"] # 6種

# ライバルの画像パス生成関数 (30通り: 5見た目 × 6属性)
def get_rival_image_path(appearance, attribute):
    # 例: ローカルの images/rivals/ フォルダに 'rival_硬質外骨格_炎熱.png' などの画像を置く想定
    # ※デモ用にプレースホルダーURLを返すことも可能
    return f"images/rival_{appearance}_{attribute}.png"

def get_player_image_path(appearances, attributes):
    # 初期値を除外したリストを作成
    evolved_apps = [a for a in appearances if a != "名もなき不定形"]
    evolved_attrs = [a for a in attributes if a != "無属性"]
    
    # 見た目が2つ、属性が2つ揃っている場合
    if len(evolved_apps) == 2 and len(evolved_attrs) == 2:
        
        # 1. ソートしたパスをチェック
        app_sorted = "_".join(sorted(evolved_apps))
        attr_sorted = "_".join(sorted(evolved_attrs))
        path_sorted = f"images/player_{app_sorted}_{attr_sorted}.png"
        
        if os.path.exists(path_sorted):
            return path_sorted
            
        # 2. 見つからない場合、ソートしていない（追加順の）パスをチェック
        app_raw = "_".join(evolved_apps)
        attr_raw = "_".join(evolved_attrs)
        path_raw = f"images/player_{app_raw}_{attr_raw}.png"
        
        if os.path.exists(path_raw):
            return path_raw
            
        app_sorted2 = "_".join(evolved_apps)
        attr_sorted2 = "_".join(sorted(evolved_attrs))
        path_sorted2 = f"images/player_{app_sorted2}_{attr_sorted2}.png"
        
        if os.path.exists(path_sorted2):
            return path_sorted2
            
        # 2. 見つからない場合、ソートしていない（追加順の）パスをチェック
        app_raw2 = "_".join(sorted(evolved_apps))
        attr_raw2 = "_".join(evolved_attrs)
        path_raw2 = f"images/player_{app_raw2}_{attr_raw2}.png"
        
        if os.path.exists(path_raw2):
            return path_raw2   
    # 3. どちらも見つからない、または条件を満たさない場合はデフォルト
    return "images/player_defalt.png"
BOSS_LIST = [
    {"name": "星間破壊獣ギガドラゴ", "hp": 500, "atk": 80, "def": 50, "spd": 40, "image": "images/gigadrago.png"},
    {"name": "次元侵略者ヴォイド", "hp": 600, "atk": 70, "def": 70, "spd": 50, "image": "images/void.png"},
]

# --- セッション状態の初期化 ---
if "phase" not in st.session_state:
    st.session_state.phase = "start"  # start, exploring, boss, result
if "cycle" not in st.session_state:
    st.session_state.cycle = 1
# プレイヤーのステータス
# プレイヤーのステータス初期化の部分に追加
if "player" not in st.session_state:
    st.session_state.player = {
        "appearances": ["名もなき不定形"],
        "attributes": ["無属性"],
        "hp": 100,
        "atk": 20,
        "def": 10,
        "spd": 15,
        "recovery": 5,
        "evasion": 10,
    }

# 【追加】すでに選択したステータスを記録するリスト
if "chosen_stats" not in st.session_state:
    st.session_state.chosen_stats = []
if "current_rival" not in st.session_state:
    st.session_state.current_rival = None
if "planet_env" not in st.session_state:
    st.session_state.planet_env = ""

# --- 関数群 ---
def generate_planet():
    environments = ["マグマが噴出する灼熱", "全てが凍りつく深淵", "強酸の雨が降る", "高重力で歪んだ", "サイコウェーブが飛び交う"]
    st.session_state.planet_env = random.choice(environments)

def generate_rival():
    app_name = random.choice(APPEARANCES)
    attr_name = random.choice(ATTRIBUTES)
    
    # 見た目ごとの基本ステータス（ベース値）を設定
    # 外骨格：HPと防御力高め、スピード低め
    if app_name == "外骨格":
        hp = random.randint(100, 180)
        atk = random.randint(15, 35)
        def_val = random.randint(20, 40)
        spd = random.randint(5, 15)
        recovery = random.randint(2, 6)
        evasion = random.randint(5, 15)
        
    # 発光器官：回避率高め、攻撃力低め
    elif app_name == "発光器官":
        hp = random.randint(50, 100)
        atk = random.randint(10, 25)
        def_val = random.randint(5, 15)
        spd = random.randint(15, 30)
        recovery = random.randint(2, 8)
        evasion = random.randint(25, 45)
        
    # 翼膜：スピード高め、防御力低め
    elif app_name == "翼膜":
        hp = random.randint(60, 110)
        atk = random.randint(20, 40)
        def_val = random.randint(2, 10)
        spd = random.randint(30, 50)
        recovery = random.randint(2, 8)
        evasion = random.randint(15, 30)
        
    # 触手：回復力高め、回避率低め
    elif app_name == "触手":
        hp = random.randint(80, 130)
        atk = random.randint(15, 35)
        def_val = random.randint(10, 25)
        spd = random.randint(15, 25)
        recovery = random.randint(12, 25)
        evasion = random.randint(2, 10)
        
    # 機械生命体：攻撃力高め、回復力低め
    elif app_name == "機械生命体":
        hp = random.randint(90, 140)
        atk = random.randint(35, 60)
        def_val = random.randint(15, 30)
        spd = random.randint(15, 30)
        recovery = random.randint(0, 3)
        evasion = random.randint(5, 15)
        
    else:
        # フォールバック（念のため）
        hp, atk, def_val, spd, recovery, evasion = 100, 20, 10, 15, 5, 10

    st.session_state.current_rival = {
        "appearance": app_name,
        "attribute": attr_name,
        "hp": hp,
        "atk": atk,
        "def": def_val,
        "spd": spd,
        "recovery": recovery,
        "evasion": evasion,
        "image": get_rival_image_path(app_name, attr_name)
    }

def reset_game():
    st.session_state.phase = "start"
    st.session_state.cycle = 1
    st.session_state.player = {
        "appearances": ["名もなき不定形"],
        "attributes": ["無属性"],
        "hp": 100,
        "atk": 20,
        "def": 10,
        "spd": 15,
        "recovery": 5,
        "evasion": 10,
    }
    st.session_state.current_rival = None

# --- UI: スタート画面 ---
if st.session_state.phase == "start":
    st.title("🧬 惑星進化侵略シミュレーター")
    st.write("不定形生物をランダムな惑星に送り込み、生態系の頂点に立って最強の生物へと進化させろ！")
    st.info("【ルール】\n- 全10回の進化サイクルを繰り返します。\n- 各惑星の支配的生物から「1つの特性」を奪い進化します。\n- 最終的に『見た目2つ、属性2つ、その他各1つ』の特性を持つ究極体となり、ボスに挑みます。")
    
    if st.button("進化の旅に出発する", type="primary"):
        st.session_state.phase = "exploring"
        generate_planet()
        generate_rival()
        st.rerun()

# --- UI: 探索・進化フェーズ (1〜10サイクル) ---
elif st.session_state.phase == "exploring":
    st.subheader(f"🌐 第 {st.session_state.cycle} / 10 惑星探索")
    st.write(f"現在の環境: **{st.session_state.planet_env}惑星**")
    
    # 2カラムで「プレイヤー」と「ライバル」の見た目とステータスを左右に表示
    col_player, col_rival = st.columns(2)

    with col_player:
        st.markdown("### 🧪 あなたの生物")
        # 225通りのプレイヤー画像を取得して表示
        player_img = get_player_image_path(
            st.session_state.player['appearances'], 
            st.session_state.player['attributes']
        )
        # ※画像ファイルがまだ無い場合の代替としてエラーを防ぐため st.image を使う際は注意
        st.image(player_img, width=300, caption=f"見た目: {', '.join(st.session_state.player['appearances'])}")
        st.write(f"**属性:** {', '.join(st.session_state.player['attributes'])}")
        st.write(f"HP: {st.session_state.player['hp']} | ATK: {st.session_state.player['atk']} | DEF: {st.session_state.player['def']}")

    with col_rival:
        st.markdown("### 👾 惑星の支配的生物")
        rival = st.session_state.current_rival
        st.image(rival["image"], width=300, caption=f"見た目: {rival['appearance']}")
        st.write(f"**属性:** {rival['attribute']}")
        st.write(f"HP: {rival['hp']} | ATK: {rival['atk']} | DEF: {rival['def']}")

    st.markdown("---")
    st.write("### 🧬 どの特性を奪って進化しますか？")
    
    # --- 選択肢の作成 ---
    choices = {}
    
    # 見た目（上限2つ）
    evolved_apps = [a for a in st.session_state.player["appearances"] if a != "名もなき不定形"]
    if len(evolved_apps) < 2:
        choices[f"見た目を奪う: {rival['appearance']}"] = ("appearance", None)
        
    # 属性（上限2つ）
    evolved_attrs = [a for a in st.session_state.player["attributes"] if a != "無属性"]
    if len(evolved_attrs) < 2:
        choices[f"属性を奪う: {rival['attribute']}"] = ("attribute", None)
    
    # 各ステータス（未選択のものだけ追加）
    stat_options = {
        "hp": f"HPを強化 (+{rival['hp']})",
        "atk": f"攻撃力を強化 (+{rival['atk']})",
        "def": f"防御力を強化 (+{rival['def']})",
        "spd": f"スピードを強化 (+{rival['spd']})",
        "recovery": f"回復力を強化 (+{rival['recovery']})",
        "evasion": f"回避率を強化 (+{rival['evasion']})"
    }

    for stat_key, label in stat_options.items():
        if stat_key not in st.session_state.chosen_stats:
            choices[label] = ("stat", stat_key)

    selected_choice = st.selectbox("進化先を選択", list(choices.keys()))

    if st.button("この特性を吸収して進化する", type="primary"):
        action_type, detail = choices[selected_choice]
        p = st.session_state.player
        
        # --- 1. 選択した特性の吸収処理 ---
        if action_type == "appearance":
            if "名もなき不定形" in p["appearances"]:
                p["appearances"] = [rival["appearance"]]
            else:
                if rival["appearance"] not in p["appearances"]:
                    p["appearances"].append(rival["appearance"])
                
        elif action_type == "attribute":
            if "無属性" in p["attributes"]:
                p["attributes"] = [rival["attribute"]]
            else:
                if rival["attribute"] not in p["attributes"]:
                    p["attributes"].append(rival["attribute"])
                
        elif action_type == "stat":
            # 選んだステータスを記録（2度と選べなくする）
            st.session_state.chosen_stats.append(detail)
            
            if detail == "hp":
                p["hp"] += rival["hp"] 
            elif detail == "atk":
                p["atk"] += rival["atk"]
            elif detail == "def":
                p["def"] += rival["def"]
            elif detail == "spd":
                p["spd"] += rival["spd"]
            elif detail == "recovery":
                p["recovery"] += rival["recovery"]
            elif detail == "evasion":
                p["evasion"] = min(80, p["evasion"] + rival["evasion"])
        # --- 2. 【追加】ライバルステータスの20%分を自動加算 ---
        p["hp"] += int(rival["hp"] * 0.1)
        p["atk"] += int(rival["atk"] * 0.1)
        p["def"] += int(rival["def"] * 0.1)
        p["spd"] += int(rival["spd"] * 0.1)
        p["recovery"] += int(rival["recovery"] * 0.1)
        p["evasion"] = min(80, p["evasion"] + int(rival["evasion"] * 0.1))
        # 次のサイクルへ、またはボスへ
        if st.session_state.cycle >= 10:
            st.session_state.phase = "boss"
            st.session_state.boss = random.choice(BOSS_LIST)
        else:
            st.session_state.cycle += 1
            generate_planet()
            generate_rival()
        st.rerun()

# --- UI: ボス戦フェーズ ---
elif st.session_state.phase == "boss":
    st.subheader("⚔️ 最終決戦：ボス級侵略生物との遭遇")
    boss = st.session_state.boss
    st.error(f"宇宙の覇者 **{boss['name']}** が現れた！")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🧬 あなたの究極生物")
        player_img = get_player_image_path(
            st.session_state.player['appearances'], 
            st.session_state.player['attributes']
        )
        st.image(player_img, width=300)
        st.write(f"**見た目:** {', '.join(st.session_state.player['appearances'])}")
        st.write(f"**属性:** {', '.join(st.session_state.player['attributes'])}")
        st.json(st.session_state.player)
    with col2:
        st.write(f"### 👾 {boss['name']}")
        st.image(boss["image"], width=300)
        st.json(boss)

    if st.button("ボスに戦いを挑む！", type="primary"):
        # 簡易ターン制戦闘シミュレーション
        p_hp = st.session_state.player["hp"]
        p_max_hp = p_hp
        b_hp = boss["hp"]
        
        log = []
        turn = 1
        while p_hp > 0 and b_hp > 0 and turn <= 20:
            # プレイヤーの攻撃
            if random.randint(1, 100) > boss.get("evasion", 10):
                dmg = max(5, st.session_state.player["atk"] - boss["def"] // 2)
                b_hp -= dmg
                log.append(f"ターン{turn}: あなたの攻撃！ ボスに {dmg} のダメージ (残りHP: {max(0, b_hp)})")
            else:
                log.append(f"ターン{turn}: あなたの攻撃！ しかしボスは回避した！")
                
            if b_hp <= 0:
                break
                
           # ボスの攻撃
            if random.randint(1, 100) > st.session_state.player["evasion"]:
                dmg = max(5, boss["atk"] - st.session_state.player["def"] // 2)
                p_hp -= dmg
                log.append(f"ターン{turn}: ボスの反撃！ あなたは {dmg} のダメージ (残りHP: {max(0, p_hp)})")
            else:
                log.append(f"ターン{turn}: ボスの攻撃！ しかしあなたは華麗に回避した！")
            
            # ターン終了時回復
            p_hp = min(p_max_hp, p_hp + st.session_state.player["recovery"])
            turn += 1

        st.session_state.battle_log = log
        st.session_state.battle_won = b_hp <= 0
        st.session_state.phase = "result"
        st.rerun()

# --- UI: リザルト画面 ---
elif st.session_state.phase == "result":
    st.subheader("🏆 戦闘結果")
    if st.session_state.battle_won:
        st.success("🎉 おめでとうございます！ボスを撃破し、この宇宙の真の支配者となりました！")
    else:
        st.error("💀 敗北しました… 究極生物の進化が足りなかったようです。")

    with st.expander("📜 戦闘ログの詳細"):
        for line in st.session_state.get("battle_log", []):
            st.text(line)

    if st.button("もう一度最初から遊ぶ"):
        reset_game()
        st.rerun()
