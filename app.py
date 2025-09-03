"""
ランク戦ban管理
作成日：2025/09/03
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

#アプリ作成
#アプリ名
st.title("ランク戦BANリスト")

#入力フォーム_段位
rank=st.selectbox("段位を選択",options=["5","6","7"])

#入力フォーム_サバイバー
survivors={0: '', 1: '医師', 2: '弁護士', 3: '泥棒', 4: '庭師', 5: ' マジシャン',
           6: '冒険家', 7: '傭兵', 8: '空軍', 9: '祭司', 10: '機械技師',
           11: ' オフェンス', 12: '心眼', 13: '調香師', 14: 'カウボーイ', 15: '踊り子',
           16: ' 占い師', 17: '納棺師', 18: '探鉱者', 19: '呪術師', 20: '野人',
           21: '曲芸師', 22: '一等航海士', 23: 'バーメイド', 24: 'ポストマン', 25: '墓守',
           26: '｢囚人｣', 27: '昆虫学者', 28: '画家', 29: 'バッツマン', 30: '玩具職人',
           31: '患者', 32: '｢心理学者｣', 33: '小説家', 34: '｢少女｣', 35: '泣きピエロ',
           36: '教授', 37: '骨董商', 38: '作曲家', 39: '記者', 40: '航空エンジニア',
           41: '応援団', 42: '人形師', 43: '火災調査員', 44: '｢レディ・ファウロ｣', 45: '｢騎士｣',
           46: '気象学者', 47: '弓使い', 48: '｢脱出マスター｣', 49: '幸運児'}
banA=st.selectbox("1人目のBAN済サバイバーを選択",options=list(survivors.values()))
banB=st.selectbox("2人目のBAN済サバイバーを選択",options=list(survivors.values()))
banC=st.selectbox("3人目のBAN済サバイバーを選択",options=list(survivors.values()))
#書き込む前に並べ替え
selected_survivor=[banA,banB,banC]
sorted_ban=sorted(selected_survivor,key=lambda x:survivors.get(x,x))
ban1=sorted_ban[0]
ban2=sorted_ban[1]
ban3=sorted_ban[2]

#入力フォーム_マップ
maps=["","軍需工場","赤の教会","聖心病院","湖景村","月の河公園","レオの思い出","永眠町","中華街","罪の森"]
map=st.selectbox("マップを選択",options=maps)

#入力フォーム_対戦ハンター
hunters={0: '', 1: '復讐者', 2: '道化師', 3: '断罪狩人', 4: 'リッパー', 5: '結魂者',
         6: '芸者', 7: '白黒無常', 8: '写真家', 9: '狂眼', 10: '黄衣の王',
         11: '夢の魔女', 12: '泣き虫', 13: '魔トカゲ', 14: '血の女王', 15: 'ガードNo.26',
         16: '「使徒」', 17: 'ヴァイオリニスト', 18: '彫刻師', 19: '「アンデッド」', 20: '破輪',
         21: '漁師', 22: '蝋人 形師', 23: '「悪夢」', 24: '書記官', 25: '隠者',
         26: '夜の番人', 27: 'オペラ歌手', 28: '「フールズ・ゴールド」', 29: '時空の影', 30: '「足萎えの羊」',
         31: '「フラバルー」', 32: '雑貨商', 33: '「ビリヤードプレイヤー」'} 
hunter=st.selectbox("対戦ハンターを選択",options=list(hunters.values()))
banned_hunterA=st.selectbox("1人目のBAN済ハンターを選択",options=list(hunters.values()))
banned_hunterB=st.selectbox("2人目のBAN済ハンターを選択",options=list(hunters.values()))
#並べ替え
selected_hunter=[banned_hunterA,banned_hunterB]
sorted_ban=sorted(selected_hunter,key=lambda x:hunters.get(x,x))
banned_hunter1=sorted_ban[0]
banned_hunter2=sorted_ban[1]

#データ表示
if st.button("予測"):
    if ban1 and ban2 and ban3:
        #３キャラ一致
        response=supabase.table("BannedCharaList").select("*").eq("ban1",ban1).eq("ban2",ban2).eq("ban3",ban3).execute()
        if response.data:
            st.table(response.data)
        #２キャラ一致
        response=supabase.table("BannedCharaList").select("*").execute()
        match2chara=[]
        for i in response.data:
            match_count=0
            if i["ban1"]==ban1:
                match_count+=1
            if i["ban2"]==ban2:
                match_count+=1
            if i["ban3"]==ban3:
                match_count+=1
            if match_count==2:
                match2chara.append(i)
        if match2chara!=[]:
            st.table(match2chara)
        #１キャラ一致
        response=supabase.table("BannedCharaList").select("*").or_("ban1.eq.ban1,ban2.eq.ban2,ban3.eq.ban3").execute()
        if response.data:
            st.table(response.data)

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

        








