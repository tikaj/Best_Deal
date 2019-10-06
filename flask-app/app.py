from flask import Flask, render_template, request
import sqlalchemy
import os

app = Flask(__name__)


def get_sql_engine():
    server = os.environ.get('REDSHIFT_SERVER_URL')
    user = os.environ.get('REDSHIFT_USER')
    password = os.environ.get('REDSHIFT_PASSWORD')
    database_name = os.environ.get('REDSHIFT_DATABASE')
    port = 5439
    connection = 'postgresql://%s:%s@%s:%s/%s' % (user, password, server, port, database_name)
    sql_engine = sqlalchemy.create_engine(connection)
    return sql_engine


@app.route('/', methods=['GET', 'POST'])
def home():
    cities = [
        'Antwerp', 'Athens', 'Barcelona', 'Berlin',
        'Bologna', 'Bordeaux', 'Bristol', 'Brussels',
        'Copenhagen', 'Crete', 'Dublin', 'Edinburgh',
        'Florence', 'Geneva', 'Girona', 'London', 'Lyon', 'Madrid',
        'Malaga', 'Mallorca', 'Menorca', 'Milan', 'Naples', 'Paris',
        'Puglia', 'Rome', 'Sicily', 'Tasmania', 'Vienna'
    ]

    # ignored cities:
    #   'asheville', 'barossa - valley', 'greater - manchester',
    #   'barwon - south - west - vic', 'bergamo',
    #   'northern - rivers', 'melbourne',
    #   'euskadi', 'ghent',

    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
              'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
              'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    city_price_timeline_dashboard = None
    cheapest_city_for_month = None

    if request.method == 'POST':
        if 'selected_city' in request.form:
            city = request.form['selected_city']
            app.logger.info('selected city is: %s' % city)
            city_price_timeline_dashboard = get_city_price_timeline_dashboard(city)
        if 'month' in request.form:
            month = request.form['month']
            app.logger.info('selected month is %s' % month)
            month_id = months[month]
            cheapest_city_for_month = get_cheapest_city_for_month(month_id)

    return render_template(
        'index.html',
        cities=cities,
        months=months.keys(),
        city_price_timeline_dashboard=city_price_timeline_dashboard,
        cheapest_city_for_month=cheapest_city_for_month
    )


def get_city_price_timeline_dashboard(city):
    query = '''
       SELECT 
         month,
         ROUND(median_price, 1)
       FROM (
         SELECT
           month,
           MEDIAN(price) as median_price
         FROM calendar_listing
         WHERE city = LOWER('%s')
         GROUP by 1
         ORDER by 1
       );
    ''' % city
    res = get_sql_engine().execute(query)
    return list(res)


def get_cheapest_city_for_month(month_id):
    query = '''
       SELECT top 10
         city,
         ROUND(median_price, 1)
       FROM (
         SELECT
           city,
           median(price) AS median_price
         FROM calendar_listing
         WHERE month = '%s'
         GROUP by 1
         ORDER by 2
       );
    ''' % month_id
    res = get_sql_engine().execute(query)
    return list(res)
