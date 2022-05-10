import requests
from logging_utility import logger
from db_connector.manager import Manager
from persons_data_etl.configs import *
from persons_data_etl.utils import map_person_object, retry


class ETL:
    def __init__(self):
        self.DBMS = Manager()

    @retry(num_of_retries=RETRIES_NUM, delay_time=DELAY_TIME, with_logging=LOGGING)
    def extract(self, data_size, batch_size):
        logger.info(msg="[ETL.extract]: Extracting persons data from FakerAPI")
        # Construct the url for FakerAPI
        url = f'{API_BASE_URL}/{API_VERSION}/{API_RESOURCE}'
        # Adjust the _quantity parameter according to the new batch_size instead of the default 1k
        PARAMETERS['_quantity'] = batch_size
        # Calculate the total number of data batches to be obtained
        data_batches_total_num = round(data_size / batch_size)
        # Fetch the data for all batches
        for batch_idx in range(data_batches_total_num):
            logger.info(msg=f'[ETL.extract]: Fetching the {batch_idx + 1} persons data batch')
            response = requests.request(HTTP_METHOD, url, headers=HEADERS, params=PARAMETERS)
            if response.status_code > 201:
                logger.info(msg=f'[ETL.extract]: Request error with code - {response.status_code}')
                logger.info(msg=f'[ETL.extract]: Error message - {response.text}')
                yield {}

            yield response.json()['data']

    @retry(num_of_retries=RETRIES_NUM, delay_time=DELAY_TIME, with_logging=LOGGING)
    def transform(self, persons_raw_data):
        logger.info(msg=f'[ETL.transform]: Transforming a batch of persons data with size = {len(persons_raw_data)}')
        persons_transformed_data = list(map(lambda person: map_person_object(person), persons_raw_data))
        return persons_transformed_data

    @retry(num_of_retries=RETRIES_NUM, delay_time=DELAY_TIME, with_logging=LOGGING)
    def load(self, persons_transformed_data):
        logger.info(f'[ETL.load]: Loading a batch of persons data with size = {len(persons_transformed_data)}')
        self.DBMS.insert_persons_bulk(persons_transformed_data)

    # @retry(num_of_retries=5, delay_time=5, with_logging=True)
    def run(self, data_size, batch_size, retries, delay, logging):
        RETRIES_NUM = retries
        DELAY_TIME = delay
        LOGGING = logging
        raw_data = self.extract(data_size, batch_size)
        for data_batch in raw_data:
            transformed_data_batch = self.transform(data_batch)
            self.load(transformed_data_batch)
