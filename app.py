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
survibors={0: '医師', 1: '弁護士', 2: '泥棒', 3: '庭師', 4: ' マジシャン', 5: '冒険家',
           6: '傭兵', 7: '空軍', 8: '祭司', 9: '機械技師', 10: 'オフェンス',
           11: '心眼', 12: '調香師', 13: 'カウボーイ', 14: '踊り子', 15: ' 占い師',
           16: '納棺師', 17: '探鉱者', 18: '呪術師', 19: '野人', 20: '曲芸師',
           21: '一等航海士', 22: 'バーメイド', 23: 'ポストマン', 24: '墓守', 25: '｢囚人｣',
           26: '昆虫学者', 27: '画家', 28: 'バッツマン', 29: '玩具職人', 30: '患者',
           31: '｢心理学者｣', 32: '小説家', 33: '｢少女｣', 34: '泣きピエロ', 35: '教授',
           36: '骨董商', 37: '作曲家', 38: '記者', 39: '航空エンジニア', 40: '応援団',
           41: '人形師', 42: '火災調査員', 43: '｢レディ・ファウロ｣', 44: '｢騎士｣', 45: '気象学者',
           46: '弓使い', 47: '｢脱出マスター｣', 48: '幸運児'}
banA=st.selectbox("1人目のBAN済サバイバーを選択",options=list(survibors.values()))
banB=st.selectbox("2人目のBAN済サバイバーを選択",options=list(survibors.values()))
banC=st.selectbox("3人目のBAN済サバイバーを選択",options=list(survibors.values()))
#書き込む前に並べ替え
selected_survivor=[banA,banB,banC]
sorted_ban=sorted(selected_survivor,key=lambda x:survibors.get(x,x))
ban1=sorted_ban[0]
ban2=sorted_ban[1]
ban3=sorted_ban[2]

#入力フォーム_マップ
maps=["軍需工場","赤の教会","聖心病院","湖景村","月の河公園","レオの思い出","永眠町","中華街","罪の森"]
map=st.selectbox("マップを選択",options=maps)

#入力フォーム_対戦ハンター
hunters={0: '復讐者', 1: '道化師', 2: '断罪狩人', 3: 'リッパー', 4: '結魂者', 5: '芸者',
         6: '白黒無常', 7: '写真家', 8: '狂眼', 9: '黄衣の王', 10: '夢の魔女',
         11: '泣き虫', 12: '魔トカゲ', 13: '血の女王', 14: 'ガードNo.26', 15: '「使徒」',
         16: 'ヴァイオリニスト', 17: '彫刻師', 18: '「アンデッド」', 19: '破輪', 20: '漁師',
         21: '蝋人 形師', 22: '「悪夢」', 23: '書記官', 24: '隠者', 25: '夜の番人',
         26: 'オペラ歌手', 27: '「フールズ・ゴールド」', 28: '時空の影', 29: '「足萎えの羊」', 30: '「フラバルー」',
         31: '雑貨商', 32: '「ビリヤードプレイヤー」'}
hunter=st.selectbox("対戦ハンターを選択",options=hunters)
banned_hunterA=st.selectbox("1人目のBAN済ハンターを選択",options=hunters)
banned_hunterB=st.selectbox("2人目のBAN済ハンターを選択",options=hunters)
#並べ替え
selected_hunter=[banned_hunterA,banned_hunterB]
sorted_ban=sorted(selected_hunter,key=lambda x:hunters.get(int("inf"),x))
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
    if ban1 and ban2 and ban3 and hunter:
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

        

