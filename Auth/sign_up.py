from flask import Flask, Blueprint, request, render_template, redirect, url_for, session
from Validation.validation import SignupSchema
from Data.savedata import connect_to_postgres
import string
import random
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

signup_bp = Blueprint("sign_up", __name__)

def generate_userid():
    characters = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(characters) for _ in range(12))
    return user_id

@signup_bp.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    error = None

    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            dob = request.form.get('dob')
            gender = request.form.get('gender')
            user_type = request.form.get('user_type')
            user_id = str(uuid.uuid4())  # Generates a valid UUID string


            # Sanitize inputs
            username = username.strip()
            email = email.strip()  # Assuming email needs sanitation too

            data = request.form.to_dict()

            errors = SignupSchema().validate(data)
            if errors:
                error = {'validation_error': errors}
            else:
                # Connect to the PostgreSQL database using DATABASE_URL
                db_connection, cursor = connect_to_postgres("rubytreatdb", "users")


                if db_connection and cursor:
                    # Check if the username already exists
                    existing_username_query = "SELECT COUNT(*) FROM users WHERE username = %s"
                    cursor.execute(existing_username_query, (username,))
                    existing_username_count = cursor.fetchone()[0]

                    if existing_username_count > 0:
                        error = {'username_error': 'Username already exists. Choose another username.'}
                    else:
                        # Insert user information into the specified table
                        cursor.execute(""" 
                            INSERT INTO users (username, password, email, dob, gender, user_type, user_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (username, password, email, dob, gender, user_type, user_id))

                        # Commit the transaction and close the connection
                        db_connection.commit()

                        # Store user_id in the session
                        session['user_id'] = user_id

                        # Redirect to login page
                        return redirect(url_for('login.login'))
                else:
                    error = {'db_error': 'Saving into the database failed. Try again later.'}

    except ValueError as ve:
        error = {'input_error': str(ve)}
    except Exception as ex:
        print('Error:', ex)
        error = {'system_error': 'System code failure. Try again.'}

    return render_template('signup.html', error=error)

# Register the blueprint with the Flask app
app.register_blueprint(signup_bp)

if __name__ == "__main__":
    app.run(debug=True)
