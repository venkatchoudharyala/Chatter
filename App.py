import streamlit as st
import json
import time
from LoginApp import Page
import datetime
import warnings
import os
import datetime
import pytz
from CryptTech import Recipes
import streamlit.components.v1 as components
from SMS import Send
import AdminPanel as ap

st.set_page_config(initial_sidebar_state = "collapsed")

hide_st_style = """
		<style>
		header {visibility: hidden;}
		footer {visibility: hidden;}
  		</style>
  		"""

st.markdown(hide_st_style, unsafe_allow_html = True)

warnings.filterwarnings("ignore")

Page.main()

if "user" in st.session_state:
	UserDetails = st.session_state["user"]
	#st.write(UserDetails)
	st.session_state["LoginVal"] = True
	Expand = st.sidebar.expander("Chats")

else:
	st.session_state["LoginVal"] = False

def main():
	if st.session_state["LoginVal"]:
		st.session_state['page'] = "MainRoom"
		UserName = UserDetails["Name"]
		if UserName == "Admin":
			ap.Scrapper()
		else:
			SearchStensil = st.sidebar.text_input("New Chat")
			NewChat(SearchStensil, UserName)
			path = "UserAcc/" + UserName + ".ua"
			try:
				with open(path, "r") as File:
					Account = json.load(File)
					Chats = Account["Chats"]
				if Chats:
					SelectedChat = st.sidebar.selectbox("Chats", list(Chats.keys()))
					AccountDisplay(SelectedChat)
				else:
					st.subheader("Expand Ur Account's Sidebar & find ur Friends on PINGIT")
					
			except FileNotFoundError:
				st.session_state['page'] = "LoginPage"
				st.session_state['LoginVal'] = False
				st.rerun()

def AccountDisplay(SelectedChat):
	UserName = UserDetails["Name"]
	path = "UserAcc/" + UserName + ".ua"
	with open(path, "r") as File:
		Account = json.load(File)
	if Account["Chats"]:
		ChatFile = "ChatRooms/" + GetChatFile(SelectedChat)
		ChatSelect(UserName, ChatFile, SelectedChat)

def GetChatFile(SelectedChat):
	UserName = UserDetails["Name"]
	path = "UserAcc/" + UserName + ".ua"

	with open(path, "r") as File:
		Account = json.load(File)

	Chats = Account["Chats"]
	return Chats[SelectedChat]["File"]

def ChatBox(UserName, ChatFile, SelectedChat):
	path = "UserAcc/" + UserName + ".ua"
	with open(path, "r") as file:
		Account = json.load(file)
	Key = Account["Chats"][SelectedChat]["Key"]
	seen = Account["Chats"][SelectedChat]["seen"]
	
	#st.write(Key)
	with open(ChatFile, "r") as File:
		Chat = json.load(File)
		
	PreTimeStamp = datetime.datetime(2003, 7, 4, 0, 15, 0)
	msgCounter = 0
	if seen == len(Chat):
		nitco = False
	else:
		nitco = True
	for key, value in Chat.items():
		if nitco and seen == msgCounter:
			st.write("New Messages")
		username = value["UNAME"]
		message = value["MSG"]
		TimeStamp = datetime.datetime.strptime(value["TimeStamp"], '%Y-%m-%d %H:%M:%S.%f+05:30')
		message = Recipes.MessageDecrypt(message, Key)

		Diff = TimeStamp - PreTimeStamp
		Diff = (Diff.seconds) / 60
		if Diff >= 1:
			st.write(TimeStamp)
		PreTimeStamp = TimeStamp

		if username != UserName:
			with st.chat_message("user"):
				st.markdown(message)
		else:
			with st.chat_message("assistant"):
				st.markdown(message)
		msgCounter += 1

def ChatBoxUpdater(UserName, ChatFile, SelectedChat):
	ChatBox(UserName, ChatFile, SelectedChat)
	time.sleep(1)
	st.rerun()
	#st.stop()

def ChatInp(UserName, ChatFile, SelectedChat):
	Msg = st.chat_input("Say something")
	x = False
	#st.write("Developed at PingIt Labs, Contact us at @ISheriff Chat")
	if Msg:
		#st.write(f"User has sent the following prompt: {Msg}")
		UpdateChatRoom(Msg, UserName, ChatFile, SelectedChat)

def UpdateChatRoom(Msg, UserName, ChatFile, SelectedChat):
	path = "UserAcc/" + SelectedChat + ".ua"
	with open(path, "r") as file:
		Account = json.load(file)
	Key = Account["Chats"][UserName]["Key"]
	with open(ChatFile, "r") as file:
		Chat = json.load(file)

	time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

	NewMsg = {
		"UNAME": UserName,
		"MSG": Recipes.MessageEncrypt(Msg, Key),
		"TimeStamp": str(time)
		}
	Chat[len(Chat) + 1] = NewMsg

	path = "UserAcc/" + UserName + ".ua"
	with open(path, "r") as file:
		Account = json.load(file)
	Account["Chats"][SelectedChat]["seen"] = len(Chat)
	with open(path, "w") as file:
		json.dump(Account, file)
		
	with open(ChatFile, "w") as file:
		json.dump(Chat, file)

def Blocking(UserName, SelectedChat):
	NewChat.clear()
	path = "UserAcc/" + UserName + ".ua"
	try:
		with open(path, "r") as file:
			Account = json.load(file)
		Chats = Account["Chats"]
		Block = Account["Blocked"]
		del Chats[SelectedChat]
		Block[SelectedChat] = "1"

		with open(path, "w") as file:
			json.dump(Account, file)

		UserDetails = Account
	except FileNotFoundError:
		DoNothing = 0
	NewChat.clear()
	st.rerun()

def DeleteChat(SelectedChat, UserName):
	"""try:
		with open(ChatFile, "w") as file:
			file.write("{}")
	except FileNotFoundError:
		DoNothing = 0"""
	NewChat.clear()
	path = "UserAcc/" + UserName + ".ua"
	try:
		with open(path, "r") as file:
			Account = json.load(file)
		Chats = Account["Chats"]
		RoomFile = Chats[SelectedChat]
		if(SelectedChat in list(Chats.keys())):
			del Chats[SelectedChat]
		with open(path, "w") as file:
			json.dump(Account, file)
	except FileNotFoundError:
		DoNothing = 0
	path = "UserAcc/" + SelectedChat + ".ua"
	try:
		with open(path, "r") as file:
			Account1 = json.load(file)
		Chats = Account1["Chats"]
		if(UserName in list(Chats.keys())):
			del Chats[UserName]
		with open(path, "w") as file:
			json.dump(Account1, file)
	except FileNotFoundError:
		DoNothing = 0

	path = "ChatRooms/" + RoomFile
	try:
		os.remove(path)
		st.write("Chat Room Deleted Successfully!!")
	except FileNotFoundError:
		DoNothing = 0

	UserDetails = Account
	NewChat.clear()
	#st.experimental_rerun()

def ChatSelect(UserName, ChatFile, SelectedChat):
	global Mode
	ChatInp(UserName, ChatFile, SelectedChat)
	st.title("Chat Room")
	with st.sidebar.expander("Privacy and Security Tags"):
		if(st.checkbox("Your Password Hash")):
			Framer = st.sidebar.empty()
			path = "UserAcc/" + UserName + ".ua"
			with open(path, "r") as file:
				Account = json.load(file)
			Passd = Account["Password"]
			st.write("Your Password is Hashed and stored at our Data Server, No one from the Organization can access your Account!!")
			if(st.button("Password Hash")):
				Framer.write(Passd)

		if(st.checkbox("Chat Room's Key")):
			KeyFrame = st.sidebar.empty()
			st.write(f"Your Chats are e2e Encrypted with {SelectedChat}")
			if(st.button("Display Key")):
				path = "UserAcc/" + UserName + ".ua"
				with open(path, "r") as file:
					Account = json.load(file)
				KeyFrame.write("Chats Room's Key")
				KeyFrame.write(Account["Chats"][SelectedChat]["Key"])

	with st.sidebar.expander("Misc Operations"):
		if(st.checkbox("Block This Chat")):
			st.write(f"After Blocking, {SelectedChat} can't chat with you until you Re-initiate NewChat")
			if(st.button("Confirm Blocking")):
				NewChat.clear()
				Blocking(UserName, SelectedChat)
		if(st.checkbox("Delete this Chat")):
			st.write("After Deletion, this ChatRoom gets erased")
			if(st.button("Confirm Deletion")):
				DeleteChat(SelectedChat, UserName)
		if(st.checkbox("LogOut")):
			if(st.button("Confirm LogOut")):
				st.session_state['page'] = "LoginPage"
				st.session_state['LogVal'] = False
				st.experimental_rerun()
		if(st.checkbox("Delete Your Account")):
			st.write("Your Account will be deleted Permanently!!")
			if(st.button("Confirm")):
				os.remove("UserAcc/" + UserName + ".ua")
				Page.main()

	with st.sidebar.expander("Queries and Reports"):
		st.write("Developed at PingIt Labs, Contact us at @ISheriff Chat for any Queries & Reports over Toxic Users")

	with st.sidebar.expander("Alerts"):
		st.write("Under Development, Hosting Beta services for selected Users")

	try:
		ChatBoxUpdater(UserName, ChatFile, SelectedChat)
	except FileNotFoundError:
		DoNothing = 0

def Unblocking(SearchStensil,UserName):
	#if(st.sidebar.button("Un-Block")):
	path = "UserAcc/" + SearchStensil + ".ua"
	with open(path, "r") as file:
		Account = json.load(file)
	ChatDict = Account["Chats"]
	ChatDict[UserName] = UserName + "_" + SearchStensil + ".msg"
	with open(path, "w") as File:
		json.dump(Account, File)

	path = "UserAcc/" + UserName + ".ua"
	with open(path, "r") as File:
		Account = json.load(File)
	ChatDict = Account["Chats"]
	ChatDict[SearchStensil] = UserName + "_" + SearchStensil + ".msg"
	Block = Account["Blocked"]
	del Block[SearchStensil]
	Account["Blocked"] = Block
	Account["Chats"] = ChatDict
	with open(path, "w") as File:
		json.dump(Account, File)

	path = "ChatRooms/" + UserName + "_" + SearchStensil + ".msg"
	with open(path, "w") as File:
		File.write("{}")
	st.sidebar.write("UnBlocked Successfully!!")
	#UserDetails = Account
	st.rerun()

@st.cache_data
def NewChat(SearchStensil,UserName):
	path = "UserAcc/" + SearchStensil + ".ua"
	pathrb = "UserAcc/" + UserName + ".ua"
	with open(pathrb, "r") as file:
		RootUser = json.load(file)
	ts = datetime.datetime.now().timestamp()
	try:
		with open(path, "r") as File:
			Account = json.load(File)
			#x = UserName + ":" + ts + ".msg"
		if(UserName in list(Account["Blocked"].keys())):
			st.sidebar.write(f"Sorry, U can't Chat with {SearchStensil}")

		elif(SearchStensil in list(RootUser["Blocked"].keys())):
			st.sidebar.write("U Blocked this User..")
			#if(st.button("Un-Block")):
			Unblocking(SearchStensil, UserName)

		else:
			Key = Recipes.KeyGenerator()
			ChatDict = Account["Chats"]
			ChatDict[UserName] = {}
			ChatDict[UserName]["File"] = UserName + "_" + SearchStensil + ".msg"
			ChatDict[UserName]["Key"] = Key
			ChatDict[UserName]["seen"] = 0
			with open(path, "w") as File:
				json.dump(Account, File)

			path = "UserAcc/" + UserName + ".ua"
			with open(path, "r") as File:
				Account = json.load(File)
			ChatDict = Account["Chats"]
			ChatDict[SearchStensil] = {}
			ChatDict[SearchStensil]["File"] = UserName + "_" + SearchStensil + ".msg"
			ChatDict[SearchStensil]["Key"] = Key
			ChatDict[SearchStensil]["seen"] = 0
			with open(path, "w") as File:
				json.dump(Account, File)

			path = "ChatRooms/" + UserName + "_" + SearchStensil + ".msg"
			with open(path, "w") as File:
				File.write("{}")

			#UserDetails = Account

	except FileNotFoundError:
		if(SearchStensil != ""):
			st.sidebar.write(f"User {SearchStensil} Not Found!!")

if __name__ == "__main__":
	main()
