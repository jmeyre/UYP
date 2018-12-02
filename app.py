from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '2d7596cbe025473acb2bb5d8f268f5a5'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {0}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Incorrect username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
