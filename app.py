from flask import Flask, render_template, request, redirect, url_for, session
from cardiverse import main
import secrets

secret_key = secrets.token_hex(16) 

app = Flask(__name__, '/static')
app.secret_key = secret_key
app.config["DEBUG"] = True

# give a default year since the get_tracks function now requires a year argument
default_birthday ='1998-10-05'

# when you go to the main url, it will render the index.html
# that lives inside the templates folder
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    recievers_name = request.form['recievers_name']
    senders_name = request.form['senders_name']
    #senders_name = request.form.get('name', 'Anonymous')  

    #found_birthday_song, found_lyrics, years_playlist, main_lyrics, gif_ids = main(user_birthday, user_name)
    #song_name, artists_name, released_date, song_uri = found_birthday_song
    session['recievers_name'] = recievers_name
    session['senders_name'] = senders_name

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

#can i try make it go to loading page before results page???? which has the lyrics or gifs on before then? 
#if results are in??? -- go to ... how would tell when it is loading


@app.route('/results', methods = ['GET'])
def results_post(): 
    results_data = {
        'recievers_name': session.get('recievers_name', 'Unknown'),
        'senders_name': session.get('senders_name', 'Anonymous'),
    }
    return render_template('results.html', **results_data)

