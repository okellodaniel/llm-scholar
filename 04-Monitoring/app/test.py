import streamlit as st

def main():
    st.title('Simple Streamlit App')
    user_input = st.text_input("Your message...")
    if user_input:
        st.write(f"You said: {user_input}")

if __name__ == "__main__":
    main()
