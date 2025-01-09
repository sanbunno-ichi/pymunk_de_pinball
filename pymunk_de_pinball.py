#-----------------------------------------------------------------
# title: pymunk_de_pinball
# author: sanbunnoichi
# desc: Pinball simulator
# site: https://github.com/sanbunno-ichi/pinball2
# license: MIT
# version: 1.0
#
#更新履歴
#2025.01.09 公開
#-----------------------------------------------------------------
#ピンボールシミュレーター
#ピンボール台のベースデザインはピンボールアクション
#ピンボールシステムはだいたい入ったと思う
#スコア無し、ゲームオーバー無し
#将来的に、スコアアップのための仕組みを入れたい
#が・・・？
#-----------------------------------------------------------------
#Pinball simulator
#The base design of the pinball table is The Pinball Action.
#I think the pinball system is almost here.
#No score, no game over,,,,
#n the future, I would like to introduce a system to improve scores.
#but,......?
#-----------------------------------------------------------------
import pyxel

SCREEN_WIDTH = 192
SCREEN_HEIGHT = 256
BALL_RADIUS = 5
BALLIN_ANIMMAX = 0x10
BALL_ZOOMMAX = 10
BALLPOS_SAVEMAX = 0x10


W_POSBASEX = 0
R_POSBASEX = 0x100
G_POSBASEX = 0x200
B_POSBASEX = 0x300
_POSBASEX = 0x400
_POSBASEY = 0

#-----------------------------------------------------------------
#[workass]変数
WORK_TOP			=	0
WORK_END			=	0x100
_ass = WORK_TOP
GWK = [WORK_TOP for _ass in range(WORK_END)]	#変数管理(RAM領域)

game_adv			=	WORK_TOP+0x00		#game_control number

G_TITLE				=	0
G_DEMOPLAY			=	1
G_GAME				=	2
G_SETTING			=	3
G_END				=	4
G_FIELD_CHANGE		=	5

game_subadv			=	WORK_TOP+0x01		#game_control sub-number

GS_INIT				=	0
GS_MAIN				=	1	#G_GAME

GS_WAIT1			=	1	#G_FIELD_CHANGE
GS_BALL_SMALL		=	2
GS_WAIT2			=	3
GS_FADEOUT			=	4
GS_CHANGE_FIELD		=	5
GS_WAIT3			=	6
GS_FADEIN			=	7
GS_WAIT4			=	8
GS_BALLIN			=	9
GS_WAIT5			=	10
GS_BALL_BIG			=	11
GS_WAIT6			=	12
GS_BALL_SHOOT		=	13

ball_switch			=	WORK_TOP+0x02
field_number		=	WORK_TOP+0x03
FIELD_WHITE			=	0
FIELD_RED			=	1
FIELD_GREEN			=	2
FIELD_BLUE			=	3

to_field			=	WORK_TOP+0x04
wait_counter		=	WORK_TOP+0x05
zoom_counter		=	WORK_TOP+0x06
ballpos_save_counter=	WORK_TOP+0x07

white_switch		=	WORK_TOP+0x10
red_switch			=	WORK_TOP+0x11
green_switch		=	WORK_TOP+0x12
blue_switch			=	WORK_TOP+0x13
purple_switch		=	WORK_TOP+0x14
score_switch		=	WORK_TOP+0x15
bumper_switch		=	WORK_TOP+0x16

R_white_switch		=	WORK_TOP+0x20
R_red_switch		=	WORK_TOP+0x21
R_green_switch		=	WORK_TOP+0x22
R_blue_switch		=	WORK_TOP+0x23
R_purple_switch		=	WORK_TOP+0x24
R_score_switch		=	WORK_TOP+0x25
R_bumper_switch		=	WORK_TOP+0x26

G_white_switch		=	WORK_TOP+0x30
G_red_switch		=	WORK_TOP+0x31
G_green_switch		=	WORK_TOP+0x32
G_blue_switch		=	WORK_TOP+0x33
G_purple_switch		=	WORK_TOP+0x34
G_score_switch		=	WORK_TOP+0x35
G_bumper_switch		=	WORK_TOP+0x36

B_white_switch		=	WORK_TOP+0x40
B_red_switch		=	WORK_TOP+0x41
B_green_switch		=	WORK_TOP+0x42
B_blue_switch		=	WORK_TOP+0x43
B_purple_switch		=	WORK_TOP+0x44
B_score_switch		=	WORK_TOP+0x45
B_bumper_switch		=	WORK_TOP+0x46
B_yellow_switch		=	WORK_TOP+0x47

ballpos_save		=	WORK_TOP+0x50

B_SWITCH1			=	0x01	#all switch/line
B_SWITCH2			=	0x02	#all switch/line
B_SWITCH3			=	0x04	#all switch/line
B_SWITCH4			=	0x08	#all switch/line
B_SWITCH5			=	0x10	#all switch
B_HOLEOPEN			=	0x20	#all switch
B_HOLECLOSE			=	0x40	#ホール閉め命令
B_HOLEIN			=	0x80	#ホールイン
B_HOLEIN2			=	0x100	#ホールイン2（赤ステージ用

B_THROUGH1			=	0x10	#line
B_THROUGH2			=	0x20	#line
B_THROUGH3			=	0x40	#line
B_THROUGH4			=	0x80	#line

B_YSWITCH1			=	0x001
B_YSWITCH2			=	0x002
B_YSWITCH3			=	0x004
B_YSWITCH4			=	0x008
B_YSWITCH5			=	0x010
B_YSWITCH6			=	0x020
B_YSWITCH7			=	0x040
B_YSWITCH8			=	0x080
B_YSWITCH9			=	0x100

#DEFAULT COLOR
defcol_tbl = [
				0x000000,
				0x2b335f,
				0x7e2072,
				0x19959c,
				0x8b4852,
				0x395c98,
				0xa9c1ff,
				0xeeeeee,
				0xd4186c,
				0xd38441,
				0xe9c35b,
				0x70c6a9,
				0x7696de,
				0xa3a3a3,
				0xff9798,
				0xedc7b0,
			]

ballin_postbl = [
					0, 0,
					#0, 0,
					0, 64,
					0, 128,
					0, 192,
					0, 256,
					192, 0,
					192, 64,
					192, 128,
					192, 192,
					192, 256,
					#0, 0,
					48, 0,
					96, 0,
					144, 0,
					#192, 0,
					#0, 256,
					48, 256,
					96, 256,
					144, 256,
					#192, 256,
				]

class App:
	#-----------------------------------------------------------------
	#初期化
	#-----------------------------------------------------------------
	def __init__( self, pymunk, fps=60 ):
		self.pymunk = pymunk
		self.fps = fps

		pyxel.init( SCREEN_WIDTH, SCREEN_HEIGHT, fps=fps, title="pyxel flipper" )
		pyxel.load("pinball.pyxres")
		self.work_clear()

		GWK[ball_switch] = 1	#StartUp

		GWK[field_number] = FIELD_WHITE
		GWK[game_adv] = G_GAME

		self.create_world()

		if( GWK[field_number] == FIELD_WHITE ):
			pyxel.camera(W_POSBASEX, _POSBASEY)
		elif( GWK[field_number] == FIELD_RED ):
			pyxel.camera(R_POSBASEX, _POSBASEY)
		elif( GWK[field_number] == FIELD_GREEN ):
			pyxel.camera(G_POSBASEX, _POSBASEY)
		elif( GWK[field_number] == FIELD_BLUE ):
			pyxel.camera(B_POSBASEX, _POSBASEY)

		pyxel.run(self.update, self.draw)

	#-----------------------------------------------------------------
	#効果音セット
	#-----------------------------------------------------------------
	def se_set(self,_number):
			pyxel.play( 3,_number )

	#-----------------------------------------------------------------
	#ワーク初期化
	#-----------------------------------------------------------------
	def work_clear(self):
		for _cnt in range(WORK_TOP,WORK_END):
			GWK[_cnt] = 0


	#-----------------------------------------------------------------
	#白ステージ用コールバック関数
	#衝突時の処理[arbiter: pymunk.Arbiter]
	#-----------------------------------------------------------------
	def W_pre_solve( self, arbiter, space, data ):

		cps: self.pymunk.ContactPointSet = arbiter.contact_point_set
		for p in cps.points:
			_hittype = arbiter.shapes[1].collision_type
			if( _hittype == 2 ):	#白穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((-100, 0), (0, 0))
					#GWK[white_switch] |= B_HOLEIN
					pass	#射出で使うので設定しない

			elif( _hittype == 3 ):	#紫穴
				if( abs( p.distance ) >= 3.0 ):
					self.ball_body.apply_impulse_at_local_point((300, -300), (0, 0))
					#GWK[purple_switch] |= B_HOLEIN

					#全ホール蓋閉め（暫定）
					GWK[red_switch] |= B_HOLECLOSE
					GWK[green_switch] |= B_HOLECLOSE
					GWK[blue_switch] |= B_HOLECLOSE
					GWK[white_switch] |= B_HOLECLOSE

			elif( _hittype == 10 ):	#赤穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, -400), (0, 0))
					GWK[red_switch] |= B_HOLEIN
					self.se_set(27)
			elif( _hittype == 20 ):	#緑穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, 100), (0, 0))
					GWK[green_switch] |= B_HOLEIN
					self.se_set(27)
			elif( _hittype == 30 ):	#青穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, -400), (0, 0))
					GWK[blue_switch] |= B_HOLEIN
					self.se_set(27)
			elif( _hittype == 4 ):	#白スイッチ
				GWK[white_switch] |= B_SWITCH1
			elif( _hittype == 11 ):	#赤スイッチ
				GWK[red_switch] |= B_SWITCH1
			elif( _hittype == 12 ):	#赤スイッチ
				GWK[red_switch] |= B_SWITCH2
			elif( _hittype == 13 ):	#赤スイッチ
				GWK[red_switch] |= B_SWITCH3
			elif( _hittype == 21 ):	#緑スイッチ
				GWK[green_switch] |= B_SWITCH1
			elif( _hittype == 22 ):	#緑スイッチ
				GWK[green_switch] |= B_SWITCH2
			elif( _hittype == 23 ):	#緑スイッチ
				GWK[green_switch] |= B_SWITCH3
			elif( _hittype == 24 ):	#緑スイッチ
				GWK[green_switch] |= B_SWITCH4
			elif( _hittype == 25 ):	#緑スイッチ
				GWK[green_switch] |= B_SWITCH5
			elif( _hittype == 31 ):	#青スイッチ
				GWK[blue_switch] |= B_SWITCH1
			elif( _hittype == 32 ):	#青スイッチ
				GWK[blue_switch] |= B_SWITCH2
			elif( _hittype == 33 ):	#青スイッチ
				GWK[blue_switch] |= B_SWITCH3
			elif( _hittype == 34 ):	#青スイッチ
				GWK[blue_switch] |= B_SWITCH4
			elif( _hittype == 5 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH1
				self.se_set(5)
				#左端ライン通過で右端蓋閉め
				if( GWK[white_switch] & B_HOLEOPEN ):
					GWK[white_switch] |= B_HOLECLOSE
			elif( _hittype == 6 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH2
			elif( _hittype == 7 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH3
			elif( _hittype == 8 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH4
			elif( _hittype == 41 ):	#バンパー
				GWK[bumper_switch] |= B_SWITCH1
				self.se_set(14)
			elif( _hittype == 42 ):	#小バンパー
				GWK[bumper_switch] |= B_SWITCH2
				self.se_set(19)
			elif( _hittype == 43 ):	#小バンパー
				GWK[bumper_switch] |= B_SWITCH3
				self.se_set(19)
			elif( _hittype == 44 ):	#小バンパー
				GWK[bumper_switch] |= B_SWITCH4
				self.se_set(19)

		return True

	#-----------------------------------------------------------------
	#赤ステージ用コールバック関数
	#衝突時の処理[arbiter: pymunk.Arbiter]
	#-----------------------------------------------------------------
	def R_pre_solve( self, arbiter, space, data ):
		cps: self.pymunk.ContactPointSet = arbiter.contact_point_set
		for p in cps.points:
			_hittype = arbiter.shapes[1].collision_type
			if( _hittype == 141 ):	#バンパー
				GWK[R_bumper_switch] |= B_SWITCH1
				self.se_set(14)
			elif( _hittype == 142 ):	#バンパー
				GWK[R_bumper_switch] |= B_SWITCH2
				self.se_set(14)
			elif( _hittype == 143 ):	#バンパー
				GWK[R_bumper_switch] |= B_SWITCH3
				self.se_set(14)
			elif( _hittype == 102 ):	#白穴（右上）
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, 200), (0, 0))
					GWK[R_white_switch] |= B_HOLEIN
					self.se_set(27)
			elif( _hittype == 103 ):	#白穴（左上）
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, -400), (0, 0))
					GWK[R_white_switch] |= B_HOLEIN2
					self.se_set(27)
			elif( _hittype == 104 ):	#赤穴
				if( abs( p.distance ) >= 3.0 ):
					#GWK[R_red_switch] |= B_HOLEIN
					pass	#射出で使うので設定しない
			elif( _hittype == 105 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH1

				#左端ライン通過で赤穴蓋閉め
				GWK[R_red_switch] |= B_HOLECLOSE
			elif( _hittype == 106 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH2
			elif( _hittype == 107 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH3
			elif( _hittype == 108 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH4
			elif( _hittype == 109 ):	#白スイッチ
				GWK[R_white_switch] |= B_SWITCH1

		return True

	#-----------------------------------------------------------------
	#緑ステージ用コールバック関数
	#衝突時の処理[arbiter: pymunk.Arbiter]
	#-----------------------------------------------------------------
	def G_pre_solve( self, arbiter, space, data ):
		cps: self.pymunk.ContactPointSet = arbiter.contact_point_set
		for p in cps.points:
			_hittype = arbiter.shapes[1].collision_type
			if( _hittype == 241 ):	#バンパー
				GWK[G_bumper_switch] |= B_SWITCH1
				self.se_set(14)
			elif( _hittype == 242 ):	#バンパー
				GWK[G_bumper_switch] |= B_SWITCH2
				self.se_set(14)
			elif( _hittype == 202 ):	#白穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, 200), (0, 0))
					GWK[G_white_switch] |= B_HOLEIN
					self.se_set(27)
			elif( _hittype == 203 ):	#緑穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, 100), (0, 0))
					#GWK[G_green_switch] |= B_HOLEIN
					pass	#射出使用
			elif( _hittype == 204 ):	#白スイッチ
				GWK[G_white_switch] |= B_SWITCH1
			elif( _hittype == 205 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH1
				#左端ライン通過で白スイッチ戻す
				GWK[G_white_switch] |= B_HOLECLOSE
			elif( _hittype == 206 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH2
			elif( _hittype == 207 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH3
			elif( _hittype == 208 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH4

		return True

	#-----------------------------------------------------------------
	#青ステージ用コールバック関数
	#衝突時の処理[arbiter: pymunk.Arbiter]
	#-----------------------------------------------------------------
	def B_pre_solve( self, arbiter, space, data ):
		cps: self.pymunk.ContactPointSet = arbiter.contact_point_set
		for p in cps.points:
			_hittype = arbiter.shapes[1].collision_type
			if( _hittype == 341 ):	#バンパー
				GWK[B_bumper_switch] |= B_SWITCH1
				self.se_set(14)
			elif( _hittype == 302 ):	#白穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, 200), (0, 0))
					GWK[B_white_switch] |= B_HOLEIN
					self.se_set(27)
			elif( _hittype == 303 ):	#青穴
				if( abs( p.distance ) >= 3.0 ):
					#self.ball_body.apply_impulse_at_local_point((0, -200), (0, 0))
					#GWK[B_red_switch] |= B_HOLEIN
					pass	#射出で使うので設定しない
			elif( _hittype == 305 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH1
				#左端ライン通過で白スイッチ戻す
				GWK[B_white_switch] |= B_HOLECLOSE
				#黄スイッチ全OFF
				GWK[B_yellow_switch] = 0
			elif( _hittype == 306 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH2
			elif( _hittype == 307 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH3
			elif( _hittype == 308 ):	#スコアライン
				GWK[score_switch] |= B_SWITCH4
			elif( _hittype == 309 ):	#白スイッチ
				GWK[B_white_switch] |= B_SWITCH1

			elif( _hittype == 311 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH1
			elif( _hittype == 312 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH2
			elif( _hittype == 313 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH3
			elif( _hittype == 314 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH4
			elif( _hittype == 315 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH5
			elif( _hittype == 316 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH6
			elif( _hittype == 317 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH7
			elif( _hittype == 318 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH8
			elif( _hittype == 319 ):	#黄スイッチ
				GWK[B_yellow_switch] |= B_YSWITCH9

		if( ( GWK[B_yellow_switch] & 0x1ff ) == 0x1ff ):
			#全部ONになったらクリアする
			GWK[B_yellow_switch] = 0

		return True

	#-----------------------------------------------------------------
	#白ステージ用ホールゲート（スイッチによっての開閉（add/remove））制御
	#初期状態では全蓋閉め状態
	#-----------------------------------------------------------------
	def W_holegate_control(self):

		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[red_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#赤穴蓋閉め
			self.space.remove(self.W_holegate_red_open_body, self.W_holegate_red_open_segment)		#赤穴の蓋開き除去
			self.space.add(self.W_holegate_red_close_body, self.W_holegate_red_close_segment)		#赤穴の蓋閉め追加
			GWK[red_switch] = 0

		if( ( ( GWK[red_switch] & (B_SWITCH1+B_SWITCH2+B_SWITCH3) ) == (B_SWITCH1+B_SWITCH2+B_SWITCH3) ) and
			( ( GWK[red_switch] & B_HOLEOPEN ) == 0 ) ):
			#赤穴蓋開き
			self.space.remove(self.W_holegate_red_close_body, self.W_holegate_red_close_segment)	#赤穴の蓋閉め除去
			self.space.add(self.W_holegate_red_open_body, self.W_holegate_red_open_segment)			#赤穴の蓋開き追加
			#蓋開きセット
			GWK[red_switch] |= B_HOLEOPEN

		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[green_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#緑穴蓋閉め
			self.space.remove(self.W_holegate_green_open_body, self.W_holegate_green_open_segment)	#緑穴の蓋開き除去
			self.space.add(self.W_holegate_green_close_body, self.W_holegate_green_close_segment)	#緑穴の蓋閉め追加
			GWK[green_switch] = 0

		if( ( ( GWK[green_switch] & (B_SWITCH1+B_SWITCH2+B_SWITCH3+B_SWITCH4+B_SWITCH5) ) == (B_SWITCH1+B_SWITCH2+B_SWITCH3+B_SWITCH4+B_SWITCH5) ) and
			( ( GWK[green_switch] & B_HOLEOPEN ) == 0 ) ):
			#緑穴蓋開き
			self.space.remove(self.W_holegate_green_close_body, self.W_holegate_green_close_segment)#緑穴の蓋閉め除去
			self.space.add(self.W_holegate_green_open_body, self.W_holegate_green_open_segment)		#緑穴の蓋開き追加
			#蓋開きセット
			GWK[green_switch] |= B_HOLEOPEN

		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[blue_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#青穴蓋閉め
			self.space.remove(self.W_holegate_blue_open_body, self.W_holegate_blue_open_segment)	#青穴の蓋開き除去
			self.space.add(self.W_holegate_blue_close_body, self.W_holegate_blue_close_segment)		#青穴の蓋閉め追加
			GWK[blue_switch] = 0

		if( ( ( GWK[blue_switch] & (B_SWITCH1+B_SWITCH2+B_SWITCH3+B_SWITCH4) ) == (B_SWITCH1+B_SWITCH2+B_SWITCH3+B_SWITCH4) ) and
			( ( GWK[blue_switch] & B_HOLEOPEN ) == 0 ) ):
			#青穴蓋開き
			self.space.remove(self.W_holegate_blue_close_body, self.W_holegate_blue_close_segment)	#青穴の蓋閉め除去
			self.space.add(self.W_holegate_blue_open_body, self.W_holegate_blue_open_segment)		#青穴の蓋開き追加
			#蓋開きセット
			GWK[blue_switch] |= B_HOLEOPEN

		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[white_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#白穴蓋閉め
			self.space.remove(self.W_holegate_white_open_body, self.W_holegate_white_open_segment)	#白穴の蓋開き除去
			self.space.add(self.W_holegate_white_close_body, self.W_holegate_white_close_segment)	#白穴の蓋閉め追加
			GWK[white_switch] = 0

		if( ( ( GWK[white_switch] & (B_SWITCH1) ) == (B_SWITCH1) ) and
			( ( GWK[white_switch] & B_HOLEOPEN ) == 0 ) ):
			#白穴蓋開き
			self.space.remove(self.W_holegate_white_close_body, self.W_holegate_white_close_segment)	#白穴の蓋閉め除去
			self.space.add(self.W_holegate_white_open_body, self.W_holegate_white_open_segment)			#白穴の蓋開き追加
			#蓋開きセット
			GWK[white_switch] |= B_HOLEOPEN

	#-----------------------------------------------------------------
	#赤ステージ用ホールゲート（スイッチによっての開閉（add/remove））制御
	#初期状態では全蓋閉め状態
	#-----------------------------------------------------------------
	def R_holegate_control(self):
		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[R_red_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#赤穴蓋閉め
			self.space.remove(self.R_holegate_red_open_body, self.R_holegate_red_open_segment)		#赤穴の蓋開き除去
			self.space.add(self.R_holegate_red_close_body, self.R_holegate_red_close_segment)		#赤穴の蓋閉め追加
			GWK[R_red_switch] = 0

		if( ( ( GWK[R_red_switch] & (B_SWITCH1) ) == (B_SWITCH1) ) and
			( ( GWK[R_red_switch] & B_HOLEOPEN ) == 0 ) ):
			#赤穴蓋開き
			self.space.remove(self.R_holegate_red_close_body, self.R_holegate_red_close_segment)	#赤穴の蓋閉め除去
			self.space.add(self.R_holegate_red_open_body, self.R_holegate_red_open_segment)			#赤穴の蓋開き追加
			#蓋開きセット
			GWK[R_red_switch] |= B_HOLEOPEN

		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[R_white_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#白穴蓋閉め
			self.space.remove(self.R_holegate_white_open_body, self.R_holegate_white_open_segment)	#白穴の蓋開き除去
			self.space.add(self.R_holegate_white_close_body, self.R_holegate_white_close_segment)	#白穴の蓋閉め追加
			GWK[R_white_switch] = 0

		if( ( ( GWK[R_white_switch] & (B_SWITCH1) ) == (B_SWITCH1) ) and
			( ( GWK[R_white_switch] & B_HOLEOPEN ) == 0 ) ):
			#白穴蓋開き
			self.space.remove(self.R_holegate_white_close_body, self.R_holegate_white_close_segment)	#白穴の蓋閉め除去
			self.space.add(self.R_holegate_white_open_body, self.R_holegate_white_open_segment)			#白穴の蓋開き追加
			#蓋開きセット
			GWK[R_white_switch] |= B_HOLEOPEN

	#-----------------------------------------------------------------
	#緑ステージ用ホールゲート（スイッチによっての開閉（add/remove））制御
	#初期状態では全蓋閉め状態
	#-----------------------------------------------------------------
	def G_holegate_control(self):
		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[G_white_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#白穴蓋閉め
			self.space.remove(self.G_holegate_white_open_body, self.G_holegate_white_open_segment)	#白穴の蓋開き除去
			self.space.add(self.G_holegate_white_close_body, self.G_holegate_white_close_segment)	#白穴の蓋閉め追加
			GWK[G_white_switch] = 0

		if( ( ( GWK[G_white_switch] & (B_SWITCH1) ) == (B_SWITCH1) ) and
			( ( GWK[G_white_switch] & B_HOLEOPEN ) == 0 ) ):
			#白穴蓋開き
			self.space.remove(self.G_holegate_white_close_body, self.G_holegate_white_close_segment)	#白穴の蓋閉め除去
			self.space.add(self.G_holegate_white_open_body, self.G_holegate_white_open_segment)			#白穴の蓋開き追加
			#蓋開きセット
			GWK[G_white_switch] |= B_HOLEOPEN

	#-----------------------------------------------------------------
	#青ステージ用ホールゲート（スイッチによっての開閉（add/remove））制御
	#初期状態では全蓋閉め状態
	#-----------------------------------------------------------------
	def B_holegate_control(self):
		#ホールオープンの時、かつ、蓋閉め命令ONの時、蓋閉め
		if( ( GWK[B_white_switch] & ( B_HOLEOPEN + B_HOLECLOSE ) ) == ( B_HOLEOPEN + B_HOLECLOSE ) ):
			#白穴蓋閉め
			self.space.remove(self.B_holegate_white_open_body, self.B_holegate_white_open_segment)	#白穴の蓋開き除去
			self.space.add(self.B_holegate_white_close_body, self.B_holegate_white_close_segment)	#白穴の蓋閉め追加
			GWK[B_white_switch] = 0

		if( ( ( GWK[B_white_switch] & (B_SWITCH1) ) == (B_SWITCH1) ) and
			( ( GWK[B_white_switch] & B_HOLEOPEN ) == 0 ) ):
			#白穴蓋開き
			self.space.remove(self.B_holegate_white_close_body, self.B_holegate_white_close_segment)	#白穴の蓋閉め除去
			self.space.add(self.B_holegate_white_open_body, self.B_holegate_white_open_segment)			#白穴の蓋開き追加
			#蓋開きセット
			GWK[B_white_switch] |= B_HOLEOPEN

	#-----------------------------------------------------------------
	#白ステージ用ホールイン制御
	#-----------------------------------------------------------------
	def W_holein_control(self):
		if( GWK[red_switch] & B_HOLEIN ):
			#赤穴に入った
			#穴の中心にボールをセット
			x, y = self.W_hole_red_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_RED

		elif( GWK[green_switch] & B_HOLEIN ):
			#緑穴に入った
			#穴の中心にボールをセット
			x, y = self.W_hole_green_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_GREEN

		elif( GWK[blue_switch] & B_HOLEIN ):
			#青穴に入った
			#穴の中心にボールをセット
			x, y = self.W_hole_blue_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_BLUE

	#-----------------------------------------------------------------
	#赤ステージ用ホールイン制御
	#-----------------------------------------------------------------
	def R_holein_control(self):
		if( GWK[R_white_switch] & B_HOLEIN ):
			#白穴に入った
			#穴の中心にボールをセット
			x, y = self.R_hole_white_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_WHITE

		elif( GWK[R_white_switch] & B_HOLEIN2 ):
			#白穴に入った
			#穴の中心にボールをセット
			x, y = self.R_hole_white2_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_WHITE

	#-----------------------------------------------------------------
	#緑ステージ用ホールイン制御
	#-----------------------------------------------------------------
	def G_holein_control(self):
		if( GWK[G_white_switch] & B_HOLEIN ):
			#白穴に入った
			#穴の中心にボールをセット
			x, y = self.G_hole_white_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_WHITE

	#-----------------------------------------------------------------
	#青ステージ用ホールイン制御
	#-----------------------------------------------------------------
	def B_holein_control(self):
		if( GWK[B_white_switch] & B_HOLEIN ):
			#白穴に入った
			#穴の中心にボールをセット
			x, y = self.B_hole_white_body.position
			self.ball_body.position = x, y
			#ボールの速度をリセット
			self.ball_body.velocity = (0, 0)
			#ボール挙動を停止
			self.ball_body.sleep()
			GWK[game_adv] = G_FIELD_CHANGE
			GWK[game_subadv] = GS_INIT
			GWK[to_field] = FIELD_WHITE

	#-----------------------------------------------------------------
	#create_world
	#-----------------------------------------------------------------
	def create_world(self):
		from pymunk import Vec2d

		self.space = self.pymunk.Space()
		self.space.gravity = ( 0.0, 250.0 )		#台の傾斜（重力）
		self.space.sleep_time_threshold = 0.3

		#白ステージ用
		#外壁
		W_static_lines = [
			self.pymunk.Segment(self.space.static_body, ( 62 + W_POSBASEX, 216), ( 17 + W_POSBASEX, 189), 1.0),	#右外枠始点
			self.pymunk.Segment(self.space.static_body, ( 17 + W_POSBASEX, 187), ( 17 + W_POSBASEX, 204), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 17 + W_POSBASEX, 204), ( 14 + W_POSBASEX, 207), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 14 + W_POSBASEX, 207), (  8 + W_POSBASEX, 208), 1.0),
			self.pymunk.Segment(self.space.static_body, (  8 + W_POSBASEX, 208), (  3 + W_POSBASEX, 205), 1.0),
			self.pymunk.Segment(self.space.static_body, (  3 + W_POSBASEX, 205), (  2 + W_POSBASEX, 202), 1.0),
			self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX, 202), (  2 + W_POSBASEX, 180), 1.0),

			#self.pymunk.Segment(self.space.static_body, ( 17 + W_POSBASEX, 189), (  2 + W_POSBASEX, 180), 2.0),	#赤穴の蓋閉め
			#self.pymunk.Segment(self.space.static_body, ( 17 + W_POSBASEX, 189), ( 17 + W_POSBASEX, 173), 2.0),	#赤穴の蓋開き

			self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX, 180), (  2 + W_POSBASEX, 133), 1.0),
			self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX, 133), ( 15 + W_POSBASEX, 123), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 15 + W_POSBASEX, 123), ( 39 + W_POSBASEX,  97), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 39 + W_POSBASEX,  97), ( 36 + W_POSBASEX,  91), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 36 + W_POSBASEX,  91), ( 16 + W_POSBASEX, 112), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 16 + W_POSBASEX, 112), (  9 + W_POSBASEX, 113), 1.0),
			self.pymunk.Segment(self.space.static_body, (  9 + W_POSBASEX, 113), (  5 + W_POSBASEX, 104), 1.0),
			self.pymunk.Segment(self.space.static_body, (  5 + W_POSBASEX, 104), (  8 + W_POSBASEX,  96), 1.0),
			self.pymunk.Segment(self.space.static_body, (  8 + W_POSBASEX,  96), ( 27 + W_POSBASEX,  76), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 27 + W_POSBASEX,  76), ( 27 + W_POSBASEX,  72), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 27 + W_POSBASEX,  72), ( 19 + W_POSBASEX,  65), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 19 + W_POSBASEX,  65), (  2 + W_POSBASEX,  24), 1.0),
			self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX,  24), (  2 + W_POSBASEX,  12), 1.0),
			self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX,  12), (  2 + W_POSBASEX,   3), 1.0),
			self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX,   3), ( 17 + W_POSBASEX,   3), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 17 + W_POSBASEX,   3), ( 18 + W_POSBASEX,  11), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 18 + W_POSBASEX,  11), ( 20 + W_POSBASEX,  18), 1.0),

			#self.pymunk.Segment(self.space.static_body, (  2 + W_POSBASEX,  24), ( 20 + W_POSBASEX,  18), 2.0),	#緑穴の蓋閉め
			#self.pymunk.Segment(self.space.static_body, ( 22 + W_POSBASEX,  25), ( 20 + W_POSBASEX,  18), 2.0),	#緑穴の蓋開き

			self.pymunk.Segment(self.space.static_body, ( 20 + W_POSBASEX,  18), ( 23 + W_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 23 + W_POSBASEX,   4), ( 77 + W_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 77 + W_POSBASEX,   4), ( 80 + W_POSBASEX,  16), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 80 + W_POSBASEX,  16), ( 86 + W_POSBASEX,  16), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 86 + W_POSBASEX,  16), (103 + W_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (103 + W_POSBASEX,   4), (113 + W_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (113 + W_POSBASEX,   4), (125 + W_POSBASEX,   7), 1.0),
			self.pymunk.Segment(self.space.static_body, (125 + W_POSBASEX,   7), (128 + W_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (128 + W_POSBASEX,   4), (188 + W_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX,   4), (188 + W_POSBASEX,  19), 1.0),
			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX,  19), (184 + W_POSBASEX,  23), 1.0),
			self.pymunk.Segment(self.space.static_body, (184 + W_POSBASEX,  23), (184 + W_POSBASEX,  32), 1.0),
			self.pymunk.Segment(self.space.static_body, (184 + W_POSBASEX,  32), (188 + W_POSBASEX,  40), 1.0),
			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX,  40), (188 + W_POSBASEX,  88), 1.0),

			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX,  88), (188 + W_POSBASEX, 105), 1.0),
			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX, 105), (185 + W_POSBASEX, 113), 1.0),
			self.pymunk.Segment(self.space.static_body, (185 + W_POSBASEX, 113), (175 + W_POSBASEX, 113), 1.0),
			self.pymunk.Segment(self.space.static_body, (175 + W_POSBASEX, 113), (172 + W_POSBASEX, 105), 1.0),
			self.pymunk.Segment(self.space.static_body, (172 + W_POSBASEX, 105), (172 + W_POSBASEX,  95), 1.0),

			#self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX,  88), (172 + W_POSBASEX,  95), 2.0),	#青穴の蓋閉め
			#self.pymunk.Segment(self.space.static_body, (172 + W_POSBASEX,  77), (172 + W_POSBASEX,  95), 2.0),	#青穴の蓋開き

			self.pymunk.Segment(self.space.static_body, (172 + W_POSBASEX,  95), (159 + W_POSBASEX,  99), 1.0),
			self.pymunk.Segment(self.space.static_body, (159 + W_POSBASEX,  99), (159 + W_POSBASEX, 106), 1.0),
			self.pymunk.Segment(self.space.static_body, (159 + W_POSBASEX, 106), (175 + W_POSBASEX, 123), 1.0),
			self.pymunk.Segment(self.space.static_body, (175 + W_POSBASEX, 123), (188 + W_POSBASEX, 132), 1.0),	#外枠右終点

			self.pymunk.Segment(self.space.static_body, ( 17 + W_POSBASEX, 173), ( 17 + W_POSBASEX, 149), 1.0),	#左ライン

			self.pymunk.Segment(self.space.static_body, (142 + W_POSBASEX,  85), (104 + W_POSBASEX,  43), 1.0),	#右上
			self.pymunk.Segment(self.space.static_body, (104 + W_POSBASEX,  43), (104 + W_POSBASEX,  33), 1.0),
			self.pymunk.Segment(self.space.static_body, (104 + W_POSBASEX,  33), (106 + W_POSBASEX,  24), 1.0),
			self.pymunk.Segment(self.space.static_body, (106 + W_POSBASEX,  24), (114 + W_POSBASEX,  29), 1.0),
			self.pymunk.Segment(self.space.static_body, (114 + W_POSBASEX,  29), (114 + W_POSBASEX,  47), 1.0),
			self.pymunk.Segment(self.space.static_body, (114 + W_POSBASEX,  47), (136 + W_POSBASEX,  73), 1.0),
			self.pymunk.Segment(self.space.static_body, (136 + W_POSBASEX,  73), (142 + W_POSBASEX,  75), 1.0),
			self.pymunk.Segment(self.space.static_body, (142 + W_POSBASEX,  75), (142 + W_POSBASEX,  85), 1.0),

			self.pymunk.Segment(self.space.static_body, (159 + W_POSBASEX,  82), (159 + W_POSBASEX,  72), 1.0),	#右上ライン左
			self.pymunk.Segment(self.space.static_body, (174 + W_POSBASEX,  77), (174 + W_POSBASEX,  67), 1.0),	#右上ライン右

			#各ステージ共通共通
			self.pymunk.Segment(self.space.static_body, ( 88 + W_POSBASEX, 255), ( 88 + W_POSBASEX, 251), 1.0),	#左フリッパーライン
			self.pymunk.Segment(self.space.static_body, ( 88 + W_POSBASEX, 251), ( 62 + W_POSBASEX, 241), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 62 + W_POSBASEX, 241), ( 62 + W_POSBASEX, 216), 1.0),

			self.pymunk.Segment(self.space.static_body, (133 + W_POSBASEX, 214), (174 + W_POSBASEX, 188), 1.0),	#右フリッパーライン
			self.pymunk.Segment(self.space.static_body, (174 + W_POSBASEX, 188), (174 + W_POSBASEX, 182), 1.0),
			#self.pymunk.Segment(self.space.static_body, (174 + W_POSBASEX, 182), (174 + W_POSBASEX, 165), 1.0),	#白スイッチの蓋閉め
			#self.pymunk.Segment(self.space.static_body, (174 + W_POSBASEX, 182), (188 + W_POSBASEX, 174), 1.0),	#白スイッチの蓋開き
			self.pymunk.Segment(self.space.static_body, (174 + W_POSBASEX, 165), (174 + W_POSBASEX, 149), 1.0),

			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX, 132), (188 + W_POSBASEX, 204), 1.0),	#右外枠
			self.pymunk.Segment(self.space.static_body, (188 + W_POSBASEX, 204), (104 + W_POSBASEX, 251), 1.0),
			self.pymunk.Segment(self.space.static_body, (104 + W_POSBASEX, 251), (104 + W_POSBASEX, 255), 1.0),	#外枠終点

			#self.pymunk.Segment(self.space.static_body, (137 + W_POSBASEX, 190), (159 + W_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, (159 + W_POSBASEX, 148), (159 + W_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, (159 + W_POSBASEX, 180), (137 + W_POSBASEX, 190), 1.0),
            
			#self.pymunk.Segment(self.space.static_body, ( 32 + W_POSBASEX, 148), ( 53 + W_POSBASEX, 190), 1.0),	#左三角
			self.pymunk.Segment(self.space.static_body, ( 53 + W_POSBASEX, 190), ( 32 + W_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 32 + W_POSBASEX, 180), ( 32 + W_POSBASEX, 148), 1.0),
		]
		for line in W_static_lines:
			line.elasticity = 0.7
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*W_static_lines)

		#バンパー
		self.W_bumper1_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.W_bumper1_body.position = (148 + W_POSBASEX, 37)
		self.W_bumper1_shape = self.pymunk.Circle( self.W_bumper1_body, 15 )
		self.W_bumper1_shape.elasticity = 2.5
		self.W_bumper1_shape.collision_type = 41
		self.space.add(self.W_bumper1_body, self.W_bumper1_shape)
		self.h_W_bumper1 = self.space.add_collision_handler(0, 41)
		self.h_W_bumper1.pre_solve = self.W_pre_solve

		self.W_bumper2_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.W_bumper2_body.position = (60 + W_POSBASEX, 45)
		self.W_bumper2_shape = self.pymunk.Circle( self.W_bumper2_body, 7 )
		self.W_bumper2_shape.elasticity = 1.5
		self.W_bumper2_shape.collision_type = 42
		self.space.add(self.W_bumper2_body, self.W_bumper2_shape)
		self.h_W_bumper2 = self.space.add_collision_handler(0, 42)
		self.h_W_bumper2.pre_solve = self.W_pre_solve

		self.W_bumper3_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.W_bumper3_body.position = (95 + W_POSBASEX, 90)
		self.W_bumper3_shape = self.pymunk.Circle( self.W_bumper3_body, 7 )
		self.W_bumper3_shape.elasticity = 1.5
		self.W_bumper3_shape.collision_type = 43
		self.space.add(self.W_bumper3_body, self.W_bumper3_shape)
		self.h_W_bumper3 = self.space.add_collision_handler(0, 43)
		self.h_W_bumper3.pre_solve = self.W_pre_solve

		self.W_bumper4_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.W_bumper4_body.position = (116 + W_POSBASEX, 145)
		self.W_bumper4_shape = self.pymunk.Circle( self.W_bumper4_body, 7 )
		self.W_bumper4_shape.elasticity = 1.5
		self.W_bumper4_shape.collision_type = 44
		self.space.add(self.W_bumper4_body, self.W_bumper4_shape)
		self.h_W_bumper4 = self.space.add_collision_handler(0, 44)
		self.h_W_bumper4.pre_solve = self.W_pre_solve


		#ホール設定
		#白穴
		self.W_hole_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_hole_white_body.position = 180 + W_POSBASEX, 12
		self.circle = self.pymunk.Circle(self.W_hole_white_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 2
		self.space.add(self.W_hole_white_body, self.circle)

		self.h_W_white_hole = self.space.add_collision_handler(0, 2)
		self.h_W_white_hole.pre_solve = self.W_pre_solve

		#紫穴
		self.W_hole_purple_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_hole_purple_body.position = 14 + W_POSBASEX, 103
		self.circle = self.pymunk.Circle(self.W_hole_purple_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 3
		self.space.add(self.W_hole_purple_body, self.circle)

		self.h_W_purple_hole = self.space.add_collision_handler(0, 3)
		self.h_W_purple_hole.pre_solve = self.W_pre_solve

		#赤穴
		self.W_hole_red_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_hole_red_body.position = 9 + W_POSBASEX, 199
		self.circle = self.pymunk.Circle(self.W_hole_red_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 10
		self.space.add(self.W_hole_red_body, self.circle)

		self.h_W_red_hole = self.space.add_collision_handler(0, 10)
		self.h_W_red_hole.pre_solve = self.W_pre_solve

		#緑穴
		self.W_hole_green_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_hole_green_body.position = 10 + W_POSBASEX, 11
		self.circle = self.pymunk.Circle(self.W_hole_green_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 20
		self.space.add(self.W_hole_green_body, self.circle)

		self.h_W_green_hole = self.space.add_collision_handler(0, 20)
		self.h_W_green_hole.pre_solve = self.W_pre_solve

		#青穴
		self.W_hole_blue_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_hole_blue_body.position = 180 + W_POSBASEX, 105
		self.circle = self.pymunk.Circle(self.W_hole_blue_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 30
		self.space.add(self.W_hole_blue_body, self.circle)

		self.h_W_blue_hole = self.space.add_collision_handler(0, 30)
		self.h_W_blue_hole.pre_solve = self.W_pre_solve


		#スイッチライン（当たったらOFF->ON、同色すべてONならホールオープン
		#白スイッチ
		self.W_switch_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_white_body.position = 161 + W_POSBASEX, 116
		self.segment = self.pymunk.Segment(self.W_switch_white_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 4
		self.space.add(self.W_switch_white_body, self.segment)
		self.h_W_switch_white = self.space.add_collision_handler(0, 4)
		self.h_W_switch_white.pre_solve = self.W_pre_solve

		#赤スイッチ
		self.W_switch_red1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_red1_body.position = 19 + W_POSBASEX, 126
		self.segment = self.pymunk.Segment(self.W_switch_red1_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 11
		self.space.add(self.W_switch_red1_body, self.segment)
		self.h_W_switch_red1 = self.space.add_collision_handler(0, 11)
		self.h_W_switch_red1.pre_solve = self.W_pre_solve

		self.W_switch_red2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_red2_body.position = 29 + W_POSBASEX, 116
		self.segment = self.pymunk.Segment(self.W_switch_red2_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 12
		self.space.add(self.W_switch_red2_body, self.segment)
		self.h_W_switch_red2 = self.space.add_collision_handler(0, 12)
		self.h_W_switch_red2.pre_solve = self.W_pre_solve

		self.W_switch_red3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_red3_body.position = 39 + W_POSBASEX, 106
		self.segment = self.pymunk.Segment(self.W_switch_red3_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 13
		self.space.add(self.W_switch_red3_body, self.segment)
		self.h_W_switch_red3 = self.space.add_collision_handler(0, 13)
		self.h_W_switch_red3.pre_solve = self.W_pre_solve

		#緑スイッチ
		self.W_switch_green1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_green1_body.position = 28 + W_POSBASEX, 12
		self.segment = self.pymunk.Segment(self.W_switch_green1_body, Vec2d(-5, 0), Vec2d(5, 0), 3)
		self.segment.sensor = True
		self.segment.collision_type = 21
		self.space.add(self.W_switch_green1_body, self.segment)
		self.h_W_switch_green1 = self.space.add_collision_handler(0, 21)
		self.h_W_switch_green1.pre_solve = self.W_pre_solve

		self.W_switch_green2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_green2_body.position = 39 + W_POSBASEX, 12
		self.segment = self.pymunk.Segment(self.W_switch_green2_body, Vec2d(-5, 0), Vec2d(5, 0), 3)
		self.segment.sensor = True
		self.segment.collision_type = 22
		self.space.add(self.W_switch_green2_body, self.segment)
		self.h_W_switch_green2 = self.space.add_collision_handler(0, 22)
		self.h_W_switch_green2.pre_solve = self.W_pre_solve

		self.W_switch_green3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_green3_body.position = 50 + W_POSBASEX, 12
		self.segment = self.pymunk.Segment(self.W_switch_green3_body, Vec2d(-5, 0), Vec2d(5, 0), 3)
		self.segment.sensor = True
		self.segment.collision_type = 23
		self.space.add(self.W_switch_green3_body, self.segment)
		self.h_W_switch_green3 = self.space.add_collision_handler(0, 23)
		self.h_W_switch_green3.pre_solve = self.W_pre_solve

		self.W_switch_green4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_green4_body.position = 61 + W_POSBASEX, 12
		self.segment = self.pymunk.Segment(self.W_switch_green4_body, Vec2d(-5, 0), Vec2d(5, 0), 3)
		self.segment.sensor = True
		self.segment.collision_type = 24
		self.space.add(self.W_switch_green4_body, self.segment)
		self.h_W_switch_green4 = self.space.add_collision_handler(0, 24)
		self.h_W_switch_green4.pre_solve = self.W_pre_solve

		self.W_switch_green5_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_green5_body.position = 72 + W_POSBASEX, 12
		self.segment = self.pymunk.Segment(self.W_switch_green5_body, Vec2d(-5, 0), Vec2d(5, 0), 3)
		self.segment.sensor = True
		self.segment.collision_type = 25
		self.space.add(self.W_switch_green5_body, self.segment)
		self.h_W_switch_green5 = self.space.add_collision_handler(0, 25)
		self.h_W_switch_green5.pre_solve = self.W_pre_solve

		#青スイッチ
		self.W_switch_blue1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_blue1_body.position = 104 + W_POSBASEX, 52
		self.segment = self.pymunk.Segment(self.W_switch_blue1_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 31
		self.space.add(self.W_switch_blue1_body, self.segment)
		self.h_W_switch_blue1 = self.space.add_collision_handler(0, 31)
		self.h_W_switch_blue1.pre_solve = self.W_pre_solve

		self.W_switch_blue2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_blue2_body.position = 114 + W_POSBASEX, 62
		self.segment = self.pymunk.Segment(self.W_switch_blue2_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 32
		self.space.add(self.W_switch_blue2_body, self.segment)
		self.h_W_switch_blue2 = self.space.add_collision_handler(0, 32)
		self.h_W_switch_blue2.pre_solve = self.W_pre_solve

		self.W_switch_blue3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_blue3_body.position = 124 + W_POSBASEX, 72
		self.segment = self.pymunk.Segment(self.W_switch_blue3_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 33
		self.space.add(self.W_switch_blue3_body, self.segment)
		self.h_W_switch_blue3 = self.space.add_collision_handler(0, 33)
		self.h_W_switch_blue3.pre_solve = self.W_pre_solve

		self.W_switch_blue4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_switch_blue4_body.position = 134 + W_POSBASEX, 82
		self.segment = self.pymunk.Segment(self.W_switch_blue4_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 34
		self.space.add(self.W_switch_blue4_body, self.segment)
		self.h_W_switch_blue4 = self.space.add_collision_handler(0, 34)
		self.h_W_switch_blue4.pre_solve = self.W_pre_solve

		#スコアライン（通過(HIT->OFF)でスコア加算）
		self.W_scline1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_scline1_body.position = 9 + W_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.W_scline1_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 5
		self.space.add(self.W_scline1_body, self.segment)
		self.h_W_scline1 = self.space.add_collision_handler(0, 5)
		self.h_W_scline1.pre_solve = self.W_pre_solve

		self.W_scline2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_scline2_body.position = 24 + W_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.W_scline2_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.W_collision_type = 6
		self.space.add(self.W_scline2_body, self.segment)
		self.h_W_scline2 = self.space.add_collision_handler(0, 6)
		self.h_W_scline2.pre_solve = self.W_pre_solve

		self.W_scline3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_scline3_body.position = 167 + W_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.W_scline3_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 7
		self.space.add(self.W_scline3_body, self.segment)
		self.h_W_scline3 = self.space.add_collision_handler(0, 7)
		self.h_W_scline3.pre_solve = self.W_pre_solve

		self.W_scline4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_scline4_body.position = 181 + W_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.W_scline4_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 8
		self.space.add(self.W_scline4_body, self.segment)
		self.h_W_scline4 = self.space.add_collision_handler(0, 8)
		self.h_W_scline4.pre_solve = self.W_pre_solve

		#ホールゲート
		#ここでは定義だけにして、更新処理にてholegate_controlで制御したい
		#最初は「閉め」状態にしておく

		#self.pymunk.Segment(self.space.static_body, ( 17, 189), (  2, 180), 2.0),	#赤穴の蓋閉め
		self.W_holegate_red_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_red_close_body.position = 17 + W_POSBASEX, 189
		self.W_holegate_red_close_segment = self.pymunk.Segment(self.W_holegate_red_close_body, Vec2d(0, 0), Vec2d(-15, -9), 2)
		self.space.add(self.W_holegate_red_close_body, self.W_holegate_red_close_segment)

		#self.pymunk.Segment(self.space.static_body, ( 17, 189), ( 17, 173), 2.0),	#赤穴の蓋開き
		self.W_holegate_red_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_red_open_body.position = 17 + W_POSBASEX, 189
		self.W_holegate_red_open_segment = self.pymunk.Segment(self.W_holegate_red_open_body, Vec2d(0, 0), Vec2d(0, -16), 2)
		#self.space.add(self.W_holegate_red_open_body, self.holegate_red_open_segment)

		#self.pymunk.Segment(self.space.static_body, (  2,  24), ( 20,  18), 2.0),	#緑穴の蓋閉め
		self.W_holegate_green_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_green_close_body.position = 20 + W_POSBASEX, 18
		self.W_holegate_green_close_segment = self.pymunk.Segment(self.W_holegate_green_close_body, Vec2d(0, 0), Vec2d(-18, 6), 2)
		self.space.add(self.W_holegate_green_close_body, self.W_holegate_green_close_segment)

		#self.pymunk.Segment(self.space.static_body, ( 22,  25), ( 20,  18), 2.0),	#緑穴の蓋開き
		self.W_holegate_green_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_green_open_body.position = 20 + W_POSBASEX, 18
		self.W_holegate_green_open_segment = self.pymunk.Segment(self.W_holegate_green_open_body, Vec2d(0, 0), Vec2d(2, 7), 2)
		#self.space.add(self.W_holegate_green_open_body, self.W_holegate_green_open_segment)

		#self.pymunk.Segment(self.space.static_body, (188,  88), (172,  95), 2.0),	#青穴の蓋閉め
		self.W_holegate_blue_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_blue_close_body.position = 172 + W_POSBASEX, 95
		self.W_holegate_blue_close_segment = self.pymunk.Segment(self.W_holegate_blue_close_body, Vec2d(0, 0), Vec2d(16, -7), 2)
		self.space.add(self.W_holegate_blue_close_body, self.W_holegate_blue_close_segment)

		#self.pymunk.Segment(self.space.static_body, (172,  77), (172,  95), 2.0),	#青穴の蓋開き
		self.W_holegate_blue_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_blue_open_body.position = 172 + W_POSBASEX, 95
		self.W_holegate_blue_open_segment = self.pymunk.Segment(self.W_holegate_blue_open_body, Vec2d(0, 0), Vec2d(0, -18), 2)
		#self.space.add(self.W_holegate_blue_open_body, self.W_holegate_blue_open_segment)

		#self.pymunk.Segment(self.space.static_body, (174, 182), (174, 165), 1.0),	#白穴の蓋閉め
		self.W_holegate_white_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_white_close_body.position = 174 + W_POSBASEX, 182
		self.W_holegate_white_close_segment = self.pymunk.Segment(self.W_holegate_white_close_body, Vec2d(0, 0), Vec2d(0, -17), 2)
		self.space.add(self.W_holegate_white_close_body, self.W_holegate_white_close_segment)

		#self.pymunk.Segment(self.space.static_body, (174, 182), (188, 174), 1.0),	#白穴の蓋開き
		self.W_holegate_white_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.W_holegate_white_open_body.position = 174 + W_POSBASEX, 182
		self.W_holegate_white_open_segment = self.pymunk.Segment(self.W_holegate_white_open_body, Vec2d(0, 0), Vec2d(14, -8), 2)
		#self.space.add(self.W_holegate_white_open_body, self.W_holegate_white_open_segment)

		#[共通]-----------------------------------------------------------------
		#線バンパー（三角バンパーの裏側は外壁セグメントとして登録）
		W_static_blines = [
			self.pymunk.Segment(self.space.static_body, (137 + W_POSBASEX, 190), (159 + W_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, ( 32 + W_POSBASEX, 148), ( 53 + W_POSBASEX, 190), 1.0),	#左三角
		]
		for line in W_static_blines:
			line.elasticity = 2.5	#弾性
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*W_static_blines)

		#フリッパー（positionからのオフセット）
		W_fp = [(2, -2), (-26, 0), (2, 2)]
		W_mass = 100
		W_moment = self.pymunk.moment_for_poly(W_mass, W_fp)

		# right flipper
		self.W_r_flipper_body = self.pymunk.Body(W_mass, W_moment)
		self.W_r_flipper_body.position = 130 + W_POSBASEX, 218
		self.W_r_flipper_shape = self.pymunk.Poly(self.W_r_flipper_body, W_fp)
		self.space.add(self.W_r_flipper_body, self.W_r_flipper_shape)

		self.W_r_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.W_r_flipper_joint_body.position = self.W_r_flipper_body.position
		j = self.pymunk.PinJoint(self.W_r_flipper_body, self.W_r_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.W_r_flipper_body, self.W_r_flipper_joint_body, -0.3, 20000000, 900000
		)
		self.space.add(j, s)

		# left flipper
		self.W_l_flipper_body = self.pymunk.Body(W_mass, W_moment)
		self.W_l_flipper_body.position = 65 + W_POSBASEX, 218
		self.W_l_flipper_shape = self.pymunk.Poly(self.W_l_flipper_body, [(-x, y) for x, y in W_fp])
		self.space.add(self.W_l_flipper_body, self.W_l_flipper_shape)

		self.W_l_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.W_l_flipper_joint_body.position = self.W_l_flipper_body.position
		j = self.pymunk.PinJoint(self.W_l_flipper_body, self.W_l_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.W_l_flipper_body, self.W_l_flipper_joint_body, 0.3, 20000000, 900000
		)
		self.space.add(j, s)

		self.W_r_flipper_shape.group = self.W_l_flipper_shape.group = 1
		self.W_r_flipper_shape.elasticity = self.W_l_flipper_shape.elasticity = 0.4

		#-----------------------------------------------------------------------
		#赤ステージ用
		#外壁
		R_static_lines = [
			self.pymunk.Segment(self.space.static_body, ( 188 + R_POSBASEX, 132), ( 182 + R_POSBASEX, 121), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 182 + R_POSBASEX, 121), ( 188 + R_POSBASEX, 106), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + R_POSBASEX, 106), ( 180 + R_POSBASEX,  93), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 180 + R_POSBASEX,  93), ( 188 + R_POSBASEX,  71), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + R_POSBASEX,  71), ( 188 + R_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + R_POSBASEX,   8), ( 185 + R_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 185 + R_POSBASEX,   4), ( 178 + R_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 178 + R_POSBASEX,   4), ( 174 + R_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 174 + R_POSBASEX,   8), ( 174 + R_POSBASEX,  53), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 174 + R_POSBASEX,  53), ( 169 + R_POSBASEX,  67), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 169 + R_POSBASEX,  67), ( 169 + R_POSBASEX,  53), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 169 + R_POSBASEX,  53), ( 172 + R_POSBASEX,  46), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 172 + R_POSBASEX,  46), ( 172 + R_POSBASEX,  33), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 172 + R_POSBASEX,  33), ( 168 + R_POSBASEX,  18), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 168 + R_POSBASEX,  18), ( 163 + R_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 163 + R_POSBASEX,   8), ( 155 + R_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 155 + R_POSBASEX,   4), (  32 + R_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (  32 + R_POSBASEX,   4), (  18 + R_POSBASEX,  10), 1.0),
			self.pymunk.Segment(self.space.static_body, (  18 + R_POSBASEX,  10), (   6 + R_POSBASEX,  23), 1.0),
			self.pymunk.Segment(self.space.static_body, (   6 + R_POSBASEX,  23), (   2 + R_POSBASEX,  38), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + R_POSBASEX,  38), (   2 + R_POSBASEX, 106), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + R_POSBASEX, 106), (   4 + R_POSBASEX, 110), 1.0),
			self.pymunk.Segment(self.space.static_body, (   4 + R_POSBASEX, 110), (  12 + R_POSBASEX, 110), 1.0),
			self.pymunk.Segment(self.space.static_body, (  12 + R_POSBASEX, 110), (  17 + R_POSBASEX, 106), 1.0),
			self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX, 106), (  17 + R_POSBASEX,  74), 1.0),
			self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX,  74), (  25 + R_POSBASEX,  92), 1.0),
			self.pymunk.Segment(self.space.static_body, (  25 + R_POSBASEX,  92), (   2 + R_POSBASEX, 136), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + R_POSBASEX, 136), (   2 + R_POSBASEX, 180), 1.0),

			#self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX, 189), (   2 + R_POSBASEX, 180), 2.0),	#赤穴の蓋閉め
			#self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX, 189), (  17 + R_POSBASEX, 173), 2.0),	#赤穴の蓋開き

			self.pymunk.Segment(self.space.static_body, (  62 + R_POSBASEX, 216), (  17 + R_POSBASEX, 189), 1.0),
			self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX, 189), (  17 + R_POSBASEX, 204), 1.0),
			self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX, 204), (  14 + R_POSBASEX, 207), 1.0),
			self.pymunk.Segment(self.space.static_body, (  14 + R_POSBASEX, 207), (   8 + R_POSBASEX, 208), 1.0),
			self.pymunk.Segment(self.space.static_body, (   8 + R_POSBASEX, 208), (   3 + R_POSBASEX, 205), 1.0),
			self.pymunk.Segment(self.space.static_body, (   3 + R_POSBASEX, 205), (   2 + R_POSBASEX, 202), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + R_POSBASEX, 202), (   2 + R_POSBASEX, 180), 1.0),

			self.pymunk.Segment(self.space.static_body, (  41 + R_POSBASEX,  82), (  30 + R_POSBASEX,  65), 1.0),
			self.pymunk.Segment(self.space.static_body, (  30 + R_POSBASEX,  65), (  30 + R_POSBASEX,  57), 1.0),
			self.pymunk.Segment(self.space.static_body, (  30 + R_POSBASEX,  57), (  36 + R_POSBASEX,  57), 1.0),
			self.pymunk.Segment(self.space.static_body, (  36 + R_POSBASEX,  57), (  36 + R_POSBASEX,  65), 1.0),
			self.pymunk.Segment(self.space.static_body, (  36 + R_POSBASEX,  65), (  45 + R_POSBASEX,  77), 1.0),
			self.pymunk.Segment(self.space.static_body, (  45 + R_POSBASEX,  77), (  41 + R_POSBASEX,  82), 1.0),

			self.pymunk.Segment(self.space.static_body, (  65 + R_POSBASEX,  24), (  69 + R_POSBASEX,  24), 1.0),
			self.pymunk.Segment(self.space.static_body, (  69 + R_POSBASEX,  24), (  76 + R_POSBASEX,  40), 1.0),
			self.pymunk.Segment(self.space.static_body, (  76 + R_POSBASEX,  40), (  76 + R_POSBASEX,  50), 1.0),
			self.pymunk.Segment(self.space.static_body, (  76 + R_POSBASEX,  50), (  68 + R_POSBASEX,  57), 1.0),
			self.pymunk.Segment(self.space.static_body, (  68 + R_POSBASEX,  57), (  64 + R_POSBASEX,  49), 1.0),
			self.pymunk.Segment(self.space.static_body, (  64 + R_POSBASEX,  49), (  65 + R_POSBASEX,  24), 1.0),

			self.pymunk.Segment(self.space.static_body, ( 123 + R_POSBASEX,  43), ( 123 + R_POSBASEX,  33), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 123 + R_POSBASEX,  33), ( 128 + R_POSBASEX,  23), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 128 + R_POSBASEX,  23), ( 147 + R_POSBASEX,  19), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 147 + R_POSBASEX,  19), ( 153 + R_POSBASEX,  22), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 153 + R_POSBASEX,  22), ( 156 + R_POSBASEX,  29), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 156 + R_POSBASEX,  29), ( 156 + R_POSBASEX,  40), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 156 + R_POSBASEX,  40), ( 152 + R_POSBASEX,  46), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 152 + R_POSBASEX,  46), ( 146 + R_POSBASEX,  53), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 146 + R_POSBASEX,  53), ( 135 + R_POSBASEX,  43), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 135 + R_POSBASEX,  43), ( 123 + R_POSBASEX,  43), 1.0),

			self.pymunk.Segment(self.space.static_body, (  93 + R_POSBASEX,  40), (  93 + R_POSBASEX,  50), 1.0),	#上ライン
			self.pymunk.Segment(self.space.static_body, ( 107 + R_POSBASEX,  37), ( 107 + R_POSBASEX,  47), 1.0),

			self.pymunk.Segment(self.space.static_body, (  17 + R_POSBASEX, 173), (  17 + R_POSBASEX, 149), 1.0),	#左ライン

			#各ステージ共通共通
			self.pymunk.Segment(self.space.static_body, ( 88 + R_POSBASEX, 255), ( 88 + R_POSBASEX, 251), 1.0),	#左フリッパーライン
			self.pymunk.Segment(self.space.static_body, ( 88 + R_POSBASEX, 251), ( 62 + R_POSBASEX, 241), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 62 + R_POSBASEX, 241), ( 62 + R_POSBASEX, 216), 1.0),

			self.pymunk.Segment(self.space.static_body, (133 + R_POSBASEX, 214), (174 + R_POSBASEX, 188), 1.0),	#右フリッパーライン
			self.pymunk.Segment(self.space.static_body, (174 + R_POSBASEX, 188), (174 + R_POSBASEX, 182), 1.0),
			#self.pymunk.Segment(self.space.static_body, (174 + R_POSBASEX, 182), (174 + R_POSBASEX, 165), 1.0),	#白スイッチの蓋閉め
			#self.pymunk.Segment(self.space.static_body, (174 + R_POSBASEX, 182), (188 + R_POSBASEX, 174), 1.0),	#白スイッチの蓋開き
			self.pymunk.Segment(self.space.static_body, (174 + R_POSBASEX, 165), (174 + R_POSBASEX, 149), 1.0),

			self.pymunk.Segment(self.space.static_body, (188 + R_POSBASEX, 132), (188 + R_POSBASEX, 204), 1.0),	#右外枠
			self.pymunk.Segment(self.space.static_body, (188 + R_POSBASEX, 204), (104 + R_POSBASEX, 251), 1.0),
			self.pymunk.Segment(self.space.static_body, (104 + R_POSBASEX, 251), (104 + R_POSBASEX, 255), 1.0),	#外枠終点

			#self.pymunk.Segment(self.space.static_body, (137 + R_POSBASEX, 190), (159 + R_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, (159 + R_POSBASEX, 148), (159 + R_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, (159 + R_POSBASEX, 180), (137 + R_POSBASEX, 190), 1.0),
            
			#self.pymunk.Segment(self.space.static_body, ( 32 + R_POSBASEX, 148), ( 53 + R_POSBASEX, 190), 1.0),	#左三角
			self.pymunk.Segment(self.space.static_body, ( 53 + R_POSBASEX, 190), ( 32 + R_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 32 + R_POSBASEX, 180), ( 32 + R_POSBASEX, 148), 1.0),
		]
		for line in R_static_lines:
			line.elasticity = 0.7
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*R_static_lines)

		#バンパー
		self.R_bumper1_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.R_bumper1_body.position = (37 + R_POSBASEX, 39)
		self.R_bumper1_shape = self.pymunk.Circle( self.R_bumper1_body, 15 )
		self.R_bumper1_shape.elasticity = 2.0
		self.R_bumper1_shape.collision_type = 141
		self.space.add(self.R_bumper1_body, self.R_bumper1_shape)
		self.h_R_bumper1 = self.space.add_collision_handler(0, 141)
		self.h_R_bumper1.pre_solve = self.R_pre_solve

		self.R_bumper2_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.R_bumper2_body.position = (76 + R_POSBASEX, 88)
		self.R_bumper2_shape = self.pymunk.Circle( self.R_bumper2_body, 15 )
		self.R_bumper2_shape.elasticity = 2.0
		self.R_bumper2_shape.collision_type = 142
		self.space.add(self.R_bumper2_body, self.R_bumper2_shape)
		self.h_R_bumper2 = self.space.add_collision_handler(0, 142)
		self.h_R_bumper2.pre_solve = self.R_pre_solve

		self.R_bumper3_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.R_bumper3_body.position = (117 + R_POSBASEX, 82)
		self.R_bumper3_shape = self.pymunk.Circle( self.R_bumper3_body, 15 )
		self.R_bumper3_shape.elasticity = 2.0
		self.R_bumper3_shape.collision_type = 143
		self.space.add(self.R_bumper3_body, self.R_bumper3_shape)
		self.h_R_bumper3 = self.space.add_collision_handler(0, 143)
		self.h_R_bumper3.pre_solve = self.R_pre_solve

		#白スイッチ
		self.R_switch_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_switch_white_body.position = 182 + R_POSBASEX, 103
		self.segment = self.pymunk.Segment(self.R_switch_white_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 109
		self.space.add(self.R_switch_white_body, self.segment)
		self.h_R_switch_white = self.space.add_collision_handler(0, 109)
		self.h_R_switch_white.pre_solve = self.R_pre_solve

		#ホール設定
		#白穴（右上）
		self.R_hole_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_hole_white_body.position = 181 + R_POSBASEX, 12
		self.circle = self.pymunk.Circle(self.R_hole_white_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 102
		self.space.add(self.R_hole_white_body, self.circle)

		self.h_R_white_hole = self.space.add_collision_handler(0, 102)
		self.h_R_white_hole.pre_solve = self.R_pre_solve

		#白穴（左上）
		self.R_hole_white2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_hole_white2_body.position = 9 + R_POSBASEX, 104
		self.circle = self.pymunk.Circle(self.R_hole_white2_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 103
		self.space.add(self.R_hole_white2_body, self.circle)

		self.h_R_white2_hole = self.space.add_collision_handler(0, 103)
		self.h_R_white2_hole.pre_solve = self.R_pre_solve

		#赤穴
		self.R_hole_red_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_hole_red_body.position = 9 + R_POSBASEX, 199
		self.circle = self.pymunk.Circle(self.R_hole_red_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 104
		self.space.add(self.R_hole_red_body, self.circle)

		self.h_R_red_hole = self.space.add_collision_handler(0, 104)
		self.h_R_red_hole.pre_solve = self.R_pre_solve

		#ホールゲート
		#ここでは定義だけにして、更新処理にてholegate_controlで制御したい
		#最初は「閉め」状態にしておく

		#赤穴ゲートは最初開きで開始、射出後ずっと閉じたままになる
		#self.pymunk.Segment(self.space.static_body, ( 17, 189), (  2, 180), 2.0),	#赤穴の蓋閉め
		self.R_holegate_red_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_holegate_red_close_body.position = 17 + R_POSBASEX, 189
		self.R_holegate_red_close_segment = self.pymunk.Segment(self.R_holegate_red_close_body, Vec2d(0, 0), Vec2d(-15, -9), 2)
		#self.space.add(self.W_holegate_red_close_body, self.W_holegate_red_close_segment)

		#self.pymunk.Segment(self.space.static_body, ( 17, 189), ( 17, 173), 2.0),	#赤穴の蓋開き
		self.R_holegate_red_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_holegate_red_open_body.position = 17 + R_POSBASEX, 189
		self.R_holegate_red_open_segment = self.pymunk.Segment(self.R_holegate_red_open_body, Vec2d(0, 0), Vec2d(0, -16), 2)
		self.space.add(self.R_holegate_red_open_body, self.R_holegate_red_open_segment)
		#最初から開いている状態
		GWK[R_red_switch] = B_HOLEOPEN

		#self.pymunk.Segment(self.space.static_body, (174, 182), (174, 165), 1.0),	#白穴の蓋閉め
		self.R_holegate_white_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_holegate_white_close_body.position = 174 + R_POSBASEX, 182
		self.R_holegate_white_close_segment = self.pymunk.Segment(self.R_holegate_white_close_body, Vec2d(0, 0), Vec2d(0, -17), 2)
		self.space.add(self.R_holegate_white_close_body, self.R_holegate_white_close_segment)

		#self.pymunk.Segment(self.space.static_body, (174, 182), (188, 174), 1.0),	#白穴の蓋開き
		self.R_holegate_white_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_holegate_white_open_body.position = 174 + R_POSBASEX, 182
		self.R_holegate_white_open_segment = self.pymunk.Segment(self.R_holegate_white_open_body, Vec2d(0, 0), Vec2d(14, -8), 2)
		#self.space.add(self.R_holegate_white_open_body, self.R_holegate_white_open_segment)

		#スコアライン（通過(HIT->OFF)でスコア加算）
		self.R_scline1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_scline1_body.position = 9 + R_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.R_scline1_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 105
		self.space.add(self.R_scline1_body, self.segment)
		self.h_R_scline1 = self.space.add_collision_handler(0, 105)
		self.h_R_scline1.pre_solve = self.R_pre_solve

		self.R_scline2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_scline2_body.position = 24 + R_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.R_scline2_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.R_collision_type = 106
		self.space.add(self.R_scline2_body, self.segment)
		self.h_R_scline2 = self.space.add_collision_handler(0, 106)
		self.h_R_scline2.pre_solve = self.R_pre_solve

		self.R_scline3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_scline3_body.position = 167 + R_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.R_scline3_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 107
		self.space.add(self.R_scline3_body, self.segment)
		self.h_R_scline3 = self.space.add_collision_handler(0, 107)
		self.h_R_scline3.pre_solve = self.R_pre_solve

		self.R_scline4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.R_scline4_body.position = 181 + R_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.R_scline4_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 108
		self.space.add(self.R_scline4_body, self.segment)
		self.h_R_scline4 = self.space.add_collision_handler(0, 108)
		self.h_R_scline4.pre_solve = self.R_pre_solve

		#[共通]-----------------------------------------------------------------
		#線バンパー（三角バンパーの裏側は外壁セグメントとして登録）
		R_static_blines = [
			self.pymunk.Segment(self.space.static_body, (137 + R_POSBASEX, 190), (159 + R_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, ( 32 + R_POSBASEX, 148), ( 53 + R_POSBASEX, 190), 1.0),	#左三角
		]
		for line in R_static_blines:
			line.elasticity = 2.5	#弾性
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*R_static_blines)

		#フリッパー（positionからのオフセット）
		R_fp = [(2, -2), (-26, 0), (2, 2)]
		R_mass = 100
		R_moment = self.pymunk.moment_for_poly(R_mass, R_fp)

		# right flipper
		self.R_r_flipper_body = self.pymunk.Body(R_mass, R_moment)
		self.R_r_flipper_body.position = 130 + R_POSBASEX, 218
		self.R_r_flipper_shape = self.pymunk.Poly(self.R_r_flipper_body, R_fp)
		self.space.add(self.R_r_flipper_body, self.R_r_flipper_shape)

		self.R_r_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.R_r_flipper_joint_body.position = self.R_r_flipper_body.position
		j = self.pymunk.PinJoint(self.R_r_flipper_body, self.R_r_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.R_r_flipper_body, self.R_r_flipper_joint_body, -0.3, 20000000, 900000
		)
		self.space.add(j, s)

		# left flipper
		self.R_l_flipper_body = self.pymunk.Body(R_mass, R_moment)
		self.R_l_flipper_body.position = 65 + R_POSBASEX, 218
		self.R_l_flipper_shape = self.pymunk.Poly(self.R_l_flipper_body, [(-x, y) for x, y in R_fp])
		self.space.add(self.R_l_flipper_body, self.R_l_flipper_shape)

		self.R_l_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.R_l_flipper_joint_body.position = self.R_l_flipper_body.position
		j = self.pymunk.PinJoint(self.R_l_flipper_body, self.R_l_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.R_l_flipper_body, self.R_l_flipper_joint_body, 0.3, 20000000, 900000
		)
		self.space.add(j, s)

		self.R_r_flipper_shape.group = self.R_l_flipper_shape.group = 1
		self.R_r_flipper_shape.elasticity = self.R_l_flipper_shape.elasticity = 0.4

		#-----------------------------------------------------------------------
		#緑ステージ用
		#外壁
		G_static_lines = [
			self.pymunk.Segment(self.space.static_body, ( 188 + G_POSBASEX, 132), ( 185 + G_POSBASEX, 130), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 185 + G_POSBASEX, 130), ( 188 + G_POSBASEX, 125), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + G_POSBASEX, 125), ( 188 + G_POSBASEX,  84), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + G_POSBASEX,  84), ( 181 + G_POSBASEX,  74), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 181 + G_POSBASEX,  74), ( 188 + G_POSBASEX,  54), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + G_POSBASEX,  54), ( 188 + G_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + G_POSBASEX,   8), ( 185 + G_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 185 + G_POSBASEX,   4), ( 178 + G_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 178 + G_POSBASEX,   4), ( 173 + G_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173 + G_POSBASEX,   8), ( 173 + G_POSBASEX,  49), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173 + G_POSBASEX,  49), ( 168 + G_POSBASEX,  59), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 168 + G_POSBASEX,  59), ( 164 + G_POSBASEX,  54), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 164 + G_POSBASEX,  54), ( 169 + G_POSBASEX,  41), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 169 + G_POSBASEX,  41), ( 169 + G_POSBASEX,  23), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 169 + G_POSBASEX,  23), ( 165 + G_POSBASEX,  13), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 165 + G_POSBASEX,  13), ( 158 + G_POSBASEX,   6), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 158 + G_POSBASEX,   6), ( 148 + G_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 148 + G_POSBASEX,   4), (  28 + G_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (  28 + G_POSBASEX,   4), (  17 + G_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (  17 + G_POSBASEX,   4), (   8 + G_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (   8 + G_POSBASEX,   4), (   2 + G_POSBASEX,   9), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + G_POSBASEX,   9), (   2 + G_POSBASEX,  85), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + G_POSBASEX,  85), (   6 + G_POSBASEX, 100), 1.0),
			self.pymunk.Segment(self.space.static_body, (   6 + G_POSBASEX, 100), (  13 + G_POSBASEX, 109), 1.0),
			self.pymunk.Segment(self.space.static_body, (  13 + G_POSBASEX, 109), (  13 + G_POSBASEX, 122), 1.0),
			self.pymunk.Segment(self.space.static_body, (  13 + G_POSBASEX, 122), (   6 + G_POSBASEX, 127), 1.0),
			self.pymunk.Segment(self.space.static_body, (   6 + G_POSBASEX, 127), (   2 + G_POSBASEX, 136), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + G_POSBASEX, 136), (   2 + G_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + G_POSBASEX, 180), (  62 + G_POSBASEX, 216), 1.0),

			self.pymunk.Segment(self.space.static_body, ( 173 + G_POSBASEX,  95), ( 173 + G_POSBASEX, 113), 1.0),

			self.pymunk.Segment(self.space.static_body, (  16 + G_POSBASEX,  22), (  24 + G_POSBASEX,  22), 1.0),
			self.pymunk.Segment(self.space.static_body, (  24 + G_POSBASEX,  22), (  19 + G_POSBASEX,  37), 1.0),
			self.pymunk.Segment(self.space.static_body, (  19 + G_POSBASEX,  37), (  19 + G_POSBASEX,  67), 1.0),
			self.pymunk.Segment(self.space.static_body, (  19 + G_POSBASEX,  67), (  25 + G_POSBASEX,  85), 1.0),
			self.pymunk.Segment(self.space.static_body, (  25 + G_POSBASEX,  85), (  24 + G_POSBASEX,  87), 1.0),
			self.pymunk.Segment(self.space.static_body, (  24 + G_POSBASEX,  87), (  19 + G_POSBASEX,  83), 1.0),
			self.pymunk.Segment(self.space.static_body, (  19 + G_POSBASEX,  83), (  16 + G_POSBASEX,  77), 1.0),
			self.pymunk.Segment(self.space.static_body, (  16 + G_POSBASEX,  77), (  16 + G_POSBASEX,  22), 1.0),

			self.pymunk.Segment(self.space.static_body, (  33 + G_POSBASEX,  38), (  35 + G_POSBASEX,  33), 1.0),
			self.pymunk.Segment(self.space.static_body, (  35 + G_POSBASEX,  33), (  42 + G_POSBASEX,  40), 1.0),
			self.pymunk.Segment(self.space.static_body, (  42 + G_POSBASEX,  40), (  42 + G_POSBASEX,  56), 1.0),
			self.pymunk.Segment(self.space.static_body, (  42 + G_POSBASEX,  56), (  77 + G_POSBASEX,  77), 1.0),
			self.pymunk.Segment(self.space.static_body, (  77 + G_POSBASEX,  77), (  81 + G_POSBASEX,  87), 1.0),
			self.pymunk.Segment(self.space.static_body, (  81 + G_POSBASEX,  87), (  79 + G_POSBASEX,  88), 1.0),
			self.pymunk.Segment(self.space.static_body, (  79 + G_POSBASEX,  88), (  73 + G_POSBASEX,  82), 1.0),
			self.pymunk.Segment(self.space.static_body, (  73 + G_POSBASEX,  82), (  58 + G_POSBASEX,  82), 1.0),
			self.pymunk.Segment(self.space.static_body, (  58 + G_POSBASEX,  82), (  51 + G_POSBASEX,  87), 1.0),
			self.pymunk.Segment(self.space.static_body, (  51 + G_POSBASEX,  87), (  42 + G_POSBASEX,  83), 1.0),
			self.pymunk.Segment(self.space.static_body, (  42 + G_POSBASEX,  83), (  33 + G_POSBASEX,  68), 1.0),
			self.pymunk.Segment(self.space.static_body, (  33 + G_POSBASEX,  68), (  33 + G_POSBASEX,  38), 1.0),

			self.pymunk.Segment(self.space.static_body, (  87 + G_POSBASEX,  33), (  99 + G_POSBASEX,  19), 1.0),
			self.pymunk.Segment(self.space.static_body, (  99 + G_POSBASEX,  19), ( 102 + G_POSBASEX,  31), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 102 + G_POSBASEX,  31), (  95 + G_POSBASEX,  47), 1.0),
			self.pymunk.Segment(self.space.static_body, (  95 + G_POSBASEX,  47), (  87 + G_POSBASEX,  47), 1.0),
			self.pymunk.Segment(self.space.static_body, (  87 + G_POSBASEX,  47), (  87 + G_POSBASEX,  33), 1.0),

			self.pymunk.Segment(self.space.static_body, (  57 + G_POSBASEX,  38), (  57 + G_POSBASEX,  48), 1.0),	#上のライン
			self.pymunk.Segment(self.space.static_body, (  73 + G_POSBASEX,  35), (  73 + G_POSBASEX,  45), 1.0),

			self.pymunk.Segment(self.space.static_body, ( 17 + G_POSBASEX, 173), ( 17 + G_POSBASEX, 149), 1.0),	#左ライン

			#各ステージ共通共通
			self.pymunk.Segment(self.space.static_body, ( 88 + G_POSBASEX, 255), ( 88 + G_POSBASEX, 251), 1.0),	#左フリッパーライン
			self.pymunk.Segment(self.space.static_body, ( 88 + G_POSBASEX, 251), ( 62 + G_POSBASEX, 241), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 62 + G_POSBASEX, 241), ( 62 + G_POSBASEX, 216), 1.0),

			self.pymunk.Segment(self.space.static_body, (133 + G_POSBASEX, 214), (174 + G_POSBASEX, 188), 1.0),	#右フリッパーライン
			self.pymunk.Segment(self.space.static_body, (174 + G_POSBASEX, 188), (174 + G_POSBASEX, 182), 1.0),
			#self.pymunk.Segment(self.space.static_body, (174 + G_POSBASEX, 182), (174 + G_POSBASEX, 165), 1.0),#白スイッチの蓋閉め
			#self.pymunk.Segment(self.space.static_body, (174 + G_POSBASEX, 182), (188 + G_POSBASEX, 174), 1.0),#白スイッチの蓋開き
			self.pymunk.Segment(self.space.static_body, (174 + G_POSBASEX, 165), (174 + G_POSBASEX, 149), 1.0),

			self.pymunk.Segment(self.space.static_body, (188 + G_POSBASEX, 132), (188 + G_POSBASEX, 204), 1.0),	#右外枠
			self.pymunk.Segment(self.space.static_body, (188 + G_POSBASEX, 204), (104 + G_POSBASEX, 251), 1.0),
			self.pymunk.Segment(self.space.static_body, (104 + G_POSBASEX, 251), (104 + G_POSBASEX, 255), 1.0),	#外枠終点

			#self.pymunk.Segment(self.space.static_body, (137 + G_POSBASEX, 190), (159 + G_POSBASEX, 148), 1.0),#右三角
			self.pymunk.Segment(self.space.static_body, (159 + G_POSBASEX, 148), (159 + G_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, (159 + G_POSBASEX, 180), (137 + G_POSBASEX, 190), 1.0),
            
			#self.pymunk.Segment(self.space.static_body, ( 32 + G_POSBASEX, 148), ( 53 + G_POSBASEX, 190), 1.0),#左三角
			self.pymunk.Segment(self.space.static_body, ( 53 + G_POSBASEX, 190), ( 32 + G_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 32 + G_POSBASEX, 180), ( 32 + G_POSBASEX, 148), 1.0),
		]
		for line in G_static_lines:
			line.elasticity = 0.7
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*G_static_lines)

		#白スイッチ
		self.G_switch_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_switch_white_body.position = 62 + G_POSBASEX, 86
		self.segment = self.pymunk.Segment(self.G_switch_white_body, Vec2d(-4, 2), Vec2d(4, 2), 3)
		self.segment.sensor = True
		self.segment.collision_type = 204
		self.space.add(self.G_switch_white_body, self.segment)
		self.h_G_switch_white = self.space.add_collision_handler(0, 204)
		self.h_G_switch_white.pre_solve = self.G_pre_solve

		#ホールゲート
		#self.pymunk.Segment(self.space.static_body, (174, 182), (174, 165), 1.0),	#白穴の蓋閉め
		self.G_holegate_white_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_holegate_white_close_body.position = 174 + G_POSBASEX, 182
		self.G_holegate_white_close_segment = self.pymunk.Segment(self.G_holegate_white_close_body, Vec2d(0, 0), Vec2d(0, -17), 2)
		self.space.add(self.G_holegate_white_close_body, self.G_holegate_white_close_segment)

		#self.pymunk.Segment(self.space.static_body, (174, 182), (188, 174), 1.0),	#白穴の蓋開き
		self.G_holegate_white_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_holegate_white_open_body.position = 174 + G_POSBASEX, 182
		self.G_holegate_white_open_segment = self.pymunk.Segment(self.G_holegate_white_open_body, Vec2d(0, 0), Vec2d(14, -8), 2)
		#self.space.add(self.G_holegate_white_open_body, self.G_holegate_white_open_segment)

		#ホール設定
		#白穴（右上）
		self.G_hole_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_hole_white_body.position = 181 + G_POSBASEX, 12
		self.circle = self.pymunk.Circle(self.G_hole_white_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 202
		self.space.add(self.G_hole_white_body, self.circle)

		self.h_G_green_hole = self.space.add_collision_handler(0, 202)
		self.h_G_green_hole.pre_solve = self.G_pre_solve

		#緑穴（右上）
		self.G_hole_green_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_hole_green_body.position = 10 + G_POSBASEX, 11
		self.circle = self.pymunk.Circle(self.G_hole_green_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 203
		self.space.add(self.G_hole_green_body, self.circle)

		self.h_G_green_hole = self.space.add_collision_handler(0, 203)
		self.h_G_green_hole.pre_solve = self.G_pre_solve

		#バンパー
		self.G_bumper1_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.G_bumper1_body.position = (134 + G_POSBASEX, 35)
		self.G_bumper1_shape = self.pymunk.Circle( self.G_bumper1_body, 15 )
		self.G_bumper1_shape.elasticity = 2.5
		self.G_bumper1_shape.collision_type = 241
		self.space.add(self.G_bumper1_body, self.G_bumper1_shape)
		self.h_G_bumper1 = self.space.add_collision_handler(0, 241)
		self.h_G_bumper1.pre_solve = self.G_pre_solve

		self.G_bumper2_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.G_bumper2_body.position = (112 + G_POSBASEX, 80)
		self.G_bumper2_shape = self.pymunk.Circle( self.G_bumper2_body, 15 )
		self.G_bumper2_shape.elasticity = 2.5
		self.G_bumper2_shape.collision_type = 242
		self.space.add(self.G_bumper2_body, self.G_bumper2_shape)
		self.h_G_bumper2 = self.space.add_collision_handler(0, 242)
		self.h_G_bumper2.pre_solve = self.G_pre_solve

		#スコアライン（通過(HIT->OFF)でスコア加算）
		self.G_scline1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_scline1_body.position = 9 + G_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.G_scline1_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 205
		self.space.add(self.G_scline1_body, self.segment)
		self.h_G_scline1 = self.space.add_collision_handler(0, 205)
		self.h_G_scline1.pre_solve = self.G_pre_solve

		self.G_scline2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_scline2_body.position = 24 + G_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.G_scline2_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.G_collision_type = 206
		self.space.add(self.G_scline2_body, self.segment)
		self.h_G_scline2 = self.space.add_collision_handler(0, 206)
		self.h_G_scline2.pre_solve = self.G_pre_solve

		self.G_scline3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_scline3_body.position = 167 + G_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.G_scline3_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 207
		self.space.add(self.G_scline3_body, self.segment)
		self.h_G_scline3 = self.space.add_collision_handler(0, 207)
		self.h_G_scline3.pre_solve = self.G_pre_solve

		self.G_scline4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.G_scline4_body.position = 181 + G_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.G_scline4_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 208
		self.space.add(self.G_scline4_body, self.segment)
		self.h_G_scline4 = self.space.add_collision_handler(0, 208)
		self.h_G_scline4.pre_solve = self.G_pre_solve

		#[共通]-----------------------------------------------------------------
		#線バンパー（三角バンパーの裏側は外壁セグメントとして登録）
		G_static_blines = [
			self.pymunk.Segment(self.space.static_body, (137 + G_POSBASEX, 190), (159 + G_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, ( 32 + G_POSBASEX, 148), ( 53 + G_POSBASEX, 190), 1.0),	#左三角
		]
		for line in G_static_blines:
			line.elasticity = 2.5	#弾性
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*G_static_blines)

		#フリッパー（positionからのオフセット）
		G_fp = [(2, -2), (-26, 0), (2, 2)]
		G_mass = 100
		G_moment = self.pymunk.moment_for_poly(G_mass, G_fp)

		# right flipper
		self.G_r_flipper_body = self.pymunk.Body(G_mass, G_moment)
		self.G_r_flipper_body.position = 130 + G_POSBASEX, 218
		self.G_r_flipper_shape = self.pymunk.Poly(self.G_r_flipper_body, G_fp)
		self.space.add(self.G_r_flipper_body, self.G_r_flipper_shape)

		self.G_r_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.G_r_flipper_joint_body.position = self.G_r_flipper_body.position
		j = self.pymunk.PinJoint(self.G_r_flipper_body, self.G_r_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.G_r_flipper_body, self.G_r_flipper_joint_body, -0.3, 20000000, 900000
		)
		self.space.add(j, s)

		# left flipper
		self.G_l_flipper_body = self.pymunk.Body(G_mass, G_moment)
		self.G_l_flipper_body.position = 65 + G_POSBASEX, 218
		self.G_l_flipper_shape = self.pymunk.Poly(self.G_l_flipper_body, [(-x, y) for x, y in G_fp])
		self.space.add(self.G_l_flipper_body, self.G_l_flipper_shape)

		self.G_l_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.G_l_flipper_joint_body.position = self.G_l_flipper_body.position
		j = self.pymunk.PinJoint(self.G_l_flipper_body, self.G_l_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.G_l_flipper_body, self.G_l_flipper_joint_body, 0.3, 20000000, 900000
		)
		self.space.add(j, s)

		self.G_r_flipper_shape.group = self.G_l_flipper_shape.group = 1
		self.G_r_flipper_shape.elasticity = self.G_l_flipper_shape.elasticity = 0.4

		#-----------------------------------------------------------------------
		#青ステージ用
		#外壁
		B_static_lines = [
			self.pymunk.Segment(self.space.static_body, (  62 + B_POSBASEX, 216), (   2 + B_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + B_POSBASEX, 180), (   2 + B_POSBASEX, 136), 1.0),
			self.pymunk.Segment(self.space.static_body, (   2 + B_POSBASEX, 136), (   8 + B_POSBASEX, 124), 1.0),
			self.pymunk.Segment(self.space.static_body, (   8 + B_POSBASEX, 124), (   3 + B_POSBASEX, 117), 1.0),
			self.pymunk.Segment(self.space.static_body, (   3 + B_POSBASEX, 117), (  25 + B_POSBASEX,  77), 1.0),
			self.pymunk.Segment(self.space.static_body, (  25 + B_POSBASEX,  77), (   6 + B_POSBASEX,  36), 1.0),
			self.pymunk.Segment(self.space.static_body, (   6 + B_POSBASEX,  36), (   4 + B_POSBASEX,  25), 1.0),
			self.pymunk.Segment(self.space.static_body, (   4 + B_POSBASEX,  25), (   4 + B_POSBASEX,  16), 1.0),
			self.pymunk.Segment(self.space.static_body, (   4 + B_POSBASEX,  16), (  13 + B_POSBASEX,   9), 1.0),
			self.pymunk.Segment(self.space.static_body, (  13 + B_POSBASEX,   9), (  24 + B_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (  24 + B_POSBASEX,   4), (  44 + B_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (  44 + B_POSBASEX,   4), (  75 + B_POSBASEX,  12), 1.0),
			self.pymunk.Segment(self.space.static_body, (  75 + B_POSBASEX,  12), (  83 + B_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, (  83 + B_POSBASEX,   4), ( 137 + B_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 137 + B_POSBASEX,   4), ( 146 + B_POSBASEX,   5), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 146 + B_POSBASEX,   5), ( 157 + B_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 157 + B_POSBASEX,   8), ( 165 + B_POSBASEX,  16), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 165 + B_POSBASEX,  16), ( 172 + B_POSBASEX,  28), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 172 + B_POSBASEX,  28), ( 173 + B_POSBASEX,  26), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173 + B_POSBASEX,  26), ( 173 + B_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173 + B_POSBASEX,   8), ( 178 + B_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 178 + B_POSBASEX,   4), ( 186 + B_POSBASEX,   4), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 186 + B_POSBASEX,   4), ( 188 + B_POSBASEX,   8), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + B_POSBASEX,   8), ( 188 + B_POSBASEX,  30), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + B_POSBASEX,  30), ( 180 + B_POSBASEX,  49), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 180 + B_POSBASEX,  49), ( 188 + B_POSBASEX,  85), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + B_POSBASEX,  85), ( 188 + B_POSBASEX, 108), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 188 + B_POSBASEX, 108), ( 180 + B_POSBASEX, 120), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 180 + B_POSBASEX, 120), ( 186 + B_POSBASEX, 125), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 186 + B_POSBASEX, 125), ( 188 + B_POSBASEX, 132), 1.0),

			self.pymunk.Segment(self.space.static_body, (  41 + B_POSBASEX,  71), (  74 + B_POSBASEX,  52), 1.0),
			self.pymunk.Segment(self.space.static_body, (  74 + B_POSBASEX,  52), (  74 + B_POSBASEX,  34), 1.0),
			self.pymunk.Segment(self.space.static_body, (  74 + B_POSBASEX,  34), (  60 + B_POSBASEX,  37), 1.0),
			self.pymunk.Segment(self.space.static_body, (  60 + B_POSBASEX,  37), (  59 + B_POSBASEX,  48), 1.0),
			self.pymunk.Segment(self.space.static_body, (  59 + B_POSBASEX,  48), (  54 + B_POSBASEX,  53), 1.0),
			self.pymunk.Segment(self.space.static_body, (  54 + B_POSBASEX,  53), (  36 + B_POSBASEX,  59), 1.0),
			self.pymunk.Segment(self.space.static_body, (  36 + B_POSBASEX,  59), (  41 + B_POSBASEX,  71), 1.0),

			self.pymunk.Segment(self.space.static_body, (  94 + B_POSBASEX,  63), ( 128 + B_POSBASEX,  89), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 128 + B_POSBASEX,  89), ( 128 + B_POSBASEX,  73), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 128 + B_POSBASEX,  73), ( 106 + B_POSBASEX,  66), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 106 + B_POSBASEX,  66), (  94 + B_POSBASEX,  58), 1.0),
			self.pymunk.Segment(self.space.static_body, (  94 + B_POSBASEX,  58), (  94 + B_POSBASEX,  63), 1.0),

			self.pymunk.Segment(self.space.static_body, ( 149 + B_POSBASEX,  28), ( 149 + B_POSBASEX,  55), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 149 + B_POSBASEX,  55), ( 145 + B_POSBASEX,  59), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 145 + B_POSBASEX,  59), ( 145 + B_POSBASEX,  66), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 145 + B_POSBASEX,  66), ( 152 + B_POSBASEX,  69), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 152 + B_POSBASEX,  69), ( 161 + B_POSBASEX,  51), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 161 + B_POSBASEX,  51), ( 161 + B_POSBASEX,  45), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 161 + B_POSBASEX,  45), ( 160 + B_POSBASEX,  37), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 160 + B_POSBASEX,  37), ( 149 + B_POSBASEX,  28), 1.0),

			self.pymunk.Segment(self.space.static_body, ( 170 + B_POSBASEX,  70), ( 159 + B_POSBASEX,  91), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 159 + B_POSBASEX,  91), ( 170 + B_POSBASEX, 108), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 170 + B_POSBASEX, 108), ( 173 + B_POSBASEX, 102), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173 + B_POSBASEX, 102), ( 173 + B_POSBASEX,  87), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173 + B_POSBASEX,  87), ( 170 + B_POSBASEX,  70), 1.0),

			self.pymunk.Segment(self.space.static_body, (  28 + B_POSBASEX,  28), (  28 + B_POSBASEX,  39), 1.0),		#左上のライン
			self.pymunk.Segment(self.space.static_body, (  44 + B_POSBASEX,  32), (  44 + B_POSBASEX,  43), 1.0),

			self.pymunk.Segment(self.space.static_body, (  17 + B_POSBASEX, 173), (  17 + B_POSBASEX, 149), 1.0),		#左ライン

			#各ステージ共通共通
			self.pymunk.Segment(self.space.static_body, ( 88 + B_POSBASEX, 255), ( 88 + B_POSBASEX, 251), 1.0),	#左フリッパーライン
			self.pymunk.Segment(self.space.static_body, ( 88 + B_POSBASEX, 251), ( 62 + B_POSBASEX, 241), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 62 + B_POSBASEX, 241), ( 62 + B_POSBASEX, 216), 1.0),

			self.pymunk.Segment(self.space.static_body, (133 + B_POSBASEX, 214), (174 + B_POSBASEX, 188), 1.0),	#右フリッパーライン
			self.pymunk.Segment(self.space.static_body, (174 + B_POSBASEX, 188), (174 + B_POSBASEX, 182), 1.0),
			#self.pymunk.Segment(self.space.static_body, (174 + B_POSBASEX, 182), (174 + B_POSBASEX, 165), 1.0),	#白スイッチの蓋閉め
			#self.pymunk.Segment(self.space.static_body, (174 + B_POSBASEX, 182), (188 + B_POSBASEX, 174), 1.0),	#白スイッチの蓋開き
			self.pymunk.Segment(self.space.static_body, (174 + B_POSBASEX, 165), (174 + B_POSBASEX, 149), 1.0),

			self.pymunk.Segment(self.space.static_body, (188 + B_POSBASEX, 132), (188 + B_POSBASEX, 204), 1.0),	#右外枠
			self.pymunk.Segment(self.space.static_body, (188 + B_POSBASEX, 204), (104 + B_POSBASEX, 251), 1.0),
			self.pymunk.Segment(self.space.static_body, (104 + B_POSBASEX, 251), (104 + B_POSBASEX, 255), 1.0),	#外枠終点

			#self.pymunk.Segment(self.space.static_body, (137 + B_POSBASEX, 190), (159 + B_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, (159 + B_POSBASEX, 148), (159 + B_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, (159 + B_POSBASEX, 180), (137 + B_POSBASEX, 190), 1.0),
            
			#self.pymunk.Segment(self.space.static_body, ( 32 + B_POSBASEX, 148), ( 53 + B_POSBASEX, 190), 1.0),	#左三角
			self.pymunk.Segment(self.space.static_body, ( 53 + B_POSBASEX, 190), ( 32 + B_POSBASEX, 180), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 32 + B_POSBASEX, 180), ( 32 + B_POSBASEX, 148), 1.0),
		]
		for line in B_static_lines:
			line.elasticity = 0.7
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*B_static_lines)

		#軸
		self.B_shaft1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_shaft1_body.position = 110 + B_POSBASEX, 124
		self.circle = self.pymunk.Circle(self.B_shaft1_body, 2)
		self.circle.elasticity = 0.7
		self.space.add(self.B_shaft1_body, self.circle)

		self.B_shaft2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_shaft2_body.position = 78 + B_POSBASEX, 124
		self.circle = self.pymunk.Circle(self.B_shaft2_body, 2)
		self.circle.elasticity = 0.7
		self.space.add(self.B_shaft2_body, self.circle)

		#ホール設定
		#白穴
		self.B_hole_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_hole_white_body.position = 181 + B_POSBASEX, 12
		self.circle = self.pymunk.Circle(self.B_hole_white_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 302
		self.space.add(self.B_hole_white_body, self.circle)

		self.h_B_white_hole = self.space.add_collision_handler(0, 302)
		self.h_B_white_hole.pre_solve = self.B_pre_solve

		#青穴
		self.B_hole_blue_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_hole_blue_body.position = 181 + B_POSBASEX, 104
		self.circle = self.pymunk.Circle(self.B_hole_blue_body, 6)
		self.circle.sensor = True
		self.circle.collision_type = 303
		self.space.add(self.B_hole_blue_body, self.circle)

		self.h_B_red_hole = self.space.add_collision_handler(0, 303)
		self.h_B_red_hole.pre_solve = self.B_pre_solve

		#self.pymunk.Segment(self.space.static_body, (174, 182), (174, 165), 1.0),	#白穴の蓋閉め
		self.B_holegate_white_close_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_holegate_white_close_body.position = 174 + B_POSBASEX, 182
		self.B_holegate_white_close_segment = self.pymunk.Segment(self.B_holegate_white_close_body, Vec2d(0, 0), Vec2d(0, -17), 2)
		self.space.add(self.B_holegate_white_close_body, self.B_holegate_white_close_segment)

		#self.pymunk.Segment(self.space.static_body, (174, 182), (188, 174), 1.0),	#白穴の蓋開き
		self.B_holegate_white_open_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_holegate_white_open_body.position = 174 + B_POSBASEX, 182
		self.B_holegate_white_open_segment = self.pymunk.Segment(self.B_holegate_white_open_body, Vec2d(0, 0), Vec2d(14, -8), 2)
		#self.space.add(self.B_holegate_white_open_body, self.B_holegate_white_open_segment)

		#スコアライン（通過(HIT->OFF)でスコア加算）
		self.B_scline1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_scline1_body.position = 9 + B_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.B_scline1_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 305
		self.space.add(self.B_scline1_body, self.segment)
		self.h_B_scline1 = self.space.add_collision_handler(0, 305)
		self.h_B_scline1.pre_solve = self.B_pre_solve

		self.B_scline2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_scline2_body.position = 24 + B_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.B_scline2_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.B_collision_type = 306
		self.space.add(self.B_scline2_body, self.segment)
		self.h_B_scline2 = self.space.add_collision_handler(0, 306)
		self.h_B_scline2.pre_solve = self.B_pre_solve

		self.B_scline3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_scline3_body.position = 167 + B_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.B_scline3_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 307
		self.space.add(self.B_scline3_body, self.segment)
		self.h_B_scline3 = self.space.add_collision_handler(0, 307)
		self.h_B_scline3.pre_solve = self.B_pre_solve

		self.B_scline4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_scline4_body.position = 181 + B_POSBASEX, 162
		self.segment = self.pymunk.Segment(self.B_scline4_body, Vec2d(0, -4), Vec2d(0, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 308
		self.space.add(self.B_scline4_body, self.segment)
		self.h_B_scline4 = self.space.add_collision_handler(0, 308)
		self.h_B_scline4.pre_solve = self.B_pre_solve

		#白スイッチ
		self.B_switch_white_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_white_body.position = 158 + B_POSBASEX, 103
		self.segment = self.pymunk.Segment(self.B_switch_white_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 309
		self.space.add(self.B_switch_white_body, self.segment)
		self.h_B_switch_white = self.space.add_collision_handler(0, 309)
		self.h_B_switch_white.pre_solve = self.B_pre_solve

		#黄スイッチ
		#右スイッチ
		self.B_switch_yellow1_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow1_body.position = 102 + B_POSBASEX, 76
		self.segment = self.pymunk.Segment(self.B_switch_yellow1_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 311
		self.space.add(self.B_switch_yellow1_body, self.segment)
		self.h_B_switch_yellow1 = self.space.add_collision_handler(0, 311)
		self.h_B_switch_yellow1.pre_solve = self.B_pre_solve

		self.B_switch_yellow2_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow2_body.position = 112 + B_POSBASEX, 84
		self.segment = self.pymunk.Segment(self.B_switch_yellow2_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 312
		self.space.add(self.B_switch_yellow2_body, self.segment)
		self.h_B_switch_yellow2 = self.space.add_collision_handler(0, 312)
		self.h_B_switch_yellow2.pre_solve = self.B_pre_solve

		self.B_switch_yellow3_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow3_body.position = 122 + B_POSBASEX, 91
		self.segment = self.pymunk.Segment(self.B_switch_yellow3_body, Vec2d(-4, -4), Vec2d(4, 4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 313
		self.space.add(self.B_switch_yellow3_body, self.segment)
		self.h_B_switch_yellow3 = self.space.add_collision_handler(0, 313)
		self.h_B_switch_yellow3.pre_solve = self.B_pre_solve

		#中央スイッチ
		self.B_switch_yellow4_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow4_body.position = 52 + B_POSBASEX, 76
		self.segment = self.pymunk.Segment(self.B_switch_yellow4_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 314
		self.space.add(self.B_switch_yellow4_body, self.segment)
		self.h_B_switch_yellow4 = self.space.add_collision_handler(0, 314)
		self.h_B_switch_yellow4.pre_solve = self.B_pre_solve

		self.B_switch_yellow5_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow5_body.position = 62 + B_POSBASEX, 70
		self.segment = self.pymunk.Segment(self.B_switch_yellow5_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 315
		self.space.add(self.B_switch_yellow5_body, self.segment)
		self.h_B_switch_yellow5 = self.space.add_collision_handler(0, 315)
		self.h_B_switch_yellow5.pre_solve = self.B_pre_solve

		self.B_switch_yellow6_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow6_body.position = 72 + B_POSBASEX, 64
		self.segment = self.pymunk.Segment(self.B_switch_yellow6_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 316
		self.space.add(self.B_switch_yellow6_body, self.segment)
		self.h_B_switch_yellow6 = self.space.add_collision_handler(0, 316)
		self.h_B_switch_yellow6.pre_solve = self.B_pre_solve

		#左スイッチ
		self.B_switch_yellow7_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow7_body.position = 29 + B_POSBASEX, 88
		self.segment = self.pymunk.Segment(self.B_switch_yellow7_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 317
		self.space.add(self.B_switch_yellow7_body, self.segment)
		self.h_B_switch_yellow7 = self.space.add_collision_handler(0, 317)
		self.h_B_switch_yellow7.pre_solve = self.B_pre_solve

		self.B_switch_yellow8_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow8_body.position = 23 + B_POSBASEX, 101
		self.segment = self.pymunk.Segment(self.B_switch_yellow8_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 318
		self.space.add(self.B_switch_yellow8_body, self.segment)
		self.h_B_switch_yellow8 = self.space.add_collision_handler(0, 318)
		self.h_B_switch_yellow8.pre_solve = self.B_pre_solve

		self.B_switch_yellow9_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.B_switch_yellow9_body.position = 16 + B_POSBASEX, 113
		self.segment = self.pymunk.Segment(self.B_switch_yellow9_body, Vec2d(-4, 4), Vec2d(4, -4), 3)
		self.segment.sensor = True
		self.segment.collision_type = 319
		self.space.add(self.B_switch_yellow9_body, self.segment)
		self.h_B_switch_yellow9 = self.space.add_collision_handler(0, 319)
		self.h_B_switch_yellow9.pre_solve = self.B_pre_solve

		#バンパー
		self.B_bumper1_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.B_bumper1_body.position = (118 + B_POSBASEX, 35)
		self.B_bumper1_shape = self.pymunk.Circle( self.B_bumper1_body, 15 )
		self.B_bumper1_shape.elasticity = 2.5
		self.B_bumper1_shape.collision_type = 341
		self.space.add(self.B_bumper1_body, self.B_bumper1_shape)
		self.h_B_bumper1 = self.space.add_collision_handler(0, 341)
		self.h_B_bumper1.pre_solve = self.B_pre_solve

		#線バンパー（三角バンパーの裏側は外壁セグメントとして登録）
		B_static_blines = [
			self.pymunk.Segment(self.space.static_body, (137 + B_POSBASEX, 190), (159 + B_POSBASEX, 148), 1.0),	#右三角
			self.pymunk.Segment(self.space.static_body, ( 32 + B_POSBASEX, 148), ( 53 + B_POSBASEX, 190), 1.0),	#左三角
		]
		for line in B_static_blines:
			line.elasticity = 2.5	#弾性
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*B_static_blines)

		#フリッパー（positionからのオフセット）
		B_fp = [(2, -2), (-26, 0), (2, 2)]
		B_mass = 100
		B_moment = self.pymunk.moment_for_poly(B_mass, B_fp)

		# right flipper
		self.B_r_flipper_body = self.pymunk.Body(B_mass, B_moment)
		self.B_r_flipper_body.position = 130 + B_POSBASEX, 218
		self.B_r_flipper_shape = self.pymunk.Poly(self.B_r_flipper_body, B_fp)
		self.space.add(self.B_r_flipper_body, self.B_r_flipper_shape)

		self.B_r_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.B_r_flipper_joint_body.position = self.B_r_flipper_body.position
		j = self.pymunk.PinJoint(self.B_r_flipper_body, self.B_r_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.B_r_flipper_body, self.B_r_flipper_joint_body, -0.3, 20000000, 900000
		)
		self.space.add(j, s)

		# left flipper
		self.B_l_flipper_body = self.pymunk.Body(B_mass, B_moment)
		self.B_l_flipper_body.position = 65 + B_POSBASEX, 218
		self.B_l_flipper_shape = self.pymunk.Poly(self.B_l_flipper_body, [(-x, y) for x, y in B_fp])
		self.space.add(self.B_l_flipper_body, self.B_l_flipper_shape)

		self.B_l_flipper_joint_body = self.pymunk.Body(body_type=self.pymunk.Body.KINEMATIC)
		self.B_l_flipper_joint_body.position = self.B_l_flipper_body.position
		j = self.pymunk.PinJoint(self.B_l_flipper_body, self.B_l_flipper_joint_body, (0, 0), (0, 0))
		s = self.pymunk.DampedRotarySpring(
			self.B_l_flipper_body, self.B_l_flipper_joint_body, 0.3, 20000000, 900000
		)
		self.space.add(j, s)

		self.B_r_flipper_shape.group = self.B_l_flipper_shape.group = 1
		self.B_r_flipper_shape.elasticity = self.B_l_flipper_shape.elasticity = 0.4


		#ボール生成
		self.ball_create()

	#-----------------------------------------------------------------
	#ボール生成
	#-----------------------------------------------------------------
	def ball_create(self):
		self.ball_body = self.pymunk.Body( 1, float('inf') )	#0 質量, 慣性モーメント

		#ボールの初期位置を設定
		self.ball_initpos_set()  # ボールの位置を初期化
		#ボールの速度をリセット
		self.ball_body.velocity = (0, 0)
		
		#衝突タイプ設定
		self.ball_body.sensor = True
		self.ball_body.collision_type = 0
		#ボールを円形として定義
		self.ball_shape = self.pymunk.Circle( self.ball_body, BALL_RADIUS )
		#反射係数（弾性）を設定
		self.ball_shape.elasticity = 0.4

		#ボールを物理空間に追加
		self.space.add( self.ball_body, self.ball_shape )
		
		#一旦おやすみ
		self.ball_body.sleep()

	#-----------------------------------------------------------------
	#ボール初期位置セット
	#-----------------------------------------------------------------
	def ball_initpos_set(self):

		if( GWK[field_number] == FIELD_WHITE ):
			#白ホールから左へ
			self.ball_body.position = ( 180 + W_POSBASEX, 13 )
		elif( GWK[field_number] == FIELD_RED ):
			#赤ホールから上へ
			self.ball_body.position = ( 9 + R_POSBASEX, 200 )
		elif( GWK[field_number] == FIELD_GREEN ):
			#緑ホールから右へ
			self.ball_body.position = ( 10 + G_POSBASEX, 12 )
		elif( GWK[field_number] == FIELD_BLUE ):
			#青ホールから上へ
			self.ball_body.position = ( 181 + B_POSBASEX, 104 )
	
	#-----------------------------------------------------------------
	#ボール射出
	#-----------------------------------------------------------------
	def ball_shoot(self):
		if( GWK[field_number] == FIELD_WHITE ):
			##白ホールから左へ
			self.ball_body.apply_impulse_at_local_point((-200, 0), (0, 0))
		elif( GWK[field_number] == FIELD_RED ):
			#赤ホールから上へ
			self.ball_body.apply_impulse_at_local_point((0, -250), (0, 0))
		elif( GWK[field_number] == FIELD_GREEN ):
			#緑ホールから右へ
			self.ball_body.apply_impulse_at_local_point((200, 0), (0, 0))
		elif( GWK[field_number] == FIELD_BLUE ):
			##青ホールから上へ
			self.ball_body.apply_impulse_at_local_point((0, -250), (0, 0))

	#-----------------------------------------------------------------
	#更新
	#-----------------------------------------------------------------
	def update(self):
		from pymunk import Vec2d

		#------------------------------------------
		if( GWK[game_adv] == G_FIELD_CHANGE ):
			if( GWK[game_subadv] == GS_INIT ):
				GWK[wait_counter] = 10
				GWK[game_subadv] = GS_WAIT1

			elif( GWK[game_subadv] == GS_WAIT1 ):
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[zoom_counter] = BALL_ZOOMMAX
					GWK[game_subadv] = GS_BALL_SMALL

			elif( GWK[game_subadv] == GS_BALL_SMALL ):
				#ボール縮小
				GWK[zoom_counter] -= 1
				if( GWK[zoom_counter] < 0 ):
					GWK[zoom_counter] = 0
					GWK[wait_counter] = 10
					GWK[game_subadv] = GS_WAIT2

			elif( GWK[game_subadv] == GS_WAIT2 ):
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[wait_counter] = 0x10
					GWK[game_subadv] = GS_FADEOUT

			elif( GWK[game_subadv] == GS_FADEOUT ):
				#フェードアウト
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):

					for _cnt in range(16):
						pyxel.colors[_cnt] = 0

					GWK[game_subadv] = GS_CHANGE_FIELD
				else:
					for _cnt in range(16):
						c = defcol_tbl[_cnt]
						r = int( ( ( c >> 16 ) & 0xff ) * GWK[wait_counter] / 0x10 )
						g = int( ( ( c >>  8 ) & 0xff ) * GWK[wait_counter] / 0x10 )
						b = int( (   c         & 0xff ) * GWK[wait_counter] / 0x10 )
						c = ( r << 16 ) + ( g << 8 ) + b
						pyxel.colors[_cnt] = c

			elif( GWK[game_subadv] == GS_CHANGE_FIELD ):
				#フィールド変更
			
				#穴に入ったフラグはクリアしておく
				if( GWK[field_number] == FIELD_WHITE ):
					#白ステージの時、入った穴のゲートは閉じておく
					if( GWK[to_field] == FIELD_RED ):
						GWK[red_switch] &= ~B_HOLEIN
						GWK[red_switch] |= B_HOLECLOSE
					elif( GWK[to_field] == FIELD_GREEN ):
						GWK[green_switch] &= ~B_HOLEIN
						GWK[green_switch] |= B_HOLECLOSE
					elif( GWK[to_field] == FIELD_BLUE ):
						GWK[blue_switch] &= ~B_HOLEIN
						GWK[blue_switch] |= B_HOLECLOSE
				elif( GWK[field_number] == FIELD_RED ):
					GWK[R_white_switch] &= ~B_HOLEIN
					GWK[R_white_switch] &= ~B_HOLEIN2

					#spaceにR_holegate_red_close_bodyが残ってるかどうか確認
					list = self.space.bodies
					for b in list:
						if( b == self.R_holegate_red_close_body ):
							#赤ステージの時はゲート閉まっているので開けておく
							self.space.remove(self.R_holegate_red_close_body, self.R_holegate_red_close_segment)	#赤穴の蓋閉め除去
							self.space.add(self.R_holegate_red_open_body, self.R_holegate_red_open_segment)			#赤穴の蓋開き追加

					#赤ステージの時ゲートは最初から開いている状態にしておく
					GWK[R_red_switch] = B_HOLEOPEN

				elif( GWK[field_number] == FIELD_GREEN ):
					GWK[G_white_switch] &= ~B_HOLEIN
				elif( GWK[field_number] == FIELD_BLUE ):
					GWK[B_white_switch] &= ~B_HOLEIN
			
				#FIELD更新
				GWK[field_number] = GWK[to_field]

				#カメラ位置更新
				if( GWK[field_number] == FIELD_WHITE ):
					pyxel.camera(W_POSBASEX, _POSBASEY)
				elif( GWK[field_number] == FIELD_RED ):
					pyxel.camera(R_POSBASEX, _POSBASEY)
				elif( GWK[field_number] == FIELD_GREEN ):
					pyxel.camera(G_POSBASEX, _POSBASEY)
				elif( GWK[field_number] == FIELD_BLUE ):
					pyxel.camera(B_POSBASEX, _POSBASEY)
					
				#ボール位置初期化
				self.ball_body.velocity = (0, 0)
				self.ball_initpos_set()
				self.ball_body.sleep()
				
				GWK[wait_counter] = 10
				GWK[game_subadv] = GS_WAIT3

			elif( GWK[game_subadv] == GS_WAIT3 ):
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[wait_counter] = 0x10
					GWK[game_subadv] = GS_FADEIN

			elif( GWK[game_subadv] == GS_FADEIN ):
				#フェードイン
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):

					for _cnt in range(16):
						pyxel.colors[_cnt] = defcol_tbl[_cnt]

					GWK[wait_counter] = 10
					GWK[game_subadv] = GS_WAIT4
				else:
					for _cnt in range(16):
						c = defcol_tbl[_cnt]
						r = int( ( ( c >> 16 ) & 0xff ) * ( 0x10 - GWK[wait_counter] ) / 0x10 )
						g = int( ( ( c >>  8 ) & 0xff ) * ( 0x10 - GWK[wait_counter] ) / 0x10 )
						b = int( (   c         & 0xff ) * ( 0x10 - GWK[wait_counter] ) / 0x10 )
						c = ( r << 16 ) + ( g << 8 ) + b
						pyxel.colors[_cnt] = c

			elif( GWK[game_subadv] == GS_WAIT4 ):
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[wait_counter] = BALLIN_ANIMMAX
					GWK[game_subadv] = GS_BALLIN


			elif( GWK[game_subadv] == GS_BALLIN ):
				#ボール位置に集まるエフェクト入れたい（開始位置がわかりにくいので）
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[wait_counter] = 10
					GWK[game_subadv] = GS_WAIT5

			elif( GWK[game_subadv] == GS_WAIT5 ):
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[zoom_counter] = 0
					GWK[game_subadv] = GS_BALL_BIG

			elif( GWK[game_subadv] == GS_BALL_BIG ):
				#ボール拡大
				GWK[zoom_counter] += 1
				if( GWK[zoom_counter] >= BALL_ZOOMMAX ):
					GWK[wait_counter] = 10
					GWK[game_subadv] = GS_WAIT6

			elif( GWK[game_subadv] == GS_WAIT6 ):
				GWK[wait_counter] -= 1
				if( GWK[wait_counter] < 0 ):
					GWK[game_subadv] = GS_BALL_SHOOT

			elif( GWK[game_subadv] == GS_BALL_SHOOT ):
				GWK[ball_switch] = 1	#StartUp
				#ボール射出は任せる

				##ボール自動射出
				#self.ball_shoot()
	
				GWK[game_adv] = G_GAME
				GWK[game_subadv] = GS_INIT

		#------------------------------------------
		elif( GWK[game_adv] == G_GAME ):
			if( GWK[game_subadv] == GS_INIT ):
			
				GWK[ballpos_save_counter] = 0
				x, y = self.ball_body.position
				#初期座標をセット
				for _cnt in range(BALLPOS_SAVEMAX):
					GWK[ballpos_save + (_cnt * 2) + 0] = x
					GWK[ballpos_save + (_cnt * 2) + 1] = y
				
				GWK[game_subadv] = GS_MAIN

			elif( GWK[game_subadv] == GS_MAIN ):

				#共通オブジェクト
				if( GWK[field_number] == FIELD_WHITE ):
					ofs = W_POSBASEX
				elif( GWK[field_number] == FIELD_RED ):
					ofs = R_POSBASEX
				elif( GWK[field_number] == FIELD_GREEN ):
					ofs = G_POSBASEX
				elif( GWK[field_number] == FIELD_BLUE ):
					ofs = B_POSBASEX

				step = 5  # Run multiple steps for more stable simulation
				step_dt = 1 / self.fps / step
				for _ in range(step):
					self.space.step(step_dt)

				#操作
				if self.getInputB():
					pyxel.quit()

				# 左フリッパーの制御
				if self.getInputLEFT():  # キーを押している間、フリッパーを上げる
					if( GWK[field_number] == FIELD_WHITE ):
						self.W_l_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * 7500, (-60, 0) )
					elif( GWK[field_number] == FIELD_RED ):
						self.R_l_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * 7500, (-60, 0) )
					elif( GWK[field_number] == FIELD_GREEN ):
						self.G_l_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * 7500, (-60, 0) )
					elif( GWK[field_number] == FIELD_BLUE ):
						self.B_l_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * 7500, (-60, 0) )
				# 右フリッパーの制御
				if self.getInputRIGHT():  # キーを押している間、フリッパーを上げる
					if( GWK[field_number] == FIELD_WHITE ):
						self.W_r_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * -7500, (-60, 0) )
					elif( GWK[field_number] == FIELD_RED ):
						self.R_r_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * -7500, (-60, 0) )
					elif( GWK[field_number] == FIELD_GREEN ):
						self.G_r_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * -7500, (-60, 0) )
					elif( GWK[field_number] == FIELD_BLUE ):
						self.B_r_flipper_body.apply_impulse_at_local_point( Vec2d.unit() * -7500, (-60, 0) )

				if self.getInputA():
					#ボールショット
					if( GWK[ball_switch] & 0x01 ):
						GWK[ball_switch] &= ~0x01
						self.ball_shoot()

						self.se_set(16)

				if( ( GWK[ball_switch] & 0x01 ) == 0 ):
					#ボールが画面外になったかどうかの判定
					if self.ball_body.position.get_distance((SCREEN_WIDTH//2 + ofs, 256)) > 512:
						self.ball_initpos_set()  # ボールの位置を初期化
						self.ball_body.velocity = (0, 0)  # ボールの速度をリセット
						GWK[ball_switch] |= 0x01

						#画面外からのもどりでおやすみ
						self.ball_body.sleep()

						self.se_set(29)

						#各ステージ初期化
						if( GWK[field_number] == FIELD_WHITE ):
							pass
						elif( GWK[field_number] == FIELD_RED ):
							#閉じているなら開ける
							GWK[R_red_switch] = B_SWITCH1
						elif( GWK[field_number] == FIELD_GREEN ):
							pass
						elif( GWK[field_number] == FIELD_BLUE ):
							pass

						#ホールから再開
						GWK[game_adv] = G_FIELD_CHANGE
						GWK[game_subadv] = GS_WAIT4
						GWK[wait_counter] = 10
						GWK[zoom_counter] = 0

				if( ( GWK[ball_switch] & 0x01 ) == 0 ):
					x, y = self.ball_body.position
					GWK[ballpos_save + ( GWK[ballpos_save_counter] * 2 ) + 0] = x
					GWK[ballpos_save + ( GWK[ballpos_save_counter] * 2 ) + 1] = y
					
					GWK[ballpos_save_counter] += 1
					if( GWK[ballpos_save_counter] >= BALLPOS_SAVEMAX ):
						GWK[ballpos_save_counter] = 0

				#ホールゲート制御
				if( GWK[field_number] == FIELD_WHITE ):
					self.W_holegate_control()
					self.W_holein_control()
				elif( GWK[field_number] == FIELD_RED ):
					self.R_holegate_control()
					self.R_holein_control()
				elif( GWK[field_number] == FIELD_GREEN ):
					self.G_holegate_control()
					self.G_holein_control()
				elif( GWK[field_number] == FIELD_BLUE ):
					self.B_holegate_control()
					self.B_holein_control()

	#-----------------------------------------------------------------
	#res table
	#-----------------------------------------------------------------
	IDMAX = 0x23
	ctbl = [
		# u,    v,    us,   vs
		[ 0x00, 0x50, 0x20, 0x20 ],		#0x00 バンパー
		[ 0x10, 0x00, 0x10, 0x10 ],		#0x01 スイッチ
		[ 0x30, 0x00, 0x08, 0x08 ],		#0x02 黄軸
		[ 0x00, 0x10, 0x10, 0x10 ],		#0x03 緑スイッチOFF
		[ 0x00, 0x20, 0x10, 0x10 ],		#0x04 緑スイッチON
		[ 0x10, 0x10, 0x10, 0x10 ],		#0x05 青スイッチOFF
		[ 0x20, 0x10, 0x10, 0x10 ],		#0x06 青スイッチON
		[ 0x10, 0x20, 0x10, 0x10 ],		#0x07 赤スイッチOFF
		[ 0x20, 0x20, 0x10, 0x10 ],		#0x08 赤スイッチON
		[ 0x30, 0x10, 0x08, 0x08 ],		#0x09 矢印下
		[ 0x38, 0x10, 0x08, 0x08 ],		#0x0a 矢印上
		[ 0x00, 0x30, 0x08, 0x20 ],		#0x0b 縦スコア500
		[ 0x08, 0x30, 0x08, 0x20 ],		#0x0c 縦スコア3000
		[ 0x10, 0x30, 0x08, 0x20 ],		#0x0d 縦スコア1000
		[ 0x20, 0x50, 0x20, 0x20 ],		#0x0e バンパー点滅
		[ 0x20, 0x00, 0x10, 0x10 ],		#0x0f スイッチ点滅
		[ 0x00, 0x70, 0x10, 0x10 ],		#0x10 小バンパー
		[ 0x10, 0x70, 0x10, 0x10 ],		#0x11 小バンパー点滅
		[ 0x18, 0x30, 0x08, 0x10 ],		#0x12 スコアライン
		[ 0x30, 0x18, 0x08, 0x08 ],		#0x13 矢印左
		[ 0x30, 0x18, 0x08, 0x08 ],		#0x14 矢印右
		[ 0x38, 0x00, 0x08, 0x08 ],		#0x15 白軸
		[ 0x30, 0x08, 0x08, 0x08 ],		#0x16 赤軸
		[ 0x38, 0x08, 0x08, 0x08 ],		#0x17 青軸
		[ 0x20, 0x30, 0x10, 0x10 ],		#0x18 黄右下スイッチOFF
		[ 0x30, 0x30, 0x10, 0x10 ],		#0x19 黄右下スイッチON
		[ 0x20, 0x40, 0x10, 0x10 ],		#0x1a 黄左下スイッチOFF
		[ 0x30, 0x40, 0x10, 0x10 ],		#0x1b 黄左下スイッチON
		[ 0x30, 0x20, 0x08, 0x08 ],		#0x1c 矢印左上
		[ 0x38, 0x20, 0x08, 0x08 ],		#0x1d 矢印右上
		[ 0x30, 0x28, 0x08, 0x08 ],		#0x1e 矢印左下
		[ 0x38, 0x28, 0x08, 0x08 ],		#0x1f 矢印右下
		[ 0x20, 0x70, 0x10, 0x10 ],		#0x20 白スイッチ水平
		[ 0x30, 0x70, 0x10, 0x10 ],		#0x21 白スイッチ水平点滅
		[ 0x40, 0x00, 0x0a, 0x0a ],		#0x22 ボール
	]

	#-----------------------------------------------------------------
	#キャラクタセット
	#	X座標, Y座標, id番号
	#-----------------------------------------------------------------
	def cput(self, _xp, _yp, _id ):
		if( _id < self.IDMAX ):
			pyxel.blt( _xp, _yp, 0, self.ctbl[_id][0], self.ctbl[_id][1], self.ctbl[_id][2], self.ctbl[_id][3], 0 )

	#-----------------------------------------------------------------
	#描画
	#-----------------------------------------------------------------
	def draw(self):

		pyxel.cls(0)

		#各ステージ毎の表示
		if( GWK[field_number] == FIELD_WHITE ):

			#外壁
			pyxel.line(  62 + W_POSBASEX, 216,  17 + W_POSBASEX, 189, 7 )		#外枠始点
			pyxel.line(  17 + W_POSBASEX, 189,  17 + W_POSBASEX, 204, 7 )
			pyxel.line(  17 + W_POSBASEX, 204,  14 + W_POSBASEX, 207, 7 )
			pyxel.line(  14 + W_POSBASEX, 207,   8 + W_POSBASEX, 208, 7 )
			pyxel.line(   8 + W_POSBASEX, 208,   3 + W_POSBASEX, 205, 7 )
			pyxel.line(   3 + W_POSBASEX, 205,   2 + W_POSBASEX, 204, 7 )
			pyxel.line(   2 + W_POSBASEX, 204,   2 + W_POSBASEX, 180, 7 )

			#pyxel.line(  17 + W_POSBASEX, 189,   2 + W_POSBASEX, 180, 10 )	#赤穴の蓋閉め
			#pyxel.line(  17 + W_POSBASEX, 189,  17 + W_POSBASEX, 173, 10 )	#赤穴の蓋開き

			pyxel.line(   2 + W_POSBASEX, 180,   2 + W_POSBASEX, 133, 7 )
			pyxel.line(   2 + W_POSBASEX, 133,  15 + W_POSBASEX, 123, 7 )
			pyxel.line(  15 + W_POSBASEX, 123,  39 + W_POSBASEX,  97, 7 )
			pyxel.line(  39 + W_POSBASEX,  97,  36 + W_POSBASEX,  91, 7 )
			pyxel.line(  36 + W_POSBASEX,  91,  16 + W_POSBASEX, 112, 7 )
			pyxel.line(  16 + W_POSBASEX, 112,   9 + W_POSBASEX, 113, 7 )
			pyxel.line(   9 + W_POSBASEX, 113,   5 + W_POSBASEX, 104, 7 )
			pyxel.line(   5 + W_POSBASEX, 104,   8 + W_POSBASEX,  96, 7 )
			pyxel.line(   8 + W_POSBASEX,  96,  27 + W_POSBASEX,  76, 7 )
			pyxel.line(  27 + W_POSBASEX,  76,  27 + W_POSBASEX,  72, 7 )
			pyxel.line(  27 + W_POSBASEX,  72,  19 + W_POSBASEX,  65, 7 )
			pyxel.line(  19 + W_POSBASEX,  65,   2 + W_POSBASEX,  24, 7 )
			pyxel.line(   2 + W_POSBASEX,  24,   2 + W_POSBASEX,  12, 7 )
			pyxel.line(   2 + W_POSBASEX,  12,   2 + W_POSBASEX,   3, 7 )
			pyxel.line(   2 + W_POSBASEX,   3,  17 + W_POSBASEX,   3, 7 )
			pyxel.line(  17 + W_POSBASEX,   3,  18 + W_POSBASEX,  11, 7 )
			pyxel.line(  18 + W_POSBASEX,  11,  20 + W_POSBASEX,  18, 7 )

			#pyxel.line(   2 + W_POSBASEX,  24,  20 + W_POSBASEX,  18, 10 )	#緑穴の蓋閉め
			#pyxel.line(  22 + W_POSBASEX,  25,  20 + W_POSBASEX,  18, 10 )	#緑穴の蓋開き

			pyxel.line(  20 + W_POSBASEX,  18,  23 + W_POSBASEX,   4, 7 )
			pyxel.line(  23 + W_POSBASEX,   4,  77 + W_POSBASEX,   4, 7 )
			pyxel.line(  77 + W_POSBASEX,   4,  80 + W_POSBASEX,  16, 7 )
			pyxel.line(  80 + W_POSBASEX,  16,  86 + W_POSBASEX,  16, 7 )
			pyxel.line(  86 + W_POSBASEX,  16, 103 + W_POSBASEX,   4, 7 )
			pyxel.line( 103 + W_POSBASEX,   4, 113 + W_POSBASEX,   4, 7 )
			pyxel.line( 113 + W_POSBASEX,   4, 125 + W_POSBASEX,   7, 7 )
			pyxel.line( 125 + W_POSBASEX,   7, 128 + W_POSBASEX,   4, 7 )
			pyxel.line( 128 + W_POSBASEX,   4, 188 + W_POSBASEX,   4, 7 )
			pyxel.line( 188 + W_POSBASEX,   4, 188 + W_POSBASEX,  19, 7 )
			pyxel.line( 188 + W_POSBASEX,  19, 184 + W_POSBASEX,  23, 7 )
			pyxel.line( 184 + W_POSBASEX,  23, 184 + W_POSBASEX,  32, 7 )
			pyxel.line( 184 + W_POSBASEX,  32, 188 + W_POSBASEX,  40, 7 )
			pyxel.line( 188 + W_POSBASEX,  40, 188 + W_POSBASEX,  88, 7 )
			pyxel.line( 188 + W_POSBASEX,  88, 188 + W_POSBASEX, 105, 7 )
			pyxel.line( 188 + W_POSBASEX, 105, 185 + W_POSBASEX, 113, 7 )
			pyxel.line( 185 + W_POSBASEX, 113, 175 + W_POSBASEX, 113, 7 )
			pyxel.line( 175 + W_POSBASEX, 113, 172 + W_POSBASEX, 105, 7 )
			pyxel.line( 172 + W_POSBASEX, 105, 172 + W_POSBASEX,  95, 7 )

			#pyxel.line( 188 + W_POSBASEX,  88, 172 + W_POSBASEX,  95, 10 )	#青穴の蓋閉め
			#pyxel.line( 172 + W_POSBASEX,  77, 172 + W_POSBASEX,  95, 10 )	#青穴の蓋開き

			pyxel.line( 172 + W_POSBASEX,  95, 159 + W_POSBASEX,  99, 7 )
			pyxel.line( 159 + W_POSBASEX,  99, 159 + W_POSBASEX, 106, 7 )
			pyxel.line( 159 + W_POSBASEX, 106, 175 + W_POSBASEX, 123, 7 )
			pyxel.line( 175 + W_POSBASEX, 123, 188 + W_POSBASEX, 132, 7 )


			pyxel.line(  17 + W_POSBASEX, 173,  17 + W_POSBASEX, 149, 7 )		#左ライン

			pyxel.line( 142 + W_POSBASEX,  85, 104 + W_POSBASEX,  43, 7 )		#右上
			pyxel.line( 104 + W_POSBASEX,  43, 104 + W_POSBASEX,  33, 7 )
			pyxel.line( 104 + W_POSBASEX,  33, 106 + W_POSBASEX,  24, 7 )
			pyxel.line( 106 + W_POSBASEX,  24, 114 + W_POSBASEX,  29, 7 )
			pyxel.line( 114 + W_POSBASEX,  29, 114 + W_POSBASEX,  47, 7 )
			pyxel.line( 114 + W_POSBASEX,  47, 136 + W_POSBASEX,  73, 7 )
			pyxel.line( 136 + W_POSBASEX,  73, 142 + W_POSBASEX,  75, 7 )
			pyxel.line( 142 + W_POSBASEX,  75, 142 + W_POSBASEX,  85, 7 )

			pyxel.line( 159 + W_POSBASEX,  82, 159 + W_POSBASEX,  72, 7 )		#右上ライン左
			pyxel.line( 172 + W_POSBASEX,  77, 172 + W_POSBASEX,  67, 7 )		#右上ライン右

			#ホールゲートの開け閉め
			if( GWK[red_switch] & B_HOLEOPEN ):
				pyxel.line(  17 + W_POSBASEX, 189,  17 + W_POSBASEX, 173, 10 )	#赤穴の蓋開き
			else:
				pyxel.line(  17 + W_POSBASEX, 189,   2 + W_POSBASEX, 180, 10 )	#赤穴の蓋閉め
			if( GWK[green_switch] & B_HOLEOPEN ):
				pyxel.line(  22 + W_POSBASEX,  25,  20 + W_POSBASEX,  18, 10 )	#緑穴の蓋開き
			else:
				pyxel.line(   2 + W_POSBASEX,  24,  20 + W_POSBASEX,  18, 10 )	#緑穴の蓋閉め
			if( GWK[blue_switch] & B_HOLEOPEN ):
				pyxel.line( 172 + W_POSBASEX,  77, 172 + W_POSBASEX,  95, 10 )	#青穴の蓋開き
			else:
				pyxel.line( 188 + W_POSBASEX,  88, 172 + W_POSBASEX,  95, 10 )	#青穴の蓋閉め

			#ホール
			x, y = self.W_hole_white_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 13 )	#白穴[2]
			x, y = self.W_hole_purple_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 2 )	#紫穴[3]
			x, y = self.W_hole_red_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 8 )	#赤穴[10]
			x, y = self.W_hole_green_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 3 )	#緑穴[20]
			x, y = self.W_hole_blue_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 12 )	#青穴[30]

			#バンパー
			x, y = self.W_bumper1_body.position
			if( GWK[bumper_switch] & B_SWITCH1 ):
				GWK[bumper_switch] &= ~B_SWITCH1
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			#小バンパー
			x, y = self.W_bumper2_body.position
			if( GWK[bumper_switch] & B_SWITCH2 ):
				GWK[bumper_switch] &= ~B_SWITCH2
				self.cput( x-7, y-7, 0x11 )
			else:
				self.cput( x-7, y-7, 0x10 )

			x, y = self.W_bumper3_body.position
			if( GWK[bumper_switch] & B_SWITCH3 ):
				GWK[bumper_switch] &= ~B_SWITCH3
				self.cput( x-7, y-7, 0x11 )
			else:
				self.cput( x-7, y-7, 0x10 )

			x, y = self.W_bumper4_body.position
			if( GWK[bumper_switch] & B_SWITCH4 ):
				GWK[bumper_switch] &= ~B_SWITCH4
				self.cput( x-7, y-7, 0x11 )
			else:
				self.cput( x-7, y-7, 0x10 )


			
			#白スイッチ
			if( GWK[white_switch] & B_HOLEOPEN ):
				self.cput( 155 + W_POSBASEX, 110, 0xf )
			else:
				self.cput( 155 + W_POSBASEX, 110, 1 )

			#緑スイッチ
			if( GWK[green_switch] & B_SWITCH1 ):
				self.cput( 23 + W_POSBASEX, 6, 4 )
			else:
				self.cput( 23 + W_POSBASEX, 6, 3 )
			if( GWK[green_switch] & B_SWITCH2 ):
				self.cput( 34 + W_POSBASEX, 6, 4 )
			else:
				self.cput( 34 + W_POSBASEX, 6, 3 )
			if( GWK[green_switch] & B_SWITCH3 ):
				self.cput( 45 + W_POSBASEX, 6, 4 )
			else:
				self.cput( 45 + W_POSBASEX, 6, 3 )
			if( GWK[green_switch] & B_SWITCH4 ):
				self.cput( 56 + W_POSBASEX, 6, 4 )
			else:
				self.cput( 56 + W_POSBASEX, 6, 3 )
			if( GWK[green_switch] & B_SWITCH5 ):
				self.cput( 67 + W_POSBASEX, 6, 4 )
			else:
				self.cput( 67 + W_POSBASEX, 6, 3 )

			#青スイッチ
			if( GWK[blue_switch] & B_SWITCH1 ):
				self.cput( 99 + W_POSBASEX, 46, 6 )
			else:
				self.cput( 99 + W_POSBASEX, 46, 5 )
			if( GWK[blue_switch] & B_SWITCH2 ):
				self.cput( 109 + W_POSBASEX, 56, 6 )
			else:
				self.cput( 109 + W_POSBASEX, 56, 5 )
			if( GWK[blue_switch] & B_SWITCH3 ):
				self.cput( 119 + W_POSBASEX, 66, 6 )
			else:
				self.cput( 119 + W_POSBASEX, 66, 5 )
			if( GWK[blue_switch] & B_SWITCH4 ):
				self.cput( 129 + W_POSBASEX, 76, 6 )
			else:
				self.cput( 129 + W_POSBASEX, 76, 5 )
			
			#赤スイッチ
			if( GWK[red_switch] & B_SWITCH1 ):
				self.cput( 14 + W_POSBASEX, 120, 8 )
			else:
				self.cput( 14 + W_POSBASEX, 120, 7 )
			if( GWK[red_switch] & B_SWITCH2 ):
				self.cput( 24 + W_POSBASEX, 110, 8 )
			else:
				self.cput( 24 + W_POSBASEX, 110, 7 )
			if( GWK[red_switch] & B_SWITCH3 ):
				self.cput( 34 + W_POSBASEX, 100, 8 )
			else:
				self.cput( 34 + W_POSBASEX, 100, 7 )

			self.cput( 147 + W_POSBASEX, 72, 0x12 )		#右上のスコアライン
			self.cput( 162 + W_POSBASEX, 67, 0x12 )
			self.cput( 175 + W_POSBASEX, 62, 0x12 )

			#矢印
			self.cput(   8 + W_POSBASEX,  25, 0x0a )	#左上
			self.cput(   6 + W_POSBASEX, 174, 0x09 )	#下
			self.cput( 176 + W_POSBASEX,  81, 0x09 )	#下
			self.cput(  25 + W_POSBASEX,  83, 0x1e )	#左下

			if( GWK[white_switch] & B_HOLEOPEN ):
				pyxel.line( 174 + W_POSBASEX, 182, 188 + W_POSBASEX, 174, 10 )	#白穴の蓋開き
			else:
				pyxel.line( 174 + W_POSBASEX, 182, 174 + W_POSBASEX, 165, 10 )	#白穴の蓋閉め

		#------------------------------------
		elif( GWK[field_number] == FIELD_RED ):

			pyxel.line( 188 + R_POSBASEX, 132, 182 + R_POSBASEX, 121, 7 )
			pyxel.line( 182 + R_POSBASEX, 121, 188 + R_POSBASEX, 106, 7 )
			pyxel.line( 188 + R_POSBASEX, 106, 180 + R_POSBASEX,  93, 7 )
			pyxel.line( 180 + R_POSBASEX,  93, 188 + R_POSBASEX,  71, 7 )
			pyxel.line( 188 + R_POSBASEX,  71, 188 + R_POSBASEX,   8, 7 )
			pyxel.line( 188 + R_POSBASEX,   8, 185 + R_POSBASEX,   4, 7 )
			pyxel.line( 185 + R_POSBASEX,   4, 178 + R_POSBASEX,   4, 7 )
			pyxel.line( 178 + R_POSBASEX,   4, 174 + R_POSBASEX,   8, 7 )
			pyxel.line( 174 + R_POSBASEX,   8, 174 + R_POSBASEX,  53, 7 )
			pyxel.line( 174 + R_POSBASEX,  53, 169 + R_POSBASEX,  67, 7 )
			pyxel.line( 169 + R_POSBASEX,  67, 169 + R_POSBASEX,  53, 7 )
			pyxel.line( 169 + R_POSBASEX,  53, 172 + R_POSBASEX,  46, 7 )
			pyxel.line( 172 + R_POSBASEX,  46, 172 + R_POSBASEX,  33, 7 )
			pyxel.line( 172 + R_POSBASEX,  33, 168 + R_POSBASEX,  18, 7 )
			pyxel.line( 168 + R_POSBASEX,  18, 163 + R_POSBASEX,   8, 7 )
			pyxel.line( 163 + R_POSBASEX,   8, 155 + R_POSBASEX,   4, 7 )
			pyxel.line( 155 + R_POSBASEX,   4,  32 + R_POSBASEX,   4, 7 )
			pyxel.line(  32 + R_POSBASEX,   4,  18 + R_POSBASEX,  10, 7 )
			pyxel.line(  18 + R_POSBASEX,  10,   6 + R_POSBASEX,  23, 7 )
			pyxel.line(   6 + R_POSBASEX,  23,   2 + R_POSBASEX,  38, 7 )
			pyxel.line(   2 + R_POSBASEX,  38,   2 + R_POSBASEX, 106, 7 )
			pyxel.line(   2 + R_POSBASEX, 106,   4 + R_POSBASEX, 110, 7 )
			pyxel.line(   4 + R_POSBASEX, 110,  12 + R_POSBASEX, 110, 7 )
			pyxel.line(  12 + R_POSBASEX, 110,  17 + R_POSBASEX, 106, 7 )
			pyxel.line(  17 + R_POSBASEX, 106,  17 + R_POSBASEX,  74, 7 )
			pyxel.line(  17 + R_POSBASEX,  74,  25 + R_POSBASEX,  92, 7 )
			pyxel.line(  25 + R_POSBASEX,  92,   2 + R_POSBASEX, 136, 7 )
			pyxel.line(   2 + R_POSBASEX, 136,   2 + R_POSBASEX, 180, 7 )

			#pyxel.line(  17 + R_POSBASEX, 189,   2 + R_POSBASEX, 180, 7 )	#赤穴の蓋閉め
			#pyxel.line(  17 + R_POSBASEX, 189,  17 + R_POSBASEX, 173, 7 )	#赤穴の蓋開き

			pyxel.line(  62 + R_POSBASEX, 216,  17 + R_POSBASEX, 189, 7 )
			pyxel.line(  17 + R_POSBASEX, 189,  17 + R_POSBASEX, 204, 7 )
			pyxel.line(  17 + R_POSBASEX, 204,  14 + R_POSBASEX, 207, 7 )
			pyxel.line(  14 + R_POSBASEX, 207,   8 + R_POSBASEX, 208, 7 )
			pyxel.line(   8 + R_POSBASEX, 208,   3 + R_POSBASEX, 205, 7 )
			pyxel.line(   3 + R_POSBASEX, 205,   2 + R_POSBASEX, 202, 7 )
			pyxel.line(   2 + R_POSBASEX, 202,   2 + R_POSBASEX, 180, 7 )

			pyxel.line(  41 + R_POSBASEX,  82,  30 + R_POSBASEX,  65, 7 )
			pyxel.line(  30 + R_POSBASEX,  65,  30 + R_POSBASEX,  57, 7 )
			pyxel.line(  30 + R_POSBASEX,  57,  36 + R_POSBASEX,  57, 7 )
			pyxel.line(  36 + R_POSBASEX,  57,  36 + R_POSBASEX,  65, 7 )
			pyxel.line(  36 + R_POSBASEX,  65,  45 + R_POSBASEX,  77, 7 )
			pyxel.line(  45 + R_POSBASEX,  77,  41 + R_POSBASEX,  82, 7 )

			pyxel.line(  65 + R_POSBASEX,  24,  69 + R_POSBASEX,  24, 7 )
			pyxel.line(  69 + R_POSBASEX,  24,  76 + R_POSBASEX,  40, 7 )
			pyxel.line(  76 + R_POSBASEX,  40,  76 + R_POSBASEX,  50, 7 )
			pyxel.line(  76 + R_POSBASEX,  50,  68 + R_POSBASEX,  57, 7 )
			pyxel.line(  68 + R_POSBASEX,  57,  64 + R_POSBASEX,  49, 7 )
			pyxel.line(  64 + R_POSBASEX,  49,  65 + R_POSBASEX,  24, 7 )

			pyxel.line( 123 + R_POSBASEX,  43, 123 + R_POSBASEX,  33, 7 )
			pyxel.line( 123 + R_POSBASEX,  33, 128 + R_POSBASEX,  23, 7 )
			pyxel.line( 128 + R_POSBASEX,  23, 147 + R_POSBASEX,  19, 7 )
			pyxel.line( 147 + R_POSBASEX,  19, 153 + R_POSBASEX,  22, 7 )
			pyxel.line( 153 + R_POSBASEX,  22, 156 + R_POSBASEX,  29, 7 )
			pyxel.line( 156 + R_POSBASEX,  29, 156 + R_POSBASEX,  40, 7 )
			pyxel.line( 156 + R_POSBASEX,  40, 152 + R_POSBASEX,  46, 7 )
			pyxel.line( 152 + R_POSBASEX,  46, 146 + R_POSBASEX,  53, 7 )
			pyxel.line( 146 + R_POSBASEX,  53, 135 + R_POSBASEX,  43, 7 )
			pyxel.line( 135 + R_POSBASEX,  43, 123 + R_POSBASEX,  43, 7 )

			pyxel.line(  93 + R_POSBASEX,  40,  93 + R_POSBASEX,  50, 7 )	#上ライン
			pyxel.line( 107 + R_POSBASEX,  37, 107 + R_POSBASEX,  47, 7 )

			pyxel.line(  17 + R_POSBASEX, 173,  17 + R_POSBASEX, 149, 7 )	#左ライン

			self.cput( 81 + R_POSBASEX, 38, 0x12 )		#上のスコアライン
			self.cput( 96 + R_POSBASEX, 35, 0x12 )
			self.cput( 110 + R_POSBASEX, 32, 0x12 )

			#白スイッチ
			if( GWK[R_white_switch] & B_HOLEOPEN ):
				self.cput( 176 + R_POSBASEX, 97, 0xf )
			else:
				self.cput( 176 + R_POSBASEX, 97, 1 )

			#ホール
			x, y = self.R_hole_white_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 13 )	#白穴[1]
			x, y = self.R_hole_white2_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 13 )	#白穴[2]
			x, y = self.R_hole_red_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 8 )	#赤穴

			#バンパー
			x, y = self.R_bumper1_body.position
			if( GWK[R_bumper_switch] & B_SWITCH1 ):
				GWK[R_bumper_switch] &= ~B_SWITCH1
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			x, y = self.R_bumper2_body.position
			if( GWK[R_bumper_switch] & B_SWITCH2 ):
				GWK[R_bumper_switch] &= ~B_SWITCH2
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			x, y = self.R_bumper3_body.position
			if( GWK[R_bumper_switch] & B_SWITCH3 ):
				GWK[R_bumper_switch] &= ~B_SWITCH3
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			#ホールゲートの開け閉め
			if( GWK[R_red_switch] & B_HOLEOPEN ):
				pyxel.line(  17 + R_POSBASEX, 189,  17 + R_POSBASEX, 173, 10 )	#赤穴の蓋開き
			else:
				pyxel.line(  17 + R_POSBASEX, 189,   2 + R_POSBASEX, 180, 10 )	#赤穴の蓋閉め

			if( GWK[R_white_switch] & B_HOLEOPEN ):
				pyxel.line( 174 + R_POSBASEX, 182, 188 + R_POSBASEX, 174, 10 )	#白穴の蓋開き
			else:
				pyxel.line( 174 + R_POSBASEX, 182, 174 + R_POSBASEX, 165, 10 )	#白穴の蓋閉め

			#矢印
			self.cput( 177 + R_POSBASEX,  26, 0x0a )	#上（白穴1）
			self.cput(   6 + R_POSBASEX,  82, 0x09 )	#下（白穴2）

		#------------------------------------
		elif( GWK[field_number] == FIELD_GREEN ):
			pyxel.line( 188 + G_POSBASEX, 132, 185 + G_POSBASEX, 130, 7 )
			pyxel.line( 185 + G_POSBASEX, 130, 188 + G_POSBASEX, 125, 7 )
			pyxel.line( 188 + G_POSBASEX, 125, 188 + G_POSBASEX,  84, 7 )
			pyxel.line( 188 + G_POSBASEX,  84, 181 + G_POSBASEX,  74, 7 )
			pyxel.line( 181 + G_POSBASEX,  74, 188 + G_POSBASEX,  54, 7 )
			pyxel.line( 188 + G_POSBASEX,  54, 188 + G_POSBASEX,   8, 7 )
			pyxel.line( 188 + G_POSBASEX,   8, 185 + G_POSBASEX,   4, 7 )
			pyxel.line( 185 + G_POSBASEX,   4, 178 + G_POSBASEX,   4, 7 )
			pyxel.line( 178 + G_POSBASEX,   4, 173 + G_POSBASEX,   8, 7 )
			pyxel.line( 173 + G_POSBASEX,   8, 173 + G_POSBASEX,  49, 7 )
			pyxel.line( 173 + G_POSBASEX,  49, 168 + G_POSBASEX,  59, 7 )
			pyxel.line( 168 + G_POSBASEX,  59, 164 + G_POSBASEX,  54, 7 )
			pyxel.line( 164 + G_POSBASEX,  54, 169 + G_POSBASEX,  41, 7 )
			pyxel.line( 169 + G_POSBASEX,  41, 169 + G_POSBASEX,  23, 7 )
			pyxel.line( 169 + G_POSBASEX,  23, 165 + G_POSBASEX,  13, 7 )
			pyxel.line( 165 + G_POSBASEX,  13, 158 + G_POSBASEX,   6, 7 )
			pyxel.line( 158 + G_POSBASEX,   6, 148 + G_POSBASEX,   4, 7 )
			pyxel.line( 148 + G_POSBASEX,   4,  28 + G_POSBASEX,   4, 7 )
			pyxel.line(  28 + G_POSBASEX,   4,  17 + G_POSBASEX,   4, 7 )
			pyxel.line(  17 + G_POSBASEX,   4,   8 + G_POSBASEX,   4, 7 )
			pyxel.line(   8 + G_POSBASEX,   4,   2 + G_POSBASEX,   9, 7 )
			pyxel.line(   2 + G_POSBASEX,   9,   2 + G_POSBASEX,  85, 7 )
			pyxel.line(   2 + G_POSBASEX,  85,   6 + G_POSBASEX, 100, 7 )
			pyxel.line(   6 + G_POSBASEX, 100,  13 + G_POSBASEX, 109, 7 )
			pyxel.line(  13 + G_POSBASEX, 109,  13 + G_POSBASEX, 122, 7 )
			pyxel.line(  13 + G_POSBASEX, 122,   6 + G_POSBASEX, 127, 7 )
			pyxel.line(   6 + G_POSBASEX, 127,   2 + G_POSBASEX, 136, 7 )
			pyxel.line(   2 + G_POSBASEX, 136,   2 + G_POSBASEX, 180, 7 )
			pyxel.line(   2 + G_POSBASEX, 180,  62 + G_POSBASEX, 216, 7 )

			pyxel.line( 173 + G_POSBASEX,  95, 173 + G_POSBASEX, 113, 7 )

			pyxel.line(  16 + G_POSBASEX,  22,  24 + G_POSBASEX,  22, 7 )
			pyxel.line(  24 + G_POSBASEX,  22,  19 + G_POSBASEX,  37, 7 )
			pyxel.line(  19 + G_POSBASEX,  37,  19 + G_POSBASEX,  67, 7 )
			pyxel.line(  19 + G_POSBASEX,  67,  25 + G_POSBASEX,  85, 7 )
			pyxel.line(  25 + G_POSBASEX,  85,  24 + G_POSBASEX,  87, 7 )
			pyxel.line(  24 + G_POSBASEX,  87,  19 + G_POSBASEX,  83, 7 )
			pyxel.line(  19 + G_POSBASEX,  83,  16 + G_POSBASEX,  77, 7 )
			pyxel.line(  16 + G_POSBASEX,  77,  16 + G_POSBASEX,  22, 7 )

			pyxel.line(  33 + G_POSBASEX,  38,  35 + G_POSBASEX,  33, 7 )
			pyxel.line(  35 + G_POSBASEX,  33,  42 + G_POSBASEX,  40, 7 )
			pyxel.line(  42 + G_POSBASEX,  40,  42 + G_POSBASEX,  56, 7 )
			pyxel.line(  42 + G_POSBASEX,  56,  77 + G_POSBASEX,  77, 7 )
			pyxel.line(  77 + G_POSBASEX,  77,  81 + G_POSBASEX,  87, 7 )
			pyxel.line(  81 + G_POSBASEX,  87,  79 + G_POSBASEX,  88, 7 )
			pyxel.line(  79 + G_POSBASEX,  88,  73 + G_POSBASEX,  82, 7 )
			pyxel.line(  73 + G_POSBASEX,  82,  58 + G_POSBASEX,  82, 7 )
			pyxel.line(  58 + G_POSBASEX,  82,  51 + G_POSBASEX,  87, 7 )
			pyxel.line(  51 + G_POSBASEX,  87,  42 + G_POSBASEX,  83, 7 )
			pyxel.line(  42 + G_POSBASEX,  83,  33 + G_POSBASEX,  68, 7 )
			pyxel.line(  33 + G_POSBASEX,  68,  33 + G_POSBASEX,  38, 7 )

			pyxel.line(  87 + G_POSBASEX,  33,  99 + G_POSBASEX,  19, 7 )
			pyxel.line(  99 + G_POSBASEX,  19, 102 + G_POSBASEX,  31, 7 )
			pyxel.line( 102 + G_POSBASEX,  31,  95 + G_POSBASEX,  47, 7 )
			pyxel.line(  95 + G_POSBASEX,  47,  87 + G_POSBASEX,  47, 7 )
			pyxel.line(  87 + G_POSBASEX,  47,  87 + G_POSBASEX,  33, 7 )

			pyxel.line(  57 + G_POSBASEX,  38,  57 + G_POSBASEX,  48, 7 )		#上のライン
			pyxel.line(  73 + G_POSBASEX,  35,  73 + G_POSBASEX,  45, 7 )

			pyxel.line(  17 + G_POSBASEX, 173,  17 + G_POSBASEX, 149, 7 )	#左ライン

			self.cput( 45 + G_POSBASEX, 38, 0x12 )		#上のスコアライン
			self.cput( 61 + G_POSBASEX, 35, 0x12 )
			self.cput( 77 + G_POSBASEX, 32, 0x12 )

			self.cput( 177 + G_POSBASEX, 95, 0x12 )		#右端のスコアライン

			#バンパー
			x, y = self.G_bumper1_body.position
			if( GWK[G_bumper_switch] & B_SWITCH1 ):
				GWK[G_bumper_switch] &= ~B_SWITCH1
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			x, y = self.G_bumper2_body.position
			if( GWK[G_bumper_switch] & B_SWITCH2 ):
				GWK[G_bumper_switch] &= ~B_SWITCH2
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			#白スイッチ
			if( GWK[G_white_switch] & B_HOLEOPEN ):
				self.cput( 58 + G_POSBASEX, 79, 0x21 )
			else:
				self.cput( 58 + G_POSBASEX, 79, 0x20 )

			#ホール
			x, y = self.G_hole_white_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 13 )	#白穴
			x, y = self.G_hole_green_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 3 )	#緑穴[20]

			if( GWK[G_white_switch] & B_HOLEOPEN ):
				pyxel.line( 174 + G_POSBASEX, 182, 188 + G_POSBASEX, 174, 10 )	#白穴の蓋開き
			else:
				pyxel.line( 174 + G_POSBASEX, 182, 174 + G_POSBASEX, 165, 10 )	#白穴の蓋閉め

			#矢印
			self.cput( 176 + G_POSBASEX,  26, 0x0a )	#上（白穴）

		#------------------------------------
		elif( GWK[field_number] == FIELD_BLUE ):
			pyxel.line(  62 + B_POSBASEX, 216,   2 + B_POSBASEX, 180, 7 )
			pyxel.line(   2 + B_POSBASEX, 180,   2 + B_POSBASEX, 136, 7 )
			pyxel.line(   2 + B_POSBASEX, 136,   8 + B_POSBASEX, 124, 7 )
			pyxel.line(   8 + B_POSBASEX, 124,   3 + B_POSBASEX, 117, 7 )
			pyxel.line(   3 + B_POSBASEX, 117,  25 + B_POSBASEX,  77, 7 )
			pyxel.line(  25 + B_POSBASEX,  77,   6 + B_POSBASEX,  36, 7 )
			pyxel.line(   6 + B_POSBASEX,  36,   4 + B_POSBASEX,  25, 7 )
			pyxel.line(   4 + B_POSBASEX,  25,   4 + B_POSBASEX,  16, 7 )
			pyxel.line(   4 + B_POSBASEX,  16,  13 + B_POSBASEX,   9, 7 )
			pyxel.line(  13 + B_POSBASEX,   9,  24 + B_POSBASEX,   4, 7 )
			pyxel.line(  24 + B_POSBASEX,   4,  44 + B_POSBASEX,   4, 7 )
			pyxel.line(  44 + B_POSBASEX,   4,  75 + B_POSBASEX,  12, 7 )
			pyxel.line(  75 + B_POSBASEX,  12,  83 + B_POSBASEX,   4, 7 )
			pyxel.line(  83 + B_POSBASEX,   4, 137 + B_POSBASEX,   4, 7 )
			pyxel.line( 137 + B_POSBASEX,   4, 146 + B_POSBASEX,   5, 7 )
			pyxel.line( 146 + B_POSBASEX,   5, 157 + B_POSBASEX,   8, 7 )
			pyxel.line( 157 + B_POSBASEX,   8, 165 + B_POSBASEX,  16, 7 )
			pyxel.line( 165 + B_POSBASEX,  16, 172 + B_POSBASEX,  28, 7 )
			pyxel.line( 172 + B_POSBASEX,  28, 173 + B_POSBASEX,  26, 7 )
			pyxel.line( 173 + B_POSBASEX,  26, 173 + B_POSBASEX,   8, 7 )
			pyxel.line( 173 + B_POSBASEX,   8, 178 + B_POSBASEX,   4, 7 )
			pyxel.line( 178 + B_POSBASEX,   4, 186 + B_POSBASEX,   4, 7 )
			pyxel.line( 186 + B_POSBASEX,   4, 188 + B_POSBASEX,   8, 7 )
			pyxel.line( 188 + B_POSBASEX,   8, 188 + B_POSBASEX,  30, 7 )
			pyxel.line( 188 + B_POSBASEX,  30, 180 + B_POSBASEX,  49, 7 )
			pyxel.line( 180 + B_POSBASEX,  49, 188 + B_POSBASEX,  85, 7 )
			pyxel.line( 188 + B_POSBASEX,  85, 188 + B_POSBASEX, 108, 7 )
			pyxel.line( 188 + B_POSBASEX, 108, 180 + B_POSBASEX, 120, 7 )
			pyxel.line( 180 + B_POSBASEX, 120, 186 + B_POSBASEX, 125, 7 )
			pyxel.line( 186 + B_POSBASEX, 125, 188 + B_POSBASEX, 132, 7 )

			pyxel.line(  41 + B_POSBASEX,  71,  74 + B_POSBASEX,  52, 7 )
			pyxel.line(  74 + B_POSBASEX,  52,  74 + B_POSBASEX,  34, 7 )
			pyxel.line(  74 + B_POSBASEX,  34,  60 + B_POSBASEX,  37, 7 )
			pyxel.line(  60 + B_POSBASEX,  37,  59 + B_POSBASEX,  48, 7 )
			pyxel.line(  59 + B_POSBASEX,  48,  54 + B_POSBASEX,  53, 7 )
			pyxel.line(  54 + B_POSBASEX,  53,  36 + B_POSBASEX,  59, 7 )
			pyxel.line(  36 + B_POSBASEX,  59,  41 + B_POSBASEX,  71, 7 )

			pyxel.line(  94 + B_POSBASEX,  63, 128 + B_POSBASEX,  89, 7 )
			pyxel.line( 128 + B_POSBASEX,  89, 128 + B_POSBASEX,  73, 7 )
			pyxel.line( 128 + B_POSBASEX,  73, 106 + B_POSBASEX,  66, 7 )
			pyxel.line( 106 + B_POSBASEX,  66,  94 + B_POSBASEX,  58, 7 )
			pyxel.line(  94 + B_POSBASEX,  58,  94 + B_POSBASEX,  63, 7 )

			pyxel.line( 149 + B_POSBASEX,  25, 149 + B_POSBASEX,  55, 7 )
			pyxel.line( 149 + B_POSBASEX,  55, 145 + B_POSBASEX,  59, 7 )
			pyxel.line( 145 + B_POSBASEX,  59, 145 + B_POSBASEX,  66, 7 )
			pyxel.line( 145 + B_POSBASEX,  66, 152 + B_POSBASEX,  69, 7 )
			pyxel.line( 152 + B_POSBASEX,  69, 161 + B_POSBASEX,  51, 7 )
			pyxel.line( 161 + B_POSBASEX,  51, 161 + B_POSBASEX,  45, 7 )
			pyxel.line( 161 + B_POSBASEX,  45, 160 + B_POSBASEX,  37, 7 )
			pyxel.line( 160 + B_POSBASEX,  37, 149 + B_POSBASEX,  25, 7 )

			pyxel.line( 170 + B_POSBASEX,  70, 159 + B_POSBASEX,  91, 7 )
			pyxel.line( 159 + B_POSBASEX,  91, 170 + B_POSBASEX, 108, 7 )
			pyxel.line( 170 + B_POSBASEX, 108, 173 + B_POSBASEX, 102, 7 )
			pyxel.line( 173 + B_POSBASEX, 102, 173 + B_POSBASEX,  87, 7 )
			pyxel.line( 173 + B_POSBASEX,  87, 170 + B_POSBASEX,  70, 7 )

			pyxel.line(  28 + B_POSBASEX,  28,  28 + B_POSBASEX,  39, 7 )		#左上のライン
			pyxel.line(  44 + B_POSBASEX,  32,  44 + B_POSBASEX,  43, 7 )

			pyxel.line(  17 + B_POSBASEX, 173,  17 + B_POSBASEX, 149, 7 )	#左ライン

			self.cput( 32 + B_POSBASEX, 28, 0x12 )		#左上のライン
			self.cput( 47 + B_POSBASEX, 32, 0x12 )

			#白スイッチ
			if( GWK[B_white_switch] & B_HOLEOPEN ):
				self.cput( 154 + B_POSBASEX, 95, 0xf )
			else:
				self.cput( 154 + B_POSBASEX, 95, 1 )

			#ホール
			x, y = self.B_hole_white_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 13 )	#白穴
			x, y = self.B_hole_blue_body.position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 12 )	#青穴

			#バンパー
			x, y = self.B_bumper1_body.position
			if( GWK[B_bumper_switch] & B_SWITCH1 ):
				GWK[B_bumper_switch] &= ~B_SWITCH1
				self.cput( x-15, y-15, 0xe )
			else:
				self.cput( x-15, y-15, 0 )

			if( GWK[B_white_switch] & B_HOLEOPEN ):
				pyxel.line( 174 + B_POSBASEX, 182, 188 + B_POSBASEX, 174, 10 )	#白穴の蓋開き
			else:
				pyxel.line( 174 + B_POSBASEX, 182, 174 + B_POSBASEX, 165, 10 )	#白穴の蓋閉め


			#黄スイッチ
			if( GWK[B_yellow_switch] & B_YSWITCH1 ):
				self.cput( 94 + B_POSBASEX, 68, 0x19 )
			else:
				self.cput( 94 + B_POSBASEX, 68, 0x18 )
			if( GWK[B_yellow_switch] & B_YSWITCH2 ):
				self.cput( 104 + B_POSBASEX, 76, 0x19 )
			else:
				self.cput( 104 + B_POSBASEX, 76, 0x18 )
			if( GWK[B_yellow_switch] & B_YSWITCH3 ):
				self.cput( 114 + B_POSBASEX, 83, 0x19 )
			else:
				self.cput( 114 + B_POSBASEX, 83, 0x18 )

			if( GWK[B_yellow_switch] & B_YSWITCH4 ):
				self.cput( 44 + B_POSBASEX, 68, 0x1b )
			else:
				self.cput( 44 + B_POSBASEX, 68, 0x1a )
			if( GWK[B_yellow_switch] & B_YSWITCH5 ):
				self.cput( 54 + B_POSBASEX, 62, 0x1b )
			else:
				self.cput( 54 + B_POSBASEX, 62, 0x1a )
			if( GWK[B_yellow_switch] & B_YSWITCH6 ):
				self.cput( 64 + B_POSBASEX, 56, 0x1b )
			else:
				self.cput( 64 + B_POSBASEX, 56, 0x1a )

			if( GWK[B_yellow_switch] & B_YSWITCH9 ):
				self.cput( 21 + B_POSBASEX, 80, 0x1b )
			else:
				self.cput( 21 + B_POSBASEX, 80, 0x1a )
			if( GWK[B_yellow_switch] & B_YSWITCH8 ):
				self.cput( 15 + B_POSBASEX, 93, 0x1b )
			else:
				self.cput( 15 + B_POSBASEX, 93, 0x1a )
			if( GWK[B_yellow_switch] & B_YSWITCH7 ):
				self.cput( 8 + B_POSBASEX, 105, 0x1b )
			else:
				self.cput( 8 + B_POSBASEX, 105, 0x1a )

			x, y = self.B_shaft1_body.position
			self.cput( x-2, y-2, 0x15 )
			x, y = self.B_shaft2_body.position
			self.cput( x-2, y-2, 0x15 )

			#矢印
			self.cput( 176 + B_POSBASEX,  26, 0x0a )	#上（白穴）

		#-----------------------------------------------------------------------
		#ステージ共通
		#共通オブジェクト用オフセット
		if( GWK[field_number] == FIELD_WHITE ):
			ofs = W_POSBASEX
		elif( GWK[field_number] == FIELD_RED ):
			ofs = R_POSBASEX
		elif( GWK[field_number] == FIELD_GREEN ):
			ofs = G_POSBASEX
		elif( GWK[field_number] == FIELD_BLUE ):
			ofs = B_POSBASEX

		#外壁
		pyxel.line(  88 + ofs, 255,  88 + ofs, 251, 7 )		#左フリッパーライン
		pyxel.line(  88 + ofs, 251,  62 + ofs, 241, 7 )
		pyxel.line(  62 + ofs, 241,  62 + ofs, 216, 7 )

		pyxel.line( 133 + ofs, 214, 174 + ofs, 188, 7 )		#右フリッパーライン
		pyxel.line( 174 + ofs, 188, 174 + ofs, 182, 7 )
		#pyxel.line( 174 + ofs, 182, 174 + ofs, 165, 10 )	#白スイッチの蓋閉め
		#pyxel.line( 174 + ofs, 182, 188 + ofs, 174, 10 )	#白スイッチの蓋開き
		pyxel.line( 174 + ofs, 165, 174 + ofs, 149, 7 )

		pyxel.line( 188 + ofs, 132, 188 + ofs, 204, 7 )		#右外枠
		pyxel.line( 188 + ofs, 204, 104 + ofs, 251, 7 )
		pyxel.line( 104 + ofs, 251, 104 + ofs, 255, 7 )		#外枠終点

		pyxel.line( 137 + ofs, 190, 159 + ofs, 148, 9 )		#右三角
		pyxel.line( 159 + ofs, 148, 159 + ofs, 180, 7 )
		pyxel.line( 159 + ofs, 180, 137 + ofs, 190, 7 )

		pyxel.line(  32 + ofs, 148,  53 + ofs, 190, 9 )		#左三角
		pyxel.line(  53 + ofs, 190,  32 + ofs, 180, 7 )
		pyxel.line(  32 + ofs, 180,  32 + ofs, 148, 7 )

		#縦スコア
		#self.cput( 5 + ofs, 150, 0xd )		#1000
		self.cput( 5 + ofs, 150, 0x12 )		#1000
		#self.cput( 20 + ofs, 150, 0xb )	#500
		self.cput( 20 + ofs, 150, 0x12 )	#500
		#self.cput( 163 + ofs, 150, 0xb )	#500
		self.cput( 163 + ofs, 150, 0x12 )	#500
		#self.cput( 177 + ofs, 150, 0xc )	#1000
		self.cput( 177 + ofs, 150, 0x12 )	#1000



		#フリッパー（形状は三角形（fp））
		#----------------------------
		if( GWK[field_number] == FIELD_WHITE ):
			#支点
			self.W_r_flipper_body.position = 130, 218
			self.W_l_flipper_body.position = 65, 218
			self.W_r_flipper_body.velocity = self.W_l_flipper_body.velocity = 0, 0

			_x = [0,0,0]
			_y = [0,0,0]

			_cnt = 0
			for v in self.W_r_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.W_r_flipper_shape.body.angle) + self.W_r_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

			_cnt = 0
			for v in self.W_l_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.W_l_flipper_shape.body.angle) + self.W_l_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

		#----------------------------
		elif( GWK[field_number] == FIELD_RED ):
			#支点
			self.R_r_flipper_body.position = 130 + R_POSBASEX, 218
			self.R_l_flipper_body.position = 65 + R_POSBASEX, 218
			self.R_r_flipper_body.velocity = self.R_l_flipper_body.velocity = 0, 0

			_x = [0,0,0]
			_y = [0,0,0]

			_cnt = 0
			for v in self.R_r_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.R_r_flipper_shape.body.angle) + self.R_r_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

			_cnt = 0
			for v in self.R_l_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.R_l_flipper_shape.body.angle) + self.R_l_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

		#----------------------------
		elif( GWK[field_number] == FIELD_GREEN ):
			#支点
			self.G_r_flipper_body.position = 130 + G_POSBASEX, 218
			self.G_l_flipper_body.position = 65 + G_POSBASEX, 218
			self.G_r_flipper_body.velocity = self.G_l_flipper_body.velocity = 0, 0

			_x = [0,0,0]
			_y = [0,0,0]

			_cnt = 0
			for v in self.G_r_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.G_r_flipper_shape.body.angle) + self.G_r_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

			_cnt = 0
			for v in self.G_l_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.G_l_flipper_shape.body.angle) + self.G_l_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

		#----------------------------
		elif( GWK[field_number] == FIELD_BLUE ):
			#支点
			self.B_r_flipper_body.position = 130 + B_POSBASEX, 218
			self.B_l_flipper_body.position = 65 + B_POSBASEX, 218
			self.B_r_flipper_body.velocity = self.B_l_flipper_body.velocity = 0, 0

			_x = [0,0,0]
			_y = [0,0,0]

			_cnt = 0
			for v in self.B_r_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.B_r_flipper_shape.body.angle) + self.B_r_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

			_cnt = 0
			for v in self.B_l_flipper_shape.get_vertices():
				_x[_cnt],_y[_cnt] = v.rotated(self.B_l_flipper_shape.body.angle) + self.B_l_flipper_shape.body.position
				_cnt += 1
			pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)


		if( ( GWK[game_adv] == G_FIELD_CHANGE ) and
			( ( GWK[game_subadv] >= GS_BALL_SMALL ) and ( GWK[game_subadv] < GS_WAIT6 ) ) ):
			if( GWK[game_subadv] == GS_BALLIN ):

				if( GWK[field_number] == FIELD_WHITE ):
					ofs = W_POSBASEX
				elif( GWK[field_number] == FIELD_RED ):
					ofs = R_POSBASEX
				elif( GWK[field_number] == FIELD_GREEN ):
					ofs = G_POSBASEX
				elif( GWK[field_number] == FIELD_BLUE ):
					ofs = B_POSBASEX

				x, y = self.ball_body.position
				for _cnt in range(len(ballin_postbl)//2):
					fx = ballin_postbl[_cnt * 2 + 0] + ofs
					fy = ballin_postbl[_cnt * 2 + 1]
					x2 = x - ( ( x - fx ) * GWK[wait_counter] / BALLIN_ANIMMAX )
					y2 = y - ( ( y - fy ) * GWK[wait_counter] / BALLIN_ANIMMAX )
					pyxel.circ( x2, y2, 1, 7 )
					
			else:
				x, y = self.ball_body.position
				r = BALL_RADIUS * GWK[zoom_counter] / BALL_ZOOMMAX
				pyxel.circ( x, y, r, 14 )

		else:
			#残像
			for _cnt in range(BALLPOS_SAVEMAX):
				x = GWK[ballpos_save + (_cnt * 2) + 0]
				y = GWK[ballpos_save + (_cnt * 2) + 1]
				pyxel.circ( x, y, BALL_RADIUS, 13 )

			#ボール
			x, y = self.ball_body.position
			pyxel.circ( x, y, BALL_RADIUS, 14 )

		if( GWK[ball_switch] & 0x01 ):
			pyxel.text( (SCREEN_WIDTH//2 - (4*28//2))+ofs , SCREEN_HEIGHT//2, 'Z-KEY OR A-BUTTON PUSH START', 7 )

	#-----------------------------------------------------------------
	#入力（キーボード＆ジョイパッド）
	#-----------------------------------------------------------------
	#上
	def getInputUP(self):
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
			return 1
		else:
			return 0
	#下
	def getInputDOWN(self):
		if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
			return 1
		else:
			return 0
	#左
	def getInputLEFT(self):
		if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
			return 1
		else:
			return 0
	#右
	def getInputRIGHT(self):
		if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
			return 1
		else:
			return 0
	#button-A（決定）
	def getInputA(self):
		if pyxel.btnp(pyxel.KEY_Z, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold=10, repeat=10):
			return 1
		else:
			return 0
	#button-B（キャンセル）
	def getInputB(self):
		if pyxel.btnp(pyxel.KEY_X, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold=10, repeat=10):
			return 1
		else:
			return 0


if __name__ == "__main__":
	import pymunk

	FPS = 60
	App(pymunk, FPS)
