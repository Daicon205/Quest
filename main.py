import pyxel


class GameCharacter:  # キャラクタークラスの定義
    def __init__(self, x, y):  # コンストラクタ
        self.x = x  # x属性に引数を代入
        self.y = y  # Y属性に引数を代入


class Player(GameCharacter):  # プレイヤークラスを定義
    def __init__(self, x, y, dy):  # コンストラクタ
        super().__init__(x, y)  # 親クラスのコンストラクタを実行
        self.dy = dy  # スクロール用Y座標属性に引数を代入


class Enemy(GameCharacter):  # モンスタークラスを定義
    def __init__(self, x, y):  # コンストラクタ
        super().__init__(x, y)  # 親クラスのコンストラクタを実行


class App:
    def __init__(self):
        pyxel.init(96, 96, title="8DotQuest", fps=5)  # 画面サイズFPS設定
        pyxel.load("Quest.pyxres")  # PyxelEditorの読み込み

        self.pl = Player(8, 48, 40)  # プレイヤーオブジェクト作成
        self.emy1 = Enemy(16, 96)  # モンスターオブジェクト作成

        self.map_y = -248  # マップY座標

        pyxel.run(self.update, self.draw)  # 更新処理、描画処理実行

    def update(self):  # フレームの更新処理
        self.move_player()  # プレイヤーを動かす関数実行

    def draw(self):  # 描画処理
        pyxel.cls(0)  # 背景を黒で更新
        pyxel.bltm(0, self.map_y, 0, 0, 0, 96, 320)  # タイルマップを描画
        pyxel.blt(self.pl.x, self.pl.y, 0, 8 * (pyxel.frame_count % 2), 0, 8, 8, 0)  # プレイヤー描画
        pyxel.blt(self.emy1.x, self.emy1.y + self.map_y, 0, 8 * (pyxel.frame_count % 2) + 16, 0, 8, 8, 0)  # スライム描画
        pyxel.rect(0, 72, 96, 24, 2)  # 画面下部のステータス部分を描画
        pyxel.rect(1, 73, 94, 22, 0)  # 画面下部のステータス部分を描画
        for j in range(10):
            pyxel.blt(j*8+8, 72, 0, 32, 16, 8, 8, 0)
        #for j in range(9):
        #    pyxel.blt(j*8+8, 72, 0, 40, 16, 8, 8, 0)
        

    def move_player(self):  # プレイヤーを動かす関数
        move_map_x = int(self.pl.x / 8)  # プレイヤーのマップタイルの位置を計算X座標
        move_map_y = int(self.pl.dy / 8) + 32  # プレイヤーのマップタイルの位置を計算Y座標
        r_map = pyxel.tilemap(0).pget(move_map_x + 1, move_map_y)  # プレイヤーの右のマップタイルの判定
        l_map = pyxel.tilemap(0).pget(move_map_x - 1, move_map_y)  # プレイヤーの右のマップタイルの判定
        u_map = pyxel.tilemap(0).pget(move_map_x, move_map_y - 1)  # プレイヤーの上のマップタイルの判定
        d_map = pyxel.tilemap(0).pget(move_map_x, move_map_y + 1)  # プレイヤーの下のマップタイルの判定

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):  # 上キーが押された場合
            if u_map == (0, 2):  # プレイヤーの右のマップタイルの進入禁止判定
                self.map_y += 8  # マップY座標を加算してスクロール
                self.pl.dy -= 8  # スクロール用Y座標を減算してスクロール
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):  # 下キーが押された場合
            if d_map == (0, 2):  # プレイヤーの右のマップタイルの進入禁止判定
                self.map_y -= 8  # マップY座標を減算してスクロール
                self.pl.dy += 8  # スクロール用Y座標を加算してスクロール
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):  # 右キーが押された場合
            if r_map == (0, 2):  # プレイヤーの右のマップタイルの進入禁止判定
                self.pl.x += 8  # プレイヤーX座標を加算して移動
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):  # 左キーが押された場合
            if l_map == (0, 2):  # プレイヤーの左のマップタイルの進入禁止判定
                self.pl.x -= 8  # プレイヤーX座標を減算して移動

        print(move_map_x)
        print(move_map_y)
        print(r_map)


App()  # アプリケーションの実行
