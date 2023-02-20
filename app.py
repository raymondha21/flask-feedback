"""Flask app for Feedback"""

from flask import Flask, request, redirect, render_template, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import AddFeedbackForm, UserRegisterForm, UserLoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thebestsecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar= DebugToolbarExtension(app)


def check_login(redirect="/",msg="You must be logged in to do this!"):
    if "user_id" not in session:
        
        flash(msg)
        return redirect(f"{redirect}")

@app.route('/')
def homepage():
    """User registration redirect"""

    check_login(redirect="/register")

    return redirect(f'/users/{session["user_id"]}')

@app.route('/register',methods=["GET","POST"])
def user_register():
    """Show/handle user registration"""

    form = UserRegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username,password,email,first_name,last_name)
        
        
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.username
        return redirect(f'users/{username}')

    else:
        return render_template('user_register.html',form=form)

@app.route('/login',methods=["GET","POST"])
def user_login():
    """Show/handle user login"""

    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")

        else: 
            form.username.errors = ["Invalid username/password"]

    else:
        return render_template('user_login.html',form=form)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")

@app.route('/users/<username>')
def show_user(username):
    """Show user page"""

    user = User.query.get_or_404(username)

    if "user_id" not in session:
        flash("You must be logged in to view this page!")
        return redirect("/")
    
    else:
        return render_template('user_info.html',user=user)

@app.route('/users/<username>/delete',methods=["POST"])
def delete_user(username):
    """Delete current user"""
    
    user = User.query.get_or_404(username)

    if "user_id" not in session:
        flash("You must be logged in to delete your account!")
        return redirect("/")
    
    else:
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted")
        return redirect("/")

@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def add_feedback(username):
    """Displays form to add feedback"""

    username=username

    check_login(msg = "You must be logged in to add feedback!")

    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title,content=content,username=username)
        
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"users/{username}")

    else:
        return render_template('add_feedback.html',form=form)


@app.route('/feedback/<int:feedback_id>/update',methods=["GET","POST"])
def update_feedback(feedback_id):
    """Update feedback handler"""

    fb = Feedback.query.get_or_404(feedback_id)

    form = AddFeedbackForm(obj=fb)

    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content = form.content.data

        db.session.add(fb)
        db.session.commit()

        return redirect(f"users/{fb.username}")

    else:
        return render_template('update_feedback.html',form=form)

@app.route('/feedback/<int:feedback_id>/delete',methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback"""
    
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username

    check_login()

    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback has been deleted")
    return redirect(f"/users/{username}")