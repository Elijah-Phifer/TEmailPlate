import streamlit as st
import re
from datetime import datetime

# A dictionary to store saved templates
templates = {}

# Function to replace tags in a template
def replace_tags(template, replacements):
    # Replace ${!date} with the current date
    template = template.replace('${!date}', datetime.today().strftime('%Y-%m-%d'))
    
    # Replace other tags
    for key, value in replacements.items():
        template = re.sub(rf'\${{{key}}}', value, template)
    return template

# Title
st.title("Template Filler App")

# Section to create and save templates
st.subheader("Create and Save Template")
template_name = st.text_input("Template Name", "")
new_template = st.text_area("Prewritten Template", "", height=150)

if st.button("Save Template"):
    if template_name and new_template:
        templates[template_name] = new_template
        st.success(f"Template '{template_name}' saved successfully!")

# Display saved templates
st.subheader("Saved Templates")
template_options = list(templates.keys())

if template_options:
    selected_template = st.selectbox("Choose a Template", template_options)

    # Dynamically generate form fields based on the template
    if selected_template:
        st.write("Fill out the fields for the selected template:")
        selected_template_content = templates[selected_template]
        
        # Extract the tag names using regex
        tag_matches = re.findall(r"\${(.*?)}", selected_template_content)
        tag_inputs = {}
        
        for tag in tag_matches:
            if tag == "!date":
                continue
            tag_inputs[tag] = st.text_input(f"Fill in {tag}")
        
        if st.button("Generate Filled Template"):
            # Replace tags in the template
            filled_template = replace_tags(selected_template_content, tag_inputs)
            st.subheader("Filled Template")
            st.text(filled_template)
