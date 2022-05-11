from app_service.app import DBMS


def get_persons_total_count():
    query = "SELECT COUNT(*) FROM persons"
    result = DBMS.execute_query(query)
    return {
        'count': result.first()[0]
    }


def get_persons_filtered_by_age_email_provider(age, email_provider):
    query = 'SELECT COUNT(*) FROM persons WHERE age_range_end > \'%d\' AND email_provider = \'%s\'' % (age, email_provider.lower())
    result = DBMS.execute_query(query)
    return {
        "count": result.first()[0]
    }


def get_percentage_of_country_by_email_provider(country, email_provider):
    query = \
        'SELECT\
            CAST(COUNT(*) AS FLOAT) / (SELECT CAST(COUNT(*) AS FLOAT) FROM persons) * 100\
         FROM\
            persons\
        WHERE\
            country = \'%s\' AND email_provider = \'%s\'' % (country, email_provider.lower())

    result = DBMS.execute_query(query)
    return {
        "percentage": result.first()[0]
    }


def get_top_countries_by_email_provider(top_n, email_provider):
    query = \
        'SELECT\
            country, count(*)\
        FROM\
            persons\
        WHERE\
            email_provider = \'%s\'\
        GROUP BY\
            country, email_provider\
        ORDER BY\
            count(*) DESC\
        LIMIT \'%d\'' % (email_provider.lower(), top_n)

    result = DBMS.execute_query(query)
    response = {}
    for item in result:
        response[item[0]] = item[1]

    return response

def serialize_persons_obj(person):
    person_dict = dict()

    person_dict["first_name"] = person.first_name
    person_dict["last_name"] = person.last_name
    person_dict["gender"] = person.gender
    person_dict["email"] = person.email
    person_dict["phone_number"] = person.phone_number
    person_dict["country"] = person.country
    person_dict["city"] = person.city
    person_dict["county_code"] = person.county_code
    person_dict["street"] = person.street
    person_dict["building_number"] = person.building_number
    person_dict["lat"] = person.lat
    person_dict["long"] = person.long
    person_dict["zip_code"] = person.zip_code
    person_dict["age_range_start"] = person.age_range_start
    person_dict["age_range_end"] = person.age_range_end
    person_dict["email_provider"] = person.email_provider
    person_dict["created_at"] = person.created_at.strftime('%Y/%m/%d')
    person_dict["updated_at"] = person.updated_at.strftime('%Y/%m/%d')

    return person_dict

