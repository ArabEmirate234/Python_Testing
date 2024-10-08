import json
from flask import Flask, render_template, request, redirect, url_for, flash, session

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
    return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email')
    if not email:
        flash('Veuillez entrer votre adresse mail!', 'error')
        return redirect(url_for('index'))
    matching_clubs = [club for club in clubs if club['email'] == email]
    if not matching_clubs:
        flash('Aucun club trouvé avec cette adresse e-mail.', 'error')
        return redirect(url_for('index'))
    
    club = matching_clubs[0]
    session['club'] = club  # Store the logged-in club in the session
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)
   
    try:
        placesRequired = int(request.form['places'])  # Attempt to convert input to an integer
    except ValueError:
        flash('Erreur : Le nombre de places doit être un entier valide.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    if not competition or not club:
        flash("Competition or club not found.")
        return redirect(url_for('index'))

    # Check if the club has enough points
    if int(club['points']) < placesRequired:
        flash('Point insuffisant!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Check if the competition has enough places available
    if int(competition['numberOfPlaces']) < placesRequired:
        flash('Nombre de places insuffisant!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Check if the requested places exceed the maximum booking limit
    if placesRequired > 12:
        flash('Vous ne pouvez pas réserver plus de 12 places.')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Deduct points and update available places
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash(f'Great - {placesRequired} places booked!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    session.pop('club', None) 
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
