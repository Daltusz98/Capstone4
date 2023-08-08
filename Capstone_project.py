import json
import os
# 3rd parties
import streamlit as st
import openai
from IPython.display import Markdown, display, Image
openai.api_key = "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"
story = ""

def action_sequence(side1,side2,place,result):
    global story
    system = "You are an action scene director that describe a fight scene step by step for a story or movie "
    user1 = "Describe a fight scene between two side"
    assistant = f"First, describe the place {place}. Then, in the first scene, explain how {side1} and {side2} meet and confront each other. Next, describe their fighting scene. Finally conclude the battle where {result}."
    user = f"Describe a fight scene between {side1} and {side2} at place {place}. The final outcome is {result}"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system", 
            "content": system
        },
        {
            "role":"user",
            "content": user1
        },
        {
            "role":"assistant",
            "content": assistant
        },
        {
            "role": "user", 
            "content": user
        }
    ],
    max_tokens = 1000,
    temperature=0.7,
)
    story = response.choices[0].message.content
    return story 


# Streamlit UI
st.title('AI Action sequence generator')
user_input1 = st.text_input('Enter Character 1 :')
user_input2 = st.text_input('Enter Character 2 :')
user_input3 = st.text_input('Enter the Battle Location :')
user_input4 = st.text_input('Enter the Battle Results :')
if st.button('Generate'):
    stories = action_sequence(user_input1,user_input2,user_input3,user_input4)
    st.write(stories)
    # Split each sentence of the story
    story_split = stories.split(".")
    # Remove empty strings from the list
    stories_split = [sentence for sentence in story_split if sentence.strip()]
    # Select a few lines for the picture
    first_five_sequences = stories_split[:5]
    middle_five_sequences = stories_split[8:13]
    # Display Image Url
    for ii in middle_five_sequences:
        response = openai.Image.create(
            prompt=ii,
            n=1,
            size="256x256"  
        )
        image_url = response['data'][0]['url']
        st.image(image_url, caption=ii, use_column_width=True)