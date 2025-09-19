"""
ランク戦ban管理
作成日：2025/09/03
更新日(1)：2025/09/19
"""
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

#supabaseにつなげる
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
supabase=create_client(url,key)

#マップ管理
if "spawn_h" not in st.session_state:
    st.session_state["spawn_h"]=[""]
if "spawn_s" not in st.session_state:
    st.session_state["spawn_s"]=["","","",""]

sp_list=["sp1","sp2","sp3","sp4","sp5","sp6","sp7","sp8","sp9","sp10","sp11","sp12"]

#アプリ作成
#アプリ名
st.title("ランク戦BANリスト")

with st.expander("使い方"):
    st.write("""
    テストで作った身内用です！！サーバー外に共有しないでください！！
    なにか追加したい項目などあれば気軽に教えてください～
    
    五段以上の鯖３BANを想定した記録フォームです。
    遭遇時の段位、BANされたキャラ、マップ、ハンターを選択してください。
    ※BANしたハンターは任意記録です。
    
    サバイバーのBAN入力後、
    「検索」を押すと、そのBANをしたハンターの一覧を表示します。
    「記録」を押すと、そこまでに入力した情報が記録されます。
    ※記録されたデータは次回以降の検索に使われます。

    今はただ一覧を表示するようになってます
    
    更新予定：
    2025-09-19（作業中）
    データ収集の進行に伴い更新。
    o検索結果から１キャラ一致を削除
    xマップを含めて優先順を付けた検索に仕様変更
    x記録項目（任意）にスポーン選択を追加
    """)

#入力フォーム_段位
rank=st.selectbox("段位を選択",options=["5","6","7"])

#入力フォーム_マップ
maps=["","軍需工場","赤の教会","聖心病院","湖景村","月の河公園","レオの思い出","永眠町","中華街","罪の森"]
map=st.selectbox("マップを選択",options=maps)

#入力フォーム_サバイバー
#見やすさのためにたたむ
with st.expander("BANされたサバイバーを３人記録"):
    survivors= {0: '', 1: '医師', 2: '弁護士', 3: '泥棒', 4: '庭師', 5: 'マジシャン',
                6: '冒険家', 7: '傭兵', 8: '空軍', 9: '祭司', 10: '機械技師',
                11: 'オフェンス', 12: '心眼', 13: '調香師', 14: 'カウボーイ', 15: '踊り子',
                16: '占い師', 17: '納棺師', 18: '探鉱者', 19: '呪術師', 20: '野人',
                21: '曲芸師', 22: '一等航海士', 23: 'バーメイド', 24: 'ポストマン', 25: '墓守',
                26: '｢囚人｣', 27: '昆虫学者', 28: '画家', 29: 'バッツマン', 30: '玩具職人',
                31: '患者', 32: '｢心理学者｣', 33: '小説家', 34: '｢少女｣', 35: '泣きピエロ',
                36: '教授', 37: '骨董商', 38: '作曲家', 39: '記者', 40: '航空エンジニア',
                41: '応援団', 42: '人形師', 43: '火災調査員', 44: '｢レディ・ファウロ｣', 45: '｢騎士｣',
                46: '気象学者', 47: '弓使い', 48: '｢脱出マスター｣', 49: '幸運児'}
    banA=st.selectbox("1人目のBAN済サバイバー",options=list(survivors.values()))
    banB=st.selectbox("2人目のBAN済サバイバー",options=list(survivors.values()))
    banC=st.selectbox("3人目のBAN済サバイバー",options=list(survivors.values()))
#書き込む前に並べ替え
    selected_survivor=[banA,banB,banC]
    sorted_ban=sorted(selected_survivor,key=lambda x:survivors.get(x,x))
    ban1=sorted_ban[0]
    ban2=sorted_ban[1]
    ban3=sorted_ban[2]

#入力フォーム_対戦ハンター
hunters={0: '', 1: '復讐者', 2: '道化師', 3: '断罪狩人', 4: 'リッパー', 5: '結魂者',
         6: '芸者', 7: '白黒無常', 8: '写真家', 9: '狂眼', 10: '黄衣の王',
         11: '夢の魔女', 12: '泣き虫', 13: '魔トカゲ', 14: '血の女王', 15: 'ガードNo.26',
         16: '「使徒」', 17: 'ヴァイオリニスト', 18: '彫刻師', 19: '「アンデッド」', 20: '破輪',
         21: '漁師', 22: '蝋人形師', 23: '「悪夢」', 24: '書記官', 25: '隠者',
         26: '夜の番人', 27: 'オペラ歌手', 28: '「フールズ・ゴールド」', 29: '時空の影', 30: '「足萎えの羊」',
         31: '「フラバルー」', 32: '雑貨商', 33: '「ビリヤードプレイヤー」'} 
hunter=st.selectbox("対戦ハンターを選択",options=list(hunters.values()))
#入力フォーム_BAN済ハンター
#BAN済ハンターは任意なのでたたむ
with st.expander("BAN済みハンターを記録(任意)"):
    banned_hunterA=st.selectbox("1人目のBAN済ハンター",options=list(hunters.values()))
    banned_hunterB=st.selectbox("2人目のBAN済ハンター",options=list(hunters.values()))
#並べ替え
    selected_hunter=[banned_hunterA,banned_hunterB]
    sorted_ban=sorted(selected_hunter,key=lambda x:hunters.get(x,x))
    banned_hunter1=sorted_ban[0]
    banned_hunter2=sorted_ban[1]

#データ表示
if st.button("検索"):
    if ban1!="" and ban2!="" and ban3!="":
        #３キャラ一致
        st.text("【３キャラ一致】")
        response=supabase.table("BannedCharaList").select("hunter,ban1,ban2,ban3").eq("ban1",ban1).eq("ban2",ban2).eq("ban3",ban3).execute()
        if response.data:
            st.table(response.data)
        else:
            st.text("該当なし")
        #２キャラ一致
        st.text("【２キャラ一致】")
        response=supabase.table("BannedCharaList").select("hunter,ban1,ban2,ban3").execute()
        match2chara=[]
        match1chara=[]
        for i in response.data:
            match_count=0
            if i["ban1"] in selected_survivor:
                match_count+=1
            if i["ban2"] in selected_survivor:
                match_count+=1
            if i["ban3"] in selected_survivor:
                match_count+=1
            if match_count==2:
                match2chara.append(i)
            elif match_count==1:
                match1chara.append(i)
        if match2chara!=[]:
            st.table(match2chara)
        else:
            st.text("該当なし")
        #１キャラ一致
        #データが増えたので一時削除
        #st.text("【１キャラ一致】")
        #if match1chara!=[]:
        #    st.table(match1chara)
        #else:
        #    st.text("該当なし")
    else:
        st.warning("３人入力してください")

#データ操作
if st.button("記録"):
    if ban1!="" and ban2!="" and ban3!="" and hunter!="":
        res = supabase.table("BannedCharaList").insert({
            "rank":rank,
            "ban1":ban1,
            "ban2":ban2,
            "ban3":ban3,
            "map":map,
            "hunter":hunter,
            "banned_hunter1":banned_hunter1,
            "banned_hunter2":banned_hunter2}).execute()
        st.success("記録完了")
    else:
        st.warning("未入力の項目があります")


#入力フォーム_スポーン位置
#任意・試験的であることを明記
with st.expander("【作業中】スポーン記録(任意)"):
    st.title(map)
    #ハンターの位置
    with st.container():
        if map=="永眠町":
            col_1=st.columns(4)
            col_2=st.columns(3)
            col_3=st.columns(3)
            for sp in sp_list[:4]:
                with col_1[sp_list.index(sp)]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")
            for sp in sp_list[4:7]:
                with col_2[sp_list.index(sp)-4]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")
            for sp in sp_list[7:11]:
                with col_3[sp_list.index(sp)-7]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")

        elif map=="湖景村" or map=="月の河公園":
            col_1=st.columns(4)
            col_2=st.columns(4)
            col_3=st.columns(4)
            for sp in sp_list[:4]:
                with col_1[sp_list.index(sp)]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")
            for sp in sp_list[4:8]:
                with col_2[sp_list.index(sp)-3]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")
            for sp in sp_list[8:]:
                with col_3[sp_list.index(sp)-6]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")

        else:
            col_1=st.columns(3)
            col_2=st.columns(3)
            col_3=st.columns(3)
            for sp in sp_list[:3]:
                with col_1[sp_list.index(sp)]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")
            for sp in sp_list[3:6]:
                with col_2[sp_list.index(sp)-3]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")
            for sp in sp_list[6:9]:
                with col_3[sp_list.index(sp)-6]:
                    if st.button(f"{sp}",key=f"{sp}"):
                        st.session_state["spaw_h"]=sp
                        st.write(f"選択中のスポーン位置：{sp}")