import pandas as pd
import numpy as np
import datetime
import yaml
from io import BytesIO
import sqlite3
import openpyxl

import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title = "漁獲情報確認ページ", layout="wide") # ページのレイアウト設定

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
    st.title('IQ漁獲情報管理WEBアプリ')
    st.divider()

    # このページは、集計した漁獲情報を表示するだけのページ

    if st.session_state["authentication_status"]:
        ## ログイン成功
        if st.session_state["name"] == "enmaki":
            st.session_state["login_user"] = "えんまき"
        elif st.session_state["name"] == "sanmaki":
            st.session_state["login_user"] = "さんまき"
        with st.sidebar:
            st.markdown(f'## Welcome *{st.session_state["login_user"]}*')
            authenticator.logout('Logout', 'sidebar')
            st.divider()
        
        # DBからデータを取得
        dbname = "data/TEST.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        # dbをpandasで読み出す。
        df = pd.read_sql('SELECT * FROM sample', conn)
        cur.close()
        conn.close()

        # TODO: ページを分けるのであれば、session_stateを使って情報を保持する

        # dataframe形式で表示する
        st.markdown("### さば類の漁獲情報")
        df_saba = df[df["fish"] == "さば類"]
        st.dataframe(df_saba, hide_index=True)

        # ダウンロードボタン
        df_saba.to_excel(buf := BytesIO(), index=False)
        st.download_button(
            "Download",
            buf.getvalue(),
            "saba.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.divider()

        st.markdown("### まいわしの漁獲情報")
        df_maiwashi = df[df["fish"] == "まいわし"]
        st.dataframe(df_maiwashi, hide_index=True)

        # ダウンロードボタン
        df_maiwashi.to_excel(buf := BytesIO(), index=False)
        st.download_button(
            "Download",
            buf.getvalue(),
            "maiwashi.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.divider()

        st.markdown("### まあじの漁獲情報")
        df_maaji = df[df["fish"] == "まあじ"]
        st.dataframe(df_maaji, hide_index=True)

        # ダウンロードボタン
        df_maaji.to_excel(buf := BytesIO(), index=False)
        st.download_button(
            "Download",
            buf.getvalue(),
            "maaji.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.divider()

    elif st.session_state["authentication_status"] is False:
        st.error('ユーザ名またはパスワードが間違っています')
    elif st.session_state["authentication_status"] is None:
        st.warning('ユーザ名やパスワードを入力してください')


if __name__ == '__main__':
    main()