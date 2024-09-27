import streamlit as st
import re
from datetime import datetime
import json
import os

# File to store saved templates
TEMPLATE_FILE = "templates.json"

# Load templates from a file (if it exists)
def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r") as file:
            return json.load(file)
    return {}

# Save templates to a file
def save_templates(templates):
    with open(TEMPLATE_FILE, "w") as file:
        json.dump(templates, file)

# Function to replace tags in a template
def replace_tags(template, replacements):
    # Replace ${!date} with the current date
    template = template.replace('${!date}', datetime.today().strftime('%Y-%m-%d'))
    
    # Replace other tags
    for key, value in replacements.items():
        template = re.sub(rf'\${{{key}}}', value, template)
    return template

# Load templates when the app starts
templates = load_templates()

# Title
st.title("Template Filler App")

# Section to create and save templates
st.subheader("Create and Save Template")
template_name = st.text_input("Template Name", "")
new_template = st.text_area("Prewritten Template", "", height=150)

if st.button("Save Template"):
    if template_name and new_template:
        templates[template_name] = new_template
        save_templates(templates)
        st.success(f"Template '{template_name}' saved successfully!")
    else:
        st.error("Please enter both a template name and content.")

# Display saved templates
st.subheader("Saved Templates")
template_options = list(templates.keys())

# Use session state to keep track of form inputs
if 'tag_inputs' not in st.session_state:
    st.session_state.tag_inputs = {}

if template_options:
    selected_template = st.selectbox("Choose a Template", template_options)

    # Dynamically generate form fields based on the template
    if selected_template:
        st.write("Fill out the fields for the selected template:")
        selected_template_content = templates[selected_template]
        
        # Extract the tag names using regex, but skip ${!date}
        tag_matches = re.findall(r"\${(.*?)}", selected_template_content)
        tag_matches = [tag for tag in tag_matches if tag != "!date"]  # Exclude ${!date}
        
        # Keep track of the user input for each tag in session state
        for tag in tag_matches:
            if tag not in st.session_state.tag_inputs:
                st.session_state.tag_inputs[tag] = ""
            st.session_state.tag_inputs[tag] = st.text_input(f"Fill in {tag}", st.session_state.tag_inputs[tag])
        
        # Button to generate the filled template
        if st.button("Generate Filled Template"):
            # Replace tags in the template
            filled_template = replace_tags(selected_template_content, st.session_state.tag_inputs)
            
            # Display the filled template and allow copying via text area
            st.subheader("Filled Template")
            st.text_area("Generated Email", filled_template, height=150)

            # Streamlit doesn't directly support clipboard in browser, so we tell users to copy manually
            st.info("You can copy the text above manually by selecting it.")
