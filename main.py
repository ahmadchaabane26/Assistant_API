import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import requests
import json
import streamlit as st

# The approach taken to this is manually coding the process done on  asistant as if it was openAI website. We are making sure the same process is being coded.

load_dotenv()
# popenai.api_key = os.environ.get(""")
# This step includes reqtieriving the key and welcoming the AI

news_api_key = os.environ.get("NEWS_API_KEY")
# getting news api


client = openai.OpenAI()
# you can add key directly if not inputed in and .env file

model = "gpt-3.5-turbo-16k"
# Specfying which AI we want to be used


#retriving topic
def get_news(topic):
    url =(
    # in this part we are defining "everything" as the end point and allowing the AI model to search the web with the requirments of topics that are 5 pages long"
        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"
        #Searching the web through this url
    )

    try:
        #Making a GET request to the News API
        response = requests.get(url) 
        # Checking if the response status code is 200 (OK)
        if response.status_code == 200:
            # Formatting the JSON response for better readability
            new = json.dumps(response.json(), indent =4)
             # Loading the JSON response into a Python dictionary
            news_json = json.loads(new)
            # Assigning the news JSON data to a variable
            data = news_json

            #access all fiels == loops
            # extracting all data from json data 
            status = data["status"] # updating status
            total_results = data["totalResults"]
            articles = data["articles"]
            final_news = [] # Creating an empty list to store formatted multiple news articles

            #loop through these, and extracting all info from the article
            count = 0
            for article in articles:
                if "title" in article and "description" in article and "source" in article and "url" in article:
                    source_name = article["source"]["name"]
                    author = article["author"]
                    title = article["title"]
                    description = article["description"]
                    url =article["url"]
                    content = f"""
                    - Title: {title}
                    - Author: {author}
                    - Source: {source_name}
                    - Description: {description}
                    - Read more: [{title}]({url})
                    """
                    final_news.append(content)
                    count +=1
                else:
                    continue
                if count == 5:
                    break
            return final_news
        else: # if status is not 200 (ok) then return an empty list
            return []
    except requests.exceptions.RequestException as e: #handing error
        print("Error occured during API request",e)


#allowing the AI to summarize the article in points
class AssistantManager:
    thread_id = "thread_IMbHUHR3olmM5AbxGE6UsH6J"
    assistant_id = "asst_LjZUbZzoLZ2wNBFsL92z2THW"

    def __init__(self, model: str = model)-> None:
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        # Reteriving existing assistant and thread if IDs are already created
        # We dont want the backend created multiple assistants
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id= AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id = AssistantManager.thread_id
            )
    # Making an assistant if there isnt one
    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name =name,
                instructions = instructions,
                tools = tools,
                model = self.model
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"AssisID:::: {self.assistant.id}")
    # Creating thread ID
    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"ThreadID::: {self.thread.id}")
    # Add messages to thread
    def add_messages_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role = role,
                content = content
            )
    #passing instrcutions 
    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id= self.thread.id,
                assistant_id= self.assistant.id,
                instructions= instructions
            )
    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            summary =[]

            last_messages = messages.data[0]
            role = last_messages.role
            response = last_messages.content[0].text.value
            summary.append(response)

            self.summary = "\n".join(summary)
            print(f"SUMMARY------> {role.capitalize()}: ==> {response}")
    #this is where everything is happened the funtion is being pulled
    def call_required_functions(self, required_actions):
        if not self.run:
            return 
        tools_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])

            if func_name == "get_news":
                output = get_news(topic=arguments["topic"])
                print(f"STUFFFF;;;;{output}")
                final_str =""
                for item in output:
                    final_str += "".join(item)
                tools_outputs.append({"tool_call_id": action["id"], "output": final_str})
            else:
                raise ValueError(f"Unknown function: {func_name}")

        print("Submitting outputs back to the assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id =self.thread.id,
            run_id=self.run.id,
            tool_outputs =tools_outputs
        )
    #for streamlit
    def get_summary(self):
        return self.summary
    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=self.run.id
                )
                print(f"RUN STATU::: {run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("FUNCTION CALLING NOW...")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )
    #run the steps
    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id= self.thread.id,
            run_id = self.run.id
        )
        print(f"RUN-Steps::: {run_steps}")
        return run_steps.data

def main():
    # news = get_news("bitcoin")
    # print(news[0])

    manager = AssistantManager()

    # Streamlit interface
    st.title("News Summarizer")

    with st.form(key="user_input_form"):
        instructions = st.text_input("Enter topic:")
        submit_button = st.form_submit_button(label="Run Assistant")

        if submit_button:
            manager.create_assistant(
                name="News Summarizer",
                instructions="You are a personal article summarizer Assistant who knows how to take a list of article's titles and descriptions and then write a short summary of all the news articles",
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_news",
                            "description": "Get the list of articles/news for the given topic",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "topic": {
                                        "type": "string",
                                        "description": "The topic for the news, e.g. bitcoin",
                                    }
                                },
                                "required": ["topic"],
                            },
                        },
                    }
                ],
            )
            manager.create_thread()

            # Add the message and run the assistant
            manager.add_messages_to_thread(
                role="user", content=f"summarize the news on this topic {instructions}?"
            )
            manager.run_assistant(instructions="Summarize the news")

            # Wait for completions and process messages
            manager.wait_for_completion()

            summary = manager.get_summary()

            st.write(summary)

            st.text("Run Steps:")
            st.code(manager.run_steps(), line_numbers=True)
if __name__ == "__main__":
    main()