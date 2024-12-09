from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import os 
from cardiverse import main



secret_key = secrets.token_hex(16) 

app = Flask(__name__, '/static')
app.secret_key = secret_key
app.config["DEBUG"] = True

app.config['UPLOAD_FOLDER'] = "uploads"

# give a default year since the get_tracks function now requires a year argument
default_birthday ='1998-10-05'


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
    recievers_name = request.form['recievers_name']
    senders_name = request.form['senders_name']
    #user_message = request.form['message']
    users_image = request.files["filename"]
    filename = users_image.filename
    users_image.save(os.path.join("static", "uploads", filename))

    modelname = main(filename)
    #chatbot_response = message_for_r(user_message, recievers_name)
    
    isLoading = False

    session['recievers_name'] = recievers_name
    session['senders_name'] = senders_name
    session['filename'] = filename  
    session['isLoading'] = isLoading  

    

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
    print(modelname)
    return redirect(url_for('results_post', modelname=modelname, recievers_name=recievers_name, senders_name=senders_name))



@app.route('/results', methods = ['GET'])
def results_post(): 
    modelname = request.args.get('modelname')
    recievers_name = request.args.get('recievers_name')
    senders_name = request.args.get('senders_name')
    results_data = {
        'recievers_name': recievers_name,
        'senders_name': senders_name,
        'generated_model_name': modelname
    }

    session['results_data'] = results_data
    return render_template('results.html', **results_data)
    