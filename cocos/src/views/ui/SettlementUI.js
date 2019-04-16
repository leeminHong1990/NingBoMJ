var SettlementUI = UIBase.extend({
	ctor:function() {
		this._super();
		this.resourceFilename = "res/ui/SettlementUI.json";
	},
	initUI:function(){
		var player = h1global.entityManager.player();
		var self = this;
		var confirm_btn = this.rootUINode.getChildByName("confirm_btn");
		function confirm_btn_event(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				// TEST:
				// self.hide();
				// h1global.curUIMgr.gameroomprepare_ui.show();
				// h1global.curUIMgr.gameroom_ui.hide();
				// return;
				self.hide();

				//重新开局
				player.curGameRoom.updatePlayerState(player.serverSitNum, 1);
				// player.curGameRoom.curRound = player.curGameRoom.curRound + 1;
				h1global.curUIMgr.gameroomprepare_ui.show();
				h1global.curUIMgr.gameroom_ui.hide();
				player.roundEndCallback();
			}
		}
		confirm_btn.addTouchEventListener(confirm_btn_event);
		this.kongTilesList = [[], [], [], []];

		var settlement_panel = this.rootUINode.getChildByName("settlement_panel");
		var settlement_bg_panel = this.rootUINode.getChildByName("settlement_bg_panel");
		var show_btn = this.rootUINode.getChildByName("show_btn");
		var hide_btn = this.rootUINode.getChildByName("hide_btn");
		show_btn.addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				show_btn.setVisible(false);
				hide_btn.setVisible(true);
				settlement_panel.setVisible(true);
				settlement_bg_panel.setVisible(true);
			}
		});
		show_btn.setVisible(false);
		hide_btn.addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				show_btn.setVisible(true);
				hide_btn.setVisible(false);
				settlement_panel.setVisible(false);
				settlement_bg_panel.setVisible(false);
			}
		});
	},
	
	show_by_info:function(roundRoomInfo, confirm_btn_func){
		cc.log("结算==========>:")
		cc.log("roundRoomInfo :  ",roundRoomInfo)
		var self = this;	
		this.show(function(){
			self.player_tiles_panels = [];
			self.player_tiles_panels.push(self.rootUINode.getChildByName("settlement_panel").getChildByName("victory_item_panel1"));
			self.player_tiles_panels.push(self.rootUINode.getChildByName("settlement_panel").getChildByName("victory_item_panel2"));
			self.player_tiles_panels.push(self.rootUINode.getChildByName("settlement_panel").getChildByName("victory_item_panel3"));
			self.player_tiles_panels.push(self.rootUINode.getChildByName("settlement_panel").getChildByName("victory_item_panel4"));	
			var playerInfoList = roundRoomInfo["player_info_list"];
			for(var i = 0; i < 4; i++){
				var roundPlayerInfo = playerInfoList[i];
				if (!roundPlayerInfo) {
					self.player_tiles_panels[i].setVisible(false)
					continue
				}
				self.player_tiles_panels[i].setVisible(true)
				self.update_score(roundPlayerInfo["idx"], roundPlayerInfo["score"]);  //显示分数
                self.update_player_hand_tiles(i, roundRoomInfo["player_info_list"][i]["tiles"], roundRoomInfo["win_idx_list"]);   //显示麻将
                self.update_player_up_tiles(i, roundRoomInfo["player_info_list"][i]["concealed_kong"]);
                self.update_player_info(roundPlayerInfo["idx"]);  //idx 表示玩家的座位号
			}

			self.show_title(roundRoomInfo["win_idx_list"])

			if (roundRoomInfo["win_idx_list"][0] >= 0) {
				for(var i = 0; i < roundRoomInfo["win_idx_list"].length; i++){
					self.update_player_win(roundRoomInfo["win_idx_list"][i], roundRoomInfo["player_info_list"][roundRoomInfo["win_idx_list"][i]]["tiles"], roundRoomInfo["result_list"][i]);
				}
			}
			
			if(confirm_btn_func){
				self.rootUINode.getChildByName("confirm_btn").addTouchEventListener(function(sender, eventType){
					if(eventType ==ccui.Widget.TOUCH_ENDED){
						self.hide();
						confirm_btn_func();
					}
				});
			}
		});
	},

	show_title:function(win_idx_list){
		cc.log(win_idx_list);
        var title_img = this.rootUINode.getChildByName("settlement_panel").getChildByName("title_img");
        title_img.ignoreContentAdaptWithSize(true);
        var win_sum = 0;
        for (var i = 0; i < win_idx_list.length; i++) {
            if (win_idx_list[i] >= 0) {
                win_sum++;
            }
        }
        if (win_sum === 0) {
            title_img.loadTexture("res/ui/SettlementUI/dogfull_title.png")
        } else {
            if (win_idx_list.indexOf(h1global.entityManager.player().serverSitNum) >= 0) {
                //shengli
                title_img.loadTexture("res/ui/SettlementUI/win_title.png")
            } else {
                title_img.loadTexture("res/ui/SettlementUI/fail_title.png")
            }
        }
	},

	update_player_hand_tiles:function(serverSitNum, tileList, win_idx_list){
		if(!this.is_show) {return;}
		var player = h1global.entityManager.player();
		var cur_player_tile_panel = this.player_tiles_panels[serverSitNum].getChildByName("item_hand_panel");
		if(!cur_player_tile_panel){
			return;
		}
        // tileList = tileList.sort(cutil.tileSortFunc);
		if(win_idx_list.indexOf(serverSitNum) >= 0){
			var temp_tile = tileList.pop();
			tileList = tileList.sort(cutil.tileSortFunc);
			tileList.push(temp_tile);
		}else {
			tileList = tileList.sort(cutil.tileSortFunc);
		}
		var mahjong_hand_str = "";
        cur_player_tile_panel.setPositionX((player.curGameRoom.upTilesList[serverSitNum].length * 180) + 280);
		mahjong_hand_str = "mahjong_tile_player_hand.png";
		for(var i = 0; i < 14; i++){
			var tile_img = ccui.helper.seekWidgetByName(cur_player_tile_panel, "mahjong_bg_img" + i.toString());
			tile_img.stopAllActions();
			if(tileList[i]){
				var mahjong_img = tile_img.getChildByName("mahjong_img");
				tile_img.loadTexture("Mahjong/" + mahjong_hand_str, ccui.Widget.PLIST_TEXTURE);
				tile_img.setVisible(true);
				mahjong_img.ignoreContentAdaptWithSize(true);
				mahjong_img.loadTexture("Mahjong/mahjong_big_" + tileList[i].toString() + ".png", ccui.Widget.PLIST_TEXTURE);
				mahjong_img.setVisible(true);
				if(win_idx_list.indexOf(serverSitNum) >= 0 && i === tileList.length - 1){
					tile_img.setPositionX(tile_img.getPositionX() + 20);
				}
                if(player.curGameRoom.kingTiles.indexOf(tileList[i]) >= 0){
                    var kingtilemark_img = ccui.ImageView.create("res/ui/GameRoomUI/kingtilemark.png");
                    // this.handTileMarksList[idx].push(kingtilemark_img);
                    kingtilemark_img.setAnchorPoint(0.0, 1.0);
                    kingtilemark_img.setPosition(cc.p(0, 90));
                    kingtilemark_img.setScale(0.7);
                    tile_img.addChild(kingtilemark_img);
                }
			} else {
				tile_img.setVisible(false);
			}
		}
	},

	update_player_up_tiles:function(serverSitNum, concealedKongList){
		if(!this.is_show) {return;}
		var player = h1global.entityManager.player();
        var cur_player_tile_panel = this.player_tiles_panels[serverSitNum].getChildByName("item_up_panel");
		// var cur_player_tile_panel = this.rootUINode.getChildByName("settlement_panel").getChildByName("player_tile_panel").getChildByName("player_up_panel");
		if(!cur_player_tile_panel){
			return;
		}
		// var mahjong_hand_str = "";
		var mahjong_up_str = "";
		var mahjong_down_str = "";
		// var mahjong_desk_str = "";
		// if(idx == 0){
		// 	mahjong_hand_str = "mahjong_tile_player_hand.png";
		// 	mahjong_up_str = "mahjong_tile_player_up.png";
		// 	mahjong_down_str = "mahjong_tile"
		// }
		for(var i = player.curGameRoom.upTilesList[serverSitNum].length * 3; i < 12; i++){
			var tile_img = ccui.helper.seekWidgetByName(cur_player_tile_panel, "mahjong_bg_img" + i.toString());
			tile_img.setVisible(false);
		}
		for(var i = 0; i < this.kongTilesList[serverSitNum].length; i++){
			this.kongTilesList[serverSitNum][i].removeFromParent();
		}
		this.kongTilesList[serverSitNum] = [];
		// mahjong_hand_str = "mahjong_tile_player_hand.png";
		mahjong_up_str = "mahjong_tile_player_up.png";
		mahjong_down_str = "mahjong_tile_player_down.png";
		// mahjong_desk_str = "mahjong_tile_player_desk.png";
		for(var i = 0; i < player.curGameRoom.upTilesList[serverSitNum].length; i++){
			for(var j = 0; j < 3; j++){
				var tile_img = ccui.helper.seekWidgetByName(cur_player_tile_panel, "mahjong_bg_img" + (3*i + j).toString());
				// tile_img.setPositionY(0);
				tile_img.setTouchEnabled(false);
				var mahjong_img = tile_img.getChildByName("mahjong_img");
				if(player.curGameRoom.upTilesList[serverSitNum][i][j]){
					tile_img.loadTexture("Mahjong/" + mahjong_up_str, ccui.Widget.PLIST_TEXTURE);
					mahjong_img.ignoreContentAdaptWithSize(true);
					mahjong_img.loadTexture("Mahjong/mahjong_small_" + player.curGameRoom.upTilesList[serverSitNum][i][j].toString() + ".png", ccui.Widget.PLIST_TEXTURE);
					mahjong_img.setVisible(true);
				} else {
					tile_img.loadTexture("Mahjong/" + mahjong_down_str, ccui.Widget.PLIST_TEXTURE);
					mahjong_img.setVisible(false);
				}
				tile_img.setVisible(true);
			}
			if(player.curGameRoom.upTilesList[serverSitNum][i].length > 3){
				var tile_img = ccui.helper.seekWidgetByName(cur_player_tile_panel, "mahjong_bg_img" + (3*i + 1).toString());
				var kong_tile_img = tile_img.clone();
				this.kongTilesList[serverSitNum].push(kong_tile_img);
				var mahjong_img = kong_tile_img.getChildByName("mahjong_img");
				if(player.curGameRoom.upTilesList[serverSitNum][i][3]){
					kong_tile_img.loadTexture("Mahjong/" + mahjong_up_str, ccui.Widget.PLIST_TEXTURE);
					mahjong_img.ignoreContentAdaptWithSize(true);
					mahjong_img.loadTexture("Mahjong/mahjong_small_" + player.curGameRoom.upTilesList[serverSitNum][i][j].toString() + ".png", ccui.Widget.PLIST_TEXTURE);
					mahjong_img.setVisible(true);
				} else {
					if(concealedKongList[0]){
						kong_tile_img.loadTexture("Mahjong/" + mahjong_up_str, ccui.Widget.PLIST_TEXTURE);
						mahjong_img.ignoreContentAdaptWithSize(true);
						mahjong_img.loadTexture("Mahjong/mahjong_small_" + concealedKongList[0].toString() + ".png", ccui.Widget.PLIST_TEXTURE);
						concealedKongList.splice(0, 1);
						mahjong_img.setVisible(true);
					} else {
						kong_tile_img.loadTexture("Mahjong/" + mahjong_down_str, ccui.Widget.PLIST_TEXTURE);
						mahjong_img.setVisible(false);
					}
				}
				kong_tile_img.setPositionY(kong_tile_img.getPositionY() + 16);
				kong_tile_img.setVisible(true);
				cur_player_tile_panel.addChild(kong_tile_img);
			}
		}
	},

	update_player_info:function(serverSitNum){
		if(!this.is_show) {return;}
		cc.log("update_player_info", serverSitNum)
		var player = h1global.entityManager.player();
		var cur_player_info_panel = this.player_tiles_panels[serverSitNum];
		cc.log(cur_player_info_panel)
		if(!cur_player_info_panel){
			return;
		}
		var playerInfo = player.curGameRoom.playerInfoList[serverSitNum];
		cur_player_info_panel.getChildByName("item_name_label").setString(playerInfo["nickname"]);
		// var frame_img = ccui.helper.seekWidgetByName(cur_player_info_panel, "frame_img");
		// cur_player_info_panel.reorderChild(frame_img, 1);
		cutil.loadPortraitTexture(playerInfo["head_icon"], function(img){
			if (cur_player_info_panel.getChildByName("item_avatar_img")) {
				cur_player_info_panel.getChildByName("item_avatar_img").removeFromParent();
			}
			var portrait_sprite  = new cc.Sprite(img);
			portrait_sprite.setName("portrait_sprite");
			portrait_sprite.setScale(67 / portrait_sprite.getContentSize().width);
            portrait_sprite.x = 145;
            portrait_sprite.y = 45;
			cur_player_info_panel.addChild(portrait_sprite);
			portrait_sprite.setLocalZOrder(-1);
			// frame_img.setLocalZOrder(0);
		}, playerInfo["uuid"].toString() + ".png");
	},

	update_player_win:function(serverSitNum, handTiles, result){
		if(serverSitNum < 0 || serverSitNum > 3){
			return;
		}
        var player = h1global.entityManager.player();
		var cur_player_info_panel = this.player_tiles_panels[serverSitNum];
		var win_type_img_list = [];
		for (var i = 1; i <= 7; i++) {
			var img = cur_player_info_panel.getChildByName("item_card_type_img" + String(i));
			win_type_img_list.push(img);
		}
		var index = 0;
		var quantity_list =  [10,2,16,1,1,1,1,1,6,40,2,1,1,1,1,1,20,0,0,0,0];
		for (var i = 0; i < result.length; i++) {
			if (index >= win_type_img_list.length) {break}
			if (result[i]) {
				cc.log(i, index);
				win_type_img_list[index].loadTexture("res/ui/SettlementUI/win_type_" + String(i) +".png");
				win_type_img_list[index].setVisible(true);
                this.create_label(quantity_list[i], index, win_type_img_list);
				index += 1;
			}
		}

        var classifyList = cutil.classifyTiles(handTiles, player.curGameRoom.kingTiles);
        var kingTilesNum = classifyList[0].length
        var handTilesButKing = [];
        for (var i = 1; i < classifyList.length; i++) {
            handTilesButKing = handTilesButKing.concat(classifyList[i]);
        }
        var uptiles = player.curGameRoom.upTilesList[serverSitNum];
        var wreaths = player.curGameRoom.wreathsList[serverSitNum];
        var p_wind = player.curGameRoom.playerWindList[serverSitNum];
        var prevailing_wind = player.curGameRoom.prevailing_wind;
		//花台数
        quantity_list[20] = 0 + cutil.getWreathQuantity(wreaths, p_wind);
        //碰牌杠牌中位风、圈风、中发白刻
        for (var i = 0; i < uptiles.length; i++) {
            var tileList = uptiles[i];
            if (tileList.indexOf(prevailing_wind) >= 0) {
                quantity_list[17] += 1;
            }
            if (tileList.indexOf(p_wind) >= 0) {
                quantity_list[18] += 1;
            }
            if (const_val.DRAGONS.indexOf(parseInt(tileList[0] == 0 ? tileList[3] : tileList[0])) >= 0) {
                quantity_list[19] += 1;
            }
        }
        //手牌中位风、圈风
        var temp_list = [prevailing_wind, p_wind, const_val.DRAGON_RED, const_val.DRAGON_GREEN, const_val.DRAGON_WHITE];
        var temp_kingNum = kingTilesNum;
        var temp_handTilesButKing = handTilesButKing.concat([]);
        var is_run_temp_list = false;
        for(var i = 0; i < temp_list.length; i++){
            if(handTilesButKing.indexOf(temp_list[i]) >= 0){
                var tile2NumDict = cutil.getTileNumDict(handTilesButKing);
                if(tile2NumDict[temp_list[i]] == 1 && kingTilesNum >= 2){
                    handTilesButKing.push(temp_list[i]);
                    handTilesButKing.push(temp_list[i]);
                    kingTilesNum -= 2;
                }else if(tile2NumDict[temp_list[i]] == 2 && kingTilesNum >= 1){
                    handTilesButKing.push(temp_list[i]);
                    kingTilesNum -= 1;
                }
            }
        }
        if (cutil.meld_with_pair_need_num(handTilesButKing, {}) <= kingTilesNum) {
            is_run_temp_list = true;
            var tile2Dict = cutil.getTileNumDict(handTilesButKing);
            for (var t in tile2Dict) {
                if (tile2Dict[t] >= 3) {
                    if (t == prevailing_wind) {
                        quantity_list[17] += 1;//圈风
                    }
                    if (t == p_wind) {
                        quantity_list[18] += 1;
                    }
                    if (const_val.DRAGONS.indexOf(parseInt(t)) >= 0) {
                        quantity_list[19] += 1;
                    }
                }
            }
        }
        handTilesButKing = temp_handTilesButKing;
        kingTilesNum = temp_kingNum;
        if(!is_run_temp_list) {
            var tile2NDict = cutil.getTileNumDict(handTilesButKing);
            for (var t in tile2NDict) {
                if (tile2NDict[t] >= 3) {
                    if (t == prevailing_wind) {
                        quantity_list[17] += 1;//圈风
                    }
                    if (t == p_wind) {
                        quantity_list[18] += 1;
                    }
                    if (const_val.DRAGONS.indexOf(t) >= 0) {
                        quantity_list[19] += 1;
                    }
                }
            }
        }
        for(var i = 17; i < 21 ; i++){
            if(quantity_list[i] > 0 && index <= 6){
            	if(result[9] || result[16]){
            		break;
				}
                if(i === 4 && quantity_list[i] === 10){
                    continue;
                }
                this.create_label(quantity_list[i], index, win_type_img_list);
                win_type_img_list[index].loadTexture("res/ui/SettlementUI/win_type_"+ (i).toString() +".png");
                win_type_img_list[index].setVisible(true);
                index += 1;
            }
        }
        cc.log("quantity_list:",quantity_list);
	},

    create_label:function (cannon_num, index, win_type_img_list) {
        if(!cannon_num){
            return;
        }
        var cannon_label = new cc.LabelTTF("", "Arial", 30);
        cannon_label.setAnchorPoint(0, 0.5);
        cannon_label.setColor(cc.color(255, 255, 0));
        cannon_label.setString(cannon_num.toString() + "台");
        cannon_label.setVisible(true);
        cannon_label.setPosition(cc.p(win_type_img_list[index].getContentSize().width, win_type_img_list[index].getContentSize().height * 0.45));
        win_type_img_list[index].addChild(cannon_label);
    },

	update_score:function(serverSitNum, score){
		var score_label = this.player_tiles_panels[serverSitNum].getChildByName("item_score_label");
		if(score >= 0){
			score_label.setTextColor(cc.color(62, 121, 77));
			score_label.setString("+" + score.toString());
		} else {
			score_label.setTextColor(cc.color(144, 71, 64));
			score_label.setString(score.toString());
		}
	},
});