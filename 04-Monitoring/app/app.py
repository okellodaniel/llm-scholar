# import streamlit as st
# import time
# import uuid

# from assistant import get_answer
# from db import save_conversation, save_feedback, get_recent_conversations, get_feedback_stats


# def print_log(message):
#     print(message, flush=True)


# def main():
#     print_log("Starting the Course Assistant application")
#     st.set_page_config(page_title="💬 Phi3 FAQ Chatbot")

#     with st.sidebar:
#         st.title('💬 Phi3 FAQ Chatbot')
#         st.write(
#             'This chatbot is created using the open-source Phi3 LLM model by Microsoft.')
#         st.write('The model parameters below are work in progress:')

#         temperature = st.slider(
#             'Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
#         top_p = st.slider('Top P', min_value=0.01,
#                           max_value=1.0, value=0.9, step=0.01)
#         max_length = st.slider('Max Length', min_value=32,
#                                max_value=128, value=120, step=8)
#         st.markdown(
#             '📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

#         # Course selection
#         course = st.selectbox(
#             "Select a course:",
#             ["machine-learning-zoomcamp", "data-engineering-zoomcamp", "mlops-zoomcamp"]
#         )
#         print_log(f"User selected course: {course}")

#         # Model selection
#         model_choice = st.selectbox(
#             "Select a model:",
#             ["ollama/phi3", "openai/gpt-3.5-turbo", "openai/gpt-4o", "openai/gpt-4o-mini"]
#         )
#         print_log(f"User selected model: {model_choice}")

#         # Search type selection
#         search_type = st.radio(
#             "Select search type:",
#             ["Text", "Vector"]
#         )
#         print_log(f"User selected search type: {search_type}")

#         def clear_chat_history():
#             st.session_state.messages = [
#                 {"role": "assistant", "content": "How may I assist you today?"}]
#         st.button('Clear Chat History', on_click=clear_chat_history)

#     # Session state initialization
#     if 'conversation_id' not in st.session_state:
#         st.session_state.conversation_id = str(uuid.uuid4())
#         print_log(f"New conversation started with ID: {st.session_state.conversation_id}")
#     if 'count' not in st.session_state:
#         st.session_state.count = 0
#         print_log("Feedback count initialized to 0")
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "How may I assist you today?"}]

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])
#             if message["role"] == "assistant" and "id" in message:
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button("👍", key=f"thumbs_up_{message['id']}"):
#                         save_feedback(message["content"], "thumbs_up")
#                 with col2:
#                     if st.button("👎", key=f"thumbs_down_{message['id']}"):
#                         save_feedback(message["content"], "thumbs_down")

#     # User input
#     user_input = st.chat_input(placeholder="Your message...")

#     if user_input:
#         st.session_state.messages.append(
#             {"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)

#         if st.session_state.messages[-1]["role"] != "assistant":
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     start_time = time.time()
#                     response = get_answer(
#                         user_input, course=course, model_choice=model_choice, search_type=search_type)
#                     elapsed_time = time.time() - start_time
#                     st.write(
#                         response + f"\n\n*Response generated in {int(elapsed_time)} seconds*")
#             st.session_state.messages.append(
#                 {"role": "assistant", "content": response})

#     st.write(f"Current count: {st.session_state.count}")

#     # Display recent conversations
#     st.subheader("Recent Conversations")
#     relevance_filter = st.selectbox("Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"])
#     recent_conversations = get_recent_conversations(limit=5, relevance=relevance_filter if relevance_filter != "All" else None)
#     for conv in recent_conversations:
#         st.write(f"Q: {conv['question']}")
#         st.write(f"A: {conv['answer']}")
#         st.write(f"Relevance: {conv['relevance']}")
#         st.write(f"Model: {conv['model_used']}")
#         st.write("---")

#     # Display feedback stats
#     feedback_stats = get_feedback_stats()
#     st.subheader("Feedback Statistics")
#     st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
#     st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")

# print_log("Streamlit app loop completed")


# if __name__ == "__main__":
#     print_log("Course Assistant application started")
#     main()


import streamlit as st
from time import time

from assistant import get_answer
from db import save_conversation, save_feedback, get_recent_conversations, get_feedback_stats


def print_log(message):
    print(message, flush=True)


def main():
    st.set_page_config(page_title="💬 Phi3 FAQ Chatbot")

    with st.sidebar:
        st.title('💬 Phi3 FAQ Chatbot')
        st.write(
            'This chatbot is created using the open-source Phi3 LLM model by Microsoft.')
        st.write('The model parameters below are work in progress:')

        temperature = st.slider(
            'Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
        top_p = st.slider('Top P', min_value=0.01,
                          max_value=1.0, value=0.9, step=0.01)
        max_length = st.slider('Max Length', min_value=32,
                               max_value=128, value=120, step=8)
        st.markdown(
            '📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}]

    model_choice = st.selectbox('Model Choice', [
                                'openai/gpt-4o', 'openai/gpt-4o-mini', 'openai/gpt-3.5-turbo', 'Ollama'])
    search_type = st.selectbox('Search Type', ['Vector', 'Text'])
    course = st.selectbox(
        'Course Type', ['data-engineering-zoomcamp', 'ml-zoomcamp', 'mlops-zoomcamp'])

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "id" in message:
                if st.button("👍", key=f"thumbs_up_{message['id']}"):
                    save_feedback(message["content"], "thumbs_up")
                if st.button("👎", key=f"thumbs_down_{message['id']}"):
                    save_feedback(message["content"], "thumbs_down")

    def clear_chat_history():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    user_input = st.chat_input(placeholder="Your message...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    start_time = time.time()
                    response = get_answer(
                        user_input, course=course, model_choice=model_choice, search_type=search_type)
                    elapsed_time = time.time() - start_time
                    st.write(
                        response + f"\n\n*Response generated in {int(elapsed_time)} seconds*")
            st.session_state.messages.append(
                {"role": "assistant", "content": response})


if __name__ == "__main__":
    print_log("Course Assistant application started")
    main()

