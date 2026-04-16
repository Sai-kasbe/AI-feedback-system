import streamlit as st

def build_form():
    st.subheader("Create Form")

    field = st.text_input("Field Name")
    type_ = st.selectbox("Type", ["Text", "Choice", "Rating"])

    if st.button("Add"):
        st.session_state.fields.append((field, type_))

def render_form():
    responses = {}

    for f, t in st.session_state.fields:
        if t == "Text":
            responses[f] = st.text_input(f)
        elif t == "Choice":
            responses[f] = st.selectbox(f, ["Good", "Average", "Bad"])
        elif t == "Rating":
            responses[f] = st.slider(f, 1, 5)

    return responses
