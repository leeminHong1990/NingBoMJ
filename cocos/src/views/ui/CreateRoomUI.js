// var UIBase = require("src/views/ui/UIBase.js")
// cc.loader.loadJs("src/views/ui/UIBase.js")
"use strict"
var CreateRoomUI = UIBase.extend({
	ctor:function() {
		this._super();
		this.resourceFilename = "res/ui/CreateRoomUI.json";
	},

	initUI:function(){
        if (cc.sys.localStorage.getItem("CHX_LIST") === null) {
            cc.sys.localStorage.setItem("CHX_LIST", "4,0,4,4,2");
        }
        var chx_list = cc.sys.localStorage.getItem("CHX_LIST").split(",");
		this.player_num = parseInt(chx_list[0]);
        this.pay_mode = parseInt(chx_list[1]);   //0是AA支付，1是房主支付
		this.win_num = parseInt(chx_list[2]);
		this.round_num = parseInt(chx_list[3]);
		this.king_num = parseInt(chx_list[4]);
		this.createroom_panel = this.rootUINode.getChildByName("createroom_panel");
		this.initCreateRoomPanel()

		this.initCreateRoom()
		// create_btn
		this.updateCardDiamond()
	},

	updateCardDiamond:function(){
		var Text_9 = this.rootUINode.getChildByName("createroom_panel").getChildByName("Text_9");
		// Text_9.setString("消耗8张房卡或100钻石，游戏开始后扣除");
		if(this.pay_mode == 0){
            Text_9.setString("每人消耗"+ this.round_num / 4 +"钻石，游戏开始后扣除");
		}else {
            Text_9.setString("房主消耗"+ this.round_num +"钻石，游戏开始后扣除");
		}
		Text_9.setPositionX(this.rootUINode.getChildByName("createroom_panel").getContentSize().width * 0.55);
	},

	initCreateRoomPanel:function(){
		var self = this
		var return_btn = ccui.helper.seekWidgetByName(this.createroom_panel, "return_btn")
		function return_btn_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				self.hide()
				var chx_list = [self.player_num, self.pay_mode, self.win_num, self.round_num, self.king_num];
				cc.sys.localStorage.setItem("CHX_LIST", chx_list.toString());
			}
		}
		return_btn.addTouchEventListener(return_btn_event)


		//人数
		this.player_num_chx_list = []
		function player_num_event(sender, eventType){
			if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
				for (var i = 0; i < self.player_num_chx_list.length; i++) {
					if (sender != self.player_num_chx_list[i]) {
						self.player_num_chx_list[i].setSelected(false)
						self.player_num_chx_list[i].setTouchEnabled(true)
					}else{
						self.player_num = 4-i
                        sender.setSelected(true);
						sender.setTouchEnabled(false)
						cc.log("player_num:", self.player_num)
					}
				}
			}
		}
		for (var i = 0; i < 2; i++) {
			var player_num_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "player_num_chx_" + String(i+1))
			this.player_num_chx_list.push(player_num_chx)
			player_num_chx.addTouchEventListener(player_num_event)
		}
		this.player_num_chx_list[self.player_num == 4 ? 0 : 1].setSelected(true)
		this.player_num_chx_list[self.player_num == 4 ? 0 : 1].setTouchEnabled(false)
		cc.log("player_num:", this.player_num)

        //支付模式
        this.pay_mode_chx_list = [];
        function pay_mode_event(sender, eventType){
            if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
                for (var i = 0; i < self.pay_mode_chx_list.length; i++) {
                    if (sender != self.pay_mode_chx_list[i]) {
                        self.pay_mode_chx_list[i].setSelected(false);
                        self.pay_mode_chx_list[i].setTouchEnabled(true);
                    }else{
                        self.pay_mode = i;
                        sender.setSelected(true);
                        sender.setTouchEnabled(false);
                        cc.log("pay_mode:", self.pay_mode);
                        self.updateCardDiamond();
                    }
                }
            }
        }
        for (var i = 0; i < 2; i++) {
            var pay_mode_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "pay_mode_chx_" + String(i+1));
            this.pay_mode_chx_list.push(pay_mode_chx);
            pay_mode_chx.addTouchEventListener(pay_mode_event);
        }
        this.pay_mode_chx_list[self.pay_mode == 0 ? 0 : 1].setSelected(true);
        this.pay_mode_chx_list[self.pay_mode == 0 ? 0 : 1].setTouchEnabled(false);
        cc.log("pay_mode:", this.pay_mode);

		//胡牌台数
		this.win_num_chx_list = []
		function win_num_event(sender, eventType){
			if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
				for (var i = 0; i < self.win_num_chx_list.length; i++) {
					if (sender != self.win_num_chx_list[i]) {
						self.win_num_chx_list[i].setSelected(false)
						self.win_num_chx_list[i].setTouchEnabled(true)
					}else{
						self.win_num = 4+i
                        sender.setSelected(true);
						sender.setTouchEnabled(false)
						cc.log("win_num:", self.win_num)
					}
				}
			}
		}
		for (var i = 0; i < 2; i++) {
			var win_num_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "win_num_chx_" + String(i+1))
			this.win_num_chx_list.push(win_num_chx)
			win_num_chx.addTouchEventListener(win_num_event)
		}
		this.win_num_chx_list[self.win_num == 4 ? 0 : 1].setSelected(true)
		this.win_num_chx_list[self.win_num == 4 ? 0 : 1].setTouchEnabled(false)
		cc.log("win_num:", this.win_num)

		//局数选择
		this.round_num_chx_list = []
		function round_num_event(sender, eventType){
			if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
				for (var i = 0; i < self.round_num_chx_list.length; i++) {
					if (sender != self.round_num_chx_list[i]) {
						self.round_num_chx_list[i].setSelected(false)
						self.round_num_chx_list[i].setTouchEnabled(true)
					}else{
						self.round_num = 4*(i+1)
                        sender.setSelected(true);
						sender.setTouchEnabled(false)
						cc.log("round_num:", self.round_num)
                        self.updateCardDiamond();
					}
				}
			}
		}
		for (var i = 0; i < 4; i++) {
			var round_num_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "round_chx_" + String(i+1))
			this.round_num_chx_list.push(round_num_chx)
			round_num_chx.addTouchEventListener(round_num_event)
		}
		this.round_num_chx_list[self.round_num / 4 - 1].setSelected(true)
		this.round_num_chx_list[self.round_num / 4 - 1].setTouchEnabled(false)
		cc.log("round_num:", this.round_num)
		//百搭选择
		this.king_chx_list = []
		function king_num_event(sender, eventType){
			if (eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED) {
				for (var i = 0; i < self.king_chx_list.length; i++) {
					if (sender != self.king_chx_list[i]) {
						self.king_chx_list[i].setSelected(false)
						self.king_chx_list[i].setTouchEnabled(true)
					}else{
						self.king_num = i+1
                        sender.setSelected(true);
						sender.setTouchEnabled(false)
						cc.log("king_num:", self.king_num)
					}
				}
			}
		}
		for (var i = 0; i < 2; i++) {
			var king_chx = ccui.helper.seekWidgetByName(this.createroom_panel, "king_chx_" + String(i+1))
			this.king_chx_list.push(king_chx)
			king_chx.addTouchEventListener(king_num_event)
		}
		this.king_chx_list[1].setTouchEnabled(false)
		cc.log("king_num:", this.king_num)
	},


	initCreateRoom:function(){
		var self = this
		var create_btn = ccui.helper.seekWidgetByName(this.createroom_panel, "create_btn")
		function create_btn_event(sender, eventType){
			if (eventType == ccui.Widget.TOUCH_ENDED) {
				cutil.lock_ui();
				h1global.entityManager.player().createRoom(self.player_num, self.pay_mode, self.win_num, self.round_num, self.king_num, 0);
                var chx_list = [self.player_num, self.pay_mode, self.win_num, self.round_num, self.king_num];
                cc.sys.localStorage.setItem("CHX_LIST", chx_list.toString());
				self.hide()
			}
		}
		create_btn.addTouchEventListener(create_btn_event)
	}
});