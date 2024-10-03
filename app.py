from flask import Flask

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a Message model with __tablename__
class Message(db.Model):
    __tablename__ = 'messages'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}: {self.content}>'

# Create the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the message from the form
        message_content = request.form.get('message')
        if message_content:
            # Create a new message instance
            new_message = Message(content=message_content)
            # Add and commit the message to the database
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('home'))  # Redirect after submission

    # Retrieve all messages from the database
    messages = Message.query.all()

    # Define your schedule
    schedule = {
        "16:00": {
            "Monday": "Grupe Copii",
            "Tuesday": "Grupe Adolescenți",
            "Wednesday": "Cursuri Adulți",
            "Thursday": "Grupe Copii",
            "Friday": "Cursuri Adulți",
        },
        "17:00": {
            "Monday": "Grupe Adolescenți",
            "Tuesday": "Cursuri Adulți",
            "Wednesday": "Grupe Copii",
            "Thursday": "Grupe Adolescenți",
            "Friday": "Grupe Copii",
        },
        "18:00": {
            "Monday": "Cursuri Adulți",
            "Tuesday": "Grupe Copii",
            "Wednesday": "Grupe Adolescenți",
            "Thursday": "Cursuri Adulți",
            "Friday": "Grupe Adolescenți",
        },
        "19:00": {
            "Monday": "Cursuri Adulți",
            "Tuesday": "Grupe Adolescenți",
            "Wednesday": "Cursuri Adulți",
            "Thursday": "Grupe Copii",
            "Friday": "Cursuri Adulți",
        },
        "20:00": {
            "Monday": "",
            "Tuesday": "",
            "Wednesday": "Cursuri Adulți",
            "Thursday": "",
            "Friday": "Grupe Adolescenți",
        },
    }

    return render_template('home.html', messages=messages, schedule=schedule)


@app.route('/admin/delete_messages', methods=['GET', 'POST'])
def clear_messages():
    # Delete messages on both GET and POST requests
    Message.query.delete()  # Delete all messages
    db.session.commit()  # Commit the changes to the database
    return render_template('home.html', messages=[])  # Pass an empty list after deletion

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)