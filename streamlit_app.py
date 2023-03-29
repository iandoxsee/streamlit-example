import streamlit as st
import math

st.title('Sin Calculator')

number = st.number_input('Enter a number')
if st.button('Go'):
    result = math.sin(number)
    st.write(f'The sin of {number} is {result:.2f}')
