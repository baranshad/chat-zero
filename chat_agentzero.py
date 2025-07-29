# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 21:13:39 2025

@author: yuang
"""



import streamlit as st
from openai import OpenAI
import os
#%%
st.set_page_config(page_title="Chat with ZeroAgent", page_icon="🤖")

st.title("🤖 Agent Zero Chat")
st.write("Chat with an OpenAI-powered agent Zero. It can teach you how to play stock.")
#%%
api_key = st.secrets["openai_api_key"]  # Streamlit secrets 
client = OpenAI(api_key=api_key)
#openai.api_key = api_key
#%%
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant. Please make short responses."},
        {"role": "assistant", "content": "Hello Friend! How can I help you today?"}
    ]

for msg in st.session_state["messages"][1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Your message"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=st.session_state["messages"],
            stream=True
        )
        reply = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                reply += content

        st.write(reply)
        st.session_state["messages"].append({"role": "assistant", "content": reply})
