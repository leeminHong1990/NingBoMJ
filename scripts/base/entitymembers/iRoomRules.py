# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import utility
import const
import random

class iRoomRules(object):

	def __init__(self):
		# 房间的牌堆
		self.tiles = []
		self.meld_dict = dict()

	def initTiles(self):
		# 万 条 筒
		self.tiles = const.CHARACTER * 4 + const.BAMBOO * 4 + const.DOT * 4
		# 东 西 南 北
		self.tiles += [const.WIND_EAST, const.WIND_SOUTH, const.WIND_WEST, const.WIND_NORTH] * 4
		# 中 发 白
		self.tiles += [const.DRAGON_RED, const.DRAGON_GREEN, const.DRAGON_WHITE] * 4
		# 春 夏 秋 冬
		self.tiles += [const.SEASON_SPRING, const.SEASON_SUMMER, const.SEASON_AUTUMN, const.SEASON_WINTER]
		# 梅 兰 竹 菊
		self.tiles += [const.FLOWER_PLUM, const.FLOWER_ORCHID, const.FLOWER_BAMBOO, const.FLOWER_CHRYSANTHEMUM]
		DEBUG_MSG(self.tiles)
		self.shuffle_tiles()

	def shuffle_tiles(self):
		random.shuffle(self.tiles)

	def deal(self, kingTypeNum = 1):
		""" 发牌 """
		for i in range(const.INIT_TILE_NUMBER):
			for j in range(self.player_num):
				self.players_list[j].tiles.append(self.tiles[j])
			self.tiles = self.tiles[self.player_num:]

		for i, p in enumerate(self.players_list):
			DEBUG_MSG("deal{0}:{1}".format(i, p.tiles))
		""" 杠花 """
		for i in range(self.player_num):
			for j in range(len(self.players_list[i].tiles)-1, -1, -1):
				tile = self.players_list[i].tiles[j]
				if tile in const.SEASON or tile in const.FLOWER:
					del self.players_list[i].tiles[j]
					# self.players_list[i].tiles.pop(j)
					self.players_list[i].wreaths.append(tile)
					DEBUG_MSG("kong wreath{0},{1}".format(i, tile))
		""" 补花 """
		for i in range(self.player_num):
			while len(self.players_list[i].tiles) < const.INIT_TILE_NUMBER:
				if len(self.tiles) <= 0:
					break
				tile = self.tiles[0]
				self.tiles = self.tiles[1:]
				if tile in const.SEASON or tile in const.FLOWER:
					self.players_list[i].wreaths.append(tile)
					DEBUG_MSG("add wreath{0},{1}".format(i, tile))
				else:
					self.players_list[i].tiles.append(tile)
					DEBUG_MSG("add wreath_{0},{1}".format(i, tile))
		""" 财神 """
		#第一张非花牌
		for i in range(len(self.tiles)): 
			t = self.tiles[i]
			if t not in const.SEASON and t not in const.FLOWER:
				# 1-9为一圈 东南西北为一圈 中发白为一圈
				self.kingTiles = [t]
				if kingTypeNum > 1:
					if t in const.CHARACTER:
						index = const.CHARACTER.index(t)
						self.kingTiles.append(const.CHARACTER[(index + 1)%len(const.CHARACTER)])
					elif t in const.DOT:
						index = const.DOT.index(t)
						self.kingTiles.append(const.DOT[(index + 1)%len(const.DOT)])
					elif t in const.BAMBOO:
						index = const.BAMBOO.index(t)
						self.kingTiles.append(const.BAMBOO[(index + 1)%len(const.BAMBOO)])
					elif t in const.WINDS:
						index = const.WINDS.index(t)
						self.kingTiles.append(const.WINDS[(index + 1)%len(const.WINDS)])
					elif t in const.DRAGONS:
						index = const.DRAGONS.index(t)
						self.kingTiles.append(const.DRAGONS[(index + 1)%len(const.DRAGONS)])
				del self.tiles[i]
				break
		""" 整理 """
		for i in range(self.player_num):
			self.players_list[i].tidy(self.kingTiles)

	def swapTileToTop(self, tile):
		if tile in self.tiles:
			tileIdx = self.tiles.index(tile)
			self.tiles[0], self.tiles[tileIdx] = self.tiles[tileIdx], self.tiles[0]

	def winCount(self):
		pass
	
	def can_cut_after_kong(self):
		return True

	def can_discard(self, tiles, t):
		if t in tiles:
			return True
		return False

	def can_chow(self, tiles, t):
		return False
		# if t >= 30:
		# 	return False
		# neighborTileNumList = [0, 0, 1, 0, 0]
		# for i in range(len(tiles)):
		# 	if (tiles[i] - t >= -2 and tiles[i] - t <= 2):
		# 		neighborTileNumList[tiles[i] - t + 2] += 1
		# for i in range(0,3):
		# 	tileNum = 0
		# 	for j in range(i,i+3):
		# 		if neighborTileNumList[j] > 0:
		# 			tileNum += 1
		# 		else:
		# 			break
		# 	if tileNum >= 3:
		# 		return True
		# return False

	def can_chow_one(self, tiles, tile_list):
		return False
		# """ 能吃 """
		# if tile_list[0] >= 30:
		# 	return False
		# if sum([1 for i in tiles if i == tile_list[1]]) >= 1 and sum([1 for i in tiles if i == tile_list[2]]) >= 1:
		# 	sortLis = sorted(tile_list)
		# 	if (sortLis[2] + sortLis[0])/2 == sortLis[1] and sortLis[2] - sortLis[0] == 2:
		# 		return True
		# return False

	def can_pong(self, tiles, t):
		""" 能碰 """
		if t in self.kingTiles:
			return False
		return sum([1 for i in tiles if i == t]) >= 2

	def can_exposed_kong(self, tiles, t):
		""" 能明杠 """
		if t in self.kingTiles:
			return False
		return utility.get_count(tiles, t) == 3

	def can_self_exposed_kong(self, player, t):
		""" 自摸的牌能够明杠 """
		if t in self.kingTiles:
			return False
		for op in player.op_r:
			if op[0] == const.OP_PONG and op[1][0] == t:
				return True
		return False

	def can_concealed_kong(self, tiles, t):
		""" 能暗杠 """
		if t in self.kingTiles:
			return False
		return utility.get_count(tiles, t) == 4

	def can_kong_wreath(self, tiles, t):
		if t in tiles and (t in const.SEASON or t in const.FLOWER):
			return True
		return False

	def can_wreath_win(self, wreaths):
		if len(wreaths) == len(const.SEASON) + len(const.FLOWER):
			return True
		return False

	# def can_win(self, tiles):
	# 	""" 能胡牌 """
	# 	if len(tiles) % 3 != 2:
	# 		return False

	# 	tiles = sorted(tiles)
	# 	chars, bambs, dots, dragon_red = self.classify_tiles(tiles)

	# 	c_need1 = utility.meld_only_need_num(chars, self.meld_dict)
	# 	c_need2 = utility.meld_with_pair_need_num(chars, self.meld_dict)
	# 	if c_need1 > dragon_red and c_need2 > dragon_red:
	# 		return False

	# 	b_need1 = utility.meld_only_need_num(bambs, self.meld_dict)
	# 	b_need2 = utility.meld_with_pair_need_num(bambs, self.meld_dict)
	# 	if b_need1 > dragon_red and b_need2 > dragon_red:
	# 		return False

	# 	d_need1 = utility.meld_only_need_num(dots, self.meld_dict)
	# 	d_need2 = utility.meld_with_pair_need_num(dots, self.meld_dict)
	# 	if d_need1 > dragon_red and d_need2 > dragon_red:
	# 		return False

	# 	if  c_need2 + b_need1 + d_need1 <= dragon_red or\
	# 		c_need1 + b_need2 + d_need1 <= dragon_red or\
	# 		c_need1 + b_need1 + d_need2 <= dragon_red:
	# 		return True
	# 	return False

	# # 是否包牌
	# def checkIsPack(self, idx_1, idx_2):
	# 	if idx_1 == idx_2 or idx_1 > len(self.players_list)-1 or idx_2 > len(self.players_list)-1:
	# 		return False
	# 	p1_op_r = self.players_list[idx_1].op_r
	# 	p2_op_r = self.players_list[idx_2].op_r
	# 	p1_num_List = [0] * 4
	# 	p2_num_List = [0] * 4
	# 	p1_num,p2_num = (0, 0)
	# 	for i, record in enumerate(p1_op_r)
	# 		if record[2] == idx_2 and record[0] in [const.OP_PONG, const.OP_EXPOSED_KONG]:
	# 			p1_num += 1
	# 			if p1_num >= 3:
	# 				return True
	# 	for i, record in enumerate(p2_op_r)
	# 		if record[2] == idx_1 and record[0] in [const.OP_PONG, const.OP_EXPOSED_KONG]:
	# 			p2_num += 1
	# 			if p2_num >= 3:
	# 				return True
	# 	return False

	def classify_tiles(self, tiles):
		chars = []
		bambs = []
		dots  = []
		dragon_red = 0
		for t in tiles:
			if t in const.CHARACTER:
				chars.append(t)
			elif t in const.BAMBOO:
				bambs.append(t)
			elif t in const.DOT:
				dots.append(t)
			elif t == const.DRAGON_RED:
				dragon_red += 1
			else:
				DEBUG_MSG("iRoomRules classify tiles failed, no this tile %s"%t)
		return chars, bambs, dots, dragon_red

	def can_win(self, handTiles, finalTile, win_op, idx):
		p = self.players_list[idx]
		copyTiles = handTiles[:]
		copyTiles = sorted(copyTiles)
		quantity, result = self.getCanWinQuantity(copyTiles, p.upTiles, p.wreaths, finalTile, p.op_r, p.wind, win_op, idx)
		DEBUG_MSG("idx{0}can_win:{1},{2},{3}".format(idx, quantity, self.win_quantity, result))
		if quantity >= self.win_quantity:
			return True, quantity, result
		return False, quantity, result

	def getCanWinQuantity (self, handTiles, uptiles, wreaths, finalTile, p_op_r, p_wind, win_op, idx):
		result = [0] * 17
		handTiles = sorted(handTiles)
		classifyList = utility.classifyTiles(handTiles, self.kingTiles)
		kingTilesNum = len(classifyList[0])
		handTilesButKing = []
		for i in range(1, len(classifyList)):
			handTilesButKing.extend(classifyList[i])
		def removeCheckPairWin(handTilesButKing, removeTuple, useKingNum, kingTilesNum):
			if useKingNum <= kingTilesNum:
				tryHandTilesButKing = handTilesButKing[:]
				tryHandTilesButKing = sorted(tryHandTilesButKing)
				for t in removeTuple:
					if t != -1:
						tryHandTilesButKing.remove(t)
				if utility.meld_with_pair_need_num(tryHandTilesButKing, {}) <= kingTilesNum - useKingNum:
					return True
			return False
		def removeCheckOnlyWin(handTilesButKing, removeTuple, useKingNum, kingTilesNum):
			if useKingNum <= kingTilesNum:
				tryHandTilesButKing = handTilesButKing[:]
				tryHandTilesButKing = sorted(tryHandTilesButKing)
				for t in removeTuple:
					if t != -1:
						tryHandTilesButKing.remove(t)
				if utility.meld_only_need_num(tryHandTilesButKing, {}) <= kingTilesNum - useKingNum:
					return True
			return False

		quantity = 0 #台数
		if win_op == const.OP_WREATH_WIN:#8张花
			if len(wreaths) == 8:
				# 8张花胡 = 8张花(14台) + 胡(8台) = 22台
				quantity += utility.getWreathQuantity(wreaths, p_wind)
				DEBUG_MSG("8 flower, flower:{}".format(quantity))
				# quantity += utility.getHandTileQuantity(handTilesButKing, p_wind, self.prevailing_wind)
				# DEBUG_MSG("8 flower, handTile:{}".format(quantity))
				# quantity += utility.getUpTileQuantity(uptiles, p_wind, self.prevailing_wind)
				# DEBUG_MSG("8 flower, uptile:{}".format(quantity))
				result[0] = 1
		elif len(handTiles) % 3 == 2: #其他 3x+2 胡
			
			if utility.meld_with_pair_need_num(handTilesButKing, {}) <= kingTilesNum:
				isPongPongWin = utility.checkIsPongPongWin(handTilesButKing, uptiles, kingTilesNum)
				#自摸
				if win_op == const.OP_DRAW_WIN:
					quantity += 1
					result[3] = 1
					DEBUG_MSG("zimo:{}".format(quantity))
				elif win_op == const.OP_KONG_WIN:
					quantity += 1
					result[15] = 1
					DEBUG_MSG("qiangganghu:{}".format(quantity))
				#杠上开花
				if win_op == const.OP_DRAW_WIN and utility.checkIsKongDrawWin(p_op_r):
					quantity += 1
					result[4] = 1
					DEBUG_MSG("gangkai:{}".format(quantity))
				#硬胡
				if kingTilesNum <= 0: 
					quantity += 1
					result[5] = 1
					DEBUG_MSG("yinhu:{}".format(quantity))
				#海捞
				if len(self.tiles) <= 0:
					quantity += 1
					result[6] = 1
					DEBUG_MSG("hailao:{}".format(quantity))
				#大吊车
				if len(handTiles) == 2:
					quantity += 1
					result[7] = 1
					DEBUG_MSG("dadiaoche:{}".format(quantity))
				#对倒 边 夹 单吊
				#对倒
				removeMatchOrderDict = utility.getRemoveMatchOrderDict(handTilesButKing, finalTile, self.kingTiles)
				for key in removeMatchOrderDict:
					useKingNum = removeMatchOrderDict[key]
					if removeCheckPairWin(handTilesButKing, key, useKingNum, kingTilesNum):
						quantity += 1
						result[11] = 1
						DEBUG_MSG("duidao:{}".format(quantity))
						break
				else:
					if not isPongPongWin:
						#边
						removeEdgeDict = utility.getRemoveEdgeDict(handTilesButKing, finalTile, self.kingTiles)
						for key in removeEdgeDict:
							useKingNum = removeEdgeDict[key]
							if removeCheckPairWin(handTilesButKing, key, useKingNum, kingTilesNum):
								quantity += 1
								result[12] = 1
								DEBUG_MSG("bian:{}".format(quantity))
								break
						else:
							#夹
							removeMidDict = utility.getRemoveMidDict(handTilesButKing, finalTile, self.kingTiles)
							for key in removeMidDict:
								useKingNum = removeMidDict[key]
								if removeCheckPairWin(handTilesButKing, key, useKingNum, kingTilesNum):
									quantity += 1
									result[13] = 1
									DEBUG_MSG("jia:{}".format(quantity))
									break
							else:
								#单吊
								removeSingleCraneDict = utility.getRemoveSingleCraneDict(handTilesButKing, finalTile, self.kingTiles)
								for key in removeSingleCraneDict:
									useKingNum = removeSingleCraneDict[key]
									if removeCheckOnlyWin(handTilesButKing, key, useKingNum, kingTilesNum):
										quantity += 1
										result[14] = 1
										DEBUG_MSG("dandiao:{}".format(quantity))
										break
				# 花 手牌 桌牌 非胡台数
				quantity += utility.getWreathQuantity(wreaths, p_wind)
				DEBUG_MSG("wreaths:{}".format(quantity))
				quantity += utility.getHandTileQuantityWindDragons(handTilesButKing, kingTilesNum, p_wind, self.prevailing_wind)
				DEBUG_MSG("handTilesButKing:{}".format(quantity))
				quantity += utility.getUpTileQuantity(uptiles, p_wind, self.prevailing_wind)
				DEBUG_MSG("uptiles:{}".format(quantity))
				
				isWinLimited = True
				#碰碰胡？
				if isPongPongWin:
					quantity += 2
					result[1] = 1
					isWinLimited = False
					DEBUG_MSG("PongPongWin:{}".format(quantity))
				#清一色 字一色 混一色
				colorType = utility.getTileColorType(handTilesButKing, uptiles)
				if colorType == const.SAME_SUIT:
					quantity += 6
					result[8] = 1
					isWinLimited = False
					DEBUG_MSG("qingyise:{}".format(quantity))
				elif colorType == const.SAME_HONOR:
					quantity = 40
					result = [0] * 17
					result[9] = 1
					isWinLimited = False
					DEBUG_MSG("ziyise:{}".format(quantity))
				elif colorType == const.MIXED_ONE_SUIT:
					quantity += 2
					result[10] = 1
					isWinLimited = False
					DEBUG_MSG("hunyise:{}".format(quantity))

				if isWinLimited:
					quantity = 0

				baseMul = 4 if len(wreaths) == 8 else 1
				quantity = quantity * baseMul
				#天胡
				if idx == self.dealer_idx and not utility.checkIsDiscard(self.op_record) and quantity >= self.win_quantity:
					quantity += 16 * baseMul
					result[2] = 1
					DEBUG_MSG("tianhu:{}".format(quantity))
			elif utility.getTileColorType(handTilesButKing, uptiles) == const.SAME_HONOR:
				DEBUG_MSG('SAME_HONOR')
				baseMul = 4 if len(wreaths) == 8 else 1
				quantity = 20 * baseMul
				result[16] = 1
				#天胡
				if idx == self.dealer_idx and not utility.checkIsDiscard(self.op_record) and quantity >= self.win_quantity:
					quantity += 16 * baseMul
					result[2] = 1
					DEBUG_MSG("tianhu:{}".format(quantity))
		#判断台数
		return quantity, result