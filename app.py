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

# プレイヤーの画像パス生成関数
def get_player_image_path(appearances, attributes):
    # 見た目が2つ、属性が2つ揃っているか判定
    # ※初期状態の「名もなき不定形」「無属性」を除外してカウントするため、
    # 実際には進化でリストに追加された後の長さをチェックします。
    
    # リストに「名もなき不定形」や「無属性」が含まれている間はデフォルトを表示
    has_evolved_appearances = len([a for a in appearances if a != "名もなき不定形"]) >= 2
    has_evolved_attributes = len([a for a in attributes if a != "無属性"]) >= 2
    
    if has_evolved_appearances and has_evolved_attributes:
        # 進化完了している場合、正規の画像パスを生成
        app_sorted = "_".join(sorted([a for a in appearances if a != "名もなき不定形"]))
        attr_sorted = "_".join(sorted([a for a in attributes if a != "無属性"]))
        
        path = f"images/player_{app_sorted}_{attr_sorted}.png"
        
        # ファイルが存在するか確認（存在しない場合はデフォルトを表示）
        if os.path.exists(path):
            return path
            
    # 条件を満たさない、またはファイルがない場合はデフォルト
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
    st.session_state.current_rival = {
        "appearance": app_name,
        "attribute": attr_name,
        "hp": random.randint(50, 150),
        "atk": random.randint(15, 40),
        "def": random.randint(5, 25),
        "spd": random.randint(10, 30),
        "recovery": random.randint(2, 10),
        "evasion": random.randint(5, 20),
        # 36通りのライバル画像
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
        st.image(player_img, width=150, caption=f"見た目: {', '.join(st.session_state.player['appearances'])}")
        st.write(f"**属性:** {', '.join(st.session_state.player['attributes'])}")
        st.write(f"HP: {st.session_state.player['hp']} | ATK: {st.session_state.player['atk']} | DEF: {st.session_state.player['def']}")

    with col_rival:
        st.markdown("### 👾 惑星の支配的生物")
        rival = st.session_state.current_rival
        st.image(rival["image"], width=150, caption=f"見た目: {rival['appearance']}")
        st.write(f"**属性:** {rival['attribute']}")
        st.write(f"HP: {rival['hp']} | ATK: {rival['atk']} | DEF: {rival['def']}")

    st.markdown("---")
    st.write("### 🧬 どの特性を奪って進化しますか？")
    
    # 選択肢の作成
    choices = {}
    if len(st.session_state.player["appearances"]) < 2:
        choices[f"見た目を奪う: {rival['appearance']}"] = "appearance"
    if len(st.session_state.player["attributes"]) < 2:
        choices[f"属性を奪う: {rival['attribute']}"] = "attribute"
    
    choices.update({
        f"HPを強化 (+{rival['hp']}の半分)": "hp",
        f"攻撃力を強化 (+{rival['atk']}の半分)": "atk",
        f"防御力を強化 (+{rival['def']}の半分)": "def",
        f"スピードを強化 (+{rival['spd']}の半分)": "spd",
        f"回復力を強化 (+{rival['recovery']})": "recovery",
        f"回避率を強化 (+5%)": "evasion",
    })

    selected_choice = st.selectbox("進化先を選択", list(choices.keys()))

    if st.button("この特性を吸収して進化する", type="primary"):
        action = choices[selected_choice]
        p = st.session_state.player
        
        # 進化処理
        if action == "appearance":
            p["appearances"].append(rival["appearance"])
        elif action == "attribute":
            p["attributes"].append(rival["attribute"])
        elif action == "hp":
            p["hp"] += rival["hp"] // 2
        elif action == "atk":
            p["atk"] += rival["atk"] // 2
        elif action == "def":
            p["def"] += rival["def"] // 2
        elif action == "spd":
            p["spd"] += rival["spd"] // 2
        elif action == "recovery":
            p["recovery"] += rival["recovery"]
        elif action == "evasion":
            p["evasion"] = min(80, p["evasion"] + 5)

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
        st.image(player_img, width=150)
        st.write(f"**見た目:** {', '.join(st.session_state.player['appearances'])}")
        st.write(f"**属性:** {', '.join(st.session_state.player['attributes'])}")
        st.json(st.session_state.player)
    with col2:
        st.write(f"### 👾 {boss['name']}")
        st.image(boss["image"], width=150)
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
