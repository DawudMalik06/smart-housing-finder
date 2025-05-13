import streamlit as st

st.title("Hello User!")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name}! Welcome to Streamlit.")

age = st.slider("Select your age:", 0, 100, 25)


st.write(f"You are {age} years old.")