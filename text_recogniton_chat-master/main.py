import re

from httplib2 import Authentication
import long_responses as long
from flask import Flask,render_template,request

import pyrebase
from flask import *
app = Flask(__name__)

config = {
    "apiKey": "AIzaSyApj_50QGUAf26ek3M6aSckkBvNvzMJOaE",
    "authDomain": "simabot-9da61.firebaseapp.com",
    "databaseURL": "https://simabot-9da61-default-rtdb.firebaseio.com",
    "projectId": "simabot-9da61",
    "storageBucket": "simabot-9da61.appspot.com",
    "messagingSenderId": "836676186351",
    "appId": "1:836676186351:web:3d8dfe41fce69cf2f22b1a",
    "measurementId": "G-ZP0QF60CVG"
  }

firebase = pyrebase.initialize_app(config)

# pub_key = "pk_test_tqCJtQ9f6ouxRfOkIUPDCvmO00q8KBcx76"

auth = firebase.auth()

db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}




@app.route('/Home')
@app.route('/')

def home():
    if auth.current_user != None:

        session_username = db.child("users").child(auth.current_user["localId"]).child("username").get().val()
        creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()
        return render_template("Home.html", pub_key=pub_key, session_username=session_username, creditpoints=creditpoints)
    return render_template("Home.html", user_not_authenticated=True)







@app.route('/login', methods=['GET', 'POST'])
def basic():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.sign_in_with_email_and_password(email, password)
			return render_template('ask.html', s=successful)
		except:
			return render_template('login.html', us=unsuccessful)

	return render_template('login.html')    
	

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    auth.current_user = None
    return redirect("/")





@app.route('/about')
def about():
    
	return render_template('about.html')

# def register():
# 	unsuccessful = 'Please check your credentials'
# 	successful = 'Login successful'
# 	if request.method == 'POST':
# 		firstName = request.form['firstname']
# 		lastName = request.form['lastname']
# 		email = request.form['email']
# 		password = request.form['passward']
# 		try:
# 			auth.createUserWithEmailAndPassword(firstName, lastName, email, password)
# 			return render_template('login.html', s=successful)
# 		except:
# 			return render_template('register.html', us=unsuccessful)
# 	return render_template('register.html')
# @app.route('/create account', nathoos=['GET', 'POST'])
# def create_account():
#    if request.nethod POST:
#        pwd0 = request.form['user_pwde' ]
#        pad1 = request.form[ 'user_pwd1']
#        if pedi
#     return render tenplate(create account.h


@app.route('/register', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
        
            email = request.form['name']
            password = request.form['password']
            
            # Rest_Password = request.form['Rest_Password']
            try:
             auth.create_user_with_email_and_password(email, password)
             return render_template('login.html')
            except:
             return render_template("register.html", message="Email is already taken or password has less than 6 letters" )  

            return render_template("register.html")
 
    return render_template('register.html')


    # if request.method == 'POST':
		
	# 	if request.form['submit'] == 'add':
	# 	# while request.form['submit'] == 'add':
	# 		name = request.form['name']
	# 		lname = request.form['lname']
	# 		db.child(name).set({
	# 			'name': name,
	# 			'lname': lname
				
	# 		})
		
	# 		todo=db.get()
	# 		to=todo.val()
    #  return render_template('add.html',data=to.values() )

    # if request.method == "POST":        #Only listen to POST
    #     result = request.form           #Get the data submitted
    #     email = result["email"]
    #     password = result["pass"]
    #     name = result["name"]
    #     try:
    #         #Try creating the user account using the provided data
    #         auth.create_user_with_email_and_password(email, password)
    #         # #Login the user
    #         user = auth.sign_in_with_email_and_password(email, password)
    #         #Add data to global person
    #         global person
    #         person["is_logged_in"] = True
    #         person["email"] = user["email"]
    #         person["uid"] = user["localId"]
    #         person["name"] = name
    #         #Append data to the firebase realtime database
    #         data = {"name": name, "email": email}
    #         db.child("users").child(person["uid"]).set(data)
    #         #Go to welcome page
    #         return redirect(url_for('login.html'))
    #     except:
    #         #If there is any error, redirect to register
            # return redirect(url_for('register.html'))

    # else:
    #     if person["is_logged_in"] == True:
    #         return redirect(url_for('login.html'))
    #     else:
    #         return redirect(url_for('register.html'))




@app.route('/ask')

def ask():
	return render_template('login.html')


@app.route('/add', methods=['GET', 'POST'])
def reg():
    
	if request.method == 'POST':
		if request.form['submit'] == 'submit':

			name = request.form['name']
			db.child("todo").push(name)
			todo = db.child("todo").get()
			to = todo.val()
			return render_template('register.html', t=to.values())
		
	return render_template('register.html')
			
	return render_template('register.html')
    
@app.route('/feedback', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		if request.form['submit'] == 'add':

			name = request.form['name']
			db.child("todo").push(name)
			todo = db.child("todo").get()
			to = todo.val()
			return render_template('feedback.html', t=to.values())
		
	return render_template('feedback.html')



@app.route('/chat')
def hello_world():
    return render_template('chat.html')




def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
# while True:
@app.route("/")
def index():
     return render_template("index.html") #to send context to html

@app.route("/get")
def get_bot_response():
     userText = request.args.get("msg") #get data from input,we write js  to index.html
     return str(get_response(userText))

    # print('Bot: ' + get_response(input('You: ')))
if __name__ == "__main__":
     app.run(debug = True)