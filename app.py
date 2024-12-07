from flask import Flask, render_template, request, redirect, url_for, session
from cardiverse import main
import secrets
import os 



secret_key = secrets.token_hex(16) 

app = Flask(__name__, '/static')
app.secret_key = secret_key
app.config["DEBUG"] = True

app.config['UPLOAD_FOLDER'] = "uploads"

# give a default year since the get_tracks function now requires a year argument
default_birthday ='1998-10-05'


@app.route('/')
def index():
    users_image = request.files["filename"]
    filename = users_image.filename
    users_image.save(os.path.join("static", "uploads", filename))

    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    recievers_name = request.form['recievers_name']
    senders_name = request.form['senders_name']
    users_image = request.files["filename"]
    filename = users_image.filename
    users_image.save(os.path.join("static", "uploads", filename))

    users_filename = image_pathway(filename)
    
 
    session['recievers_name'] = recievers_name
    session['senders_name'] = senders_name
    session['filename'] = filename  


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
    return redirect(url_for('results_post'))



@app.route('/results', methods = ['GET'])
def results_post(): 
    results_data = {
        'recievers_name': session.get('recievers_name', 'Unknown'),
        'senders_name': session.get('senders_name', 'Anonymous'),
    }
    return render_template('results.html', **results_data)

