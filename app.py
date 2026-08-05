import random
import streamlit as st

# ページの基本設定
st.set_page_config(page_title="惑星進化シミュレーター", page_icon="🧬", layout="centered")

# --- 定数データ ---
APPEARANCES = ["硬質外骨格", "発光器官", "翼膜", "触手","結晶の棘"]
ATTRIBUTES = ["炎熱", "極寒", "電撃", "猛毒", "光子", "暗黒"]

BOSS_LIST = [
    {"name": "星間破壊獣ギガドラゴ", "hp": 500, "atk": 80, "def": 50, "spd": 40},
    {"name": "次元侵略者ヴォイド", "hp": 600, "atk": 70, "def": 70, "spd": 50},
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
    # ライバルのステータス生成
    st.session_state.current_rival = {
        "appearance": random.choice(APPEARANCES),
        "attribute": random.choice(ATTRIBUTES),
        "hp": random.randint(50, 150),
        "atk": random.randint(15, 40),
        "def": random.randint(5, 25),
        "spd": random.randint(10, 30),
        "recovery": random.randint(2, 10),
        "evasion": random.randint(5, 20),
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
    
    # 現在のステータス表示
    with st.expander("🧪 現在のあなたの生物ステータス", expanded=True):
        st.write(f"**見た目:** {', '.join(st.session_state.player['appearances'])}")
        st.write(f"**属性:** {', '.join(st.session_state.player['attributes'])}")
        cols = st.columns(6)
        cols[0].metric("HP", st.session_state.player["hp"])
        cols[1].metric("ATK", st.session_state.player["atk"])
        cols[2].metric("DEF", st.session_state.player["def"])
        cols[3].metric("SPD", st.session_state.player["spd"])
        cols[4].metric("回復", st.session_state.player["recovery"])
        cols[5].metric("回避", f"{st.session_state.player['evasion']}%")

    st.markdown("---")
    st.write("### 👾 遭遇した惑星の支配的生物")
    rival = st.session_state.current_rival
    st.write(f"- **見た目:** {rival['appearance']}")
    st.write(f"- **属性:** {rival['attribute']}")
    r_cols = st.columns(6)
    r_cols[0].metric("HP", rival["hp"])
    r_cols[1].metric("ATK", rival["atk"])
    r_cols[2].metric("DEF", rival["def"])
    r_cols[3].metric("SPD", rival["spd"])
    r_cols[4].metric("回復", rival["recovery"])
    r_cols[5].metric("回避", f"{rival['evasion']}%")

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
        st.write(f"**見た目:** {', '.join(st.session_state.player['appearances'])}")
        st.write(f"**属性:** {', '.join(st.session_state.player['attributes'])}")
        st.json(st.session_state.player)
    with col2:
        st.write(f"### 👾 {boss['name']}")
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
                
_            # ボスの攻撃
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
