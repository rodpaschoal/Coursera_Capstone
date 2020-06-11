import streamlit as st
from PIL import Image
import os
curpath = os.path.dirname(os.path.abspath(__file__))
#Multi-command to run streamlit in the current file: ctrl+m ctrl+s

#st.write( curpath )
st.title('Data Science @ IBM')
st.subheader('Capstone project for professional certificate\n')
st.write('/rodpaschoal')
st.markdown('---')
img = Image.open(curpath + '/pegasus.jpg')
st.image(img, caption='Let the magic happen', use_column_width=True)
st.markdown('## What is this website?')
st.markdown('I am very happy to learn how to code in  \n pyhton and use this powerful tool to  \ncreate value by means of Data Science')

