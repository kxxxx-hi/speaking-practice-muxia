import streamlit as st
import json
import random

# Use st.cache_data to load the JSON file only once
@st.cache_data
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['flashcards']

data = load_data()

# Initialize session state for the game
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.flipped = False
    st.session_state.deck = random.sample(data, len(data))
    st.session_state.game_mode = 'Vocabulary'

def next_card():
    st.session_state.index = (st.session_state.index + 1) % len(st.session_state.deck)
    st.session_state.flipped = False

def flip_card():
    st.session_state.flipped = True

def switch_mode(mode):
    st.session_state.game_mode = mode
    st.session_state.index = 0
    st.session_state.flipped = False
    
    if mode == 'Vocabulary':
        st.session_state.deck = [item for item in data if item['type'] == 'vocabulary']
    elif mode == 'Sentences':
        st.session_state.deck = [item for item in data if item['type'] == 'sentence']
    else: # All
        st.session_state.deck = random.sample(data, len(data))
    
    if not st.session_state.deck:
        st.error("No items found for this category.")
        return
        
    random.shuffle(st.session_state.deck)


# --- UI Layout ---

st.title("慕夏 Part 2 Speaking Materials")
st.markdown("Practice your IELTS speaking with these vocabulary and sentence flashcards.")

# Game Mode Selection
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("All Cards"):
        switch_mode('All')
with col2:
    if st.button("Vocabulary Flashcard"):
        switch_mode('Vocabulary')
with col3:
    if st.button("Sentence Translation"):
        switch_mode('Sentences')

st.markdown("---")

# Display Flashcard
if st.session_state.deck:
    card = st.session_state.deck[st.session_state.index]

    with st.container(border=True):
        st.markdown(f'<div style="text-align: right; color: gray;">**Category:** {card["category"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Show Chinese on top
        st.markdown(f"<h1 style='text-align: center;'>{card['chinese']}</h1>", unsafe_allow_html=True)

        if st.session_state.flipped:
            st.markdown(f"<h3 style='text-align: center;'>{card['english']}</h3>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    # Buttons for actions
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.button("Flip Card", on_click=flip_card)
    with col_btn2:
        st.button("Next Card", on_click=next_card)

else:
    st.info("No items to display for the selected category.")

st.markdown("---")
st.caption("Powered by Streamlit")
