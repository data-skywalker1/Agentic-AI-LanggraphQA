import streamlit as st
from chatbot_backend import chatbotnoob2
from langchain_core.messages import HumanMessage

# with st.chat_message('user'):
#     st.text('Hi')

# with st.chat_message('assistant'):
#     st.text('Hello! How can I assist you today?')
config= {'configurable': {'thread_id': "thread_id-1"}}

if 'message_hist' not in st.session_state:
    st.session_state['message_hist'] = []

for message in st.session_state['message_hist']:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input= st.chat_input("Type Here")   #, key="input"
if user_input:
    st.session_state['message_hist'].append({"role": "user", "content": user_input})    
    with st.chat_message('user'):
        st.write(user_input)
    
    # Get response from backend
    # response= chatbotnoob2.invoke({'messages':[HumanMessage(content=user_input)]}, config=config)
    # ai_msg= response['messages'][-1].content

    # st.session_state['message_hist'].append({"role": "assistant", "content": ai_msg})
    with st.chat_message('assistant'):
        ai_msg= st.write_stream(
          # using .stream instead of .invoke
            message_chunk.content for message_chunk, metadata in chatbotnoob2.stream(
     {"messages": [HumanMessage(content= user_input)]}, 
     config= {'configurable': {'thread_id': "thread-1"}},
     stream_mode='messages')

    )

    st.session_state['message_hist'].append({"role": "assistant", "content": ai_msg})


    # if message_chunk.content:
    #         print(message_chunk.content, end="|", flush=True)
    #     ) 