import streamlit as st
import google.generativeai as genai

# Set up the Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="🎲 AI Dungeon Master", page_icon="🧙")
st.title("🎲 AI Dungeon Master")
st.markdown("Enter a fantasy world and let the AI Dungeon Master guide your adventure. Choose your actions and shape your story.")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": (
            "You are a Dungeon Master in a fantasy world. Your job is to guide the user through a dynamic text-based RPG adventure. "
            "Start by introducing the world and asking the user to choose a character class. Each turn, describe what happens next, give them 2-3 options, and ask what they do. "
            "Always keep the narrative immersive, detailed, and grounded in fantasy elements like magic, monsters, and quests."
        )}
    ]

# Display the history
for msg in st.session_state.history[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("What will you do next?"):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("The Dungeon Master is thinking..."):
            try:
                # Combine history into one prompt
                prompt_text = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.history[1:])
                full_prompt = (
                    "You are an AI Dungeon Master guiding a fantasy RPG experience. Continue the story based on the user input.\n\n"
                    + prompt_text + "\n\nDungeon Master:"
                )
                response = model.generate_content(full_prompt)
                reply = response.text
                st.markdown(reply)
                st.session_state.history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
