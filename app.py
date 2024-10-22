import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(layout="wide") # ページのレイアウト設定

def main():
    st.title('IQ枠交換WEBアプリ')
    st.divider()

    # TODO: ログイン機能
    # TODO: ユーザー情報を取得する

    # TODO: ページを分けるのであれば、session_stateを使って情報を保持する

    df = pd.read_csv('data/data_sample.csv') # 将来的にはDBから取得する.今はサンプルデータを使用
    # TODO: データをきれいに成型する必要あり

    st.markdown('## 余っている枠一覧')
    df_transfer = df[df['status'] == 'transfer']
    st.table(df_transfer)
    # 新規に余っている枠を譲渡申請する場合の機能
    st.write('新規枠譲渡申請をする')
    new_transfer_name = st.selectbox('漁業者名を選択してください', ['漁業者A', '漁業者B', '漁業者C', '漁業者D'], key = 'new_transfer_name') # 将来的にはDBもしくはconfigから取得する
    new_transfer_area = st.selectbox('海区を選択してください', ['海区1', '海区2'], key = 'new_transfer_area') # 将来的にはDBもしくはconfigから取得する
    new_transfer_fish = st.selectbox('枠の魚種を選択してください', ['さば', 'まいわし', 'あじ'], key = 'new_transfer_fish') # 将来的にはDBもしくはconfigから取得する
    new_transfer_quota = st.number_input('枠の数量を入力してください', min_value=0, max_value=1000, value=0, key = 'new_transfer_quota')
    new_transfer_submit = st.button('新規枠譲渡申請を送信する')
    if new_transfer_submit:
        new_transfer_id = df_transfer['id'].max() + 1
        new_transfer_data = pd.DataFrame({'id': [new_transfer_id], 'date': [datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))], 'name': [new_transfer_name], 'area': [new_transfer_area], 'fish': [new_transfer_fish], 'quota': [new_transfer_quota], 'status': ['transfer']})
        df = pd.concat([df, new_transfer_data], ignore_index=True)
        st.write('新規枠譲渡申請を送信しました')
        df.to_csv('data/data_sample.csv', index=False)
        # ページをリロードする
        st.rerun(scope="app")


    # TODO: 枠をもらいたい人の情報を表示
    st.divider()
    st.markdown('## 足りていない枠一覧')
    df_get = df[df['status'] == 'get']
    st.table(df_get)
    # 新規に足りない枠を取得申請する場合の機能
    st.write('新規枠取得申請をする')
    new_get_name = st.selectbox('漁業者名を選択してください', ['漁業者A', '漁業者B', '漁業者C', '漁業者D'], key = 'new_get_name') # 将来的にはDBもしくはconfigから取得する
    new_get_area = st.selectbox('海区を選択してください', ['海区1', '海区2'], key = 'new_get_area') # 将来的にはDBもしくはconfigから取得する
    new_get_fish = st.selectbox('枠の魚種を選択してください', ['さば', 'まいわし', 'あじ'], key = 'new_get_fish') # 将来的にはDBもしくはconfigから取得する
    new_get_quota = st.number_input('枠の数量を入力してください', min_value=0, max_value=1000, value=0, key = 'new_get_quota')
    new_get_submit = st.button('新規枠取得申請を送信する')
    if new_get_submit:
        new_get_id = df_get['id'].max() + 1
        new_get_data = pd.DataFrame({'id': [new_get_id], 'date': [datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))], 'name': [new_get_name], 'area': [new_get_area], 'fish': [new_get_fish], 'quota': [new_get_quota], 'status': ['get']})
        df = pd.concat([df, new_get_data], ignore_index=True)
        st.write('新規枠取得申請を送信しました')
        df.to_csv('data/data_sample.csv', index=False)
        # ページをリロードする
        st.rerun(scope="app")

    # すでに提示されている枠の中から、枠交換を依頼する機能
    st.divider()
    st.markdown('## 枠交換依頼')
    st.write('枠を譲りたいか、もらいたいかを選択してください')
    select_get_or_transfer = st.selectbox('枠をもらうor枠を譲る', ['枠をもらう', '枠を譲る'], key = 'select_get_or_transfer')
    if select_get_or_transfer == '枠をもらう':
        st.write('どの枠をもらいたいですか？')
        select_get = st.selectbox('枠を選択してください', df_transfer['id'], key = 'select_get')
        if select_get is not None:
            st.write('もらう枠の詳細情報')
            st.table(df_transfer[df_transfer['id'] == select_get])
            get_request = st.button('枠をもらう依頼を確定する')
            if get_request:
                st.write('枠をもらう依頼を確定しました')
                df.loc[df['id'] == select_get, 'status'] = 'got'
                df.to_csv('data/data_sample.csv', index=False)
                # ページをリロードする
                st.rerun(scope="app")
    elif select_get_or_transfer == '枠を譲る':
        st.write('どの枠を譲りますか？')
        select_transfer = st.selectbox('枠を選択してください', df_get['id'])
        if select_transfer is not None:
            st.write('譲る枠の詳細情報')
            st.table(df_get[df_get['id'] == select_transfer])
            transfer_request = st.button('枠を譲る依頼を確定する')
            if transfer_request:
                st.write('枠を譲る依頼を確定しました')
                df.loc[df['id'] == select_transfer, 'status'] = 'transferred'
                df.to_csv('data/data_sample.csv', index=False)
                # ページをリロードする
                st.rerun(scope="app")


if __name__ == '__main__':
    main()