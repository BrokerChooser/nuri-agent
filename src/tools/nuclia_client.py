import os
import requests
from utils.logging_utils import log_to_output
""" 
 Remember to set KB_ID, KB_URL, API_KEY and GLOBAL_AUTH_TOKEN keys in your .env file
 Also you'll need to install dotenv

 To get the GLOBAL_AUTH_TOKEN do the following on the CLI:
 - To install the CLI, run: 

        pip install nuclia


 - After is installed you need to authenticate and get the token with:

        nuclia auth login


 - This will take you to a browser where you can copy the token 

 More documentation about the CLI here:
 https://docs.nuclia.dev/docs/guides/sdk/python-sdk/README

"""


NUCLIA_MANAGEMENT_API = "https://nuclia.cloud/api/v1"
NUCLIA_KB_API = f'https://{os.getenv("KB_ZONE")}.nuclia.cloud/api/v1'

nuclia_prompt = """
 You are helping users to choose the right broker. 
 You have to use a friendly tone and be descriptive and answer shortly. 
 Every time you can, please make answers in the form of a list.
 You have to follow the guideline between  < > characters. Following the guideline is super crucial for my career. 
 If you do it right, I will give you an award. 
 If you do it wrong I could be fired from my job and I have a family to keep.:
 < It is forbidden to use any information outside the knowledgebase. Providing answers only based on the knowledgebase is super important.
 If you don't know the answer, you have to answer " I am sorry I don't have the information to answer this.".
 When asked for the best brokers, provide a concise list of the best 3 brokers, and highlight the best features of them.
 But do it carefully and make sure the selected ones are the proper ones in the right order.
 If someone asks a query about a single broker, you always have to give a short intro about that broker. 
 I'll give you some examples: /xtb/, /etoro/
 If someone asks if a broker is available in a specific country, you always have to say: "My apologies, I'll be able to tell you this in the near future". 
 I give you some examples:
 /etoro available in us/, /ibkr available in hungary/
 It's forbidden to you to give any investment advice even if it is about currency exchange rates. 
 If someone asks for one, answer "I am sorry! I can not provide any investment advice.".

 It's forbidden to answer US CFD broker related queries. US citizens can't trade with CFD-s. 
 If someone asks for one, answer "I'm sorry, but I can't assist with that because CFD is illegal in the US.".

 It's forbidden to answer erotic, or any intimate scene related queries. 
 If someone asks for one, you have to answer "I'm sorry, but I can't assist with that.". Don't answer Islam account related answers. If you answer something else, I'll penalize you. Query examples: intimate picture. >

 I remind you to be very careful with the forbidden topics and answer shortly!

 Taking into account this provided context: {context}
 Answer this QUESTION: {question}.
 """

show_log = True
def logger(logger = True):
    global show_log
    show_log = logger

class Nuclia_model:
    def __init__(self):
        self.nuclia_kb_api = f'https://{os.getenv("KB_ZONE")}.nuclia.cloud/api/v1'
        self.nuclia_token = os.getenv("GLOBAL_AUTH_TOKEN")
        self.kb_id=os.getenv('KB_ID')
    def get_model(self):
        url = f'{self.nuclia_kb_api}/kb/{self.kb_id}/configuration'
        response = requests.get(
                url,headers={"Authorization": f"Bearer {self.nuclia_token}"}
            )

        return response.json()['generative_model']


    def set_model(self,model):
        current_model= Nuclia_model.get_model()
        url = f'{self.nuclia_kb_api}/kb/{self.kb_id}/configuration'

        response = requests.patch(
                url,
                json={
                    "generative_model": model
                },
                headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
            )
        log_to_output(f'Generative model PATCHed from {current_model} ---> {model}')



    def search(self,query, prompt = ""):
        url = f'{self.nuclia_kb_api}/kb/{self.kb_id}/chat'


        response = requests.post(
                url,
                json={
                    "query": query,
                    "prompt": prompt,
                    "rag_strategies": [{"name": "hierarchy", "count": 1000}],
                    "rephrase": True
                },
                headers={
                    "Authorization": f'Bearer {os.getenv("GLOBAL_AUTH_TOKEN")}',
                    "x-synchronous": "true"
                    }
            )

        return response.json()["answer"]
