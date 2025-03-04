#!/usr/bin/env python
# coding: utf-8

# # Requirements Specification
# ## Install the libraries 

# In[1]:


pip install streamlit


# In[2]:


pip install google.generativeai


# #### Restart the Kernal

# In[3]:


import IPython

app = IPython.Application.instance()
app.kernel.do_shutdown(True)


# # Initialize the pre-trained model

# In[1]:


import streamlit as st
import google.generativeai as genai


# In[2]:


api_key = 'AIzaSyBlxwry1MefGi_7ZTGaqVvhb8ylv-TPEY8'
genai.configure(api_key = api_key)


# In[3]:


generation_config = {
    "temperature" : 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mine_type": "text/plain",
 }


# # Interfacing with Pre-trained Model

# In[4]:


def generate_resume(name, job_title):
    model = genai.GenerativeModel(
        model_name = "gemini-1.5-pro",
        generation_config = generation_config,
    )
    context = f'name:{name}\njob_title:{job_title}\nwrite a resume on above data.' # Moved this line inside the function

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [context],
            },
        ]
    )
    response = chat_session.send_message(context)
    text = response.candidates[0].content if isinstance(response.candidates[0].content, str) else response.candidates[0].content.parts[0].text
    return text


# In[5]:


def clean_resume_text(text):
    
    cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
    cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
    cleaned_text = cleaned_text.replace("[Add Linkedin Profile URL (optional)]", "[Your Linkedin Profile URL (optional)]")
    cleaned_text = cleaned_text.replace("[University Name]", "[Your University Name]")
    cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
    
    return cleaned_text


# # Model Deployment

# In[6]:


st.title("Resume Generator")
name = st.text_input("Enter your Name")
job_title = st.text_input("Enter your Job Title")
if st.button("Generate Resume"):
    if name and job_title:
        resume = generate_resume(name, job_tilte)
        cleaned = clean_resume_text(resume)
        st.markdown("### Generated Resume")
        st.markdown(cleaned)
    else:
        st.warning("Please enter both your name and job title.")


# In[ ]:




