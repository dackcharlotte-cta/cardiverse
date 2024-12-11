from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import os 
from cardiverse import main
from poembot import get_poem
from dalle import get_image

#makes a secret key and assign it to the variable
#need this as i am using session 
secret_key = secrets.token_hex(16) 

#set up of flask app 
app = Flask(__name__, '/static')

#futher set up for secret key 
app.secret_key = secret_key

#set up if debugging mode - this is so i can debug in browser 
app.config["DEBUG"] = True

#set up of upload folder for user image uploads 
app.config['UPLOAD_FOLDER'] = "uploads"


@app.route('/')
def index():
    #for my loading page - set up  
    isLoading = False
    data = {
        'isLoading': isLoading,
    }
    #pass the data dictionary to index.html page
    return render_template('index.html', **data)

@app.route('/', methods=['POST'])
def index_post():
    isLoading = True
    # Get the input values from the HTML form and assign them to variables
    recievers_name = request.form['recievers_name']
    senders_name = request.form['senders_name']
    user_message = request.form['user_message']
    users_image = request.files["filename"]
    occasions = request.args.get('occasions')
    print(occasions)

    # Save the uploaded image file
    filename = users_image.filename
    users_image.save(os.path.join("static", "uploads", filename))

    # Call the main() function from cardiverse.py with the filename as an argument
    modelname = main(filename)

    # Get the poem and prompt from the get_poem() function in poembot.py
    poembot_response = get_poem(user_message, recievers_name, occasions)
    bot_poem = poembot_response.split('-')[0]
    bot_prompt = poembot_response.split('-')[1]

    # Get the name of the generated image from the get_image() function in dalle.py
    image_name = get_image(bot_prompt)
    isLoading = False

    #store the values in the session for later use 
    session['recievers_name'] = recievers_name
    session['senders_name'] = senders_name
    session['filename'] = filename  
    session['isLoading'] = isLoading  
    session['bot_poem'] = bot_poem

    #redircet the the above to results_post i.e. a different page 
    #i am passing the info as url parameters 
    return redirect(url_for('results_post', bot_poem=bot_poem, image_name=image_name, modelname=modelname, recievers_name=recievers_name, senders_name=senders_name))

@app.route('/results', methods = ['GET'])
def results_post(): 
    #I am getting the values from the URL parameters
    modelname = request.args.get('modelname')
    recievers_name = request.args.get('recievers_name')
    senders_name = request.args.get('senders_name')
    bot_poem = request.args.get('bot_poem')

    # Create a dictionary with the retrieved values
    results_data = {
        'recievers_name': recievers_name,
        'senders_name': senders_name,
        'generated_model_name': modelname,
        'bot_poem' : bot_poem
    }

    session['results_data'] = results_data


    return render_template('results.html', **results_data)