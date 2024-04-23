# Personal Trainer Assistant using OpenAI

This project implements a personal trainer and nutritionist assistant using OpenAI's GPT-3.5 model. The assistant provides guidance on workouts and nutrition to help users build lean muscles.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install openai python-dotenv
   ```

2. **Obtain API Key:**
   - Obtain an API key from OpenAI.
   - Create a `.env` file in the project root with the following content:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

3. **Create Virtual Environment (Optional):**
   ```bash
   python -m venv myenv
   ```

4. **Activate Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Run the Script:**
   ```bash
   python personal_trainer_assistant.py
   ```

## Steps to Create the Assistant

1. **Set Up Project Environment:**
   - Load the OpenAI API key from the `.env` file.
   - Initialize the OpenAI client with the API key and specify the model.

2. **Create the Assistant:**
   - Create the assistant with a name, description, and model.

3. **Create a Thread:**
   - Create a thread for the assistant with a user message.

4. **Send a Message:**
   - Send a message to the thread and wait for the assistant's response.

5. **Display Response:**
   - Display the assistant's response and completion time.

## Notes

- This project demonstrates how to create and interact with an OpenAI assistant programmatically.
- Make sure to handle errors and exceptions gracefully in a production environment.
