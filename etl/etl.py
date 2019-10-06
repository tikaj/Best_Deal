import sqlalchemy
from source_data import get_data
from jinja2 import Template
import os


def get_sql_engine():
    server = os.environ.get('REDSHIFT_SERVER_URL')
    user = os.environ.get('REDSHIFT_USER')
    password = os.environ.get('REDSHIFT_PASSWORD')
    database_name = os.environ.get('REDSHIFT_DATABASE')
    port = 5439
    connection = 'postgresql://%s:%s@%s:%s/%s' % (user, password, server, port, database_name)
    sql_engine = sqlalchemy.create_engine(connection)
    return sql_engine


def flow():
    sql_engine = get_sql_engine()

    city_infos = get_data.cities_info()
    load_calendar_source = open('load_calendar.sql').read()
    load_calendar_template = Template(load_calendar_source)

    load_listings_source = open('load_listings.sql').read()
    load_listings_template = Template(load_listings_source)

    join_query = open('join.sql').read()

    for city, case in city_infos.items():
        for date in case[1]:
            print('processing %s for %s' % (city, date))

            # load calendar
            load_calendar_query = load_calendar_template.render(
                city=city, date=date)
            sql_engine.execute(load_calendar_query)

            # load listings
            load_listings_query = load_listings_template.render(
                 city=city, date=date)
            sql_engine.execute(load_listings_query)

    # join
    sql_engine.execute(join_query)


if __name__ == '__main__':
    flow()

