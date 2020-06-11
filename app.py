import pandas as pd
import numpy as np
import streamlit as st
#from PIL import Image
#import os
#curpath = os.path.dirname(os.path.abspath(__file__))
#Multi-command to run streamlit in the current file: ctrl+m ctrl+s

#st.write( curpath )
st.title('Capstone Project')
st.subheader('IBM Data Science Professional Certificate')
st.write('@rodpaschoal')
st.markdown('---')
#img = Image.open('pegasus.jpg')
st.image(image='pegasus.jpg', caption='Hello Capstone Project Course!', use_column_width=True)
st.markdown('---')
st.markdown('## What is this website?')
st.markdown('I am very happy to code in python  \n and use this powerful tool to  \ncreate value with Data Science')
st.header('Streamlit is more beautiful than Jupyter notebook')
st.code('[1] print(\'Hello Capstone Project Course!\')')
st.write('Hello *Capstone* Project Course! :sunglasses:')