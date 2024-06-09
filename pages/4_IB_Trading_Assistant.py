import time
import threading
import time

import streamlit as st
import asyncio

from llama_index.core.chat_engine.types import AgentChatResponse

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from ib_insync import *
import pandas as pd
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure

loop = asyncio.get_event_loop()


st.header("I am your IB Trading Assistant!")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]




@st.cache(show_spinner=True)
def get_vector_query_tool_from_yt_video():
    df = pd.read_csv(
            "https://raw.githubusercontent.com/adidror005/youtube-videos/main/small_news_dataset%20(1).csv")
    documents = []
    for index, row in df.iterrows():
            text = row['content']
            row_dict = row.to_dict()
            meta_data_dict = {k: v for k, v in row_dict.items() if k in ['created_at', 'author']}
            documents.append(Document(text=text, metadata=meta_data_dict))
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=64)
    nodes = parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    query_engine = index.as_query_engine(
            response_mode='tree_summarize', similarity_top_k=3
    )
    def vector_query(
            query: str
    ):
        response = query_engine.query(query)
        return response

    vector_query_tool = FunctionTool.from_defaults(
        name="vector_tool",
        fn=vector_query
    )
    return vector_query_tool


def get_stock_chart_tool():
    import queue
    def get_stock_chart_thread(symbol: str, bar_size: int, bar_size_unit: str, duration: int, duration_unit: str,
                    use_rth: bool,result_queue) -> Figure:
        """Get current stock chart for ticker symbol for bar_size for last duration and use regular trading hours as default or not When specifying a unit, historical data request duration format is integer{SPACE}unit (S|D|W|M|Y).,"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ib = IB()
        ib.connect(port=4001, clientId=123)
        stock = Stock(symbol=symbol, exchange='SMART', currency='USD')

        durationStr = str(duration) + " " + duration_unit
        barSizeSetting = str(bar_size) + " " + bar_size_unit + ('s' if duration > 1 else '')

        ib.qualifyContracts(stock)
        bars = ib.reqHistoricalData(stock, "", durationStr=durationStr, barSizeSetting=barSizeSetting, whatToShow='TRADES',
                                useRTH=use_rth)
        df = util.df(bars)
        fig = px.line(df, x='date', y='close')
        ib.disconnect()
        result_queue.put(fig)
    def get_stock_chart(symbol: str, bar_size: int, bar_size_unit: str, duration: int, duration_unit: str,
                    use_rth: bool) -> Figure:
        """Get current stock chart for ticker symbol for bar_size for last duration and use regular trading hours as default or not When specifying a unit, historical data request duration format is integer{SPACE}unit (S|D|W|M|Y).,"""
        result_queue = queue.Queue()  # Create a queue to share the result
        thread=threading.Thread(target=get_stock_chart_thread,args=(symbol, bar_size, bar_size_unit, duration, duration_unit,use_rth,result_queue))
        thread.start()
        thread.join()
        return result_queue.get()
    return FunctionTool.from_defaults(fn=get_stock_chart)

def get_current_stock_price_tool():
    import queue
    def get_current_stock_price_thread(symbol,result_queue):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ib = IB()
        ib.connect(port=4001, clientId=123)
        stock = Stock(symbol=symbol, exchange='SMART', currency='USD')
        ib.qualifyContracts(stock)
        ticker = ib.reqMktData(stock, "", True, False)
        ib.sleep(2)
        mkt_price = ticker.marketPrice()
        ib.disconnect()
        result_queue.put(f"{symbol} is currently trading at {mkt_price:,.2f}")

    def get_current_stock_price(symbol:str)->str:
        "Get the current stock price for given stock symbol"
        result_queue = queue.Queue()  # Create a queue to share the result
        thread=threading.Thread(target=get_current_stock_price_thread,args=(symbol,result_queue))
        thread.start()
        thread.join()
        return result_queue.get()

    return FunctionTool.from_defaults(fn=get_current_stock_price)




llm=OpenAI(model="gpt-4o")


use_vector_tool = False
current_stock_price_tool = get_current_stock_price_tool()
stock_chart_tool = get_stock_chart_tool()
tool_list = [current_stock_price_tool,stock_chart_tool]
if use_vector_tool:
    vector_query_tool = get_vector_query_tool_from_yt_video()
    tool_list.append(vector_query_tool)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])



if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response: AgentChatResponse = llm.predict_and_call(tool_list, prompt, verbose=True)
            st.write(response.sources[0].raw_output)
            message = {"role": "assistant", "content": response.sources[0].raw_output}
            st.session_state.messages.append(message) # Add response to message history
