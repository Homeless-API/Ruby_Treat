from flask import Blueprint, render_template, redirect, url_for, flash, request
import time, random

payout_bp = Blueprint('payout', __name__)

@payout_bp.route('/payout', methods=['GET'])
def show_payout():
    return render_template('payout.html')

@payout_bp.route('/process_payment', methods=['POST'])
def process_payment():
    card_number = request.form.get('card_number')
    expiration_date = request.form.get('expiration_date')
    cvv = request.form.get('cvv')

    # Simulate payment processing
    if validate_payment(card_number, expiration_date, cvv):
        flash('Payment successful! Your order has been placed.')
    else:
        flash('Payment failed. Please check your payment information and try again.')

    return redirect(url_for('orders.orders'))

def validate_payment(card_number, expiration_date, cvv):
    # Simulate payment processing delay
    time.sleep(2)

    # Simulate random success/failure of payment processing
    success = random.choice([True, False])
    return success
#test