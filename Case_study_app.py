#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('run', 'Input_data.py')

import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm
StreamlitPatcher().jupyter() 

st.write(""" 
# My first app 
Hello *word!*
""")

st.write(sales_fig)

boroughs = sales_NY["Borough"].unique()

for i in boroughs:
    check_i = st.checkbox(i)
    if check_i:
        st.write(fig_neighborhood_by_brough(sales_NY, i))