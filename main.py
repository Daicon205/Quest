import pyxel


class App:
    def __init__(self):
        pyxel.init(96, 96, fps=5)  # 画面サイズFPS設定
        pyxel.load("Quest.pyxres")  # PyxelEditorの読み込み

        self.player_x = 8   # プレイヤーX座標
        self.player_y = 56  # プレイヤーY座標

        self.map_y = -64 # マップY座標

        pyxel.run(self.update, self.draw)   # 更新処理、描画処理実行

    # フレームの更新処理
    def update(self):
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):    # 上キーが押された場合
            self.map_y = self.map_y + 8 # マップY座標を加算してスクロール


    # 描画処理
    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, self.map_y, 0, 0, 0, 96, 128)   # タイルマップを描画
        pyxel.blt(self.player_x, self.player_y, 0, 8*(pyxel.frame_count % 2), 0, 8, 8, 0)   # プレイヤー描画
        pyxel.blt(8, 8, 0, 8*(pyxel.frame_count % 2) + 16, 0, 8, 8, 0)   # スライム描画
        pyxel.rect(0, 64, 96, 32, 0) # 画面下部のステータス部分を描画
        print(8*(pyxel.frame_count % 2)+16)


App()  # アプリケーションの実行
