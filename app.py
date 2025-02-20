from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from functools import wraps


basedir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False


app.config["SECRET_KEY"] = "Your secret key"




db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager()


login_manager.init_app(app)


login_manager.login_view = "login"


class User(db.Model, UserMixin):


    __tablename__ = "user"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)




@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))




with app.app_context():
    db.create_all()

    if not User.query.filter_by(role="admin").first():
        admin_user = User(name="Admin", email="admin@gmail.com",
                          mobile="1234567890", role="admin")
        admin_user.set_password("admin123")  
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with email: admin@gmail.com and password: admin123")




@app.route("/home")
@login_required
def home():
    return  render_template("index.html")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard1")
@login_required
def dashboard1():
    return render_template("dashboard1.html")

@app.route('/contact')
def contact():
    return render_template("contactus.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")


        user = User.query.filter_by(email=email, role=role).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("LogIn.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")


        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("signup"))


        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))


        new_user = User(name=name, email=email, mobile=mobile)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()


        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("SignUp.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user = current_user)

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Access denied!", "danger")
            return redirect(url_for('dashboard'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")



@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/aboutus2")
def aboutus2():
    return render_template("aboutus2.html")

@app.route("/adoptingpets")
def adoptingpets():
    return render_template("adoptingpets.html")

@app.route("/cats")
def cats():
    return render_template("cats.html")

@app.route("/catKittenAdoption")
def catKittenAdoption():
    return render_template("catKittenAdoption.html")

@app.route("/dogPuppiesAdoption")
def dogPuppiesAdoption():
    return render_template("dogPuppiesAdoption.html")

@app.route('/dogs')
def dogs():
    pets = Pet.query.all()  # Fetch all pet records
    return render_template('dogs.html', pets=pets)

@app.route("/behaviordog")
def behaviordog():
    return render_template("behavior_dog.html")


@app.route("/behaviorcat")
def behaviorcat():
    return render_template("behavior_cat.html")


@app.route("/learnmore2.html")
def learnmore2():
    return render_template("learnmore2.html")

@app.route("/learnmore3.html")
def learnmore3():
    return render_template("learnmore3.html")

@app.route("/foundation")
def foundation():
    return render_template("Foundation.html")

@app.route("/checklist")
def checklist():
    return render_template("checklist.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

class Cart(db.Model):  # Move Cart model above db.create_all()
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet', backref=db.backref('cart_items', lazy=True))

def seed_data():
    if not Pet.query.first():
        pets = [
            Pet(name="Noodle", age="Adult", breed="Affenpinscher", distance="1 mile", image_url="https://example.com/noodle.jpg"),
            Pet(name="Qiqi", age="Puppy", breed="Husky", distance="1 mile", image_url="https://example.com/qiqi.jpg"),
            Pet(name="Buddy", age="Young", breed="Labrador", distance="2 miles", image_url="https://example.com/buddy.jpg"),
        ]
        db.session.add_all(pets)
        db.session.commit()

with app.app_context():
    db.create_all()  # Now, both Pet and Cart exist when this runs
    seed_data()

@app.route('/add_to_cart/<int:pet_id>', methods=['POST'])
@login_required
def add_to_cart(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if pet is already in the cart
    existing_item = Cart.query.filter_by(user_id=current_user.id, pet_id=pet_id).first()
    if existing_item:
        flash('This pet is already in your cart!', 'warning')
        return redirect(url_for('dogs'))

    new_cart_item = Cart(user_id=current_user.id, pet_id=pet.id)
    db.session.add(new_cart_item)
    db.session.commit()
    
    flash(f'{pet.name} added to your cart!', 'success')
    return redirect(url_for('dogs'))

@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    item = Cart.query.get_or_404(cart_id)
    
    if item.user_id != current_user.id:
        flash("You can't remove this item!", 'danger')
        return redirect(url_for('cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'success')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
