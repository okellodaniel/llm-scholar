# import streamlit as st
# from time import time

# from assistant import get_answer
# from db import save_conversation, save_feedback, get_recent_conversations, get_feedback_stats
# import json

# def print_log(message):
#     print(message, flush=True)


# def main():
#     st.set_page_config(page_title="💬 Phi3 FAQ Chatbot")

#     with st.sidebar:
#         st.title('💬 Zoomcamp FAQ Chatbot')
#         st.write(
#             'This chatbot explores multple models')
#         st.write('The model parameters below are work in progress:')

       
#         model_choice = st.selectbox('Model Choice', [
#                                     'openai/gpt-4o', 'openai/gpt-4o-mini', 'openai/gpt-3.5-turbo', 'Ollama'])
#         search_type = st.selectbox('Search Type', ['Vector', 'Text'])
#         course = st.selectbox(
#             'Course Type', ['data-engineering-zoomcamp', 'ml-zoomcamp', 'mlops-zoomcamp'])
#         st.markdown(
#             '📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "How may I assist you today?"}]

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])
#             if message["role"] == "assistant" and "id" in message:
#                 if st.button("👍", key=f"thumbs_up_{message['id']}"):
#                     save_feedback(message["content"], "thumbs_up")
#                 if st.button("👎", key=f"thumbs_down_{message['id']}"):
#                     save_feedback(message["content"], "thumbs_down")

#     def clear_chat_history():
#         st.session_state.messages = [
#             {"role": "assistant", "content": "How may I assist you today?"}]
#     st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

#     user_input = st.chat_input(placeholder="Your message...")

#     if user_input:
#         st.session_state.messages.append(
#             {"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)

#         if st.session_state.messages[-1]["role"] != "assistant":
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     start_time = time()
#                     response = get_answer(
#                         user_input, course=course, model_choice=model_choice, search_type=search_type)

#                     response_json = json.loads(response)

#                     answer = response_json['answer']
#                     relevance = response_json['relevance']
#                     response_time = response_json['response_time']
#                     cost = response_json['openai_cost']

#                     elapsed_time = time() - start_time
#                     st.write(
#                         f"{answer}\n\n"
#                         f"*Response generated in {int(elapsed_time)} seconds*\n"
#                         f"*Relevance: {relevance}*\n"
#                         f"*LLM Response time: {response_time} seconds*\n"
#                         f"*Excecution Cost: ${cost}*"
#                     )
#             st.session_state.messages.append({"role": "assistant", "content": response})


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
        st.title('💬 Zoomcamp FAQ Chatbot')
        st.write('This chatbot explores multiple models')
        st.write('The model parameters below are work in progress:')

        model_choice = st.selectbox('Model Choice', [
                                    'openai/gpt-4o', 'openai/gpt-4o-mini', 'openai/gpt-3.5-turbo', 'Ollama'])
        search_type = st.selectbox('Search Type', ['Vector', 'Text'])
        course = st.selectbox(
            'Course Type', ['data-engineering-zoomcamp', 'ml-zoomcamp', 'mlops-zoomcamp'])
        st.markdown(
            '📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "id" in message:
                if st.button("👍", key=f"thumbs_up_{message['id']}"):
                    save_feedback(message["id"], "thumbs_up")
                if st.button("👎", key=f"thumbs_down_{message['id']}"):
                    save_feedback(message["id"], "thumbs_down")

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
                    start_time = time()
                    response = get_answer(
                        user_input, course=course, model_choice=model_choice, search_type=search_type)

                    # The response is already a dictionary, so no need to parse JSON
                    answer = response.get('answer', 'No answer provided.')
                    relevance = response.get('relevance', 'N/A')
                    response_time = response.get('response_time', 'N/A')
                    cost = response.get('openai_cost', 'N/A')

                    elapsed_time = time() - start_time
                    st.write(
                        f"{answer}\n\n"
                        f"*Response generated in {int(elapsed_time)} seconds*\n"
                        f"*Relevance: {relevance}*\n"
                        f"*LLM Response time: {response_time} seconds*\n"
                        f"*Execution Cost: ${cost}*"
                    )
            st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    print_log("Course Assistant application started")
    main()
