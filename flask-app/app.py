from flask import Flask, render_template, request, send_from_directory
import sqlalchemy
import os

app = Flask(__name__)

month_name_to_id = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}


def get_sql_engine():
    server = os.environ.get('REDSHIFT_SERVER_URL')
    user = os.environ.get('REDSHIFT_USER')
    password = os.environ.get('REDSHIFT_PASSWORD')
    database_name = os.environ.get('REDSHIFT_DATABASE')
    port = 5439
    connection = 'postgresql://%s:%s@%s:%s/%s' % (user, password, server, port, database_name)
    sql_engine = sqlalchemy.create_engine(connection)
    return sql_engine


@app.route('/.well-known/pki-validation/<path:path>')
def send_static(path):
    return send_from_directory('.well-known/pki-validation', path)


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

    selected_month = None
    selected_city = None
    selected_bedrooms = None
    selected_bathrooms = None

    if request.method == 'POST':
        if 'selected_city' in request.form:
            selected_city = request.form['selected_city']
            app.logger.info('selected city is: %s' % selected_city)
            city_price_timeline_dashboard = get_city_price_timeline_dashboard(selected_city)
        if 'month' in request.form:
            selected_month = request.form['month']
            app.logger.info('selected month is %s' % selected_month)
            month_id = months[selected_month]
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
        selected_city=selected_city,
        selected_bedrooms=selected_bedrooms,
        selected_bathrooms=selected_bathrooms,
        selected_month=selected_month,
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
           MEDIAN(price) AS median_price
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
    WHERE city=LOWER('%s') AND bathrooms='%s' AND bedrooms='%s'
    GROUP BY 1
    ORDER BY 1;
    ''' % (city, bathrooms, bedrooms)
    app.logger.info(query)
    res = get_sql_engine().execute(query)
    return [(month_name_to_id[row[0]], row[1]) for row in res]


if __name__ == "__main__":
    if os.environ.get('TEST_ENV'):
        app.run(host="localhost", port=8888, debug=True)
    else:
        '''on production server, actual certificate is used'''
        app.run(host="0.0.0.0", port=443, ssl_context=('www_datamaster_dev.crt', 'private-key.pem'))
