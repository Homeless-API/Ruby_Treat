from flask import Flask, render_template, session, redirect, url_for
from Auth.sign_up import signup_bp
from Auth.login import login_bp
from orders import orders_bp
from Admin_control import control_bp
from payout import payout_bp

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'null'
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(control_bp)
app.register_blueprint(payout_bp)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/Jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/main/<username>')
def main():
    if 'user_id' in session:
        user_id = session[user_id]
        return render_template('main.html')
    else:
        return redirect('/sign-up')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    # Use socketio.run instead of app.run
    app.run(debug=True, port=5020)
    