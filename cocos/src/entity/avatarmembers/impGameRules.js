"use strict";
/*-----------------------------------------------------------------------------------------
												interface
-----------------------------------------------------------------------------------------*/
var impGameRules = impGameOperation.extend({
	__init__ : function()
	{
		this._super();
		this.allTiles = const_val.CHARACTER.concat(const_val.BAMBOO);
  	this.allTiles = this.allTiles.concat(const_val.DOT);
  	this.allTiles.push(const_val.DRAGON_RED);
    // this.meld_history = {};
	  KBEngine.DEBUG_MSG("Create impGameRules");
  	},

  	getCanWinTiles:function(){
      return [];
      //听牌提示
  		var canWinTiles = [];
  		for(var i = 0; i < this.allTiles.length; i++){
  			var handTiles = this.curGameRoom.handTilesList[this.serverSitNum].concat([this.allTiles[i]]);
  			if(this.canWin(handTiles)){
  				canWinTiles.push(this.allTiles[i]);
  			}
  		}
  		return canWinTiles;
  	},

  	canConcealedKong:function(tiles){
      //暗杠
  		if(this.getOneConcealedKongNum(tiles) > 0){
        return true;
      } else {
        return false;
      }
  	},

    getOneConcealedKongNum:function(tiles){
      var hashDict = {};
      for(var i = 0; i < tiles.length; i++){
        if (this.curGameRoom.kingTiles.indexOf(tiles[i]) >= 0) {continue;}
        if(hashDict[tiles[i]]){
          hashDict[tiles[i]]++;
          if(hashDict[tiles[i]] >= 4){
            return tiles[i];
          }
        } else {
          hashDict[tiles[i]] = 1;
        }
      }
      return 0;
    },

  	canExposedKong:function(tiles, lastTile){
      if (this.curGameRoom.kingTiles.indexOf(lastTile) >= 0) {return false;}
  		var tile = 0;
  		for(var i = 0; i < tiles.length; i++){
  			if(tiles[i] == lastTile){
  				tile++;
  			}
  		}
  		if(tile >= 3){
  			return true;
  		}
  		return false;
  	},

  	canSelfExposedKong:function(upTilesList, drawTile){
  		if(this.getSelfExposedKongIdx(upTilesList, drawTile) >= 0){
  			return true;
  		}
  		return false;
  	},

  	getSelfExposedKongIdx:function(upTilesList, drawTile){
      if (this.curGameRoom.kingTiles.indexOf(drawTile) >= 0) {return -1;}
  		for(var i = 0; i < upTilesList.length; i++){
  			if(upTilesList[i].length == 3 && drawTile == upTilesList[i][0] && 
  				upTilesList[i][0] == upTilesList[i][1] && upTilesList[i][1] == upTilesList[i][2]){
  				return i;
  			}
  		}
  		return -1;
  	},

    canSelfRiskKong: function (upTilesList, handTiles) {
        if (upTilesList.length == 0) {return -1;}
        var upKongTile = [];
        for (var i = 0; i < upTilesList.length; i++) {
            if (upTilesList[i].length == 3 && upTilesList[i][0] == upTilesList[i][1] && upTilesList[i][1] == upTilesList[i][2]) {
                upKongTile.push(upTilesList[i][0]);
            }
        }

        if (upKongTile.length == 0) {
            return -1;
        }else{
            for (var i = 0; i < handTiles.length; i++) {
                if (upKongTile.indexOf(handTiles[i]) >= 0) {
                    return i;
                }
            }
        }
        return -1;
    },

  	canPong:function(tiles, lastTile){
      if (this.curGameRoom.kingTiles.indexOf(lastTile) >= 0) {return false;}
      // 正常碰牌逻辑
  		var tile = 0;
  		for(var i = 0; i < tiles.length; i++){
  			if(tiles[i] == lastTile){
  				tile++;
  			}
  		}
  		if(tile >= 2){
  			return true;
  		}
  		return false;
  	},

    getCanChowTilesList:function(lastTile){
      return false
    },

    canChow:function(tiles, lastTile){
      return false;
    },

  	// canWin:function(tiles){
  	// 	if (tiles.length % 3 != 2){
			// return false;
  	// 	}

   //    tiles = tiles.concat([]).sort(function(a, b){return a-b;});

  	// 	var tilesInfo = this.classifyTiles(tiles);
  	// 	var chars = tilesInfo[0];
  	// 	var bambs = tilesInfo[1];
  	// 	var dots = tilesInfo[2];
  	// 	var dragon_red = tilesInfo[3];
  	// 	var c_need1 = cutil.meld_only_need_num(chars, cutil.meld_history);
  	// 	var c_need2 = cutil.meld_with_pair_need_num(chars, cutil.meld_history);
  	// 	if (c_need1 > dragon_red && c_need2 > dragon_red){
  	// 		return false;
  	// 	}

  	// 	var b_need1 = cutil.meld_only_need_num(bambs, cutil.meld_history);
  	// 	var b_need2 = cutil.meld_with_pair_need_num(bambs, cutil.meld_history);
  	// 	if (b_need1 > dragon_red && b_need2 > dragon_red){
  	// 		return false;
  	// 	}

  	// 	var d_need1 = cutil.meld_only_need_num(dots, cutil.meld_history);
  	// 	var d_need2 = cutil.meld_with_pair_need_num(dots, cutil.meld_history);
  	// 	if (d_need1 > dragon_red && d_need2 > dragon_red){
  	// 		return false;
  	// 	}

  	// 	if(	(c_need2 + b_need1 + d_need1) <= dragon_red ||
  	// 		(c_need1 + b_need2 + d_need1) <= dragon_red ||
  	// 		(c_need1 + b_need1 + d_need2) <= dragon_red){
  	// 		return true;
  	// 	}
  	// 	return false;
  	// },
    
    canWin:function(handTiles, finalTile, win_op){
      for (var i = 0; i < handTiles.length; i++) {
        var tile = handTiles[i]
        if (const_val.SEASON.indexOf(tile) >= 0 && const_val.FLOWER.indexOf(tile) >= 0) {
          cc.log("can not win,bcz of have season or flower.")
          return false
        }
      }
      var copyTiles = handTiles.concat([]).sort(function(a,b){return a-b;})
      var quantity = this.getCanWinQuantity(copyTiles, finalTile, win_op)
      cc.log('canWin', quantity)
      if (quantity >= this.curGameRoom.win_quantity) {
        return true
      }
      // return true
      return false
    },

    getCanWinQuantity:function(handTiles, finalTile, win_op){
      cc.log(handTiles, finalTile, win_op)
      var discardTilesList = this.curGameRoom.discardTilesList
      var upTilesOpsList = this.curGameRoom.upTilesOpsList
      var cutIdxsList = this.curGameRoom.cutIdxsList
      var wreaths = this.curGameRoom.wreathsList[this.serverSitNum]
      var p_wind = this.curGameRoom.playerWindList[this.serverSitNum]
      var prevailing_wind = this.curGameRoom.prevailing_wind
      var uptiles = this.curGameRoom.upTilesList[this.serverSitNum]

      function removeCheckPairWin(handTilesButKing, removeList, useKingNum, kingTilesNum) {
        if (useKingNum <= kingTilesNum) {
          var tryHandTilesButKing = handTilesButKing.concat([])
          for (var i = 0; i < removeList.length; i++) {
            var t = removeList[i]
            if (t != -1) {
              tryHandTilesButKing.splice(tryHandTilesButKing.indexOf(t), 1)
            }
          }
          if (cutil.meld_with_pair_need_num(tryHandTilesButKing, {}) <= kingTilesNum - useKingNum) {
            return true
          }
        }
        return false
      }
      function removeCheckOnlyWin(handTilesButKing, removeList, useKingNum, kingTilesNum) {
        if (useKingNum <= kingTilesNum) {
          var tryHandTilesButKing = handTilesButKing.concat([])
          for (var i = 0; i < removeList.length; i++) {
            var t = removeList[i]
            if (t != -1) {
              tryHandTilesButKing.splice(tryHandTilesButKing.indexOf(t), 1)
            }
          }
          if (cutil.meld_only_need_num(tryHandTilesButKing, {}) <= kingTilesNum - useKingNum) {
            return true
          }
        }
        return false
      }

      var quantity = 0
      var classifyList = cutil.classifyTiles(handTiles, this.curGameRoom.kingTiles)
      var kingTilesNum = classifyList[0].length
      var handTilesButKing = []
      for (var i = 1; i < classifyList.length; i++) {
        handTilesButKing = handTilesButKing.concat(classifyList[i])
      }
      if (win_op == const_val.OP_WREATH_WIN) { //8 张花
        if (wreaths.length == 8) {
          quantity += cutil.getWreathQuantity(wreaths, p_wind)
          cc.log('8张花胡', quantity)
        }
      }else if (handTiles.length % 3 == 2) { //其他3X2胡 
        cc.log("其他3X2胡：")
        cc.log(handTilesButKing, cutil.meld_with_pair_need_num(handTilesButKing, {}), kingTilesNum)
        var isCanWin = false
        if (cutil.meld_with_pair_need_num(handTilesButKing, {}) <= kingTilesNum || cutil.getTileColorType(handTilesButKing, uptiles) == const_val.SAME_HONOR) {
          isCanWin = true
          var isPongPongWin = cutil.checkIsPongPongWin(handTilesButKing, uptiles, kingTilesNum)
          //自摸
          if (win_op == const_val.OP_DRAW_WIN) {
            quantity += 1
            cc.log('自摸胡,台数:' + String(quantity))
          }else if (win_op == const_val.OP_KONG_WIN){
            quantity += 1
            cc.log('抢杠胡,台数:' + String(quantity))
          }
          //杠上开花
          if (win_op == const_val.OP_DRAW_WIN && cutil.getNearlyKongType(upTilesOpsList, discardTilesList, cutIdxsList, this.serverSitNum) > 0) {
            quantity += 1
            cc.log('杠上开花,台数:' + String(quantity))
          }
          //硬胡
          if (kingTilesNum <= 0) {
            quantity += 1
            cc.log('硬胡,台数:' + String(quantity))
          }
          //海捞
          if (this.curGameRoom.leftTileNum <= 0) {
            quantity += 1
            cc.log('海捞胡,台数:' + String(quantity))
          }
          //大吊
          if (handTiles.length == 2) {
            quantity += 1
            cc.log('大吊,台数:' + String(quantity))
          }

          //对倒 边 夹 单吊
          //对倒
          var removeMatchOrderDict = cutil.getRemoveMatchOrderDict(handTilesButKing, finalTile, this.curGameRoom.kingTiles)
          var isMatchOrder = false
          for (var key in removeMatchOrderDict) {
            key = eval("[" +key + "]")
            var useKingNum = removeMatchOrderDict[key]
            if (removeCheckPairWin(handTilesButKing, key, useKingNum, kingTilesNum)) {
              quantity += 1
              isMatchOrder = true
              cc.log("对倒,台数:"+String(quantity))
              break
            }
          }
          if (!isPongPongWin && !isMatchOrder) {
            //边
            var removeEdgeDict = cutil.getRemoveEdgeDict(handTilesButKing, finalTile, this.curGameRoom.kingTiles)
            var isEdge = false
            for (var key in removeEdgeDict) {
              key = eval("[" +key + "]")
              useKingNum = removeEdgeDict[key]
              if (removeCheckPairWin(handTilesButKing, key, useKingNum, kingTilesNum)) {
                quantity += 1
                isEdge = true
                cc.log("边,台数:"+String(quantity))
                break
              }
            }
            // 夹
            var isMid = false
            if (!isEdge) {
              var removeMidDict = cutil.getRemoveMidDict(handTilesButKing, finalTile, this.curGameRoom.kingTiles)
              for (var key in removeMidDict) {
                key = eval("[" +key + "]")
                useKingNum = removeMidDict[key]
                if (removeCheckPairWin(handTilesButKing, key, useKingNum, kingTilesNum)) {
                  quantity += 1
                  isMid = true
                  cc.log("夹,台数:"+String(quantity))
                  break
                }
              }
            }
            // 单吊
            if (!isEdge && !isMid) {
              var removeSingleCraneDict = cutil.getRemoveSingleCraneDict(handTilesButKing, finalTile, this.curGameRoom.kingTiles)
              for (var key in removeSingleCraneDict) {
                key = eval("[" + key + "]")
                useKingNum = removeSingleCraneDict[key]
                if (removeCheckOnlyWin(handTilesButKing, key, useKingNum, kingTilesNum)) {
                  quantity += 1
                  cc.log("单吊,台数:"+String(quantity))
                  break
                }
              }
            }
          }
          //花 手牌 桌牌 非胡台数
          quantity += cutil.getWreathQuantity(wreaths, p_wind)
          cc.log("花,台数:"+String(quantity))
          quantity += cutil.getHandTileQuantityWindDragons(handTilesButKing, kingTilesNum, p_wind, prevailing_wind);
          cc.log("手牌,台数:"+String(quantity))
          quantity += cutil.getUpTileQuantity(uptiles, p_wind, prevailing_wind)
          cc.log("桌牌,台数:"+String(quantity))

          var isWinLimited = true
          //碰碰胡?
          if (isPongPongWin) {
            quantity += 2
            isWinLimited = false
            cc.log('碰碰胡,台数:' + String(quantity))
          }
          
          //清一色 字一色 混一色
          var colorType = cutil.getTileColorType(handTilesButKing, uptiles)
          if (colorType == const_val.SAME_SUIT) {
            quantity += 6
            isWinLimited = false
            cc.log("清一色,台数:"+String(quantity))
          } else if(colorType == const_val.SAME_HONOR){
            quantity = 40
            isWinLimited = false
            cc.log("字一色(全风字),台数:"+String(quantity))
          } else if (colorType == const_val.MIXED_ONE_SUIT) {
            quantity += 2
            isWinLimited = false
            cc.log("混一色,台数:"+String(quantity))
          }
          //非碰混清不能胡
          if (isWinLimited) {
            quantity = 0
          }
          var baseMul = wreaths.length == 8 ? 4 : 1 //8花 结果乘以4倍
          quantity = quantity * baseMul
          // 天胡
          var discardNum = cutil.getDiscardNum(discardTilesList, upTilesOpsList, cutIdxsList, this.serverSitNum)
          if (discardNum <= 0 && this.serverSitNum == this.curGameRoom.dealerIdx && quantity >= this.curGameRoom.win_quantity) {
            quantity += 16 * baseMul
            cc.log('天胡,台数:' + String(quantity))
          }
        } else if(cutil.getTileColorType(handTilesButKing, uptiles) == const_val.SAME_HONOR){
          cc.log("字一色(乱风字)")
          var baseMul = wreaths.length == 8 ? 4 : 1 //8花 结果乘以4倍
          quantity = 20 * baseMul
          // 天胡必须 满足 大于最低胡牌台数才可以胡
          var discardNum = cutil.getDiscardNum(discardTilesList, upTilesOpsList, cutIdxsList, this.serverSitNum)
          if (discardNum <= 0 && this.serverSitNum == this.curGameRoom.dealerIdx && quantity >= this.curGameRoom.win_quantity) {
            quantity += 16 * baseMul
            cc.log('天胡,台数:' + String(quantity))
          }
        }
      }
      return quantity
    },
});
