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

def serialize_persons_obj(person_obj, with_masking=True, mask_len=4):
    person_dict = dict()

    person_dict["first_name"] = person_obj.first_name
    person_dict["last_name"] = person_obj.last_name
    person_dict["gender"] = person_obj.gender
    person_dict["email"] = person_obj.email
    person_dict["phone_number"] = person_obj.phone_number
    person_dict["country"] = person_obj.country
    person_dict["city"] = person_obj.city
    person_dict["county_code"] = person_obj.county_code
    person_dict["street"] = person_obj.street
    person_dict["building_number"] = person_obj.building_number
    person_dict["lat"] = person_obj.lat
    person_dict["long"] = person_obj.long
    person_dict["zip_code"] = person_obj.zip_code
    person_dict["age_range_start"] = person_obj.age_range_start
    person_dict["age_range_end"] = person_obj.age_range_end
    person_dict["email_provider"] = person_obj.email_provider
    person_dict["created_at"] = person_obj.created_at.strftime('%Y/%m/%d')
    person_dict["updated_at"] = person_obj.updated_at.strftime('%Y/%m/%d')

    if with_masking:
        return mask(person_dict, mask_len)

    return person_dict



def mask(serialized_person_dict, mask_len):
    person_identifications = [
        'first_name', 'last_name', 'phone_number', 'email', 
        'country', 'city', 'county_code', 'street', 'building_number', 'zip_code'
    ]

    # Discard the email_provider to apply the masking on the email itself
    serialized_person_dict['email'] = serialized_person_dict['email'].split('@')[0]

    for identifier in person_identifications:
        identifier_val = serialized_person_dict[identifier]
        if len(identifier_val) > mask_len:
            identifier_val_part_1 = identifier_val[0: len(identifier_val) - mask_len]
            identifier_val_part_2 = "X" * mask_len
            serialized_person_dict[identifier] = identifier_val_part_1 + identifier_val_part_2
        else:
            serialized_person_dict[identifier] = "X" * len(identifier_val)

    # Restor the email_provider
    serialized_person_dict['email'] = f"{serialized_person_dict['email']}@{serialized_person_dict['email_provider']}"

    return serialized_person_dict