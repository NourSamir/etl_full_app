import time
from logging_utility import logger
from datetime import datetime
from functools import wraps


def map_person_object(person_obj):
    transformed_person = dict()

    transformed_person["first_name"] = person_obj.get("firstname", "")
    transformed_person["last_name"] = person_obj.get("lastname", "")
    transformed_person["gender"] = person_obj.get("gender", "")
    transformed_person["email"] = person_obj.get("email", "")
    transformed_person["phone_number"] = person_obj.get("phone", "")
    transformed_person["country"] = person_obj.get("address", {}).get("country", "")
    transformed_person["city"] = person_obj.get("address", {}).get("city", "")
    transformed_person["county_code"] = person_obj.get("address", {}).get("county_code", "")
    transformed_person["street"] = person_obj.get("address", {}).get("streetName", "")
    transformed_person["building_number"] = person_obj.get("address", {}).get("buildingNumber", "")
    transformed_person["lat"] = person_obj.get("address", {}).get("latitude", "")
    transformed_person["long"] = person_obj.get("address", {}).get("longitude", "")
    transformed_person["zip_code"] = person_obj.get("address", {}).get("zipcode", "")

    age_range_start, age_range_end = calculate_age_range(person_obj.get("birthday", ""))
    transformed_person["age_range_start"] = age_range_start
    transformed_person["age_range_end"] = age_range_end

    if len(person_obj.get("email", "")) != 0:
        transformed_person["email_provider"] = person_obj.get("email").split('@')[1]
    else:
        transformed_person["email_provider"] = ""

    return transformed_person


def calculate_age_range(date_str):
    if len(date_str) == 0:
        return ""

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    birth_year = date_obj.year
    current_year = datetime.now().year
    age_range_start = ((current_year - birth_year) // 10) * 10
    age_range_end = age_range_start + 10

    return age_range_start, age_range_end


def retry(num_of_retries=5, delay_time=5, with_logging=False):
    def retry_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = num_of_retries
            delay = delay_time
            while retries > 1:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    msg = f"{e.__doc__} {str(e)}, Retrying in {delay} seconds..."
                    if with_logging:
                        logger.error(msg)
                    else:
                        print(msg)
                    time.sleep(delay)
                    retries -= 1

            return func(*args, **kwargs)
        return wrapper
    return retry_decorator


