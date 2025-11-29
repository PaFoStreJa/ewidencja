from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
print("Working directory:", os.getcwd())
print("Templates folder:", os.path.join(os.getcwd(), 'templates'))
#tworzenie aplikacji
app = Flask(__name__)

# konfiguracja bazy SQLite (plik w folderze projektu)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ewidencja.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modele tabeli w bazie
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    page_number = db.Column(db.Integer)


#definiowanie stron
# główna strona
@app.route('/')
def index():
    query = request.args.get('q')
    items = []
    if query:
        items = Song.query.filter(Song.name.contains(query)).all()
    else:
        items = Song.query.all()
    return render_template('index.html', items=items)

# strona dodawania
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        page_number = request.form.get('page_number')
        page_number = int(page_number) if page_number else None

        item = Song(name=name, page_number=page_number)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template('add_item.html')

# strona usuwania
@app.route("/delete/<int:item_id>", methods=['POST'])
def delete_item(item_id):
    item = Song.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:item_id>", methods=['GET', 'POST'])
def edit_item(item_id):
    item = Song.query.get_or_404(item_id)

    if request.method == 'POST':
        name = request.form.get('name')
        page_number = request.form.get('page_number')

        item.name = name
        item.page_number = int(page_number) if page_number else None

        db.session.commit()
        return redirect(url_for("index"))
    return render_template('edit_item.html', item=item)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)