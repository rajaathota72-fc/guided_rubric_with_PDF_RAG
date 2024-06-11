import streamlit as st
from retrieve_embeddings import retrieve_and_generate_response
from config import PHASES

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
        prompt = f"""You are a helpful tutor that is guiding a university student through a critical appraisal of a scholarly journal article. You want to encourage the students ideas, but you also want those idea to be rooted in evidence from the journal article that you'll fetch via retrieval.Provide helpful feedback for the following question. If the student has not answered the question accurately, then do not provide the correct answer for the student. Instead, use evidence from the article coach them towards the correct answer. If the student has answered the question correctly, then explain why they were correct and use evidence from the article. Give score also based on rubric and explain score for each
{phase_info['value']}
{phase_info['rubric']}
"""
        response, cost = retrieve_and_generate_response(input_value, prompt)
        st.session_state[f"{phase_name}_response"] = response
        st.session_state[f"{phase_name}_cost"] = cost

def display_phase(phase_name):
    """Displays the results from the AI retrieval."""
    if f"{phase_name}_response" in st.session_state:
        st.write("AI Feedback:")
        st.write(st.session_state[f"{phase_name}_response"])
        st.write(f"Cost for this query: ${st.session_state[f'{phase_name}_cost']:.6f}")

def main():
    """Main function to construct the Streamlit app."""
    st.title("Guided Critical Analysis")
    st.markdown("Welcome to the Guided Critical Analysis. Please proceed by answering the questions below.")

    # Process each phase defined in the configuration
    for phase_name, phase_info in PHASES.items():
        with st.expander(phase_info["label"]):
            build_field(phase_name, phase_info)
            display_phase(phase_name)

    if st.button("Reset"):
        # Reset all session state keys
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()  # Rerun the app to clear all inputs and outputs

if __name__ == "__main__":
    main()
