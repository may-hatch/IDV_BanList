"""
ランク戦ban管理
作成日：2025/09/03
"""
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

#supabaseにつなげる
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
supabase=create_client(url,key)

#検索ボタン稼働用
if "submit_s" not in st.session_state:
    st.session_state["submit_s"]=False
if "submit_h" not in st.session_state:
    st.session_state["submit_h"]=False

#キャラ記録用
if "banned_s" not in st.session_state:
    st.session_state["banned_s"]=[None]*3
ban1=st.session_state["banned_s"][0]
ban2=st.session_state["banned_s"][1]
ban3=st.session_state["banned_s"][2]
if "banned_h" not in st.session_state:
    st.session_state["banned_h"]=[None]*3
banned_hunter1=st.session_state["banned_h"][0]
banned_hunter2=st.session_state["banned_h"][1]
banned_hunter3=st.session_state["banned_h"][2]

#マップ記録用
if "choosed_map" not in st.session_state:
    st.session_state["choosed_map"]=None
if "spawn_h" not in st.session_state:
    st.session_state["spawn_h"]=None
if "spawn_s" not in st.session_state:
    st.session_state["spawn_s"]=[None]*4
spawn_s1=st.session_state["spawn_s"][0]
spawn_s2=st.session_state["spawn_s"][1]
spawn_s3=st.session_state["spawn_s"][2]
spawn_s4=st.session_state["spawn_s"][3]
spawn_h=st.session_state["spawn_h"]


maps=["","軍需工場","赤の教会","聖心病院","湖景村","月の河公園","レオの思い出","永眠町","中華街","罪の森"]
sp_list=["01","02","03","04","05","06","07","08","09","10","11","12"]

survivors= {999:None, 1: '医師', 2: '弁護士', 3: '泥棒', 4: '庭師', 5: 'マジシャン',
                6: '冒険家', 7: '傭兵', 8: '空軍', 9: '祭司', 10: '機械技師',
                11: 'オフェンス', 12: '心眼', 13: '調香師', 14: 'カウボーイ', 15: '踊り子',
                16: '占い師', 17: '納棺師', 18: '探鉱者', 19: '呪術師', 20: '野人',
                21: '曲芸師', 22: '一等航海士', 23: 'バーメイド', 24: 'ポストマン', 25: '墓守',
                26: '｢囚人｣', 27: '昆虫学者', 28: '画家', 29: 'バッツマン', 30: '玩具職人',
                31: '患者', 32: '｢心理学者｣', 33: '小説家', 34: '｢少女｣', 35: '泣きピエロ',
                36: '教授', 37: '骨董商', 38: '作曲家', 39: '記者', 40: '航空エンジニア',
                41: '応援団', 42: '人形師', 43: '火災調査員', 44: '｢レディ・ファウロ｣', 45: '｢騎士｣',
                46: '気象学者', 47: '弓使い', 48: '｢脱出マスター｣', 49: '幸運児'}
survivors_name=list(survivors.values())

hunters={999:None, 1: '復讐者', 2: '道化師', 3: '断罪狩人', 4: 'リッパー', 5: '結魂者',
         6: '芸者', 7: '白黒無常', 8: '写真家', 9: '狂眼', 10: '黄衣の王',
         11: '夢の魔女', 12: '泣き虫', 13: '魔トカゲ', 14: '血の女王', 15: 'ガードNo.26',
         16: '「使徒」', 17: 'ヴァイオリニスト', 18: '彫刻師', 19: '「アンデッド」', 20: '破輪',
         21: '漁師', 22: '蝋人形師', 23: '「悪夢」', 24: '書記官', 25: '隠者',
         26: '夜の番人', 27: 'オペラ歌手', 28: '「フールズ・ゴールド」', 29: '時空の影', 30: '「足萎えの羊」',
         31: '「フラバルー」', 32: '雑貨商', 33: '「ビリヤードプレイヤー」'} 

#アプリ作成
#アプリ名
st.title("BAN記録/検索")

tab1,tab2,tab3,tab4=st.tabs(["記録","検索","統計","使い方"])

#使い方
with tab4:
    st.text("""
    五段以上の鯖３BANを想定した記録フォームです。

    【使い方：記録タブ】
    サバイバー段位(最高峰は7)、BANされたキャラ、マップ、ハンターを必ず選択してください。
        ※仕様変更でサバイバー３人入力後は確定ボタンを押さないと反映されなくなりました！
    全ての必須項目入力後に「記録」を押すと、そこまでに入力した情報が記録されます。

    【使い方：検索タブ】
    記録タブでサバイバーを確定後、「サバイバーから検索」を押すと、そのBANをしたハンターの一覧を表示します。
    ２キャラのみ一致の場合は、マップが一致しているハンターが先に表示されます。
        ※マップ未入力でも検索できます
    「ハンターから検索」を押すと、記録タブで選択しているハンターの
            BAN記録(全件)
            マップ割合
            サバイバーごとのBAN割合
        が表示されます。
    
    【使い方：統計タブ】
    統計を表示ボタンを押すと、ボタンが押される直前までに記録された情報の
        総件数
        ハンター別件数
        マップ別ハンター件数
    が確認できます。
        ※スポーンはデータも少なく、まだ調整中です
            左から右、上から下に番号を振っているので、見たい人は手動で見てください
            （永眠町は墓が04、正門ゲート前が05です）
    """)
    with st.expander("更新予定・履歴"):
        st.text("""
        【今後の予定】
        ・コードを綺麗に書き直す
        ・２キャラ一致時の表示の調整
            特徴的なキャラに絞って順序入れ替え
        ・スポーン位置別ハンターの視覚的表示
            これは各ハンターの記録がもっと増えたら…
        ・ハンターから検索時の機能追加
            スポーン位置・BANキャラ割合(多いペア)
                
        【履歴】
        2025-09-20-11:45
            ★統計タブ：
                検索タブ同様、BANキャラ割合(1キャラ単位)の表示機能を実装
        2025-09-29-12:45
            ★検索タブ：
                ハンターから検索時にBANキャラ割合(1キャラ単位)の表示機能を実装
        2025-09-29-10:20
            ★検索タブ：
                ハンターから検索時にマップ割合の表示機能を実装
        2025-09-28-22:30
            ★統計タブ：
                遭遇率の表示順の不具合を修正
        2025-09-26-19:30
            ★全体：
                細かい内部的な修正。
            ★記録タブ：
                サバイバー・ハンターの確定ボタンを設置。
                押すまでは記録されませんが、裏で行われていた再読み込みも挟まりません。
                軽量化…にはなってないと思う。私の好み。
            ★検索タブ：
                サバイバー未入力時・ハンター未入力時は各検索ボタンが押せないように変更。
            ★統計タブ：
                スポーン別表示をスポーン位置順に変更。
        2025-09-26-12:00
            ★全体：
                タブ分割に伴い表示を調整
            ★記録タブ：
                サバイバーのスポーン選択を確定するまで内部再読み込みしない仕様に修正。
            ★検索タブ：
                タブ分割に伴い表示を調整
            ★統計タブ：
                マップごとの遭遇数を表示。
                スポーン記録済みハンターのスポーン位置を仮実装。
        2025-09-26-00:00
                統計ボタンの動作確認完了。
                全記録のうちどのハンターとどれくらい会ったかを見られます。
        """)

#統計表示
with tab3:
    if st.button("統計を表示"):
        response_all=supabase.table("BannedCharaList").select("map","hunter","spawn_h","ban1","ban2","ban3").execute()
        records_all=response_all.data

        survivors_allBan_list=[]

        #単純なハンター遭遇数、マップ選択数、サバイバー数を集計
        hunter_list=[rec["hunter"] for rec in records_all if rec["hunter"]]
        hunter_counts=Counter(hunter_list)
        map_list=[rec["map"] for rec in records_all if rec["map"]]
        map_counts=Counter(map_list)
        for rec in records_all:
            survivors_allBan_list.append(rec["ban1"])
            survivors_allBan_list.append(rec["ban2"])
            survivors_allBan_list.append(rec["ban3"])
        survivors_allBan_count=Counter(survivors_allBan_list)
        
        #ハンターの割合を計算
        total_hunters=sum(hunter_counts.values())
        sorted_byCnt_h={k:v for k,v in hunter_counts.items()}
        hunter_ratio={k:round(v/total_hunters*100,2) for k,v in hunter_counts.items()}
        #ハンター名と割合を並び替えたリストに変換
        sorted_items_h = sorted(sorted_byCnt_h.items(), key=lambda x: x[1], reverse=True)

        #遭遇率を表示するためデータフレームに入れる
        df_h = pd.DataFrame({
            "ハンター": list(hunter_ratio.keys()),
            "記録数":[f"{sbh}試合" for sbh in sorted_byCnt_h.values()],
            "割合(%)":[f"{v:.2f}" for v in hunter_ratio.values()]
        }).dropna().query("ハンター != ''").sort_values("割合(%)", ascending=False)
    
        #★表示
        #遭遇率
        st.write(f"総記録件数：{total_hunters}件")
        with st.expander("ハンター遭遇率"):
            st.table(df_h[["ハンター","記録数","割合(%)"]])

        #サバイバー(単体)ごとのBAN率を計算
        total_survivors=sum(survivors_allBan_count.values())
        sorted_byCnt_s={k:v for k,v in survivors_allBan_count.items()}
        survivors_ratio={k:round(v/total_survivors*300,2) for k,v in survivors_allBan_count.items()}
        #サバイバーと割合を並び替えたリストに変換
        sorted_items_s=sorted(sorted_byCnt_s.items(),key=lambda x: x[1], reverse=True)

        #BAN率を表示するためにデータフレームに入れる
        df_s=pd.DataFrame({
            "サバイバー":list(survivors_ratio.keys()),
            "記録数":[f"{sbs}試合" for sbs in sorted_byCnt_s.values()],
            "割合(%)":[round(v,2) for v in survivors_ratio.values()]
        }).sort_values("割合(%)",ascending=False)

        #最もBANされたサバイバー(単体)
        with st.expander("サバイバーBAN率(単体)"):
            st.table(df_s[["サバイバー","記録数","割合(%)"]])

        #マップ&ハンターの出現回数を集計
        df_map = pd.DataFrame(records_all)
        df_map = df_map.query("map != '' and hunter != ''")
        map_hunter_counts = df_map.groupby(["map", "hunter"]).size().reset_index(name="count")

        #マップ&ハンター&スポーン位置の集計
        df_sp=pd.DataFrame(records_all)
        df_sp=df_sp.dropna().query("map != '' and hunter != ''")
        spawn_counts=df_sp.groupby(["map","hunter","spawn_h"]).size().reset_index(name="count")
        
        #マップ別
        with st.expander("マップ別ハンター"):
            # pandasで整形済みの map_hunter_counts を使って
            for map_name in map_hunter_counts["map"].unique():
                with st.expander(f"【{map_name}】記録数：{map_counts[map_name]}"):
                    map_df = map_hunter_counts.query(f"map == '{map_name}'")
                    st.bar_chart(map_df.set_index("hunter")["count"],height=250)

        #スポーン別
        with st.expander("スポーン別(準備中)"):
            for map_name in map_hunter_counts["map"].unique():
                with st.expander(f"【{map_name}】記録数：{map_counts[map_name]}"):
                    sp_df=spawn_counts.query(f"map=='{map_name}'").sort_values("spawn_h")
                    st.table(sp_df[["spawn_h","hunter","count"]])
    
#記録
with tab1:
    #入力フォーム_段位
    rank=st.selectbox("段位を選択",options=["5","6","7"])

    #入力フォーム_マップ
    map=st.selectbox("マップを選択（必須）",options=maps)

    #入力フォーム_サバイバー
    #見やすさのためにたたむ
    with st.expander("BANされたサバイバーを記録（必須）"):
        with st.form("鯖ban選択"):
            banA=st.selectbox("1人目のBAN済サバイバー",options=list(survivors.values()))
            banB=st.selectbox("2人目のBAN済サバイバー",options=list(survivors.values()))
            banC=st.selectbox("3人目のBAN済サバイバー",options=list(survivors.values()))
            submitted_s=st.form_submit_button("サバイバーのBANを確定")
        if submitted_s:
            if banA==None or banB==None or banC==None:
                st.warning("３キャラ入力して下さい")
                st.session_state["submit_s"]=False
            else:
                st.session_state["submit_s"]=True
            #書き込む前に並べ替え
                name_to_id_s={v_s:k_s for k_s,v_s in survivors.items()}
                selected_survivor=[banA,banB,banC]
                st.session_state["banned_s"]=sorted(selected_survivor,key=lambda x:name_to_id_s.get(x,999))
                #st.session_state["banned_s"][0]=sorted_ban[0]
                #st.session_state["banned_s"][1]=sorted_ban[1]
                #st.session_state["banned_s"][2]=sorted_ban[2]
                ban1=st.session_state["banned_s"][0]
                ban2=st.session_state["banned_s"][1]
                ban3=st.session_state["banned_s"][2]
                st.success(f"入力を確定：{ban1}、{ban2}、{ban3}")

    #入力フォーム_対戦ハンター
    hunter=st.selectbox("対戦ハンターを選択（必須）",options=list(hunters.values()))
    if hunter!=None:
        st.session_state["submit_h"]=True
    #入力フォーム_BAN済ハンター
    #BAN済ハンターは任意なのでたたむ
    with st.expander("BANしたハンターを記録（任意）"):
        with st.form("ban_h"):
            banned_hunterA=st.selectbox("1人目のBAN済ハンター",options=list(hunters.values()))
            banned_hunterB=st.selectbox("2人目のBAN済ハンター",options=list(hunters.values()))
            banned_hunterC=st.selectbox("3人目のBAN済ハンター(空欄可)",options=list(hunters.values()))
            submitted_h=st.form_submit_button("ハンターのBANを確定")
        if submitted_h:
        #並べ替え
            name_to_id_h={v_h:k_h for k_h,v_h in hunters.items()}
            selected_hunter=[banned_hunterA,banned_hunterB,banned_hunterC]
            st.session_state["banned_h"]=sorted(selected_hunter,key=lambda x:name_to_id_h.get(x,999))
            banned_hunter1=st.session_state["banned_h"][0]
            banned_hunter2=st.session_state["banned_h"][1]
            banned_hunter3=st.session_state["banned_h"][2]
            st.success(f"入力を確定：{banned_hunter1}、{banned_hunter2}、{banned_hunter3}")

    #入力フォーム_スポーン位置
    with st.expander("スポーン記録(任意)"):
    #ハンターの位置
        with st.expander("ハンターの位置"):
            st.text(f"現在のマップ：{map}")
            with st.container():
                if map=="永眠町":
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[:4]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[4:7]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[7:10]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                elif map=="湖景村" or map=="月の河公園":
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[:4]:    
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[4:8]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[8:]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                else:
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[:3]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[3:6]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
                    with st.container(horizontal=True,horizontal_alignment="left"):
                        for sp in sp_list[6:9]:
                            if st.button(f"{sp}",key=f"bu_{sp}"):
                                st.session_state["spawn_h"]=sp
            if st.button("スポーン位置をリセット"):
                st.session_state["spawn_h"]=None
            spawn_h=st.session_state["spawn_h"]
            st.text(f"選択中スポーン位置：{spawn_h}")        
    #サバイバーの位置
        with st.expander("サバイバーの位置"):
            with st.form("鯖スポーン"):
                st.text(f"現在のマップ：{map}")
                with st.container():
                    if map=="永眠町":
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[:4]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[4:7]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[7:10]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        st.session_state["checkBox_11"]=False
                        st.session_state["checkBox_12"]=False
                    elif map=="湖景村" or map=="月の河公園":
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[:4]:    
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[4:8]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[8:]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                    else:
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[:3]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[3:6]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        with st.container(horizontal=True,horizontal_alignment="left"):
                            for sp in sp_list[6:9]:
                                key = f"checkBox_{sp}"
                                st.checkbox("",key=key)
                        st.session_state["checkBox_10"]=False
                        st.session_state["checkBox_11"]=False
                        st.session_state["checkBox_12"]=False
                submitted_sp=st.form_submit_button("スポーンを確定")
            if submitted_sp:    
                cnt=0
                for sp in sp_list:
                    if st.session_state.get(f"checkBox_{sp}",False)==True:
                        if cnt>=4:
                            st.warning("スポーン位置が多すぎます")
                            st.session_state["spawn_s"]=[None,None,None,None]
                            cnt+=1
                            break
                        st.session_state["spawn_s"][cnt]=sp
                        cnt+=1
                if cnt==4:
                    st.success(f"スポーンを確定しました：{st.session_state["spawn_s"]}")
                spawn_s1=st.session_state["spawn_s"][0]
                spawn_s2=st.session_state["spawn_s"][1]
                spawn_s3=st.session_state["spawn_s"][2]
                spawn_s4=st.session_state["spawn_s"][3]
    #データ操作
    if st.button("記録"):
        if ban1!="" and ban2!="" and ban3!="" and hunter!="" and map!="":
            res = supabase.table("BannedCharaList").insert({
                "rank":rank,
                "ban1":ban1,
                "ban2":ban2,
                "ban3":ban3,
                "map":map,
                "hunter":hunter,
                "banned_hunter1":banned_hunter1,
                "banned_hunter2":banned_hunter2,
                "banned_hunter3":banned_hunter3,
                "spawn_h":spawn_h,
                "spawn_s1":spawn_s1,
                "spawn_s2":spawn_s2,
                "spawn_s3":spawn_s3,
                "spawn_s4":spawn_s4
                }).execute()
            st.success("記録完了")
        else:
            st.warning("未入力の項目があります")

#検索
with tab2:
    #サバイバーからハンターを検索
    if st.session_state["submit_s"]==True:
        st.text(f"サバイバー：{ban1},{ban2},{ban3}")
        st.text(f"マップ：{map}")
    else:
        st.text("↓記録タブで「BANされたサバイバー」を確定後に利用できます")

    if st.button("サバイバーから検索",disabled=not st.session_state["submit_s"]):
        if ban1!="" and ban2!="" and ban3!="":
            #３キャラ一致
            st.text("【３キャラ一致】")
            response=supabase.table("BannedCharaList").select("hunter,map,ban1,ban2,ban3").eq("ban1",ban1).eq("ban2",ban2).eq("ban3",ban3).order("hunter").execute()
            if response.data:
                st.table(response.data)
            else:
                st.text("該当なし")
            #２キャラ一致
            st.text("【２キャラ一致】")
            response=supabase.table("BannedCharaList").select("hunter,map,ban1,ban2,ban3").order("hunter").execute()
            records=response.data
            match2chara_map=[]
            match2chara=[]
            #match1chara=[]
            for i in response.data:
                match_m=False
                match_count_c=0
                if i["map"] == map:
                    match_m=True
                if i["ban1"] in st.session_state["banned_s"]:
                    match_count_c+=1
                if i["ban2"] in st.session_state["banned_s"]:
                    match_count_c+=1
                if i["ban3"] in st.session_state["banned_s"]:
                    match_count_c+=1
                if match_count_c==2 and match_m==True:
                    match2chara_map.append(i)
                elif match_count_c==2:
                    match2chara.append(i)
                #elif match_count==1:
                #    match1chara.append(i)
            if match2chara_map!=[]:
                st.text("マップ一致")
                st.table(match2chara_map)
            if match2chara!=[]:
                #list_for_2chara=[rec2["hunter"] for rec2 in match2chara if rec2["hunter"]]
                #cnt_2chara = Counter(list_for_2chara)
                #list_h_2chara=cnt_2chara.keys()
                #sorted_2chara=sorted(cnt_2chara.items(),key=lambda x: x[1],reverse=True)
                if len(match2chara)>=5:
                    with st.expander("マップ不一致(該当多数のため折り畳み)"):
                        st.table(match2chara)                        
                else:
                    st.text("マップ不一致")
                    st.table(match2chara)
            if match2chara_map==[] and match2chara==[]:
                st.text("該当なし")
        else:
            st.warning("３人入力してください")

    #ハンターからサバイバーを検索
    if st.session_state["submit_h"]==False:
        st.text(f"↓記録タブで「対戦ハンター」を選択後に利用できます")
    else:
        st.text(f"ハンター：{hunter}")
    if st.button("ハンターから検索",disabled=not st.session_state["submit_h"]):
        if hunter!="":
            response_h=supabase.table("BannedCharaList").select("map,spawn_h,ban1,ban2,ban3").eq("hunter",hunter).order("map").order("spawn_h").execute()
            if response_h.data:
                #データ集計
                #BAN割合
                bans_list_h=[]
                bans_name_h=[]
                bans_ratio_h=[]
                for res_h in response_h.data:
                    bans_list_h.append(res_h["ban1"])
                    bans_list_h.append(res_h["ban2"])
                    bans_list_h.append(res_h["ban3"])
                bans_counts_h=Counter(bans_list_h)
                for b in survivors_name:
                    if b in bans_counts_h:
                        value=round(bans_counts_h[b]/sum(bans_counts_h.values())*300,2)
                        bans_name_h.append(b)
                        bans_ratio_h.append(value)
                    else:
                        pass
                df_data_h=pd.DataFrame({
                    "キャラ":bans_name_h,
                    "BAN率":bans_ratio_h})
                #マップ
                map_list_h=[res_h["map"] for res_h in response_h.data if res_h["map"]]
                map_counts_h=Counter(map_list_h)
                map_ratio_h=[round(map_counts_h[m]/sum(map_counts_h.values())*100,2) for m in maps[1:]]
                df_map_h=pd.DataFrame({
                    "マップ":maps[1:],
                    "割合":map_ratio_h})
                #スポーン位置
                #まだ作ってない

                #表示
                st.text(f"記録数：{len(map_list_h)}件")
                with st.expander("全件"):
                    st.table(response_h.data)
                st.text("BANしたサバイバー割合")
                st.bar_chart(df_data_h.set_index("キャラ"))
                st.text("マップ割合")
                st.bar_chart(df_map_h.set_index("マップ"))
            else:
                st.text("記録なし")