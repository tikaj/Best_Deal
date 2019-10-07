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

    bathrooms = ['0', '0.5', '1.0', '1.5', '2.0', '2.5',
                 '3.0', '3.5', '4.0', '5.0', '8.0']

    bedrooms = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

    city_price_timeline_dashboard = None
    cheapest_city_for_month = None
    test_dashboard = None

    app.logger.info('--------')
    app.logger.info(request.form)
    app.logger.info('--------')
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
        if 'city' in request.form and 'bathrooms' in request.form and 'bedrooms' in request.form:
            selected_city = request.form['city']
            selected_bathrooms = request.form['bathrooms']
            selected_bedrooms = request.form['bedrooms']
            app.logger.info('selected city is: %s' % selected_city)
            app.logger.info('selected bathrooms is: %s' % selected_bathrooms)
            app.logger.info('selected bedrooms is: %s' % selected_bedrooms)
            test_dashboard = get_cheapest_city_bath_bed(selected_city, selected_bathrooms, selected_bedrooms)
            app.logger.info(test_dashboard)

    return render_template(
        'index.html',
        cities=cities,
        months=months.keys(),
        bathrooms=bathrooms,
        bedrooms=bedrooms,
        city_price_timeline_dashboard=city_price_timeline_dashboard,
        cheapest_city_for_month=cheapest_city_for_month,
        test_dashboard=test_dashboard
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


def get_cheapest_city_bath_bed(city, bathrooms, bedrooms):
    query = '''
    SELECT month, median(price)::int
    FROM calendar_listing
    WHERE city=LOWER('%s') and bathrooms='%s' and bedrooms='%s'
    group by 1
    ORDER BY 1;
    ''' % (city, bathrooms, bedrooms)
    app.logger.info(query)
    res = get_sql_engine().execute(query)
    return list(res)
