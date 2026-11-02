"""Streamlit Cloud chat interface and Gemini 3.8 Flash tool-calling agent."""

import os
import streamlit as st
from google import genai
from google.genai import types
from tools import get_live_weather, lookup_wikipedia_summary, search_study_dataset

st.set_page_config(page_title="Zero-Cost Cloud AI Agent", page_icon="🤖")
st.title("🤖 Cloud Research & Weather Agent")
st.caption("Free-tier Gemini 3.8 Flash + Open-Meteo + Wikimedia + CSV Dataset")

api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    api_key = ""
api_key = api_key or os.getenv("GEMINI_API_KEY", "")

if not api_key:
    st.warning("Add GEMINI_API_KEY in Streamlit Secrets (or environment) to begin.")
    st.stop()

SYSTEM_INSTRUCTIONS = (
    "You are a friendly, precise AI research concierge. Use get_live_weather for "
    "current weather, lookup_wikipedia_summary for factual background, and "
    "search_study_dataset for learning recommendations. Always include source links."
)

if "chat_session" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)
    st.session_state.chat_session = st.session_state.client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            tools=[get_live_weather, lookup_wikipedia_summary, search_study_dataset],
            temperature=0.2,
        ),
    )
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about live weather, a concept, or free AI courses..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking live tools..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                reply = response.text or "Tool check finished—please try rephrasing."
            except Exception as err:
                reply = f"⚠️ Temporary API limit or network hiccup: `{err}`"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
