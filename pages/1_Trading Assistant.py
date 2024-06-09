import streamlit as st

st.title("Predefined Response Chat")

# Initialize chat history and response list
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.responses = ["Today there is a 10 year auction at 2PM EST", "Are you sure that would mean yields go up which should put pressure on long duration risk assets?",
                                  "You aren't subscribed to 10Y auction streaming data, do you want to add this subscription for 1.99$ a month before I can set this rule.",
                                  ["Ok your subscriptions are updated in the subscriptions tab",
                                  "I am setting the rule to Buy 100 TSLA at Market if 10 yr auction beats analyist expectations.","I sent you a confimation rule in the rules tab"],
                                  "It seems like china insurance number of 13,000 are up 55 pct from last week. Also There is some rebound optimism regarding semi delivery",
                                   """
                                   Sure you can access it with the followng event callback code:
                                   ```
                                   def on_event(event):
                                       if event.event_id =='auction' and event.value>event.expected_value:
                                              place_order(contract=Stock("TSLA"),LimitOrder("BUY",QTY=100,LMTPRICE=170)
                                   ```
                                   """]# List of responses
    st.session_state.response_index = 0  # Track which response to use next

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=None):
        st.markdown(message["content"])

# Handle user input and system response
if prompt := st.chat_input("Your message:"):
    with st.chat_message("user", avatar=None):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get the next response and handle running out of responses
    if st.session_state.response_index < len(st.session_state.responses):
        response = st.session_state.responses[st.session_state.response_index]
        response2 = None
        if type(response) == list:
            response2 = response[-1]
            response = response[0]
        st.session_state.response_index += 1
    else:
        response = "I've run out of things to say!"  # Or any other message

    with st.chat_message("system", avatar=None):
        st.markdown(response)
    if response2 is not None:
        with st.chat_message("system",avatar=None):
            st.markdown(response2)
    st.session_state.messages.append({"role": "system", "content": response})

