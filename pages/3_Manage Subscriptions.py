import streamlit as st
import pandas as pd
import streamlit as st

# Sample data with categories
items = {
    'Item': ['10Y Auction', '30Y Auction', 'TSLA China Insured Vehicles', 'CPI', 'PPI', 'PCE', 'Retail Sales'],
    'Price': [1.99, 1.99, 2.99, 0.19, 0.19, 0.19, 0.19],
    'Category': ['auctions', 'auctions', 'stock specific', 'macro', 'macro', 'macro', 'macro']
}

# Convert to DataFrame
df = pd.DataFrame(items)

import streamlit as st

tab1, tab2 = st.tabs(["Subscriptions", "API Documentation"])

with tab1:
    # Streamlit app
    st.title('Select Items and Prices by Category')
    st.write('We have over 12,000 data events you can subscribe to!')

    # Initialize an empty list to store selected routes
    selected_routes = []

    # Iterate through unique categories and display checkboxes for each item in the category
    for category in df['Category'].unique():
        with st.expander(category.capitalize()):
            category_df = df[df['Category'] == category]
            for i, row in category_df.iterrows():
                if st.checkbox(f"{row['Item']} ({row['Price']})", key=row['Item'],value=True):
                    selected_routes.append(row)

    # Convert selected routes to DataFrame if any items are selected
    if selected_routes:
        selected_df = pd.DataFrame(selected_routes).drop_duplicates()
    else:
        selected_df = pd.DataFrame(columns=['Item', 'Price', 'Category'])

    # Display the table
    if selected_df.empty:
        st.write("Please select at least one item.")
    else:
        st.write("Selected Items and Prices")
        for category in selected_df['Category'].unique():
            st.subheader(category.capitalize())
            category_df = selected_df[selected_df['Category'] == category]
            st.dataframe(category_df)

    # Calculate total price
    total_price = selected_df['Price'].sum()

    # Display total price
    st.write(f"Your total is: {total_price}")

    # Toggle subscribe button
    if 'subscribed' not in st.session_state:
        st.session_state['subscribed'] = False

    if st.session_state['subscribed']:
        if st.button('Unsubscribe'):
            st.session_state['subscribed'] = False
    else:
        if st.button('Subscribe'):
            st.session_state['subscribed'] = True

    # Display current subscription status
    if st.session_state['subscribed']:
        st.write("You are subscribed.")
    else:
        st.write("You are not subscribed.")
with tab2:
    st.title("You can access events with the following callback")
    st.markdown(
        """
        ```
        def on_event(event):
            if event.event_id =='auction' and event.value>event.expected_value:
                place_order(contract=Stock("TSLA"),LimitOrder("BUY",QTY=100,LMTPRICE=170)
        ```
        """)