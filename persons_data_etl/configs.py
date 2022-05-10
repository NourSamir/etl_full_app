# region Faker Data API Configs

API_BASE_URL = "https://fakerapi.it/api"

API_VERSION = "v1"

API_RESOURCE = "persons"

HTTP_METHOD = "GET"

HEADERS = {
    'cache-control': "no-cache",
    'Content-type': "application/json; charset=UTF-8",
}

PARAMETERS = {
    "_quantity": 0,
    "_birthday_start": "1940-01-01"
}

# endregion

# region Retry Policy Configs

RETRIES_NUM = 0
DELAY_TIME = 0
LOGGING = True

# endregion