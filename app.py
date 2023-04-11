from flask import Flask, render_template, request, flash
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SOMETHINGHARDTOGUESS!'

class Currency:

    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag

    def __repr__(self):
        return '<Currency {}>'.format(self.code)

class CantorOffer:

    def __init__(self):
        self.currencies = []
        self.denied_codes = []
        self.load_offer()


    def load_offer(self):
        self.currencies.append(Currency('JPY', 'Yen', 'japan_flag.png'))
        self.currencies.append(Currency('GBP', 'Pound', 'england_flag.jpg'))
        self.currencies.append(Currency('EUR', 'Euro', 'europe_flag.png'))
        self.currencies.append(Currency('USD', 'Dollar', 'usa_flag.png'))
        self.denied_codes.append('USD')

    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return Currency('unknown', 'unknown', 'pirate_flag.png')

class Hotel:
    def __init__(self, room_number, guest_name, notification_from_guest):
        self.room_number = room_number
        self.guest_name = guest_name
        self.notification_from_guest = notification_from_guest

    def __repr__(self):
        return f'<Hotel {self.room_number}>'

class PriorityType:
    def __init__(self, code, description, selected):
        self.code = code
        self.description = description
        self.selected = selected

class NotificationPriorities:
    def __init__(self):
        self.list_of_priorities = []
        self.load_priorities()

    def load_priorities(self):
        self.list_of_priorities.append(PriorityType('high','HIGH PRIORITY', False))
        self.list_of_priorities.append(PriorityType('medium','MEDIUM', False))
        self.list_of_priorities.append(PriorityType('normal', 'NOT URGENT', True))

    def get_priority_by_code(self, code):
        for priority in self.list_of_priorities:
            if code == priority.code:
                return priority
        return None

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():

    offer = CantorOffer()

    if request.method == 'GET':
        return render_template('exchange.html', offer=offer)

    else:
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        if currency in offer.denied_codes:
            flash(f'The currency {currency} cannot be accepted')
        elif offer.get_by_code(currency) == 'unknown':
            flash('The selected currency is unknown and cannot be accepted')
        else:
            flash(f'Request to exchange {currency} was accepted.')


        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        # print(offer.currencies)
        # print()
        # print(offer.get_by_code(currency))
        # print()
        # print(currency)
        return render_template('exchange_result.html', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))

@app.route('/hotel', methods=['GET', 'POST'])
def hotel():

    notifications = NotificationPriorities()

    if request.method == 'GET':
        return render_template('hotel.html', notifications=notifications)

    else:
        room_number = 0
        if 'room_number' in request.form:
            room_number = request.form['room_number']

        guest_name = 'Kowalski'
        if 'guest_name' in request.form:
            guest_name = request.form['guest_name']

        notification_from_guest = 'Everything is fine'
        if 'notification_from_guest' in request.form:
            notification_from_guest = request.form['notification_from_guest']

        priority = 'normal'
        if 'priority' in request.form:
            priority = request.form['priority']

        the_hour = datetime.now().hour

        raise_priority = (the_hour >= 20 or the_hour < 6) and priority == 'medium'

        if raise_priority:
            priority = 'high'
            flash('Rising priority from medium to high')

        #flash("Notification has been sent")

    return render_template('hotel_result.html', room_number=room_number, guest_name=guest_name,
                           notification_from_guest=notification_from_guest, priority=priority, notification_info=notifications.get_priority_by_code(priority))
