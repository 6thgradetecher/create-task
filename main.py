"""
*Name:Rohan
*Due Date:
*Program Name:Botero Survival Guide Chatbot
*Extra:Uses OpenRouter AI
"""
import os#for reading the api key
import requests#for sending the question to the AI
from dotenv import load_dotenv#for reading the .env file
from flask import Flask, render_template, request#for making the website

load_dotenv("_env")#loads the secret key from the .env file
from dotenv import find_dotenv
print("env file found at:", find_dotenv())
url="https://openrouter.ai/api/v1/chat/completions"
model="openrouter/free"
apikey=os.getenv("OPENROUTER_API_KEY")

app=Flask(__name__)#makes the website

#The list that stores every line of the chat
chat=[]

#Function A: gives the help message
def helpmessage():
    return "Commands you can type: /help shows this message, /clear erases the chat"

#Function B: erases the whole chat
def clearchat():
    chat.clear()

#Sends the chat to the AI and returns its answer
def askai(lines):
    if apikey==None:#the .env file was not found or the name is wrong
        return "No api key found. Check your .env file."
    conversation=""
    for line in lines:#loop through every line in the chat list
        conversation=conversation+line+"\n"
    prompt="You are the Botero Survival Guide. Give short friendly survival tips. Reply with only your answer. Here is the chat so far:\n"+conversation
    headers={"Authorization":"Bearer "+apikey}
    data={"model":model,"messages":[{"role":"user","content":prompt}]}#copy this line exactly, it is the format OpenRouter needs
    response=requests.post(url,headers=headers,json=data)#sends it to OpenRouter
    if response.status_code==200:#200 means it worked
        answer=response.json()["choices"][0]["message"]["content"]
        return answer
    else:
        return "Sorry the AI could not answer. Check your api key."

#Runs when the page opens or when the user presses Send
@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        usertext=request.form.get("message").strip()#what the user typed
        if usertext=="/help":#goes to function A
            chat.append("You: "+usertext)
            chat.append("Bot: "+helpmessage())
        elif usertext=="/clear":#goes to function B
            clearchat()
        elif usertext!="":#anything else goes to the AI
            chat.append("You: "+usertext)
            chat.append("Bot: "+askai(chat))
    return render_template("index.html",messages=chat)

app.run(debug=True)