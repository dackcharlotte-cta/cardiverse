from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import os 
from cardiverse import main
from poembot import get_poem
from dalle import get_image



secret_key = secrets.token_hex(16) 

app = Flask(__name__, '/static')
app.secret_key = secret_key
app.config["DEBUG"] = True

app.config['UPLOAD_FOLDER'] = "uploads"


@app.route('/')
def index():
    isLoading = False
    data = {
        'isLoading': isLoading,
    }
    return render_template('index.html', **data)


@app.route('/', methods=['POST'])
def index_post():
    isLoading = True
    #getting input from HTML and assigning to variable 
    recievers_name = request.form['recievers_name']
    senders_name = request.form['senders_name']
    user_message = request.form['user_message']
    users_image = request.files["filename"]
    occasions = request.args.get('occasions')
    print(occasions)

    #saving uploaded image 
    filename = users_image.filename
    users_image.save(os.path.join("static", "uploads", filename))

    #sending the filename into my cardiverse.py  
    modelname = main(filename)

    #the poem and the prompt 
    poembot_response = get_poem(user_message, recievers_name, occasions)
    bot_poem = poembot_response.split('-')[0]
    bot_prompt = poembot_response.split('-')[1]
    #getting my name of the image from my dalle.py whilst sending arg 
    image_name = get_image(bot_prompt)
    isLoading = False

    session['recievers_name'] = recievers_name
    session['senders_name'] = senders_name
    session['filename'] = filename  
    session['isLoading'] = isLoading  
    session['bot_poem'] = bot_poem

    print(bot_poem)

    #results_data = {
        #'song_name': song_name,
        #'artists_name': artists_name,
        #'released_date': released_date,
        #'lyrics': found_lyrics,
        #'playlist_id': years_playlist,
        #'gif_ids': gif_ids,
        #'user_birthday': user_birthday,
        #'user_name': user_name,
 
    #}

    #session['results_data'] = results_data
    
    return redirect(url_for('results_post', bot_poem=bot_poem, image_name=image_name, modelname=modelname, recievers_name=recievers_name, senders_name=senders_name))



@app.route('/results', methods = ['GET'])
def results_post(): 
    modelname = request.args.get('modelname')
    recievers_name = request.args.get('recievers_name')
    senders_name = request.args.get('senders_name')
    bot_poem = request.args.get('bot_poem')
    results_data = {
        'recievers_name': recievers_name,
        'senders_name': senders_name,
        'generated_model_name': modelname,
        'bot_poem' : bot_poem
    }

    session['results_data'] = results_data
    return render_template('results.html', **results_data)
    