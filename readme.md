# Guided Critical Analysis Tool

## Overview
This project is a Streamlit-based web application designed to facilitate a guided critical analysis of articles using AI-generated feedback and scoring. The application interacts with an AI model and uses RAG with PDF to provide feedback on user responses based on predefined questions and rubrics.

## Files Description
- **config.py**: Contains configuration settings for the app, including phases of questions, AI model settings, and other static information.
- **main.py**: The main Streamlit application script that renders the UI and handles user interactions.
- **retrieve_embeddings.py**: Manages the retrieval of document embeddings and generating responses using an AI model.
- **store_embeddings.py**: Handles the storage of document embeddings to enhance retrieval capabilities.

## Setup and Installation

**Clone the Repository**
   ```bash
   git clone https://your-repository-url.git
   cd your-project-directory
   ```

**Environment Setup**
   - Ensure Python 3.8+ is installed on your system.
   - It's recommended to use a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
  
**Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

**Configuration**
   - Modify the `config.py` to suit your project requirements, like setting up different phases or adjusting model configurations.
   - Ensure MongoDB is set up for storing and retrieving embeddings as specified in `retrieve_embeddings.py` and `store_embeddings.py`.

**Run the Application**
   ```bash
   streamlit run main.py
   ```

## Usage

- **Web Interface**: Once the application is running, access it via a web browser at `http://localhost:8501`.
- **Interacting with the tool**: Follow on-screen prompts to interact with the AI, where you can input answers to guided questions, receive feedback, and view AI-generated scores based on the rubrics.
- **Reset function**: Use the reset button to clear all inputs and restart the analysis process.

## Notes

- **Customizing Questions and Rubrics**: Edit `config.py` to modify or extend the questions and rubrics according to different articles or subjects.
- **Enhancing AI Responses**: Adjustments in `retrieve_embeddings.py` might be necessary to improve response relevance and accuracy by fine-tuning the model or modifying retrieval queries.

