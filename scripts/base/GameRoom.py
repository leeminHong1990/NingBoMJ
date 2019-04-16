# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import time
from datetime import datetime
from interfaces.GameObject import GameObject
from entitymembers.iRoomRules import iRoomRules
from entitymembers.PlayerProxy import PlayerProxy
import json
import const
import random
import switch
import utility

class GameRoom(KBEngine.Base, GameObject, iRoomRules):
	"""
	这是一个游戏房间/桌子类
	该类处理维护一个房间中的实际游戏， 例如：斗地主、麻将等
	该房间中记录了房间里所有玩家的mailbox，通过mailbox我们可以将信息推送到他们的客户端。
	"""
	def __init__(self):
		GameObject.__init__(self)
		iRoomRules.__init__(self)

		self.owner_uid = 0
		self.agent = None
		self.roomID = None

		# 状态0：未开始游戏， 1：某一局游戏中
		self.state = 0

		# 存放该房间内的玩家mailbox
		self.players_dict = {}
		self.players_list = [None] * self.player_num
		self.origin_players_list = [None] * const.ROOM_PLAYER_NUMBER

		# 庄家index
		self.dealer_idx = 0
		# 当前控牌的玩家index
		self.current_idx = 0
		# 对当前打出的牌可以进行操作的玩家的index, 服务端会限时等待他的操作
		self.wait_idx_list = []
		self.wait_op = None
		# 房间基础轮询timer
		self._poll_timer = None
		# 玩家操作限时timer
		self._op_timer = None
		# 一局游戏结束后, 玩家准备界面等待玩家确认timer
		self._next_game_timer = None

		#财神(多个)
		self.kingTiles = []
		#圈风
		self.prevailing_wind = const.WIND_EAST
		#玩家坐庄状态,所有玩家做过庄换圈风 0-没做过庄 1-做过庄
		self.player_dealer_state = [0] * self.player_num

		self.current_round = 0
		self.all_discard_tiles = []
		# 最后一位出牌的玩家
		self.last_player_idx = -1
		# 房间开局所有操作的记录(aid, src, des, tile)
		self.op_record = []
		# 确认继续的玩家
		self.confirm_next_idx = []

		# 解散房间操作的发起者
		self.dismiss_room_from = -1
		# 解散房间操作开始的时间戳
		self.dismiss_room_ts = 0
		# 解散房间操作投票状态
		self.dismiss_room_state_list = [0] * self.player_num
		self.dismiss_timer = None
		# 等待玩家确认胡的dict
		self.wait_for_win_dict = {} # waitIdx:{"state": 0, "formIdx": idx, "win_op":aid, "quantity":4, "result":[]}


		# 等待确认放弃玩家列表
		self.wait_give_up_list = []
		# 放弃玩家列表
		self.give_up_list = []
		# 本局轮询放弃的操作
		self.polling_give_up_op = -1

		# self.addTimer(const.ROOM_EXIST_TIME, 0, const.TIMER_TYPE_ROOM_EXIST)
		self.roomOpenTime = time.time()

	@property
	def isFull(self):
		count = sum([1 for i in self.players_list if i is not None])
		return count == self.player_num

	@property
	def isEmpty(self):
		count = sum([1 for i in self.players_list if i is not None])
		return count == 0 and self.agent is None

	@property
	def nextIdx(self):
		tryNext = (self.current_idx + 1) % self.player_num
		for j in range(2):
			for i in range(self.player_num):
				if self.player_num > tryNext and self.players_list[tryNext] not in self.give_up_list:
					return tryNext
				tryNext = (tryNext + 1) % self.player_num
		return (self.current_idx + 1) % self.player_num

	def getSit(self):
		for i, j in enumerate(self.players_list):
			if j is None:
				return i

	def _reset(self):
		self.state = 0
		self.agent = None
		self.players_list = [None] * self.player_num
		self.dealer_idx = 0
		self.current_idx = 0
		self._poll_timer = None
		self._op_timer = None
		self._next_game_timer = None
		self.all_discard_tiles = []
		self.kingTiles = []
		self.current_round = 0
		self.confirm_next_idx = []
		self.prevailing_wind = const.WIND_EAST
		self.dismiss_timer = None
		self.dismiss_room_ts = 0
		self.dismiss_room_state_list = [0, 0, 0, 0]
		self.wait_give_up_list = []
		self.give_up_list = []
		self.polling_give_up_op = -1
		KBEngine.globalData["GameWorld"].delRoom(self)

	def throwTheDice(self, idxList):
		if self.player_num == 3:
			diceList = [[0, 0], [0, 0], [0, 0]]
		else:
			diceList = [[0, 0], [0, 0], [0, 0], [0, 0]]
		for idx in idxList:
			for i in range(0,2):
				diceNum = random.randint(1, 6)
				diceList[idx][i] = diceNum
		return diceList

	def getMaxDiceIdx(self, diceList):
		numList = []
		for i in range(len(diceList)):
			numList.append(diceList[i][0] + diceList[i][1])

		idx = 0
		num = 0
		for i in range(len(numList)):
			if numList[i] > num:
				idx = i
				num = numList[i]
		return idx, num

	def onTimer(self, id, userArg):
		DEBUG_MSG("Room.onTimer called: id %i, userArg: %i" % (id, userArg))

		if userArg == const.TIMER_TYPE_DISMISS_WAIT:
			self.delTimer(id)
			self.dropRoom()
		# if userArg == const.TIMER_TYPE_ROOM_EXIST:
		# 	self.game_round = self.current_round
		# 	self.delTimer(id)


	def reqEnterRoom(self, avt_mb, first=False):
		"""
		defined.
		客户端调用该接口请求进入房间/桌子
		"""
		if self.isFull:
			avt_mb.enterRoomFailed(const.ENTER_FAILED_ROOM_FULL)
			return

		def callback(content):
			content = content.decode()
			try:
				data = json.loads(content)
				card_cost, diamond_cost = switch.calc_cost(self.game_round, self.player_num, self.pay_mode)
				if diamond_cost > data["diamond"]:
					avt_mb.enterRoomFailed(const.ENTER_FAILED_ROOM_DIAMOND_NOT_ENOUGH)
					return
				# 代开房
				if first and self.is_agent == 1:
					self.agent = PlayerProxy(avt_mb, self, -1)
					self.players_dict[avt_mb.userId] = self.agent
					avt_mb.enterRoomSucceed(self, -1)
					return

				for i, p in enumerate(self.players_list):
					if p and p.mb and p.mb.userId == avt_mb.userId:
						p.mb = avt_mb
						avt_mb.enterRoomSucceed(self, i)
						return

				DEBUG_MSG("Room.reqEnterRoom: %s" % (self.roomID))
				idx = self.getSit()
				n_player = PlayerProxy(avt_mb, self, idx)
				self.players_dict[avt_mb.userId] = n_player
				self.players_list[idx] = n_player
				# 确认准备
				# if idx not in self.confirm_next_idx:
				# 	self.confirm_next_idx.append(idx)

				if not first:
					self.broadcastEnterRoom(idx)
					self.check_same_ip()

				if self.isFull:
					self.origin_players_list = self.players_list[:]
			except:
				DEBUG_MSG("enterRoomFailed callback error:{}".format(content))
		if switch.DEBUG_BASE:
			callback('{"card":99, "diamond":999}'.encode())
		else:
			if first or self.pay_mode != 0:
				callback('{"card":99, "diamond":999}'.encode())
			else:
				utility.get_user_info(avt_mb.accountName, callback)

		# # 代开房
		# if first and self.is_agent == 1:
		# 	self.agent = PlayerProxy(avt_mb, self, -1)
		# 	self.players_dict[avt_mb.userId] = self.agent
		# 	avt_mb.enterRoomSucceed(self, -1)
		# 	return

		# for i, p in enumerate(self.players_list):
		# 	if p and p.mb and p.mb.userId == avt_mb.userId:
		# 		p.mb = avt_mb
		# 		avt_mb.enterRoomSucceed(self, i)
		# 		return

		# DEBUG_MSG("Room.reqEnterRoom: %s" % (self.roomID))
		# idx = self.getSit()
		# n_player = PlayerProxy(avt_mb, self, idx)
		# self.players_dict[avt_mb.userId] = n_player
		# self.players_list[idx] = n_player
		# # 确认准备
		# # if idx not in self.confirm_next_idx:
		# # 	self.confirm_next_idx.append(idx)

		# if not first:
		# 	self.broadcastEnterRoom(idx)
		# 	self.check_same_ip()

		# if self.isFull:
		# 	self.origin_players_list = self.players_list[:]

		# if self.isFull:
		# 	if self.is_agent == 1 and self.agent and self.agent.mb:
		# 		try:
		# 			self.agent.mb.quitRoomSucceed()
		# 			leave_tips = "您代开的房间已经开始游戏, 您已被请离.\n房间号【{}】".format(self.roomID)
		# 			self.agent.mb.showTip(leave_tips)
		# 		except:
		# 			pass

		# 	self.startGame()
			# self.addTimer(const.START_GAME_WAIT_TIME, 0, const.TIMER_TYPE_START_GAME)

	def reqReconnect(self, avt_mb):
		DEBUG_MSG("GameRoom reqReconnect userid = {}".format(avt_mb.userId))
		if avt_mb.userId not in self.players_dict.keys():
			return

		DEBUG_MSG("GameRoom reqReconnect player is in room".format(avt_mb.userId))
		# 如果进来房间后牌局已经开始, 就要传所有信息
		# 如果还没开始, 跟加入房间没有区别
		player = self.players_dict[avt_mb.userId]
		if self.agent and player.userId == self.agent.userId:
			self.agent.mb = avt_mb
			self.agent.online = 1
			avt_mb.enterRoomSucceed(self, -1)
			return
		
		player.mb = avt_mb
		player.online = 1
		if self.state == 1 or 0 < self.current_round <= self.game_round:
			if self.state == 0:
				# 重连回来直接准备
				self.roundEndCallback(avt_mb)
			rec_room_info = self.get_reconnect_room_dict(player.mb.userId)
			player.mb.handle_reconnect(rec_room_info)
		else:
			sit = 0
			for idx, p in enumerate(self.players_list):
				if p and p.mb:
					if p.mb.userId == avt_mb.userId:
						sit = idx
						break
			avt_mb.enterRoomSucceed(self, sit)

		# self.check_same_ip()

	def reqLeaveRoom(self, player):
		"""
		defined.
		客户端调用该接口请求离开房间/桌子
		"""
		DEBUG_MSG("Room.reqLeaveRoom:{0}, is_agent={1}".format(self.roomID, self.is_agent))
		if player.userId in self.players_dict.keys():
			n_player = self.players_dict[player.userId]
			idx = n_player.idx


			if idx == -1 and self.is_agent == 1:
				self.dropRoom()
			elif idx == 0 and self.is_agent == 0:
				# 房主离开房间, 则解散房间
				self.dropRoom()
			else:
				n_player.mb.quitRoomSucceed()
				self.players_list[idx] = None
				del self.players_dict[player.userId]
				if idx in self.confirm_next_idx:
					self.confirm_next_idx.remove(idx)
				# 通知其它玩家该玩家退出房间
				for i, p in enumerate(self.players_list):
					if i != idx and p and p.mb:
						p.mb.othersQuitRoom(idx)
				if self.agent and self.agent.mb:
					self.agent.mb.othersQuitRoom(idx)

		if self.isEmpty:
			self._reset()

	def dropRoom(self):
		for p in self.players_list:
			if p and p.mb:
				try:
					p.mb.quitRoomSucceed()
				except:
					pass

		if self.agent and self.agent.mb:
			try:
				# # 如果是代开房, 没打完一局返还房卡
				# if self.is_agent == 1 and self.current_round < 2:
				# 	# cost = 2 if self.game_round == 16 else 1
				# 	cost = 1
				# 	self.agent.mb.addCards(cost, "dropRoom")
				self.agent.mb.quitRoomSucceed()
			except:
				pass

		self._reset()

	def startGame(self):
		""" 开始游戏 """
		DEBUG_MSG("startGame")
		self.op_record = []
		self.state = 1
		self.current_round += 1
		self.wait_give_up_list = []
		self.give_up_list = []
		self.polling_give_up_op = -1
		for i,p in enumerate(self.players_list):
			if p is not None:
				p.wreaths = []

		diceList = self.throwTheDice([self.dealer_idx])
		idx, num = self.getMaxDiceIdx(diceList)

		# 仅仅在第1局扣房卡, 不然每局都会扣房卡
		def callback(content):
			content = content.decode()
			try:
				if content[0] != '{':
					DEBUG_MSG(content)
					self.dropRoom()
					return
				# 第一局时房间默认房主庄家, 之后谁上盘赢了谁是, 如果臭庄, 最后摸牌的人是庄
				for p in self.players_list:
					p.reset()
				self.current_idx = self.dealer_idx
				#圈风
				if sum([1 for state in self.player_dealer_state if state == 1]) == self.player_num:
					windIdx = (self.prevailing_wind + 1 - const.WIND_EAST)%len(const.WINDS)
					self.prevailing_wind = const.WINDS[windIdx]
					self.player_dealer_state = [0, 0, 0, 0]
				self.player_dealer_state[self.dealer_idx] = 1
				#自风
				for i,p in enumerate(self.players_list):
					if p is not None:
						p.wind = (self.player_num + i - self.dealer_idx)%self.player_num + const.WIND_EAST
				self.initTiles()
				self.deal(self.king_num)
				wreathsList = [p.wreaths for i,p in enumerate(self.players_list)]
				playerWindList = [p.wind for i,p in enumerate(self.players_list)]
				
				for p in self.players_list:
					if p and p.mb:
						DEBUG_MSG("start game,dealer_idx:{0},tiles:{1}, wreathsList:{2}, kingTiles:{3}, diceList:{4},leftTileNum:{5}".format(self.dealer_idx, p.tiles, wreathsList, self.kingTiles, diceList, len(self.tiles)))
						p.mb.startGame(self.dealer_idx, p.tiles, wreathsList, self.kingTiles, self.prevailing_wind, playerWindList, diceList)
				
				self.beginRound()
			except:
				DEBUG_MSG("consume failed!")

		if self.current_round == 1 and self.is_agent == 0:
			card_cost, diamond_cost = switch.calc_cost(self.game_round, self.player_num, self.pay_mode)
			if switch.DEBUG_BASE:
				callback('{"card":99, "diamond":999}'.encode())
			elif self.pay_mode == 1:
				utility.update_card_diamond(self.players_list[0].mb.accountName, -card_cost, -diamond_cost, callback, "FengHua RoomID:{}".format(self.roomID))
			else:
				signal = 0
				def payCallback(content):
					nonlocal signal
					try:
						signal += 1
						if signal == len(self.players_list):
							callback(content)
					except:
						DEBUG_MSG("AA payCallback Failed")
				if self.player_num == 3:
					utility.update_card_diamond(self.players_list[0].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
					utility.update_card_diamond(self.players_list[1].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
					utility.update_card_diamond(self.players_list[2].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
				else:
					utility.update_card_diamond(self.players_list[0].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
					utility.update_card_diamond(self.players_list[1].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
					utility.update_card_diamond(self.players_list[2].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
					utility.update_card_diamond(self.players_list[3].mb.accountName, -card_cost, -diamond_cost, payCallback, "NingBoMJ RoomID:{}".format(self.roomID))
			return

		DEBUG_MSG("start Game: Room{0} - Round{1}".format(self.roomID, str(self.current_round)+'/'+str(self.game_round)))

		callback('{"card":99, "diamond":999}'.encode())

	def cutAfterKong(self):
		if not self.can_cut_after_kong():
			return
		if len(self.tiles) <= 0:
			self.drawEnd()
			return

		player = self.players_list[self.current_idx]
		ti = self.tiles[0]
		self.tiles = self.tiles[1:]
		player.cutTile(ti)

	def beginRound(self):
		if len(self.tiles) <= 0:
			self.drawEnd()
			return

		player = self.players_list[self.current_idx]
		ti = self.tiles[0]
		self.tiles = self.tiles[1:]
		DEBUG_MSG("beginRound len:{0}".format(len(self.tiles)))
		player.drawTile(ti)

	def reqStopGame(self, player):
		"""
		客户端调用该接口请求停止游戏
		"""
		DEBUG_MSG("Room.reqLeaveRoom: %s" % (self.roomID))
		self.state = 0
		# self.delTimer(self._poll_timer)
		# self._poll_timer = None


	def drawEnd(self):
		""" 臭庄 """
		info = dict()
		info['win_type'] = -1
		info['win_idx_list'] = []
		info['quantity_list'] = [0]
		info['lucky_tiles'] = []
		info['result_list'] = []
		if self.current_round < self.game_round:
			self.broadcastRoundEnd(info)
		else:
			self.endAll(info)

	def winGame(self, idx, op, quantity, result):
		""" 座位号为idx的玩家胡牌 """
		self.cal_score(idx, op, quantity)

		if self.dealer_idx != idx:
			self.dealer_idx = (self.dealer_idx + 1) % self.player_num

		info = dict()
		info['win_type'] = op
		info['win_idx_list'] = [idx]
		info['quantity_list'] = [quantity]
		info['lucky_tiles'] = []
		info['result_list'] = [result]
		if self.current_round < self.game_round:
			self.broadcastRoundEnd(info)
		else:
			self.endAll(info)

	def endAll(self, info):
		""" 游戏局数结束, 给所有玩家显示最终分数记录 """

		# 先记录玩家当局战绩, 会累计总得分
		self.record_round_result()

		info['left_tiles'] = info['left_tiles'] = self.tiles
		info['player_info_list'] = [p.get_round_client_dict() for p in self.players_list if p is not None]
		player_info_list = [p.get_final_client_dict() for p in self.players_list if p is not None]
		# DEBUG_MSG("%" * 30)
		# DEBUG_MSG("FinalEnd info = {}".format(player_info_list))
		for p in self.players_list:
			if p and p.mb:
				p.mb.finalResult(player_info_list, info)

		self._reset()

	def sendEmotion(self, avt_mb, eid):
		""" 发表情 """
		# DEBUG_MSG("Room.Player[%s] sendEmotion: %s" % (self.roomID, eid))
		idx = None
		for i, p in enumerate(self.players_list):
			if p and avt_mb == p.mb:
				idx = i
				break
		else:
			if self.agent and self.agent.userId == avt_mb.userId:
				idx = -1

		if idx is None:
			return

		if self.agent and idx != -1 and self.agent.mb:
			self.agent.mb.recvEmotion(idx, eid)

		for i, p in enumerate(self.players_list):
			if p and i != idx:
				p.mb.recvEmotion(idx, eid)

	def sendMsg(self, avt_mb, mid):
		""" 发消息 """
		# DEBUG_MSG("Room.Player[%s] sendMsg: %s" % (self.roomID, mid))
		idx = None
		for i, p in enumerate(self.players_list):
			if p and avt_mb == p.mb:
				idx = i
				break
		else:
			if self.agent and self.agent.userId == avt_mb.userId:
				idx = -1

		if idx is None:
			return

		if self.agent and idx != -1 and self.agent.mb:
			self.agent.mb.recvMsg(idx, mid)

		for i, p in enumerate(self.players_list):
			if p and i != idx:
				p.mb.recvMsg(idx, mid)

	def sendVoice(self, avt_mb, url):
		# DEBUG_MSG("Room.Player[%s] sendVoice" % (self.roomID))
		idx = None
		for i, p in enumerate(self.players_list):
			if p and avt_mb.userId == p.userId:
				idx = i
				break
		else:
			if self.agent and self.agent.userId == avt_mb.userId:
				idx = -1

		if idx is None:
			return
		if self.agent and idx != -1 and self.agent.mb:
			self.agent.mb.recvVoice(idx, url)

		for i, p in enumerate(self.players_list):
			if p and p.mb:
				p.mb.recvVoice(idx, url)

	def sendAppVoice(self, avt_mb, url, time):
		# DEBUG_MSG("Room.Player[%s] sendVoice" % (self.roomID))
		idx = None
		for i, p in enumerate(self.players_list):
			if p and avt_mb.userId == p.userId:
				idx = i
				break
		else:
			if self.agent and self.agent.userId == avt_mb.userId:
				idx = -1

		if idx is None:
			return
		if self.agent and idx != -1 and self.agent.mb:
			self.agent.mb.recvAppVoice(idx, url, time)

		for i, p in enumerate(self.players_list):
			if p and p.mb:
				p.mb.recvAppVoice(idx, url, time)

	def doOperation(self, avt_mb, aid, tile_list):
		"""
		当前控牌玩家摸牌后向服务端确认的操作
		:param idx: 当前打牌的人的座位
		:param aid: 操作id
		:param tile: 针对的牌
		:return: 确认成功或者失败
		"""
		if self.dismiss_room_ts != 0 and int(time.time() - self.dismiss_room_ts) < const.DISMISS_ROOM_WAIT_TIME:
			# 说明在准备解散投票中,不能进行其他操作
			return

		tile = tile_list[0]
		idx = -1
		for i, p in enumerate(self.players_list):
			if p and p.mb == avt_mb:
				idx = i

		if idx != self.current_idx or len(self.wait_idx_list) > 0:
			avt_mb.doOperationFailed(const.OP_ERROR_NOT_CURRENT)
			return

		# self.delTimer(self._op_timer)
		p = self.players_list[idx]
		if aid == const.OP_DISCARD and self.can_discard(p.tiles, tile) and p not in self.give_up_list:
			self.all_discard_tiles.append(tile)
			p.discardTile(tile)
		elif aid == const.OP_CONCEALED_KONG and self.can_concealed_kong(p.tiles, tile) and p not in self.give_up_list:
			p.concealedKong(tile)
		elif aid == const.OP_EXPOSED_KONG and self.can_self_exposed_kong(p, tile) and p not in self.give_up_list:
			p.self_exposedKong(tile)
		elif aid == const.OP_KONG_WREATH and self.can_kong_wreath(p.tiles, tile) and p not in self.give_up_list:
			p.kongWreath(tile)
		elif aid == const.OP_PASS:
			# 自己摸牌的时候可以杠或者胡时选择过, 则什么都不做. 继续轮到该玩家打牌.
			pass
		elif aid == const.OP_DRAW_WIN and p not in self.give_up_list: #普通自摸胡
			is_win, quantity, result = self.can_win(list(p.tiles), p.last_draw, const.OP_DRAW_WIN, idx)
			if is_win:
				p.win(aid, quantity, result)
			else:
				avt_mb.doOperationFailed(const.OP_ERROR_ILLEGAL)
				self.current_idx = self.nextIdx
				self.beginRound()
		elif aid == const.OP_WREATH_WIN and p not in self.give_up_list: #自摸8张花胡
			is_win, quantity, result = self.can_win(list(p.tiles), p.last_draw, const.OP_WREATH_WIN, idx)
			if is_win:
				p.win(aid, quantity, result)
			else:
				avt_mb.doOperationFailed(const.OP_ERROR_ILLEGAL)
				self.current_idx = self.nextIdx
				self.beginRound()
		else:
			avt_mb.doOperationFailed(const.OP_ERROR_ILLEGAL)
			self.current_idx = self.nextIdx
			self.beginRound()


	def confirmOperation(self, avt_mb, aid, tile_list):
		""" 被轮询的玩家确认了某个操作 """
		if self.dismiss_room_ts != 0 and int(time.time() - self.dismiss_room_ts) < const.DISMISS_ROOM_WAIT_TIME:
			# 说明在准备解散投票中,不能进行其他操作
			return

		tile = tile_list[0]
		idx = -1
		for i, p in enumerate(self.players_list):
			if p and p.mb == avt_mb:
				idx = i

		if idx not in self.wait_idx_list and len(self.wait_idx_list) > 0:
			avt_mb.doOperationFailed(const.OP_ERROR_NOT_CURRENT)
			return
		# 确认要操作的牌是否是最后一张被打的牌
		if aid != const.OP_PASS and tile != self.all_discard_tiles[-1] and len(self.wait_for_win_dict) <= 0:
			avt_mb.doOperationFailed(const.OP_ERROR_ILLEGAL)
			return

		# self.delTimer(self._poll_timer)
		temp_op = self.wait_op

		self.wait_idx_list = []
		self.wait_op = None
		p = self.players_list[idx]
		if aid == const.OP_PONG and self.can_pong(p.tiles, tile) and p not in self.give_up_list:
			self.current_idx = idx
			p.pong(tile)
		elif aid == const.OP_EXPOSED_KONG and self.can_exposed_kong(p.tiles, tile) and p not in self.give_up_list:
			self.current_idx = idx
			p.exposedKong(tile)
		elif aid == const.OP_CHOW and self.can_chow_one(p.tiles, tile_list) and (idx+self.player_num-1)%self.player_num == self.last_player_idx and p not in self.give_up_list:
			self.current_idx = idx
			p.chow(tile_list)
		elif aid == const.OP_KONG_WIN:
			if len(self.wait_for_win_dict) > 0:
				if idx in self.wait_for_win_dict:
					if self.wait_for_win_dict[idx]["state"] != 0:
						DEBUG_MSG("player is already commit win information.")
						return
					self.wait_for_win_dict[idx]["state"] = 1
					self.handleMutiWinAfterCommit(tile)		
			else:
				avt_mb.doOperationFailed(const.OP_ERROR_ILLEGAL)
				#无任何操作 过牌
				self.confirmPass(idx)
		else:
			#无任何操作 过牌
			#设置玩家 确认胡状态
			if idx in self.wait_for_win_dict:
				self.wait_for_win_dict[idx]["state"] = 2 #state 0 未确认 1确认胡 2不胡
			
			isAllCommit, isWin = self.handleMutiWinAfterCommit(tile)
			DEBUG_MSG("isAllCommit:{0},isWin:{1}".format(isAllCommit, isWin))
			if isAllCommit and not isWin: # 所有玩家提交完毕，并且所有玩家都不胡
				DEBUG_MSG("check pong kong or pass,wait_op:{0}".format(temp_op))
				if temp_op == const.OP_KONG_WIN:
					for i, p in enumerate(self.players_list):
						if p and i != self.last_player_idx and p not in self.give_up_list:
							DEBUG_MSG("check==>idx:{0},tiles:{1},tile:{2}".format(i,str(p.tiles),str(tile)))
							if self.can_pong(p.tiles, tile) or self.can_exposed_kong(p.tiles, tile):
								self.wait_idx_list = [i]
								self.wait_op = const.OP_DISCARD
								DEBUG_MSG("can pong,idx:{0}".format(i))
								p.mb.waitForOperation(const.OP_DISCARD, [tile,])
								break
					else:
						self.confirmPass(idx)
				else:
					self.confirmPass(idx)

	def handleMutiWinAfterCommit(self, tile): # return 是否提交完毕， 是否可以胡
		"""任一可以胡的玩家提交结果完毕"""
		DEBUG_MSG("handleMutiWinAfterCommit:{0}".format(str(self.wait_for_win_dict)))
		win_list = []
		quantity_list = []
		formIdxList = []
		result_list = []
		win_op = const.OP_KONG_WIN
		for waitIdx in self.wait_for_win_dict:
			if self.wait_for_win_dict[waitIdx]["state"] == 0:
				return False, False
			elif self.wait_for_win_dict[waitIdx]["state"] == 1:
				win_list.append(self.players_list[waitIdx])
				quantity_list.append(self.wait_for_win_dict[waitIdx]['quantity'])
				win_op = self.wait_for_win_dict[waitIdx]["win_op"]
				formIdxList.append(self.wait_for_win_dict[waitIdx]["formIdx"])
				result_list.append(self.wait_for_win_dict[waitIdx]["result"])
		self.wait_for_win_dict = {}
		# 所有玩家都选择不胡
		if not win_list:
			DEBUG_MSG("all player select not win")
			return True, False
		# 有玩家选择胡
		self.processMutiWin(win_list, quantity_list, result_list, win_op, formIdxList, tile)
		return True,True

	def confirmPass(self, idx):
		nextIdx = self.nextIdx
		nextMb = self.players_list[nextIdx]
		if idx != nextIdx and self.can_chow(nextMb.tiles, self.all_discard_tiles[-1]) and nextMb not in self.give_up_list:
			self.wait_idx_list = [nextIdx]
			self.wait_op = const.OP_DISCARD
			nextMb.mb.waitForOperation(const.OP_DISCARD, [self.all_discard_tiles[-1],])
		else:
			self.current_idx = nextIdx
			self.beginRound()

	#抢杠 胡处理
	def processMutiWin(self, win_list, quantity_list, result_list, win_op, formIdx_list, tile):
		""" 处理抢杠胡, 可能有多人胡的情况 """
		win_idx_list = [mem.idx for mem in win_list]
		op_list = [const.OP_KONG_WIN] * len(win_idx_list)
		self.broadcastMultiOperation(win_idx_list, op_list, win_op, [tile,])

		#结算
		for i in range(len(win_list)):
			fromIdx = formIdx_list[i]
			self.players_list[fromIdx].addScore(-quantity_list[i] * 5)
			win_list[i].addScore(quantity_list[i] * 5)

		if self.dealer_idx not in win_idx_list:
			self.dealer_idx = (self.dealer_idx + 1) % self.player_num

		for mem in win_list:
			mem.kong_win(tile)
		
		info = dict()
		info['win_type'] = const.OP_KONG_WIN
		info['win_idx_list'] = win_idx_list
		info['quantity_list'] = quantity_list
		info['lucky_tiles'] = []
		info['result_list'] = result_list
		if self.current_round < self.game_round:
			self.broadcastRoundEnd(info)
		else:
			self.endAll(info)

	def broadcastOperation(self, idx, aid, tile_list = None):
		"""
		将操作广播给所有人, 包括当前操作的玩家
		:param idx: 当前操作玩家的座位号
		:param aid: 操作id
		:param tile_list: 出牌的list
		"""
		for i, p in enumerate(self.players_list):
			if p is not None:
				p.mb.postOperation(idx, aid, tile_list)

	def broadcastOperation2(self, idx, aid, tile_list = None):
		""" 将操作广播除了自己之外的其他人 """
		for i, p in enumerate(self.players_list):
			if p and i != idx:
				p.mb.postOperation(idx, aid, tile_list)

	def broadcastMultiOperation(self, idx_list, aid_list, win_op, tile_list=None):
		for i, p in enumerate(self.players_list):
			if p is not None:
				p.mb.postMultiOperation(idx_list, aid_list, tile_list)

	def broadcastRoundEnd(self, info):
		# 广播胡牌或者流局导致的每轮结束信息, 包括算的扎码和当前轮的统计数据

		# 先记录玩家当局战绩, 会累计总得分
		self.record_round_result()

		self.state = 0
		info['left_tiles'] = self.tiles
		info['player_info_list'] = [p.get_round_client_dict() for p in self.players_list if p is not None]

		DEBUG_MSG("&" * 30)
		DEBUG_MSG("RoundEnd info = {}".format(info))
		self.confirm_next_idx = []
		for p in self.players_list:
			if p:
				p.mb.roundResult(info)

	def pollingGiveUp(self, operation, op_idx, oped_idx):
		self.polling_give_up_op = operation
		self.wait_give_up_list = []
		for i, p in enumerate(self.players_list):
			if p and i != op_idx and i != oped_idx:
				self.wait_give_up_list.append(p)
				p.mb.notifyPlayerGiveUp()

	def confirmGiveUp(self, avt_mb, isGiveUp):
		if len(self.wait_give_up_list) <= 0:
			return
		for i, p in enumerate(self.wait_give_up_list):
			if p and avt_mb == p.mb:
				if isGiveUp and p not in self.give_up_list:
					self.give_up_list.append(p)
				self.wait_give_up_list.remove(p)
				break
		if len(self.wait_give_up_list) <= 0:
			'''所有玩家提交完毕'''
			DEBUG_MSG('all player committed')
			if self.polling_give_up_op == const.OP_PONG:
				'''碰的玩家可以打牌，解锁操作面板'''
				self.unlockPongPlayerOperation(self.current_idx)
			else:
				'''明杠玩家开始摸牌'''
				self.beginRound()

	def unlockPongPlayerOperation(self, idx):
		for i, p in enumerate(self.players_list):
			if p and i == idx:
				p.mb.unlockPongPlayerOperation()

	def waitForOperation(self, idx, aid, tile):
		isHaveWaitOp = False
		if aid == const.OP_KONG_WREATH: 										#玩家杠花 是否可以8张花胡
			for i, p in enumerate(self.players_list):
				if p and i == idx and p not in self.give_up_list and self.can_wreath_win(p.wreaths):
					isHaveWaitOp = True
					p.mb.waitForOperation(const.OP_WREATH_WIN, [tile,])
					break
			else:
				self.beginRound()
				return
		elif aid == const.OP_EXPOSED_KONG or aid == const.OP_CONCEALED_KONG:	#玩家普通杠 是否可以抢杠胡
			self.wait_idx_list = []
			self.wait_for_win_dict = {}
			player_list, quantity_list, result_list = self.checkKongWin(idx, tile)
			for i,p in enumerate(player_list):
				if p is not None:
					wait_idx = self.players_list.index(p)
					self.wait_idx_list.append(wait_idx)
					self.wait_op = const.OP_KONG_WIN
					self.wait_for_win_dict[wait_idx] = {"state": 0, "formIdx": idx, "win_op":aid, "quantity":quantity_list[i], "result":result_list[i]}
					isHaveWaitOp = True
					p.mb.waitForOperation(const.OP_KONG_WIN, [tile,])
					DEBUG_MSG("wait for operation win:{0}".format(wait_idx))
		elif aid == const.OP_DISCARD:											#玩家打牌 是否有其他玩家碰 杠
			for i, p in enumerate(self.players_list):
				DEBUG_MSG("op_discard : {0},{1},{2}".format(i, idx, self.give_up_list))
				if p and i != idx and p not in self.give_up_list:
					DEBUG_MSG("discard can_pong or can_exposed_kong")
					if self.can_pong(p.tiles, tile) or self.can_exposed_kong(p.tiles, tile):
						self.wait_idx_list = [i]
						self.wait_op = aid
						isHaveWaitOp = True
						p.mb.waitForOperation(aid, [tile,])
						break
		if not isHaveWaitOp:
			#下家能不能吃
			nextIdx = self.nextIdx
			p = self.players_list[nextIdx]
			if aid == const.OP_DISCARD and self.can_chow(p.tiles, tile) and p not in self.give_up_list:	#能吃
				self.wait_idx_list = [nextIdx]
				self.wait_op = aid
				p.mb.waitForOperation(aid, [tile,])
			else:
				self.current_idx = nextIdx
				self.beginRound()

	#可以抢杠胡 玩家列表
	def checkKongWin(self, idx, tile):
		wait_player_list = []
		quantity_list = []
		result_list = []
		for i, p in enumerate(self.players_list):
			if i == idx or p in self.give_up_list:
				continue
			tmp = list(p.tiles)
			tmp.append(tile)
			is_win, quantity, result = self.can_win(tmp, tile, const.OP_KONG_WIN, i)
			if is_win:
				wait_player_list.append(p)
				quantity_list.append(quantity)
				result_list.append(result)
		return wait_player_list, quantity_list, result_list

	def get_init_client_dict(self):
		agent_d = {
			'nickname': "",
			'userId': 0,
			'head_icon': "",
			'ip': '0.0.0.0',
			'sex': 1,
			'idx': -1,
			'uuid': 0,
			'online': 1,
		}
		if self.is_agent and self.agent:
			d = self.agent.get_init_client_dict()
			agent_d.update(d)

		return {
			'roomID': self.roomID,
			'ownerId': self.owner_uid,
			'isAgent': self.is_agent,
			'agentInfo': agent_d,
			'dealerIdx': self.dealer_idx,
			'curRound': self.current_round,
			'maxRound': self.game_round,
			'player_num': self.player_num,
			'pay_mode': self.pay_mode,
			'win_quantity': self.win_quantity,
			'king_num': self.king_num,
			'player_base_info_list': [p.get_init_client_dict() for p in self.players_list if p is not None],
			'player_state_list': [1 if i in self.confirm_next_idx else 0 for i in range(const.ROOM_PLAYER_NUMBER)],
		}

	def get_reconnect_room_dict(self, userId):
		dismiss_left_time = int(time.time() - self.dismiss_room_ts)
		if self.dismiss_room_ts == 0 or dismiss_left_time >= const.DISMISS_ROOM_WAIT_TIME:
			dismiss_left_time = 0

		idx = 0
		for p in self.players_list:
			if p and p.userId == userId:
				idx = p.idx
		waitAid = -1
		if len(self.wait_idx_list) >= 0 and self.wait_op and idx in self.wait_idx_list:
			waitAid = self.wait_op

		giveUpState = const.NOT_GIVE_UP
		if self.players_list[idx] in self.give_up_list:
			giveUpState = const.GIVE_UP
		elif self.players_list[idx] in self.wait_give_up_list:
			giveUpState = const.WAIT_GIVE_UP

		return {
			'init_info' : self.get_init_client_dict(),
			'curPlayerSitNum': self.current_idx,
			'isPlayingGame': self.state,
			'player_state_list': [1 if i in self.confirm_next_idx else 0 for i in range(self.player_num)],
			'lastDiscardTile': 0 if not self.all_discard_tiles else self.all_discard_tiles[-1],
			'lastDrawTile' : self.players_list[idx].last_draw,
			'lastDiscardTileFrom': self.last_player_idx,
			'kingTiles' : self.kingTiles,
			'waitAid': waitAid,
			'giveUpState': giveUpState,
			'leftTileNum': len(self.tiles),
			'applyCloseFrom': self.dismiss_room_from,
			'applyCloseLeftTime': dismiss_left_time,
			'applyCloseStateList': self.dismiss_room_state_list,
			'player_advance_info_list': [p.get_reconnect_client_dict(userId) for p in self.players_list if p is not None],
			'prevailing_wind': self.prevailing_wind,
		}

	def broadcastEnterRoom(self, idx):
		new_p = self.players_list[idx]

		if self.is_agent == 1:
			if self.agent and self.agent.mb:
				self.agent.mb.othersEnterRoom(new_p.get_init_client_dict())

		for i, p in enumerate(self.players_list):
			if p is None:
				continue
			if i == idx:
				p.mb.enterRoomSucceed(self, idx)
			else:
				p.mb.othersEnterRoom(new_p.get_init_client_dict())

	def cal_score(self, idx, aid, quantity = 0):
		if aid == const.OP_EXPOSED_KONG:
			pass
		elif aid == const.OP_CONCEALED_KONG:
			pass
		elif aid == const.OP_POST_KONG:
			pass
		elif aid == const.OP_GET_KONG:
			pass
		elif aid == const.OP_DRAW_WIN:
			for i, p in enumerate(self.players_list):
				if p is None or p in self.give_up_list:
					continue
				if idx == i:
					DEBUG_MSG("score:{0},{1},{2},{3},{4}".format(i, quantity, self.player_num, len(self.give_up_list), self.polling_give_up_op))
					p.addScore(quantity * (self.player_num - 1 - len(self.give_up_list)) * (5 if self.polling_give_up_op > 0 else 1))
				else:
					DEBUG_MSG("score:{0}, {1}, {2}".format(i, quantity, self.polling_give_up_op))
					p.addScore(-quantity  * (5 if self.polling_give_up_op > 0 else 1))
		elif aid == const.OP_KONG_WIN:
			pass

	def roundEndCallback(self, avt_mb):
		""" 一局完了之后玩家同意继续游戏 """
		if self.state == 1:
			return
		idx = -1
		for i, p in enumerate(self.players_list):
			if p and p.userId == avt_mb.userId:
				idx = i
				break
		if idx not in self.confirm_next_idx:
			self.confirm_next_idx.append(idx)
			for p in self.players_list:
				if p and p.idx != idx:
					p.mb.readyForNextRound(idx)

		if len(self.confirm_next_idx) == self.player_num and self.isFull:
			if self.current_round == 0 and self.is_agent == 1 and self.agent:
				try:
					self.agent.mb.quitRoomSucceed()
					leave_tips = "您代开的房间已经开始游戏, 您已被请离.\n房间号【{}】".format(self.roomID)
					self.agent.mb.showTip(leave_tips)
				except:
					pass
			self.startGame()

	def record_round_result(self):
		# 玩家记录当局战绩
		d = datetime.fromtimestamp(time.time())
		round_result_d = {
			'date': '-'.join([str(d.year), str(d.month), str(d.day)]),
			'time': ':'.join([str(d.hour), str(d.minute)]),
			'round_record': [p.get_round_result_info() for p in self.origin_players_list if p],
		}

		# 第一局结束时push整个房间所有局的结构, 以后就增量push
		if self.current_round == 1:
			game_result_l = [[round_result_d]]
			for p in self.players_list:
				if p:
					p.record_all_result(game_result_l)
		else:
			for p in self.players_list:
				if p:
					p.record_round_game_result(round_result_d)

	def check_same_ip(self):
		ip_list = []
		for p in self.players_list:
			if p and p.mb and p.ip != '0.0.0.0':
				ip_list.append(p.ip)
			else:
				ip_list.append(None)

		tips = []
		checked = []
		for i in range(self.player_num):
			if ip_list[i] is None or i in checked:
				continue
			checked.append(i)
			repeat = []
			repeat.append(i)
			for j in range(i+1, self.player_num):
				if ip_list[j] is None or j in checked:
					continue
				if ip_list[i] == ip_list[j]:
					repeat.append(j)
			if len(repeat) > 1:
				name = []
				for k in repeat:
					checked.append(k)
					name.append(self.players_list[k].nickname)
				tip = '和'.join(name) + '有相同的ip地址'
				tips.append(tip)
		if tips:
			tips = '\n'.join(tips)
			# DEBUG_MSG(tips)
			for p in self.players_list:
				if p and p.mb:
					p.mb.showTip(tips)

	def apply_dismiss_room(self, avt_mb):
		""" 游戏开始后玩家申请解散房间 """
		self.dismiss_room_ts = time.time()
		src = None
		for i, p in enumerate(self.players_list):
			if p.userId == avt_mb.userId:
				src = p
				break

		# 申请解散房间的人默认同意
		self.dismiss_room_from = src.idx
		self.dismiss_room_state_list[src.idx] = 1

		self.dismiss_timer = self.addTimer(const.DISMISS_ROOM_WAIT_TIME, 0, const.TIMER_TYPE_DISMISS_WAIT)

		for p in self.players_list:
			if p and p.mb and p.userId != avt_mb.userId:
				p.mb.req_dismiss_room(src.idx)

	def vote_dismiss_room(self, avt_mb, vote):
		""" 某位玩家对申请解散房间的投票 """
		src = None
		for p in self.players_list:
			if p and p.userId == avt_mb.userId:
				src = p
				break

		self.dismiss_room_state_list[src.idx] = vote
		for p in self.players_list:
			if p and p.mb:
				p.mb.vote_dismiss_result(src.idx, vote)

		yes = self.dismiss_room_state_list.count(1)
		no = self.dismiss_room_state_list.count(2)
		if yes >= 3:
			self.delTimer(self.dismiss_timer)
			self.dismiss_timer = None
			self.dropRoom()

		if no >= 2:
			self.delTimer(self.dismiss_timer)
			self.dismiss_timer = None
			self.dismiss_room_from = -1
			self.dismiss_room_ts = 0
			self.dismiss_room_state_list = [0,0,0,0]

	def notify_player_online_status(self, userId, status):
		src = -1
		for idx, p in enumerate(self.players_list):
			if p and p.userId == userId:
				p.online = status
				src = idx
				break

		if src == -1:
			return

		for idx, p in enumerate(self.players_list):
			if p and p.mb and p.userId != userId:
				p.mb.notifyPlayerOnlineStatus(src, status)
