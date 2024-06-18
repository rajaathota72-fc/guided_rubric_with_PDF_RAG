import streamlit as st
from retrieve_embeddings import retrieve_and_generate_response
from config import *
import json
import re
import math
def build_field(phase_name, phase_info):
    """Generates UI components based on phase configuration and handles submission."""
    input_value = st.session_state.get(phase_name, phase_info.get("value", ""))

    if phase_info["type"] == "text_input":
        input_value = st.text_input(phase_info["label"], value=input_value)
    elif phase_info["type"] == "text_area":
        input_value = st.text_area(phase_info["label"], value=input_value, height=phase_info.get("height", 150))

    st.session_state[phase_name] = input_value  # Store the current input value back to the session state

    if st.button("Submit", key=f"{phase_name}_submit"):
        # Generate the prompt using the template and the user's input
        prompt = PROMPT_TEMPLATE.format(rubric=phase_info['rubric'])
        response, cost = retrieve_and_generate_response(input_value, prompt)
        st.session_state[f"{phase_name}_response"] = response
        st.session_state[f"{phase_name}_cost"] = cost

        # Extract the score from the response
        score = extract_score(response)
        st.session_state[f"{phase_name}_score"] = score

        # Check if the score meets the minimum criteria
        if score >= phase_info.get("minimum_score", 0):
            st.session_state[f"{phase_name}_passed"] = True
        else:
            st.session_state[f"{phase_name}_passed"] = False

def display_phase(phase_name):
    """Displays the results from the AI retrieval."""
    if f"{phase_name}_response" in st.session_state:
        st.write("AI Feedback:")
        st.write(st.session_state[f"{phase_name}_response"])
        st.write(f"Cost for this query: ${st.session_state[f'{phase_name}_cost']:.6f}")
        st.write(f"Score: {st.session_state[f'{phase_name}_score']}")

def extract_score(response):
    """Extracts the score from the AI response."""
    total_score_match = re.search(r'Score:\s*(\d+)', response)
    if total_score_match:
        score = float(total_score_match.group(1))
        return math.ceil(score)
    return 0

def check_score(phase_name):
    """Checks if the score meets the minimum criteria."""
    score = st.session_state.get(f"{phase_name}_score", 0)
    return score >= PHASES[phase_name].get("minimum_score", 0)

def main():
    """Main function to construct the Streamlit app."""
    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    if 'CURRENT_PHASE' not in st.session_state:
        st.session_state['CURRENT_PHASE'] = 0

    # Process each phase defined in the configuration
    for i, (phase_name, phase_info) in enumerate(PHASES.items()):
        if i > st.session_state['CURRENT_PHASE']:
            break

        build_field(phase_name, phase_info)
        display_phase(phase_name)

        if st.session_state.get(f"{phase_name}_passed", False):
            st.success("You have passed this phase. You can proceed to the next phase.")
            if i == st.session_state['CURRENT_PHASE']:
                st.session_state['CURRENT_PHASE'] += 1
                st.experimental_rerun()  # Rerun the app to move to the next phase
        elif f"{phase_name}_response" in st.session_state:
            st.warning("You have not passed this phase. Please try again.")

    if st.button("Reset"):
        # Reset all session state keys
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

if __name__ == "__main__":
    main()
