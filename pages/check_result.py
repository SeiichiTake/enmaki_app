import pandas as pd
import numpy as np
import datetime
import yaml

import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(layout="wide") # ページのレイアウト設定

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def main():
    st.title('IQ枠交換WEBアプリ')
    st.divider()

    if st.session_state["authentication_status"]:
    ## ログイン成功
        with st.sidebar:
            st.markdown(f'## Welcome *{st.session_state["name"]}*')
            authenticator.logout('Logout', 'sidebar')

        st.markdown('### 交換情報')
        if 'df_transfered' not in st.session_state:
            st.session_state.df_transfered = pd.read_csv('data/data_transfered.csv')
        if 'df_got' not in st.session_state:
            st.session_state.df_got = pd.read_csv('data/data_got.csv')
            
        st.dataframe(pd.concat([st.session_state.df_transfered, st.session_state.df_got], axis=0))
    
    else:
        st.markdown('## ログインしてください')
        authenticator.login()

if __name__ == '__main__':
    main()