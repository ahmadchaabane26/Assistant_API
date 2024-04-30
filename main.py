import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

# The approach taken to this is manually coding the process done on  asistant as if it was openAI website. We are making sure the same process is being coded.

load_dotenv()
# popenai.api_key = os.environ.get(""")
# This step includes reqtieriving the key and welcoming the AI

client = openai.OpenAI()
# you can add key directly if not inputed in and .env file

model = "gpt-3.5-turbo-16k"
# Specfying which AI we want to be used



# Now create our assitant 

# ///// We commented it out because we already got the assistant ID and thread ID after running this code once

personal_trainer_assis = client.beta.assistants.create(
    name = "Personal Trainer testing", 
    instructions =""" You are the best personal trainer and nutritionist who knows how to get clients to build lean muscles. \n
      You've trained high-caliber athletes and movie stars.""",
      model = model
)
asistant_id = personal_trainer_assis.id
print (asistant_id)




# This creates the ID for the personal trainer

# Now we have to create the thread

# ///// We commented it out because we already got the assistant ID and thread ID after running this code once

thread = client.beta.threads.create(
    # We are adding a user input also known as a "message", we are just saying the person asking is user and this is the message
    messages= [
        {
            "role" : "user",
            "content": "How do I get started working out to lose fat and build muscles?", 
        }
    ]
)

thread_id = thread.id
print(thread_id)

# From here on we run the actual interaction between the bot and the user

# Hard code the IDs
asistant_id = asistant_id
thread_id = thread_id

# Create a message 
while True:
    message = input("How can I help your fitness journey (Type 'done' to exit): ")

        # Check if user wants to exit
    if message.lower() == "done":
        print("Thank you for using me! Good luck on your journey!")
        break

    #this is where you can change the message
    message = client.beta.threads.messages.create(
        thread_id= thread_id,
        role="user",
        content=message
    )

    # To run our assistant 

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=asistant_id,
        instructions="Please address the user as Ahmad Chaabane",
    )

    # run time / response / Error message / message to user while waiting
    def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
        """

        Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
        :param thread_id: The ID of the thread.
        :param run_id: The ID of the run.
        :param sleep_interval: Time in seconds to wait between checks.
        """
        while True:
            try:
                run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.completed_at:
                    elapsed_time = run.completed_at - run.created_at
                    formatted_elapsed_time = time.strftime(
                        "%H:%M:%S", time.gmtime(elapsed_time)
                    )
                    # This just tells us how long it took to complete/run
                    print(f"Run completed in {formatted_elapsed_time}")
                    logging.info(f"Run completed in {formatted_elapsed_time}")
                    # Get messages here once Run is completed!
                    messages = client.beta.threads.messages.list(thread_id=thread_id)
                    last_message = messages.data[0]
                    response = last_message.content[0].text.value
                    #Printing the respose
                    print(f"Assistant Response: {response}")
                    break
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
                break
            logging.info("Waiting for run to complete...")
            time.sleep(sleep_interval)

    # Running 
    wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

    # Show logs to see the Steps the AI goes through

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run.id
    )
    print(f"steps:: {run_steps.data}")