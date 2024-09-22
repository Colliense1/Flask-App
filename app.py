from flask import Flask, render_template, request, redirect, url_for

from models import db, Contact

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()        # Creating the table before running the app


@app.route("/")
def index():
    contacts = Contact.query.all()
    return render_template("index.html", contacts = contacts)


@app.route("/contact", methods= ["GET", "POST"])
def contact():
    header = "Create Contact"
    greet = "Welcome To Contact page..!"
    if request.method == "POST":
        form_data = request.form
        name = form_data.get("name")
        email = form_data.get("email")
        message = form_data.get("message")

        #save them to the database (3 step)
        # 1. object will make
        # 2. add() and
        # 3. commit() will do
        new_contact = Contact(
            name = name,
            email = email,
            message = message
        )
        db.session.add(new_contact)
        db.session.commit()
        # Redirect to the index page after successful submission
        return redirect(url_for('index'))
    return render_template("contact.html", 
                           header = header,
                           greet = greet)
    
@app.route("/update/<int:contact_id>", methods = ["GET", "POST"])
def update_contact(contact_id):

    header = "Update Contact"
    greet = ""

    contacts = Contact.query.get_or_404(contact_id)
    if request.method == "POST":
        update_data = request.form
        contacts.name = update_data.get("name")
        contacts.email = update_data.get("email")
        contacts.message = update_data.get("message")

        db.session.commit()

        return redirect(url_for('index'))
    return render_template("contact.html", 
                           contacts = contacts, 
                           header = header,
                           greet = greet)


@app.route("/delete/<int:contact_id>", methods =["GET", "POST"])
def delete_contact(contact_id):
    contacts = Contact.query.get_or_404(contact_id)
    if request.method == "POST":
        db.session.delete(contacts)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template("delete_contact.html", contacts = contacts)

if __name__ == '__main__':
    app.run(debug=True)