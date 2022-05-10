from db_connector.utils import session
from db_connector.models import Persons, create_db_tables


class Manager:
    def __init__(self):
        create_db_tables()

    def insert_person(self, person_data_dict):
        # Un-back a python dict to sqlalchemy table row
        person = Persons(**person_data_dict)
        try:
            session.add(person)
            session.commit()
        except Exception as e:
            session.rollback()

    def insert_persons_bulk(self, persons_data_list):
        try:
            session.bulk_insert_mappings(
                mapper=Persons,
                mappings=persons_data_list,
                return_defaults=False,
                render_nulls=False
            )
            session.commit()
        except Exception as e:
            session.rollback()

    def execute_query(self, query_txt):
        try:
            result = session.execute(query_txt)
            return result
        except Exception as e:
            session.rollback()

    def get_data_generator(self):
        try:
            data_generator = session.query(Persons)
            return data_generator
        except Exception as e:
            session.rollback()

    def __del__(self):
        pass
        # session.close()
