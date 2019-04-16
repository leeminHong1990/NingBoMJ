// var UIBase = require("src/views/ui/UIBase.js")
// cc.loader.loadJs("src/views/ui/UIBase.js")
var GameConfigUI = UIBase.extend({
	ctor:function() {
		this._super();
		this.resourceFilename = "res/ui/GameConfigUI.json";
	},

	initUI:function(){
        if (cc.sys.localStorage.getItem("MUSIC_VOLUME") === null) {
            cc.sys.localStorage.setItem("MUSIC_VOLUME", 50);
        }
        if (cc.sys.localStorage.getItem("EFFECT_VOLUME") === null) {
            cc.sys.localStorage.setItem("EFFECT_VOLUME", 50);
        }
        if (cc.sys.localStorage.getItem("VIB_CHX") === null) {
            cc.sys.localStorage.setItem("VIB_CHX", "true");
        }
		this.gameconfig_panel = this.rootUINode.getChildByName("gameconfig_panel");
		var player = h1global.entityManager.player();
		var self = this;
		this.gameconfig_panel.getChildByName("return_btn").addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				self.hide();
			}
		});

		this.out_btn = this.gameconfig_panel.getChildByName("out_btn");
		this.out_btn.addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				player.quitRoom();
				self.hide();
			}
		});

		this.close_btn = this.gameconfig_panel.getChildByName("close_btn");
		this.close_btn.addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				player.quitRoom();
				self.hide();
			}
		});

		this.applyclose_btn = this.gameconfig_panel.getChildByName("applyclose_btn");
		this.applyclose_btn.addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
				player.applyDismissRoom();
				self.hide();
			}
		});

		this.gameconfig_panel.getChildByName("music_slider").addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
			// if(eventType == ccui.Slider.EVENT_PERCENT_CHANGED){
				cc.audioEngine.setMusicVolume(sender.getPercent()*0.01);
				cc.sys.localStorage.setItem("MUSIC_VOLUME", sender.getPercent());
			}
		});
		this.gameconfig_panel.getChildByName("music_slider").setPercent(cc.sys.localStorage.getItem("MUSIC_VOLUME"));

		this.gameconfig_panel.getChildByName("effect_slider").addTouchEventListener(function(sender, eventType){
			if(eventType == ccui.Widget.TOUCH_ENDED){
			// if(eventType == ccui.Slider.EVENT_PERCENT_CHANGED){
				cc.audioEngine.setEffectsVolume(sender.getPercent()*0.01);
				cc.sys.localStorage.setItem("EFFECT_VOLUME", sender.getPercent());
			}
		});
		this.gameconfig_panel.getChildByName("effect_slider").setPercent(cc.sys.localStorage.getItem("EFFECT_VOLUME") );

        var vib_chx = this.gameconfig_panel.getChildByName("vib_chx");
        vib_chx.addTouchEventListener(function(sender, eventType){
            if(eventType == ccui.CheckBox.EVENT_SELECTED || eventType == ccui.CheckBox.EVENT_UNSELECTED){
                cc.sys.localStorage.setItem("VIB_CHX", (!vib_chx.isSelected()).toString());
            }
        });
        vib_chx.setSelected(cc.sys.localStorage.getItem("VIB_CHX") == "true" ? true : false);

		this.update_state();
	},

	update_state:function(){
		if(!this.is_show){
			return;
		}
		var player = h1global.entityManager.player();
		if(player.curGameRoom){
			if(player.curGameRoom.curRound > 0){
				this.applyclose_btn.setVisible(true);
				this.close_btn.setVisible(false);
				this.out_btn.setVisible(false);
			} else if(player.serverSitNum == 0){
				this.applyclose_btn.setVisible(false);
				this.close_btn.setVisible(true);
				this.out_btn.setVisible(false);
			} else {
				this.applyclose_btn.setVisible(false);
				this.close_btn.setVisible(false);
				this.out_btn.setVisible(true);
			}
		}
	},
});