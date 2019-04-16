# -*- coding: utf-8 -*-


PUBLISH_VERSION = 0

DEBUG_BASE = 1

PHP_SERVER_URL = 'http://10.0.0.4:9981/api/'
PHP_SERVER_SECRET = "zDYnetiVvFgWCRMIBGwsAKaqPOUjfNXS"

#计算消耗
def calc_cost(game_round, player_num, pay_mode):
	if pay_mode == 0:
		return (game_round / 4, game_round / 4)
	else:
		return (game_round, game_round)
	return (8, 100)