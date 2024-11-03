from marshmallow import Schema, fields, validate
from datetime import datetime

def validate_age(dob):
    current_year = datetime.now().date()

    age = current_year.year - dob.year - ((current_year.month, current_year.day) < (dob.month, dob.day))

    if not (13 <= age <= 150):
        raise validate.ValidationError("Age not valid")

class SignupSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=40),
        error_messages={"required": "Username is required.",
                        "length": "Username must be between 5 and 40 characters."}
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=40),
        error_messages={"required": "Password is required.",
                        "length": "Password must be between 5 and 40 characters."}
    )
    email = fields.Email(required=True, error_messages={"required": "Email is required."})

    dob = fields.Date(
        required=True,
        format="%Y-%m-%d",
        validate=[validate_age],
        error_messages={"required": "Date of Birth is required.",
                        "format": "Date of Birth must be in the format YYYY-MM-DD"})
    
    gender = fields.Str(required=True, 
                        validate=validate.OneOf(["Male", "Female", "Child pre..."]),
                        error_messages={"required": "Gender is required."})
    
    user_type = fields.Str(required=True, 
                        validate=validate.OneOf(["Customer", "Admin"]),
                        error_messages={"required": "user type is required."})


