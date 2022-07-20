from flask import Flask, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6dfonkWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)

class EditForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(3,250)])
    map_link = StringField(label="Maps link", validators=[DataRequired()])
    img_link = StringField(label="Photo link")
    location = StringField(label="Location", validators=[DataRequired(), Length(3,250)])
    has_sockets = BooleanField(label = "Has sockets")
    has_toilet = BooleanField(label="Has Toilet")
    has_wifi = BooleanField(label="Has Wifi")
    can_take_calls = BooleanField(label="Can take calls")
    seats = SelectField(label="Number of seats", choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"])
    price = StringField(label="Coffee price")
    submit = SubmitField(label="Save")



class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(1000), nullable=False,)
    img_url = db.Column(db.String(1000), nullable=False,)
    location = db.Column(db.String(250), nullable=False,)
    has_sockets = db.Column(db.Boolean, nullable=False,)
    has_toilet = db.Column(db.Boolean, nullable=False,)
    has_wifi = db.Column(db.Boolean, nullable=False,)
    can_take_calls = db.Column(db.Boolean, nullable=False,)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))

    def __repr__(self):
        return '<Cafe %r>' % self.name

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

db.create_all()


@app.route('/')
def index():
    all_cafes = db.session.query(Cafe).all()
    cafes = [cafe.to_dict() for cafe in all_cafes]

    return render_template("index.html", cafes=cafes)


@app.route('/<cafe_id>', methods=["GET", "POST"])
def get_cafe(cafe_id):
    selected_cafe = Cafe.query.get(cafe_id)
    cafe_data = selected_cafe.to_dict()
    random_cafes = []
    for n in range(6):
        random_cafes.append(Cafe.query.get(random.randint(1, len(Cafe.query.all()))))
    return render_template("cafe.html", cafe=cafe_data, random_cafes=random_cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = EditForm()
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.name.data,
                        map_url=form.map_link.data,
                        img_url=form.img_link.data,
                        location=form.location.data,
                        has_sockets=form.has_sockets.data,
                        has_toilet=form.has_toilet.data,
                        has_wifi=form.has_wifi.data,
                        can_take_calls=form.can_take_calls.data,
                        seats=form.seats.data,
                        coffee_price=form.price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        random_cafes = []
        for n in range(6):
            random_cafes.append(Cafe.query.get(random.randint(1, len(Cafe.query.all()))))
        return render_template("add_cafe.html", form=form, random_cafes=random_cafes, new_cafe=True)


@app.route("/edit/<cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    current_cafe = Cafe.query.get(cafe_id)
    form = EditForm(name=current_cafe.name,
                    map_link=current_cafe.map_url,
                    img_link=current_cafe.img_url,
                    location=current_cafe.location,
                    has_sockets=current_cafe.has_sockets,
                    has_toilet=current_cafe.has_toilet,
                    has_wifi=current_cafe.has_wifi,
                    can_take_calls=current_cafe.can_take_calls,
                    seats=current_cafe.seats,
                    price=current_cafe.coffee_price
                    )
    random_cafes = []
    for n in range(6):
        random_cafes.append(Cafe.query.get(random.randint(1,len(Cafe.query.all()))))
    if form.validate_on_submit():
        current_cafe.name = form.name.data
        current_cafe.map_url = form.map_link.data
        current_cafe.img_url = form.img_link.data
        current_cafe.location = form.location.data
        current_cafe.has_sockets = form.has_sockets.data
        current_cafe.has_toilet = form.has_toilet.data
        current_cafe.has_wifi = form.has_wifi.data
        current_cafe.can_take_calls = form.can_take_calls.data
        current_cafe.seats = form.seats.data
        current_cafe.coffee_price = form.price.data
        db.session.commit()
        return redirect(url_for("get_cafe", cafe_id=cafe_id))
    return render_template("add_cafe.html", form=form, random_cafes=random_cafes )


if __name__ == '__main__':
    app.run(debug=True)