import pandas as pd
import numpy as np
import datetime
import yaml

import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title = "漁獲情報入力ページ", layout="wide") # ページのレイアウト設定

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def main():
    st.title('IQ漁獲情報管理WEBアプリ')
    st.divider()

    if st.session_state["authentication_status"]:
    ## ログイン成功
        with st.sidebar:
            st.markdown(f'## Welcome *{st.session_state["login_user"]}*')
            authenticator.logout('Logout', 'sidebar')

        st.markdown('### 漁獲情報のファイルをアップロード')
    
    else:
        st.markdown('## ログインしてください')
        authenticator.login()

if __name__ == '__main__':
    main()