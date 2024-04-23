    # Personal Trainer Assistant using OpenAI

    This project implements a personal trainer and nutritionist assistant using OpenAI's GPT-3.5 model. The assistant provides guidance on workouts and nutrition to help users build lean muscles.

    ## Setup

    1. Install dependencies:
       ```bash
       pip install openai python-dotenv
       ```

    2. Obtain an API key from OpenAI and create a `.env` file in the project root with the following content:
       ```
       OPENAI_API_KEY=your_api_key_here
       ```

    3. Create a virtual environment (optional but recommended):
       ```bash
       python -m venv venv
       ```

    4. Activate the virtual environment:
       - On Windows:
         ```bash
         venv\Scripts\activate
         ```
       - On macOS/Linux:
         ```bash
         source venv/bin/activate
         ```

    5. Run the script to interact with the assistant:
       ```bash
       python personal_trainer_assistant.py
       ```

    ## Steps to Create the Assistant

    1. Set up the project environment.
    2. Load the OpenAI API key from the `.env` file.
    3. Initialize the OpenAI client with the API key and specify the model.
    4. Create the assistant with a name, description, and model.
    5. Create a thread for the assistant with a user message.
    6. Send a message to the thread and wait for the assistant's response.
    7. Display the assistant's response and completion time.

    ## Notes

    - This project demonstrates how to create and interact with an OpenAI assistant programmatically.
    - Make sure to handle errors and exceptions gracefully in a production environment.
    """
