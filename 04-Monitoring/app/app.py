import streamlit as st
from time import time
from assistant import get_answer
from db import save_conversation, save_feedback, get_recent_conversations, get_feedback_stats,clear_conversation
import uuid

def print_log(message):
    print(message, flush=True)

def main():
    st.set_page_config(page_title="💬 Zoomcamp FAQ Chatbot")

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(f"New conversation started with ID: {st.session_state.conversation_id}")
    
    if "count" not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

    with st.sidebar:
        st.title('💬 Zoomcamp FAQ Chatbot')
        st.write('This chatbot explores multiple models')
        st.write('The model parameters below are work in progress:')

        model_choice = st.selectbox('Model Choice', [
                                    'openai/gpt-4o', 'openai/gpt-4o-mini', 'openai/gpt-3.5-turbo', 'ollama/phi3'])
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
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍", key=f"thumbs_up_{message['id']}"):
                        # save_feedback(message["id"], 1)  # Pass integer 1 for thumbs up
                        save_feedback(st.session_state.conversation_id, 1)  # Pass integer 1 for thumbs up
                        st.session_state.count += 1
                        print_log(f"Positive feedback received. New count: {st.session_state.count}")
                with col2:
                    if st.button("👎", key=f"thumbs_down_{message['id']}"):
                        # save_feedback(message["id"], -1)  # Pass integer -1 for thumbs down
                        save_feedback(st.session_state.conversation_id, -1)  # Pass integer -1 for thumbs down
                        st.session_state.count -= 1
                        print_log(f"Negative feedback received. New count: {st.session_state.count}")


    def clear_chat_history():
        clear_conversation(st.session_state.conversation_id)
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}]
        st.session_state.conversation_id = str(uuid.uuid4())
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    user_input = st.chat_input(placeholder="Your message...")

    if user_input:
    # Save user input as part of the conversation
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    start_time = time()
                    response = get_answer(
                        user_input, course=course, model_choice=model_choice, search_type=search_type)

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
                    # Save the conversation before saving feedback
                    conversation_id = st.session_state.conversation_id
                    try:
                        save_conversation(conversation_id, user_input, response, course)
                        print_log("Conversation saved successfully")
                    except Exception as e:
                        print_log(f"Error saving conversation: {str(e)}")

                    # Append the assistant's response to the session state
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "id": str(uuid.uuid4())}
                    )
    
    st.subheader("Recent Conversations")
    relevance_filter = st.selectbox("Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"])
    recent_conversations = get_recent_conversations(limit=5, relevance=relevance_filter if relevance_filter != "All" else None)
    for conv in recent_conversations:
        st.write(f"Q: {conv['question']}")
        st.write(f"A: {conv['answer']}")
        st.write(f"Relevance: {conv['relevance']}")
        st.write(f"Model: {conv['model_used']}")
        st.write("---")

    feedback_stats = get_feedback_stats()
    st.subheader("Feedback Statistics")
    st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
    st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")

if __name__ == "__main__":
    print_log("Course Assistant application started")
    main()
