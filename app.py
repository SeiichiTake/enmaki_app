import pandas as pd
import numpy as np
import datetime
import yaml

import streamlit as st
import streamlit_authenticator as stauth

from configs.config import(
    NAMES, AREAS, FISHES
)

name_list = NAMES
area_list = AREAS
fish_list = FISHES

st.set_page_config(layout="wide") # ページのレイアウト設定

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# ログイン機能
authenticator.login()

def main():
    st.title('IQ枠交換WEBアプリ')
    st.divider()

    if st.session_state["authentication_status"]:
        ## ログイン成功
        with st.sidebar:
            st.markdown(f'## Welcome *{st.session_state["name"]}*')
            authenticator.logout('Logout', 'sidebar')
            st.divider()
    
        # TODO: ユーザー情報は日本語に変換したほうがよさそう
        login_user = st.session_state["name"]

        # TODO: ページを分けるのであれば、session_stateを使って情報を保持する

        df = pd.read_csv('data/data_sample.csv') # 将来的にはDBから取得する.今はサンプルデータを使用
        df_transfered_old = pd.read_csv('data/data_transfered.csv') # 将来的にはDBから取得する.今はサンプルデータを使用
        df_got_old = pd.read_csv('data/data_got.csv') # 将来的にはDBから取得する.今はサンプルデータを使用
        # TODO: データをきれいに成型する必要あり

        # session_stateにデータを保存
        if 'df_transfer' not in st.session_state:
            st.session_state.df_transfer = df[df['status'] == 'transfer']
        if 'df_get' not in st.session_state:
            st.session_state.df_get = df[df['status'] == 'get']
        if 'df_transfered' not in st.session_state:
            st.session_state.df_transfered = df_transfered_old
        if 'df_got' not in st.session_state:
            st.session_state.df_got = df_got_old

        df_transfer = st.session_state.df_transfer
        df_get = st.session_state.df_get

        st.markdown('## 余っている枠一覧')
        st.dataframe(df_transfer, hide_index=True)
        # 新規に余っている枠を譲渡申請する場合の機能
        st.write('新規枠譲渡申請をする')
        new_transfer_name = login_user
        new_transfer_area = st.selectbox('海区を選択してください', area_list, key = 'new_transfer_area') # 将来的にはDBもしくはconfigから取得する
        new_transfer_fish = st.selectbox('枠の魚種を選択してください', fish_list, key = 'new_transfer_fish') # 将来的にはDBもしくはconfigから取得する
        new_transfer_quota = st.number_input('枠の数量を入力してください', min_value=0, max_value=1000, value=0, key = 'new_transfer_quota')
        new_transfer_submit = st.button('新規枠譲渡申請を送信する')
        if new_transfer_submit:
            new_transfer_id = int(df_transfer['id'].max() + 1)
            formatted_date = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d'))
            new_transfer_data = pd.DataFrame({'id': [new_transfer_id], 'date': [formatted_date], 'name': [new_transfer_name], 'area': [new_transfer_area], 'fish': [new_transfer_fish], 'quota': [new_transfer_quota], 'status': ['transfer']})
            df_transfer = pd.concat([df_transfer, new_transfer_data], ignore_index=True)
            st.session_state.df_transfer = df_transfer
            st.info('新規枠譲渡申請を送信しました')
            df = pd.concat([df_transfer, df_get], ignore_index=True)
            df.to_csv('data/data_sample.csv', index=False)
            # ページをリロードする
            # st.rerun(scope="app")

        st.divider()
        st.markdown('## 足りていない枠一覧')
        st.dataframe(df_get, hide_index=True)
        # 新規に足りない枠を取得申請する場合の機能
        st.write('新規枠取得申請をする')
        new_get_name = login_user
        new_get_area = st.selectbox('海区を選択してください', area_list, key = 'new_get_area') # 将来的にはDBもしくはconfigから取得する
        new_get_fish = st.selectbox('枠の魚種を選択してください', fish_list, key = 'new_get_fish') # 将来的にはDBもしくはconfigから取得する
        new_get_quota = st.number_input('枠の数量を入力してください', min_value=0, max_value=1000, value=0, key = 'new_get_quota')
        new_get_submit = st.button('新規枠取得申請を送信する')
        if new_get_submit:
            new_get_id = int(df_get['id'].max() + 1)
            formatted_date = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d'))
            new_get_data = pd.DataFrame({'id': [new_get_id], 'date': [formatted_date], 'name': [new_get_name], 'area': [new_get_area], 'fish': [new_get_fish], 'quota': [new_get_quota], 'status': ['get']})
            df_get = pd.concat([df_get, new_get_data], ignore_index=True)
            st.session_state.df_get = df_get
            st.info('新規枠取得申請を送信しました')
            df = pd.concat([df_transfer, df_get], ignore_index=True)
            df.to_csv('data/data_sample.csv', index=False)
            # ページをリロードする
            # st.rerun(scope="app")

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
                st.dataframe(df_transfer[df_transfer['id'] == select_get], hide_index=True)
                get_request = st.button('枠をもらう依頼を確定する')
                if get_request:
                    df_transfer_new = df_transfer[df_transfer['id'] != select_get]
                    df_transfered = df_transfer[df_transfer['id'] == select_get]
                    df_transfered['got-name'] = login_user
                    df_transfered['date'] = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d'))
                    df_transfered.rename(columns={'name':'transfer-name'}, inplace=True)
                    df_transfered = df_transfered[['date', 'transfer-name', 'got-name', 'area', 'fish', 'quota']]
                    st.session_state.df_transfered = pd.concat([st.session_state.df_transfered, df_transfered], ignore_index=True)              
                    st.session_state.df_transfer = df_transfer_new
                    df = pd.concat([df_transfer_new, df_get], ignore_index=True)
                    df.to_csv('data/data_sample.csv', index=False)
                    df_transfered_new = st.session_state.df_transfered
                    df_transfered_new.to_csv('data/data_transfered.csv', index=False)
                    st.info('枠をもらう依頼を確定しました')
                    # ページをリロードする
                    # st.rerun(scope="app")
        elif select_get_or_transfer == '枠を譲る':
            st.write('どの枠を譲りますか？')
            select_transfer = st.selectbox('枠を選択してください', df_get['id'])
            if select_transfer is not None:
                st.write('譲る枠の詳細情報')
                st.dataframe(df_get[df_get['id'] == select_transfer], hide_index=True)
                transfer_request = st.button('枠を譲る依頼を確定する')
                if transfer_request:
                    df_get_new = df_get[df_get['id'] != select_transfer]
                    df_got = df_get[df_get['id'] == select_transfer]
                    df_got['transfer-name'] = login_user
                    df_got['date'] = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y/%m/%d'))
                    df_got.rename(columns={'name':'got-name'}, inplace=True)
                    df_got = df_got[['date', 'transfer-name', 'got-name', 'area', 'fish', 'quota']]
                    st.session_state.df_got = pd.concat([st.session_state.df_got, df_got], ignore_index=True)
                    st.session_state.df_get = df_get_new
                    df = pd.concat([df_transfer, df_get_new], ignore_index=True)
                    df.to_csv('data/data_sample.csv', index=False)
                    df_got_new = st.session_state.df_got
                    df_got_new.to_csv('data/data_got.csv', index=False)
                    st.info('枠を譲る依頼を確定しました')
                    # ページをリロードする
                    # st.rerun(scope="app")

    elif st.session_state["authentication_status"] is False:
        st.error('ユーザ名またはパスワードが間違っています')
    elif st.session_state["authentication_status"] is None:
        st.warning('ユーザ名やパスワードを入力してください')


if __name__ == '__main__':
    main()