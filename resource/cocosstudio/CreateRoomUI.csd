<GameFile>
  <PropertyGroup Name="CreateRoomUI" Type="Layer" ID="3e9685ee-d303-4a20-98e6-0d67342f76ef" Version="3.10.0.0" />
  <Content ctype="GameProjectContent">
    <Content>
      <Animation Duration="0" Speed="1.0000" />
      <ObjectData Name="Layer" ctype="GameLayerObjectData">
        <Size X="1280.0000" Y="720.0000" />
        <Children>
          <AbstractNodeData Name="bg_panel" ActionTag="-836818764" Tag="2" IconVisible="False" PercentWidthEnable="True" PercentHeightEnable="True" PercentWidthEnabled="True" PercentHeightEnabled="True" TouchEnable="True" ClipAble="False" BackColorAlpha="178" ComboBoxIndex="1" ColorAngle="90.0000" Scale9Width="1" Scale9Height="1" ctype="PanelObjectData">
            <Size X="1280.0000" Y="720.0000" />
            <AnchorPoint />
            <Position />
            <Scale ScaleX="1.0000" ScaleY="1.0000" />
            <CColor A="255" R="255" G="255" B="255" />
            <PrePosition />
            <PreSize X="1.0000" Y="1.0000" />
            <SingleColor A="255" R="0" G="0" B="0" />
            <FirstColor A="255" R="150" G="200" B="255" />
            <EndColor A="255" R="255" G="255" B="255" />
            <ColorVector ScaleY="1.0000" />
          </AbstractNodeData>
          <AbstractNodeData Name="createroom_panel" ActionTag="-1659094001" Tag="3" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="142.0000" RightMargin="142.0000" TopMargin="25.0000" BottomMargin="25.0000" TouchEnable="True" ClipAble="False" BackColorAlpha="102" ColorAngle="90.0000" LeftEage="29" RightEage="29" TopEage="35" BottomEage="35" Scale9OriginX="29" Scale9OriginY="35" Scale9Width="938" Scale9Height="600" ctype="PanelObjectData">
            <Size X="996.0000" Y="670.0000" />
            <Children>
              <AbstractNodeData Name="bg1_img" ActionTag="311797222" Tag="871" IconVisible="False" LeftMargin="186.2537" RightMargin="159.7463" TopMargin="114.0288" BottomMargin="463.9712" LeftEage="214" RightEage="214" TopEage="30" BottomEage="30" Scale9OriginX="214" Scale9OriginY="30" Scale9Width="222" Scale9Height="32" ctype="ImageViewObjectData">
                <Size X="650.0000" Y="92.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="511.2537" Y="509.9712" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5133" Y="0.7612" />
                <PreSize X="0.6526" Y="0.1373" />
                <FileData Type="Normal" Path="BackGround/createroom_bg1.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="bg2_img" ActionTag="1590861306" Tag="872" IconVisible="False" LeftMargin="179.3069" RightMargin="166.6931" TopMargin="174.6400" BottomMargin="125.3600" LeftEage="214" RightEage="214" TopEage="84" BottomEage="84" Scale9OriginX="214" Scale9OriginY="84" Scale9Width="222" Scale9Height="88" ctype="ImageViewObjectData">
                <Size X="650.0000" Y="370.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="504.3069" Y="310.3600" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5063" Y="0.4632" />
                <PreSize X="0.6526" Y="0.5522" />
                <FileData Type="Normal" Path="BackGround/createroom_bg2.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="title_img" ActionTag="-1592769131" Tag="870" IconVisible="False" LeftMargin="402.0000" RightMargin="398.0000" TopMargin="26.0000" BottomMargin="604.0000" LeftEage="48" RightEage="48" TopEage="15" BottomEage="15" Scale9OriginX="48" Scale9OriginY="15" Scale9Width="100" Scale9Height="10" ctype="ImageViewObjectData">
                <Size X="196.0000" Y="40.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="500.0000" Y="624.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5020" Y="0.9313" />
                <PreSize X="0.1968" Y="0.0597" />
                <FileData Type="Normal" Path="CreateRoomUI/title.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="player_num_label" ActionTag="-1682740503" Tag="25" IconVisible="False" LeftMargin="212.6263" RightMargin="687.3737" TopMargin="146.1100" BottomMargin="499.8900" FontSize="24" LabelText="人数选择" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="96.0000" Y="24.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="260.6263" Y="511.8900" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="56" G="54" B="54" />
                <PrePosition X="0.2617" Y="0.7640" />
                <PreSize X="0.0964" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="player_num_chx_1" ActionTag="1323015504" Tag="5" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="317.3808" RightMargin="606.6192" TopMargin="130.1920" BottomMargin="481.8080" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="353.3808" Y="510.8080" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3548" Y="0.7624" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="player_num_chx_2" ActionTag="-141107793" Tag="7" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="560.9028" RightMargin="363.0972" TopMargin="129.7900" BottomMargin="482.2100" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="596.9028" Y="511.2100" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5993" Y="0.7630" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="p_num_1" ActionTag="-1487135814" Tag="499" IconVisible="False" LeftMargin="405.0000" RightMargin="555.0000" TopMargin="145.0000" BottomMargin="501.0000" FontSize="24" LabelText="4人" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="36.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="405.0000" Y="513.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4066" Y="0.7657" />
                <PreSize X="0.0361" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="p_num_2" ActionTag="-749287181" Tag="500" IconVisible="False" LeftMargin="644.0000" RightMargin="316.0000" TopMargin="145.0000" BottomMargin="501.0000" FontSize="24" LabelText="3人" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="36.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="644.0000" Y="513.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.6466" Y="0.7657" />
                <PreSize X="0.0361" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="pay_mode_label" ActionTag="148699786" Tag="81" IconVisible="False" LeftMargin="215.4000" RightMargin="684.6000" TopMargin="230.0000" BottomMargin="416.0000" FontSize="24" LabelText="支付选择" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="96.0000" Y="24.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="263.4000" Y="428.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="56" G="54" B="54" />
                <PrePosition X="0.2645" Y="0.6388" />
                <PreSize X="0.0964" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="pay_mode_chx_1" ActionTag="998819179" Tag="79" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="312.6000" RightMargin="611.4000" TopMargin="215.5500" BottomMargin="396.4500" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="348.6000" Y="425.4500" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3500" Y="0.6350" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="pay_mode_chx_2" ActionTag="1702278288" Tag="80" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="561.6000" RightMargin="362.4000" TopMargin="215.5500" BottomMargin="396.4500" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="597.6000" Y="425.4500" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.6000" Y="0.6350" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="pay_mode_1" ActionTag="383968202" Tag="77" IconVisible="False" LeftMargin="406.0000" RightMargin="518.0000" TopMargin="230.0000" BottomMargin="416.0000" FontSize="24" LabelText="AA支付" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="72.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="406.0000" Y="428.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4076" Y="0.6388" />
                <PreSize X="0.0723" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="pay_mode_2" ActionTag="875960319" Tag="78" IconVisible="False" LeftMargin="646.0000" RightMargin="254.0000" TopMargin="230.0000" BottomMargin="416.0000" FontSize="24" LabelText="房主支付" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="96.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="646.0000" Y="428.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.6486" Y="0.6388" />
                <PreSize X="0.0964" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="win_num_label" ActionTag="-1290722923" Tag="491" IconVisible="False" LeftMargin="215.3990" RightMargin="684.6010" TopMargin="295.0000" BottomMargin="351.0000" FontSize="24" LabelText="胡牌台数" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="96.0000" Y="24.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="263.3990" Y="363.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="56" G="54" B="54" />
                <PrePosition X="0.2645" Y="0.5418" />
                <PreSize X="0.0964" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="win_num_chx_1" ActionTag="971007705" Tag="27" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="314.1936" RightMargin="609.8064" TopMargin="279.2000" BottomMargin="332.8000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="350.1936" Y="361.8000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3516" Y="0.5400" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="win_num_chx_2" ActionTag="646392886" Tag="492" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="563.1936" RightMargin="360.8064" TopMargin="279.2000" BottomMargin="332.8000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="599.1936" Y="361.8000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.6016" Y="0.5400" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="win_num_1" ActionTag="-673466421" Tag="501" IconVisible="False" LeftMargin="405.5691" RightMargin="458.4309" TopMargin="295.0000" BottomMargin="351.0000" FontSize="24" LabelText="4台(混清碰)" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="132.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="405.5691" Y="363.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4072" Y="0.5418" />
                <PreSize X="0.1325" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="win_num_2" ActionTag="-1791537363" Tag="502" IconVisible="False" LeftMargin="645.5700" RightMargin="218.4300" TopMargin="295.0000" BottomMargin="351.0000" FontSize="24" LabelText="5台(混清碰)" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="132.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="645.5700" Y="363.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.6482" Y="0.5418" />
                <PreSize X="0.1325" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_label" ActionTag="2010332949" Tag="493" IconVisible="False" LeftMargin="214.0027" RightMargin="685.9973" TopMargin="358.0000" BottomMargin="288.0000" FontSize="24" LabelText="局数选择" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="96.0000" Y="24.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="262.0027" Y="300.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="56" G="54" B="54" />
                <PrePosition X="0.2631" Y="0.4478" />
                <PreSize X="0.0964" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_chx_1" ActionTag="-750004856" Tag="494" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="314.4924" RightMargin="609.5076" TopMargin="339.5000" BottomMargin="272.5000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="350.4924" Y="301.5000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3519" Y="0.4500" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_chx_2" ActionTag="973481761" Tag="495" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="560.6040" RightMargin="363.3960" TopMargin="339.5000" BottomMargin="272.5000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="596.6040" Y="301.5000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5990" Y="0.4500" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_chx_3" ActionTag="-1501460933" Tag="508" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="316.0860" RightMargin="607.9140" TopMargin="399.8000" BottomMargin="212.2000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="352.0860" Y="241.2000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3535" Y="0.3600" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_chx_4" ActionTag="591399223" Tag="507" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="562.1976" RightMargin="361.8024" TopMargin="399.8000" BottomMargin="212.2000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="598.1976" Y="241.2000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.6006" Y="0.3600" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_num_1" ActionTag="614653572" Tag="503" IconVisible="False" LeftMargin="406.5749" RightMargin="553.4251" TopMargin="358.0000" BottomMargin="288.0000" FontSize="24" LabelText="4局" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="36.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="406.5749" Y="300.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4082" Y="0.4478" />
                <PreSize X="0.0361" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_num_2" ActionTag="278706652" Tag="504" IconVisible="False" LeftMargin="646.5751" RightMargin="313.4249" TopMargin="358.0000" BottomMargin="288.0000" FontSize="24" LabelText="8局" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="36.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="646.5751" Y="300.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.6492" Y="0.4478" />
                <PreSize X="0.0361" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_num_3" ActionTag="282779375" Tag="509" IconVisible="False" LeftMargin="404.7842" RightMargin="543.2158" TopMargin="414.0000" BottomMargin="232.0000" FontSize="24" LabelText="12局" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="48.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="404.7842" Y="244.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4064" Y="0.3642" />
                <PreSize X="0.0482" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="round_num_4" ActionTag="1770120017" Tag="510" IconVisible="False" LeftMargin="644.7878" RightMargin="303.2122" TopMargin="414.0000" BottomMargin="232.0000" FontSize="24" LabelText="16局" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="48.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="644.7878" Y="244.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.6474" Y="0.3642" />
                <PreSize X="0.0482" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="king_num_label" ActionTag="-1118637749" Tag="496" IconVisible="False" LeftMargin="214.9012" RightMargin="685.0988" TopMargin="470.0000" BottomMargin="176.0000" FontSize="24" LabelText="百搭选择" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="96.0000" Y="24.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="262.9012" Y="188.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="56" G="54" B="54" />
                <PrePosition X="0.2640" Y="0.2806" />
                <PreSize X="0.0964" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="king_chx_1" ActionTag="641033355" VisibleForFrame="False" Tag="498" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="316.8828" RightMargin="607.1172" TopMargin="453.4000" BottomMargin="158.6000" TouchEnable="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="352.8828" Y="187.6000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3543" Y="0.2800" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="king_chx_2" ActionTag="1934827653" Tag="497" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="316.8828" RightMargin="607.1172" TopMargin="453.4000" BottomMargin="158.6000" TouchEnable="True" CheckedState="True" ctype="CheckBoxObjectData">
                <Size X="72.0000" Y="58.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="352.8828" Y="187.6000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.3543" Y="0.2800" />
                <PreSize X="0.0723" Y="0.0866" />
                <NormalBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <PressedBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <DisableBackFileData Type="Normal" Path="Default/chx_bg.png" Plist="" />
                <NodeNormalFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
                <NodeDisableFileData Type="Normal" Path="Default/chx_img.png" Plist="" />
              </AbstractNodeData>
              <AbstractNodeData Name="king_num_1" ActionTag="937403752" VisibleForFrame="False" Tag="505" IconVisible="False" LeftMargin="405.0000" RightMargin="531.0000" TopMargin="470.0000" BottomMargin="176.0000" FontSize="24" LabelText="3百搭" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="60.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="405.0000" Y="188.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4066" Y="0.2806" />
                <PreSize X="0.0602" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="king_num_2" ActionTag="-1713685702" Tag="506" IconVisible="False" LeftMargin="405.0000" RightMargin="531.0000" TopMargin="470.0000" BottomMargin="176.0000" FontSize="24" LabelText="7百搭" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="60.0000" Y="24.0000" />
                <AnchorPoint ScaleY="0.5000" />
                <Position X="405.0000" Y="188.0000" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="7" G="7" B="7" />
                <PrePosition X="0.4066" Y="0.2806" />
                <PreSize X="0.0602" Y="0.0358" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="Text_9" ActionTag="1623749359" Tag="39" IconVisible="False" PositionPercentXEnabled="True" LeftMargin="251.0000" RightMargin="251.0000" TopMargin="608.9629" BottomMargin="35.0371" FontSize="26" LabelText="消耗4张房卡或100钻石，游戏开始后扣除。" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="TextObjectData">
                <Size X="494.0000" Y="26.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="498.0000" Y="48.0371" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5000" Y="0.0717" />
                <PreSize X="0.4960" Y="0.0388" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="return_btn" ActionTag="-2051928181" Tag="60" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="875.0212" RightMargin="38.9788" TopMargin="17.0690" BottomMargin="578.9310" TouchEnable="True" FontSize="14" Scale9Enable="True" LeftEage="15" RightEage="15" TopEage="11" BottomEage="11" Scale9OriginX="15" Scale9OriginY="11" Scale9Width="52" Scale9Height="52" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="ButtonObjectData">
                <Size X="82.0000" Y="74.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="916.0212" Y="615.9310" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.9197" Y="0.9193" />
                <PreSize X="0.0823" Y="0.1104" />
                <TextColor A="255" R="65" G="65" B="70" />
                <NormalFileData Type="Normal" Path="Default/return_btn.png" Plist="" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
              <AbstractNodeData Name="create_btn" ActionTag="754604719" Tag="17" IconVisible="False" PositionPercentXEnabled="True" PositionPercentYEnabled="True" LeftMargin="405.5816" RightMargin="396.4185" TopMargin="509.1470" BottomMargin="74.8530" TouchEnable="True" FontSize="14" LeftEage="15" RightEage="15" TopEage="11" BottomEage="11" Scale9OriginX="15" Scale9OriginY="11" Scale9Width="164" Scale9Height="64" ShadowOffsetX="2.0000" ShadowOffsetY="-2.0000" ctype="ButtonObjectData">
                <Size X="194.0000" Y="86.0000" />
                <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
                <Position X="502.5816" Y="117.8530" />
                <Scale ScaleX="1.0000" ScaleY="1.0000" />
                <CColor A="255" R="255" G="255" B="255" />
                <PrePosition X="0.5046" Y="0.1759" />
                <PreSize X="0.1948" Y="0.1284" />
                <TextColor A="255" R="65" G="65" B="70" />
                <NormalFileData Type="Normal" Path="Default/ok_btn.png" Plist="" />
                <OutlineColor A="255" R="255" G="0" B="0" />
                <ShadowColor A="255" R="110" G="110" B="110" />
              </AbstractNodeData>
            </Children>
            <AnchorPoint ScaleX="0.5000" ScaleY="0.5000" />
            <Position X="640.0000" Y="360.0000" />
            <Scale ScaleX="1.0000" ScaleY="1.0000" />
            <CColor A="255" R="255" G="255" B="255" />
            <PrePosition X="0.5000" Y="0.5000" />
            <PreSize X="0.7781" Y="0.9306" />
            <FileData Type="Normal" Path="BackGround/big_win.png" Plist="" />
            <SingleColor A="255" R="0" G="0" B="0" />
            <FirstColor A="255" R="150" G="200" B="255" />
            <EndColor A="255" R="255" G="255" B="255" />
            <ColorVector ScaleY="1.0000" />
          </AbstractNodeData>
        </Children>
      </ObjectData>
    </Content>
  </Content>
</GameFile>