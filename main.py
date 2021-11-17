from telethon import TelegramClient, sync
import pandas as pd
from flask_restful import Resource, Api, reqparse
from flask import Flask
from flask import jsonify,request
from flask_cors import CORS, cross_origin
import ast
import json
App_ID=15611004
App_Hash="4cf14851116f86dd1ede638e93d70500"
GroupName="RamLogicsTesting"

client = TelegramClient("session_name",App_ID,App_Hash).start()

# Get Client Details 
participants = client.get_participants(GroupName)
firstname =[]
lastname = []
username = []
phone = []
if len(participants):
    for x in participants:
        firstname.append(x.first_name)
        lastname.append(x.last_name)
        username.append(x.username)
        phone.append(x.phone)

print(participants)
# list to data frame conversion

data ={'first_name' :firstname, 'last_name':lastname, 'user_name':username,"phone":phone}
userdetails = pd.DataFrame(data)
userdetails = userdetails.to_json(orient='records')



# Get Chats of the Client 

chats =client.get_messages(GroupName, 4) # n number of messages to be extracted
# Get message id, message, sender id, reply to message id, and timestamp

message_id =[]
message =[]
sender =[]
reply_to =[]
time = []
if len(chats):
    for chat in chats:
        message_id.append(chat.id)
        message.append(chat.message)
        sender.append(chat.from_id)
        reply_to.append(chat.reply_to_msg_id)
        time.append(chat.date)
data ={'message_id':message_id, 'message': message, 'sender_ID':sender, 'reply_to_msg_id':reply_to, 'time':time}
df = pd.DataFrame(data)
print("\n\n")
# print(df)

# Get Specific Message

messages =[]
time = []
for message in client.iter_messages(GroupName, search='hellown'):
    messages.append(message.message) # get messages 
    time.append(message.date) # get timestamp
data ={'time':time, 'message':messages}

df = pd.DataFrame(data)

print(df)


# # Flask APP Create 

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# @app.route("/")
@cross_origin()




# User API For Get USer Details
@app.route('/users/', methods=['POST'])
def get():

    UserData = json.loads(request.data)
    print(UserData)
    for i in json.loads(userdetails):
       if(UserData["TUserName"]!=""):
        if i['user_name']==UserData["TUserName"] and i['phone']==UserData["Phone"]:
            print('True')
            return json.dumps({"msg":True})
    
    return json.dumps({"msg":False})
    # return jsonify(json.loads(userdetails)) # return data and 200 OK code


@app.route('/user/phone/', methods=['POST'])
def getPhone():
    phoneData = json.loads(request.data)
    print(phoneData)
    for i in json.loads(userdetails):
       if(phoneData["Phone"]!=""):
        if i['phone']==phoneData["Phone"]:
            print('True')
            return json.dumps({"msg":True}) 

    return json.dumps({"msg":False})



if __name__ == "__main__":
        app.run()


