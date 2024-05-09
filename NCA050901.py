import streamlit as st
import pandas as pd
import base64

# データフレームを初期化
data = {'食品名': [], 'エネルギー': [], 'たんぱく質': [], '脂質': [], '炭水化物': [], '食塩': [], '単価': []}
df = pd.DataFrame(data)

# Streamlitアプリを設定
st.title('食品データベース')

# サイドバーに配置する要素（Aページの場合）
st.sidebar.title('食品成分の登録')
food_name = st.sidebar.text_input('食品名')
energy = st.sidebar.number_input('エネルギー', min_value=0.0, step=0.1, format="%.1f")
protein = st.sidebar.number_input('たんぱく質', min_value=0.0, step=0.1, format="%.1f")
fat = st.sidebar.number_input('脂質', min_value=0.0, step=0.1, format="%.1f")
carbs = st.sidebar.number_input('炭水化物', min_value=0.0, step=0.1, format="%.1f")
salt = st.sidebar.number_input('食塩', min_value=0.0, step=0.1, format="%.1f")
price = st.sidebar.number_input('単価', min_value=0.0, step=0.01, format="%.1f")
register_button = st.sidebar.button('食品成分を登録')

# 食品成分を登録する関数
def register_food(food_name, energy, protein, fat, carbs, salt, price):
    df.loc[len(df)] = [food_name, energy, protein, fat, carbs, salt, price]

# 登録ボタンがクリックされたら食品成分を登録
if register_button:
    if food_name != '':
        register_food(food_name, energy, protein, fat, carbs, salt, price)

# 新しく登録された食品成分を表示する
st.subheader('新しい食品データ:')
st.write(df)

# CSVファイルをストリーミングしてダウンロード
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="food_data.csv">食品データをダウンロード</a>'
st.markdown(href, unsafe_allow_html=True)

# 保存した食品データをアップロード
uploaded_file = st.sidebar.file_uploader('保存した食品データをアップロード', type=['csv'])
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    combined_df = pd.concat([df, uploaded_df], ignore_index=True)
    st.subheader('保存した食品データと新しい食品データ:')
    st.write(combined_df)
    
else:
    st.subheader('保存した食品データと新しい食品データ:')
    st.write(df)
    
# 初期表示時に結合した食品データをダウンロードできるリンクを表示
combined_filename = 'combined_food_list.csv'
b64_combined = base64.b64encode(df.to_csv(index=False).encode()).decode()
href_combined = f'<a href="data:file/csv;base64,{b64_combined}" download="{combined_filename}">結合した食品データをダウンロード</a>'
st.markdown(href_combined, unsafe_allow_html=True)

# リセットボタンを配置
st.sidebar.markdown('---')
reset_button = st.sidebar.button('リセット')
if reset_button:
    df = pd.DataFrame(data)
    st.sidebar.success('データをリセットしました。')
