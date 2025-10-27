import os, json, numpy as np, streamlit as st
from engine import Engine

st.set_page_config(page_title="Akinatoresque", page_icon="🧞", layout="wide")

# ---- Utilities ----
def mascot():
    # Resolve path robustly and fallback gracefully
    here = os.path.dirname(__file__)
    for cand in ("assets/mascot.png","assets/mascot.jpg","assets/mascot.jpeg","assets/mascot.webp"):
        p = os.path.join(here, cand)
        if os.path.exists(p):
            st.image(p, width=180)
            return
    st.write(" ")  # no image found, keep layout clean

@st.cache_resource
def load_data():
    with open("data/entities.json","r",encoding="utf-8") as f:
        entities = json.load(f)
    with open("data/questions.json","r",encoding="utf-8") as f:
        questions = json.load(f)
    L = np.load("data/likelihood.npy")
    return entities, questions, L

entities, questions, L = load_data()

# Validate likelihood shape early to avoid None selections
if L.shape != (len(questions), len(entities), 3):
    st.error(f"likelihood.npy shape {L.shape} != (Q={len(questions)}, E={len(entities)}, 3). "
             f"Re-run scripts/make_likelihood.py after editing questions/entities.")
    st.stop()

# Engine in session
if "engine" not in st.session_state:
    st.session_state.engine = Engine(entities, questions, L)
eng = st.session_state.engine

# ---- Sidebar ----
with st.sidebar:
    mascot()
    st.markdown("### Controls")
    thresh = st.slider("Reveal threshold", 0.5, 0.99, value=0.85, step=0.01)
    maxq   = st.slider("Max questions", 10, 30, value=25, step=1)
    if st.button("Reset game", use_container_width=True):
        eng.__init__(entities, questions, L, thresh=thresh, max_q=maxq)
    st.markdown("---")
    st.markdown("Top candidates")
    for i,p in eng.topk(5):
        st.write(f"{entities[i]['name']}: {p*100:.1f}%")

# ---- Main stage ----
colH, colC = st.columns([1,2])
with colH:
    st.markdown("### Progress")
    pct = min(1.0, eng.turn / max(1, maxq))
    st.progress(pct, text=f"Question {min(eng.turn+1, maxq)} of {maxq}")

with colC:
    # Ensure a question is selected before indexing
    if not eng.done and eng.current_q is None:
        qidx = eng.select_question()
        if qidx is None:
            eng.done = True  # no available question (edge case)

    if not eng.done and eng.current_q is not None:
        qtext = questions[eng.current_q]["text"]
        st.markdown(f"## {qtext}")
        b1, b2, b3, b4, b5 = st.columns(5)
        if b1.button("Yes",           use_container_width=True): eng.apply_answer("YES")
        if b2.button("Probably",      use_container_width=True): eng.apply_answer("PROB")
        if b3.button("Don't know",    use_container_width=True): eng.apply_answer("IDK")
        if b4.button("Probably not",  use_container_width=True): eng.apply_answer("PNOT")
        if b5.button("No",            use_container_width=True): eng.apply_answer("NO")
        # After answering, attempt to pick the next question
        if not eng.done:
            qidx = eng.select_question()
            if qidx is None:
                eng.done = True
    else:
        idx, conf = eng.guess()
        st.success(f"Is it: {entities[idx]['name']}? (confidence {conf*100:.1f}%)")
        if st.button("Play again", use_container_width=True):
            eng.__init__(entities, questions, L, thresh=thresh, max_q=maxq)
