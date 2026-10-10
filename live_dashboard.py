import streamlit as st
import psycopg2
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Live Payment", layout="wide")

st_autorefresh(interval=1000, key="payment_refresh")


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="raiseup",
        user="postgres",
        password="5591"
    )
    
def get_payments():
    connection = get_connection()
    query="""
        SELECT * FROM streaming_payments ORDER BY id DESC 
        LIMIT 100
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

#================================
# Dashboard
#================================

st.title("Live CRM Payment")

df = get_payments()

#================================
# KPI
#================================

total_payment = len(df)
total_revenue = df['amount'].sum()
average_payment = (
    df['amount'].mean()
    if len(df) > 0 
    else 0
)

last_payment = (
    df.iloc[0]['amount']
    if len(df) > 0 
    else 0
)

col1,col2,col3,col4 = st.columns(4)
col1.metric("total payments", total_payment)
col2.metric("total revenue", f"{total_revenue} EGP")
col3.metric("average payment", f"{average_payment} EGP")
col4.metric("last payment", f"{last_payment} EGP")

st.divider()
if not df.empty:
    st.subheader("Payment Methods")
    payment_methods = (
        df.groupby('payment_method')['amount'].sum().reset_index()     
    )
    st.bar_chart(
        payment_methods.set_index('payment_method')
    )
    
    st.subheader("Last Payments")
    st.dataframe(df, use_container_width=True, hide_index=True)