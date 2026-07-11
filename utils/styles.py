import streamlit as st

def load_css():

    st.markdown(
        """
        <style>

        .main-title{
            text-align:center;
            font-size:40px;
            font-weight:bold;
            color:#4F46E5;
        }

        .sub-title{
            text-align:center;
            font-size:18px;
            color:gray;
        }

        .question-box{
            padding:20px;
            border-radius:10px;
            background:#f8f9fa;
            border:1px solid #ddd;
            margin-top:20px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )