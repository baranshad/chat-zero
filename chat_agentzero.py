# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 21:13:39 2025

@author: yuang
"""



import streamlit as st
import openai
import os
#%%
st.set_page_config(page_title="Chat with ZeroAgent", page_icon="🤖")

st.title("🤖 AI Agent Chat")
st.write("Chat with an OpenAI-powered agent. Type a message and press enter.")
#%%
api_key = st.secrets["openai_api_key"]  # Streamlit secrets 

openai.api_key = api_key
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
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=st.session_state["messages"],
            stream=True
        )
        reply = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if "content" in delta:
                reply += delta.content

        st.write(reply)
        st.session_state["messages"].append({"role": "assistant", "content": reply})
