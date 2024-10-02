

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

@app.route('/showSummary',methods=['POST'])
@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)
    email = request.form.get('email')
    if not email:
        flash('Veuillez entrer votre adresse mail!', 'error')
        return redirect(url_for('index'))
    matching_clubs = [club for club in clubs if club['email'] == email]
    if not matching_clubs:
        flash('Aucun club trouvé avec cette adresse e-mail.', 'error')
        return redirect(url_for('index'))
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
else:
flash("Something went wrong-please try again")
return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
competition = [c for c in competitions if c['name'] == request.form['competition']][0]
club = [c for c in clubs if c['name'] == request.form['club']][0]
placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
       
    if int(club['points']) < placesRequired:
        flash('Point insuffisant!')
        return render_template('welcome.html', club=club, competitions=competitions)

    if int(competition['numberOfPlaces']) < placesRequired:
        flash('Nombre de places insuffisant!')
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
flash('Great-booking complete!')
return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
return redirect(url_for('index'))

if __name__ == "__main__":