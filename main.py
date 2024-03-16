import pyxel

SCENE_TITLE = 0  # タイトル画面
SCENE_PLAY = 1  # ゲーム画面
SCENE_GAMEOVER = 2  # ゲームオーバー画面


class GameCharacter:  # キャラクタークラスの定義
    def __init__(self, x, y, hp, atk, flg, dmg):  # コンストラクタ
        self.x = x  # x属性に引数を代入
        self.y = y  # Y属性に引数を代入
        self.hp = hp  # HP属性に引数を代入
        self.atk = atk  # 攻撃属性に引数を代入
        self.flg = flg  # 出現フラグ属性に引数を代入
        self.dmg = dmg  # ダメージ描画フラグ属性に引数を代入


class Player(GameCharacter):  # プレイヤークラスを定義
    def __init__(self, x, y, hp, atk, flg, dmg, dy, atkcnt, dfs, food, life):  # コンストラクタ
        super().__init__(x, y, hp, atk, flg, dmg)  # 親クラスのコンストラクタを実行
        self.dy = dy  # スクロール用Y座標属性に引数を代入
        self.atkcnt = atkcnt  # 素手攻撃用カウント（3回ダメージで1回攻撃）
        self.dfs = dfs  # 防御属性に引数を代入
        self.food = food  # 食料属性に引数を代入
        self.life = life  # ライフ属性に引数を代入


class Enemy(GameCharacter):  # モンスタークラスを定義
    def __init__(self, x, y, hp, atk, flg, dmg):  # コンストラクタ
        super().__init__(x, y, hp, atk, flg, dmg)  # 親クラスのコンストラクタを実行


def draw_title_scene():  # タイトル画面描画関数
    pyxel.blt(26, 12, 0, 0, 32, 40, 16, 0)  # ロゴ描画
    pyxel.blt(26, 28, 0, 0, 48, 40, 16, 0)  # ロゴ描画
    pyxel.text(33, 45, "8X8Dot", 7)  # タイトル文字描画
    pyxel.text(43, 51, "Quest", 7)  # タイトル文字描画
    pyxel.text(21, 74, "-PRESS SPACE-", (pyxel.frame_count % 8) + 1)  # スタート文字描画


def draw_gameover_scene():  # ゲームオーバー画面描画
    pyxel.text(55, 40, "GAME OVER", 7)  # ゲームオーバー文字描画


class App:
    def __init__(self):  # 初回1回のみ実行
        pyxel.init(96, 96, title="8X8DotQuest", fps=8)  # 画面サイズFPS設定
        pyxel.load("Quest.pyxres")  # PyxelEditorの読み込み
        self.scene = SCENE_TITLE  # 画面遷移の初期化
        self.map_y = None  # マップY座標定義
        self.tmr = None  # 時間を管理する変数定義
        self.pl = None  # プレイヤーオブジェクト作成定義
        self.emy1 = None  # モンスターオブジェクト作成(スライム：map1）定義
        self.emy2 = None  # モンスターオブジェクト作成(スライム：map1）定義
        self.emy_x = None  # 敵X座標リスト定義
        self.emy_y = None  # 敵Y座標リスト定義
        self.emy_hp = None  # 敵HPリスト定義
        self.emy_atk = None  # 敵攻撃フラグリスト定義
        self.emy_flg = None  # 敵出現フラグリスト定義
        self.emy_dmg = None  # 敵ダメージ描画フラグリスト定義
        self.init()  # 初期化関数実行
        pyxel.run(self.update, self.draw)  # 更新処理、描画処理実行

    def init(self):  # 初期化関数
        self.map_y = -248  # マップY座標
        self.tmr = 0  # 時間を管理する変数
        self.pl = Player(8, 48, 10, 10, True, False, 40, 3, 5, 100, 10)  # プレイヤーオブジェクト作成
        self.emy1 = Enemy(56, 272, 10, 1, True, False)  # モンスターオブジェクト作成(スライム：map1）
        self.emy2 = Enemy(72, 272, 10, 1, True, False)  # モンスターオブジェクト作成(スライム：map1）
        self.emy_x = [self.emy1.x, self.emy2.x]  # 敵X座標リスト
        self.emy_y = [self.emy1.y, self.emy2.y]  # 敵Y座標リスト
        self.emy_hp = [self.emy1.hp, self.emy2.hp]  # 敵HPリスト
        self.emy_atk = [self.emy1.atk, self.emy2.atk]  # 敵攻撃フラグリスト
        self.emy_flg = [self.emy1.flg, self.emy2.flg]  # 敵出現フラグリスト
        self.emy_dmg = [self.emy1.dmg, self.emy2.dmg]  # 敵ダメージ描画フラグリスト

    def update(self):  # フレームの更新処理
        self.tmr += 1  # 時間を加算
        if self.scene == SCENE_TITLE:  # 画面遷移がタイトル画面の場合
            self.update_title_scene()  # タイトル画面処理更新関数実行
        elif self.scene == SCENE_PLAY:  # 画面遷移がゲーム画面の場合
            self.update_play_scene()  # ゲーム画面更新処理関数実行
        elif self.scene == SCENE_GAMEOVER:  # 画面遷移がゲームオーバーの場合
            self.update_gameover_scene()  # ゲームオーバー画面更新処理関数実行
        if not self.pl.flg and self.tmr == 10: self.scene = SCENE_GAMEOVER  # プレイヤー出現フラグがFalseかつ10秒後にゲームオーバーに画面遷移

    def update_title_scene(self):  # タイトル画面更新処理関数
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):  # SPACEキーが押された場合
            self.scene = SCENE_PLAY  # ゲーム画面に遷移

    def update_play_scene(self):  # ゲーム画面更新処理関数
        if self.pl.flg: self.move_player()  # プレイヤーを動かす関数実行
        if (0, 8) == pyxel.tilemap(0).pget(move_map_x, move_map_y): # プレイヤーのマップ位置が剣タイルチップの場合
            self.pl.atk += 1    # 攻撃の個数を加算
            pyxel.tilemap(0).pset(move_map_x, move_map_y, (0, 2))   # 

    def update_gameover_scene(self):  # ゲームオーバー画面更新処理関数
        if not self.pl.flg and self.tmr == 20:  # プレイヤー出現フラグがFalseで20秒後
            self.init()  # 初期化関数実行
            self.scene = SCENE_TITLE  # タイトル画面へ遷移

    def draw(self):  # 描画処理
        pyxel.cls(0)  # 背景を黒で更新(画面クリア)

        if self.scene == SCENE_TITLE:  # 画面遷移がタイトル画面の場合
            draw_title_scene()  # タイトル画面描画関数実行
        elif self.scene == SCENE_PLAY:  # 画面遷移がゲーム画面の場合
            self.draw_play_scene()  # ゲーム画面更新処理関数実行
        elif self.scene == SCENE_GAMEOVER:  # 画面遷移がゲームオーバー画面の場合
            draw_gameover_scene()  # ゲーム画面更新処理関数実行

    def draw_play_scene(self):  # ゲーム画面描画関数
        animation = [1, 1, 0, 0]  # キャラアニメーションリスト
        pyxel.bltm(0, self.map_y, 0, 0, 0, 96, 320)  # タイルマップを描画
        pyxel.blt(self.pl.x, self.pl.y, 0, 40, 0, 8, 8, 0) if not self.pl.flg \
            else pyxel.blt(self.pl.x, self.pl.y, 0, 8 * animation[self.tmr % 4], 0, 8, 8, 11)  # プレイヤー描画
        if self.pl.dmg and self.pl.flg:  # ダメージ描画フラグ、出現フラグがTrueの場合
            pyxel.blt(self.pl.x, self.pl.y, 0, 8 * animation[self.tmr % 4], 8, 8, 8, 0)  # プレイヤー描画(ダメージ)
            self.pl.dmg = False  # ダメージ描画フラグをFalseへ
        for i in range(len(self.emy_flg)):  # 敵の要素数
            if self.emy_flg[i]: pyxel.blt(self.emy_x[i], self.emy_y[i] + self.map_y, 0, 8 * animation[self.tmr % 4] + 16, 0, 8, 8, 0)  # スライム描画
        for i in range(len(self.emy_flg)):  # 敵の要素数
            if self.emy_dmg[i]:  # ダメージ描画フラグがTrueの場合
                pyxel.blt(self.emy_x[i], self.emy_y[i] + self.map_y, 0, 33, 0, 8, 8, 0) if self.emy_hp[i] == 0 \
                    else pyxel.blt(self.emy_x[i], self.emy_y[i] + self.map_y, 0, 8 * animation[self.tmr % 4] + 16, 8, 8, 8, 0)  # スライム描画(ダメージ)
                self.draw_enemyhp(i)  # モンスターHP描画関数実行
                # if pyxel.frame_count % 16:
                self.emy_dmg[i] = False  # ダメージ描画フラグをFalseへ
        pyxel.rect(0, 72, 96, 24, 2)  # 画面下部のステータス部分を描画
        pyxel.rect(1, 73, 94, 22, 0)  # 画面下部のステータス部分を描画
        pyxel.text(3, 74, "HP", 8)  # HPテキスト描画
        for s in range(10, -1, -1):  # 10～-1の範囲を-1減算
            if self.pl.hp == s:  # プレイヤーHPがsの場合
                for j in range(s):  # s回forで回す
                    pyxel.blt(j * 8 + 12, 72, 0, 32, 16, 8, 8, 0)  # プレイヤーHP画像描画(ステータス)
                for i in range(10 - s):  # 10-s回forで回す
                    pyxel.blt(i * 8 + (84 - (9 - s) * 8), 72, 0, 40, 16, 8, 8, 0)  # プレイヤー空HP画像描画(ステータス)
        pyxel.blt(3, 80, 0, 24, 16, 8, 8, 0)  # 剣アイコン描画
        a = f" {self.pl.atk}"  # 剣の数を変数に代入
        pyxel.text(8, 81, a, 7)  # 剣の数をテキスト描画
        pyxel.blt(27, 80, 0, 16, 24, 8, 8, 0)  # 盾アイコン描画
        d = f" {self.pl.dfs}"  # 盾の数を変数に代入
        pyxel.text(32, 81, d, 7)  # 盾の数をテキスト描画
        pyxel.blt(51, 80, 0, 48, 16, 8, 8, 0)  # 食料アイコン描画
        f = f" {self.pl.food}"  # 食事の数を変数に代入
        pyxel.text(56, 81, f, 7)  # 食事の数をテキスト描画
        pyxel.blt(75, 80, 0, 24, 24, 8, 8, 0)  # ライフアイコン描画
        l = f" {self.pl.life}"  # ライフの数を変数に代入
        pyxel.text(80, 81, l, 7)  # ライフの数をテキスト描画

    def move_player(self):  # プレイヤーを動かす関数
        global move_map_x, move_map_y  # グローバル変数
        move_map_x = int(self.pl.x / 8)  # プレイヤーのマップタイルの位置を計算X座標
        move_map_y = int(self.pl.dy / 8) + 32  # プレイヤーのマップタイルの位置を計算Y座標
        r_map = pyxel.tilemap(0).pget(move_map_x + 1, move_map_y)  # プレイヤーの右のマップタイルの判定
        l_map = pyxel.tilemap(0).pget(move_map_x - 1, move_map_y)  # プレイヤーの右のマップタイルの判定
        u_map = pyxel.tilemap(0).pget(move_map_x, move_map_y - 1)  # プレイヤーの上のマップタイルの判定
        d_map = pyxel.tilemap(0).pget(move_map_x, move_map_y + 1)  # プレイヤーの下のマップタイルの判定
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):  # 上キーが押された場合
            if u_map == (0, 2) or u_map == (0, 8):  # プレイヤーの右のマップタイルの進入禁止判定
                self.map_y += 8  # マップY座標を加算してスクロール
                self.pl.dy -= 8  # スクロール用Y座標を減算してスクロール
                for i in range(len(self.emy_flg)):  # 敵の要素数
                    if self.check_enemy(i) and self.emy_flg[i]:  # 敵出現フラグがTrueなら敵との接触をチェックする関数実行
                        self.map_y -= 8  # マップY座標を加算してスクロール
                        self.pl.dy += 8  # スクロール用Y座標を減算してスクロール
                        self.attack(i)  # 攻撃関数実行
                        self.defence(i)  # 防御関数実行
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):  # 下キーが押された場合
            if d_map == (0, 2) or d_map == (0, 8):  # プレイヤーの右のマップタイルの進入禁止判定
                self.map_y -= 8  # マップY座標を減算してスクロール
                self.pl.dy += 8  # スクロール用Y座標を加算してスクロール
                for i in range(len(self.emy_flg)):  # 敵の要素数
                    if self.check_enemy(i) and self.emy_flg[i]:  # 敵出現フラグがTrueなら敵との接触をチェックする関数実行
                        self.map_y += 8  # マップY座標を減算してスクロール
                        self.pl.dy -= 8  # スクロール用Y座標を加算してスクロール
                        self.attack(i)  # 攻撃関数実行
                        self.defence(i)  # 防御関数実行
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):  # 右キーが押された場合
            if r_map == (0, 2) or r_map == (0, 8):  # プレイヤーの右のマップタイルの進入禁止判定
                self.pl.x += 8  # プレイヤーX座標を加算して移動
                for i in range(len(self.emy_flg)):  # 敵の要素数
                    if self.check_enemy(i) and self.emy_flg[i]:  # 敵出現フラグがTrueなら敵との接触をチェックする関数実行
                        self.pl.x -= 8  # プレイヤーX座標を加算して移動
                        self.attack(i)  # 攻撃関数実行
                        self.defence(i)  # 防御関数実行
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):  # 左キーが押された場合
            if l_map == (0, 2) or l_map == (0, 8):  # プレイヤーの左のマップタイルの進入禁止判定
                self.pl.x -= 8  # プレイヤーX座標を減算して移動
                for i in range(len(self.emy_flg)):  # 敵の要素数
                    if self.check_enemy(i) and self.emy_flg[i]:  # 敵出現フラグがTrueなら敵との接触をチェックする関数実行
                        self.pl.x += 8  # プレイヤーX座標を減算して移動
                        self.attack(i)  # 攻撃関数実行
                        self.defence(i)  # 防御関数実行

    def check_enemy(self, en):  # 敵との接触をチェックする関数
        chk = False  # chkにFalseを代入
        dx = abs(self.emy_x[en] - self.pl.x)  # 絶対値で敵との距離を計算
        dy = abs(self.emy_y[en] - (self.pl.dy + 256))  # 絶対値で敵との距離を計算
        if dx <= 0 and dy <= 0: chk = True  # 敵との距離判定→chkにTrueを代入
        return chk  # chkを戻り値として返す

    def attack(self, en):  # 攻撃関数
        if self.pl.atk > 0:  # プレイヤー攻撃力が1以上の場合
            self.emy_hp[en] -= 1  # 敵HP減算
            self.pl.atk -= 1  # プレイヤー攻撃力減算
            self.emy_dmg[en] = True  # ダメージ描画フラグをTrueへ
        else:
            self.pl.atkcnt -= 1  # 素手攻撃用カウントを減算
            if self.pl.atkcnt == 0:  # 素手攻撃用カウントが0の場合
                self.emy_hp[en] -= 1  # 敵HP減算
                self.pl.atkcnt = 3  # 素手攻撃用カウントを初期化
                self.emy_dmg[en] = True  # ダメージ描画フラグをTrueへ
        if self.emy_hp[en] <= 0:  # 敵HPが0以下の場合
            self.emy_flg[en] = False  # 敵出現フラグをFalseへ

    def defence(self, en):  # 防御関数
        if self.pl.dfs > 0:  # プレイヤー防御力が1以上の場合
            ed = self.emy_atk[en] - 1  # ダメージ値計算
            self.pl.hp -= ed  # プレイヤHP減算
            self.pl.dfs -= 1  # プレイヤー防御力を減算
            if ed > 0: self.pl.dmg = True  # ダメージが1以上の場合のみダメージ描画フラグをTrueへ
        else:
            self.pl.hp -= self.emy_atk[en]  # プレイヤHP減算
            self.pl.dmg = True  # ダメージ描画フラグをTrueへ
        if self.pl.hp <= 0:  # プレイヤーHPが0以下の場合
            self.pl.flg = False  # プレイヤー出現フラグをFalseへ
            self.tmr = 0

    def draw_enemyhp(self, en):  # モンスターHP描画関数
        for j in range(9, 0, -1):  # 9～0の範囲を-1減算
            if self.pl.atk > 0 and self.emy_hp[en] == j: pyxel.text(self.emy_x[en] + 2, (self.emy_y[en] + 2) + self.map_y, f'{j}', 8)  # モンスターHP描画
            if self.pl.atkcnt == 3 and self.emy_hp[en] == j: pyxel.text(self.emy_x[en] + 2, (self.emy_y[en] + 2) + self.map_y, f'{j}', 8)  # モンスターHP描画(素手攻撃用)


App()  # アプリケーションの実行
