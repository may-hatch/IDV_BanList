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
import streamlit as st

#supabaseにつなげる
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
supabase=create_client(url,key)

#マップ管理
if "spawn_h" not in st.session_state:
    st.session_state["spawn_h"]=[""]

if "spawn_s" not in st.session_state:
    st.session_state["spawn_s"]=[None]*4

sp_list=["01","02","03","04","05","06","07","08","09","10","11","12"]

#アプリ作成
#アプリ名
st.title("BAN記録/検索")

with st.expander("使い方"):
    st.write("""
    【目的】
    五段以上の鯖３BANを想定した記録フォームです。

    サバイバー段位(最高峰は7)、BANされたキャラ、マップ、ハンターを選択してください。
    
    必須項目を入力後「サバイバーから検索」を押すと、そのBANをしたハンターの一覧を表示します。
    ２キャラのみ一致の場合は、マップが一致しているハンターが先に表示されます。
    
    入力後に「記録」を押すと、そこまでに入力した情報が記録されます。

    「ハンターから検索」を押すと、過去にそのハンターがどんなBANをしたかの記録が表示されます。
    
    【更新】
    2025-09-25-11:30
    記録時のソート方法を更新。
    統計表示ボタンを追加。
             
    【更新予定】
    段位を考慮して表示(私の段位が上がれば…)
    """)

#統計表示
if st.button("統計を表示（テスト中）"):
    response_all=supabase.table("BannedCharaList").select("hunter").execute()
    records_all=response_all.data

    hunter_list=[rec["hunter"] for rec in records_all if rec["hunter"]]
    hunter_counts=Counter(hunter_list)
    
    total=sum(hunter_counts.values())
    sorted_by_cnt={k:v for k,v in hunter_counts.items()}
#    hunter_ratio={k:round(v/total*100,2) for k,v in hunter_counts.items()}

#ハンター名と割合を並び替えたリストに変換
    sorted_items = sorted(sorted_by_cnt.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    
    st.write(f"総記録件数：{total}件")
    st.write("【遭遇率上位3キャラ】")
    for si in sorted_items[:3]:
        st.write(f"{si[0]}：{si[1]}試合({si[1]/total}%)")

#pltでグラフ描画
#    fig, ax = plt.subplots()
#    ax.bar(labels, values)
#    ax.set_ylabel("割合（％）")
#    ax.set_title("ハンター遭遇率")
#    plt.xticks(rotation=45)
# Streamlitで表示
#    st.pyplot(fig)

#pandasでつくって表示
    df=pd.DataFrame({
        "ハンター":list(hunter_ratio.keys()),
        "割合(％)":list(hunter_ratio.values())
    }).sort_values("割合(％)",ascending=False)
    st.bar_chart(df.set_index("ハンター"))
    
#入力フォーム_段位
rank=st.selectbox("段位を選択",options=["5","6","7"])

#入力フォーム_マップ
maps=["","軍需工場","赤の教会","聖心病院","湖景村","月の河公園","レオの思い出","永眠町","中華街","罪の森"]
map=st.selectbox("マップを選択（必須）",options=maps)

#入力フォーム_サバイバー
#見やすさのためにたたむ
with st.expander("BANされたサバイバーを記録（必須）"):
    survivors= {999: '', 1: '医師', 2: '弁護士', 3: '泥棒', 4: '庭師', 5: 'マジシャン',
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
    name_to_id_s={v_s:k_s for k_s,v_s in survivors.items()}
    selected_survivor=[banA,banB,banC]
    sorted_ban=sorted(selected_survivor,key=lambda x:name_to_id_s.get(x,999))
    ban1=sorted_ban[0]
    ban2=sorted_ban[1]
    ban3=sorted_ban[2]

#入力フォーム_対戦ハンター
hunters={999: '', 1: '復讐者', 2: '道化師', 3: '断罪狩人', 4: 'リッパー', 5: '結魂者',
         6: '芸者', 7: '白黒無常', 8: '写真家', 9: '狂眼', 10: '黄衣の王',
         11: '夢の魔女', 12: '泣き虫', 13: '魔トカゲ', 14: '血の女王', 15: 'ガードNo.26',
         16: '「使徒」', 17: 'ヴァイオリニスト', 18: '彫刻師', 19: '「アンデッド」', 20: '破輪',
         21: '漁師', 22: '蝋人形師', 23: '「悪夢」', 24: '書記官', 25: '隠者',
         26: '夜の番人', 27: 'オペラ歌手', 28: '「フールズ・ゴールド」', 29: '時空の影', 30: '「足萎えの羊」',
         31: '「フラバルー」', 32: '雑貨商', 33: '「ビリヤードプレイヤー」'} 
hunter=st.selectbox("対戦ハンターを選択（必須）",options=list(hunters.values()))
#入力フォーム_BAN済ハンター
#BAN済ハンターは任意なのでたたむ
with st.expander("BANしたハンターを記録（任意）"):
    banned_hunterA=st.selectbox("1人目のBAN済ハンター",options=list(hunters.values()))
    banned_hunterB=st.selectbox("2人目のBAN済ハンター",options=list(hunters.values()))
    banned_hunterC=st.selectbox("3人目のBAN済ハンター",options=list(hunters.values()))
#並べ替え
    name_to_id_h={v_h:k_h for k_h,v_h in hunters.items()}
    selected_hunter=[banned_hunterA,banned_hunterB,banned_hunterC]
    sorted_ban=sorted(selected_hunter,key=lambda x:name_to_id_h.get(x,999))
    banned_hunter1=sorted_ban[0]
    banned_hunter2=sorted_ban[1]
    banned_hunter3=sorted_ban[2]

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
            st.session_state["spawn_h"]=""
        spawn_h=st.session_state["spawn_h"]
        st.text(f"選択中スポーン位置：{spawn_h}")        
#サバイバーの位置
    with st.expander("サバイバーの位置"):
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
        if st.button("スポーンを確定"):    
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

#データ表示
#サバイバーからハンターを検索
if st.button("サバイバーから検索"):
    if ban1!="" and ban2!="" and ban3!="":
        #３キャラ一致
        st.text("【３キャラ一致】")
        response=supabase.table("BannedCharaList").select("hunter,map,ban1,ban2,ban3").eq("ban1",ban1).eq("ban2",ban2).eq("ban3",ban3).execute()
        if response.data:
            st.table(response.data)
        else:
            st.text("該当なし")
        #２キャラ一致
        st.text("【２キャラ一致】")
        response=supabase.table("BannedCharaList").select("hunter,map,ban1,ban2,ban3").execute()
        match2chara_map=[]
        match2chara=[]
        #match1chara=[]
        for i in response.data:
            match_m=False
            match_count_c=0
            if i["map"] == map:
                match_m=True
            if i["ban1"] in selected_survivor:
                match_count_c+=1
            if i["ban2"] in selected_survivor:
                match_count_c+=1
            if i["ban3"] in selected_survivor:
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
            st.text("マップ不一致")
            st.table(match2chara)
        if match2chara_map==[] and match2chara==[]:
            st.text("該当なし")
    else:
        st.warning("３人入力してください")

#ハンターからサバイバーを検索
if st.button("ハンターから検索"):
    if hunter!="":
        response=supabase.table("BannedCharaList").select("hunter,map,ban1,ban2,ban3").eq("hunter",hunter).execute()
        if response.data:
            st.table(response.data)
        else:
            st.text("記録なし")

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