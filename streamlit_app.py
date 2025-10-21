import streamlit as st
from openai import OpenAI

st.title("💬 Custom Assistant Chatbot")
st.write(
    "Dieser Chatbot verwendet deinen eigenen Assistant aus der OpenAI Assistants API."
)

# Eingabe des API-Keys
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Bitte gib deinen OpenAI API-Key ein, um fortzufahren.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Session State für Verlauf und Thread-ID
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        # Erstelle einmalig einen neuen Thread für die Unterhaltung
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Bisherige Nachrichten anzeigen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Eingabefeld
    if prompt := st.chat_input("Was möchtest du wissen?"):

        # Eingabe anzeigen und speichern
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Nachricht an Assistant-Thread schicken
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt,
        )

        # Assistant-Run starten
        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread_id,
            assistant_id="asst_GafW0SOeCSLJXXqbCcmv95BJ",
        )

        # Antwort abrufen
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
            last_message = messages.data[0].content[0].text.value
        else:
            last_message = f"Run-Status: {run.status}"

        # Antwort anzeigen und speichern
        with st.chat_message("assistant"):
            st.markdown(last_message)

        st.session_state.messages.append({"role": "assistant", "content": last_message})
