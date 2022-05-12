## ETL Full Application
This project implements an ETL to extract the persons data from the public FakerAPI,
Transform this data in terms of cleaning, mapping, pasing and generalization and loads
this data into Sqlite DB.
On the other side that project implements a web application (REST APIs) on top of our data to manipulate it
in terms of getting some metrics and stats, display the data to our users and implement a report to help 
our users get more insights about their data.<br /> <br /> 
**Note**:- As long as the poject is well structured, readable, parametrized and configurable hence we can consider it 
as a general purpose project that could be easily adjusted to fit any other technical or even business needs

## Project Structure
The project contains three main modules (app_service, db_connector, persons_data_etl) and some individuals files<br />
- **db_connector**:- This module is responsible for initiating a DB session on demand and implements an interface to handle
whatever needed, You can adjust the configs file to connect to any other DBMS rather than Sqlite.
- **persons_data_etl**:- This module is responsible for implementing the ETL to fetch the data from the FakerAPI persons data (https://fakerapi.it/en), transforming this data and loading it to the destination DBMS.
- **app_service**:- This module implements the web app (REST APIs) on top the destination DB.
- **Other Files**:- Files responsible for building the docker image, setup the internal python package, etc ...

## Setup And Installation
Befor following the steps below let's explain what will happen during the installation.<br />
While building the docker image the project dependencies in the **requirements.txt** will be installed
and the **data_etl_full_app** python package will be installed inside the image, This python package exposes some CLI
commands (run_persons_data_etl, run_app_service) that can be used to help us running the ETL and the web application. 
- Pull the project source code
    ``` console
    foo@bar:~$ git clone git@github.com:NourSamir/etl_full_app.git
    ```
- Inside the project directory run the following command to build the **taxfix_data_app** docker image,
You can change the image name from the build command inside the **build_image.sh** file.
    ```console
    foo@bar:~$ sh build_image.sh
    ```
- Run the following command to check the existence of the docker image
    ```console
    foo@bar:-$ docker images 
    ```
- Inside the project directory run the following command to spin-up the **data_etl_app** container, you can change
the container name from inside the **run_container.sh** file. The container will be running in the background.

    ```console
    foo@bar:-$ sh run_container.sh
    ```
- Run the following command to check the existence of the container
    ```console
    foo@bar:-$ docker ps -a
    ```
## Run Services
As mentioned above the project aims to implement an ETL and a web applicaiton on top of the destination DB hence we will explain
how to use the project to run the web app service and run the ETL on demand at the same time.
- Run the following command to run the app service, A development server will be initiated and listens to your request on port **5000** (Will be discussed later under the API Endpoints section).
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_app_service
    ```
- Copy paste the following URL in your browser to make sure that the app service is up and running, Must see the **Welcome** message.
  - http://127.0.0.1:5000
- Run the following command to run the ETL, The run command accepts a predefined set of parameters (**data_size, batch_size, retries, delay, logging**)
to help us control some interesting stuff such as the total amount of required data, get data in batches according to bacth size, number of retries on ETL failure, etc ... (Will be discussed under the ETL section)
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_persons_data_etl
    ```
## Database Model
You will find the **db.sqlite** database file created. The database has only the **persons** table,
Check the **models.py** file inside the **db_connector** sub-folder.

## ETL Usage
The ETL is defined by a set of parameters such that these parameters control the ETL run. These parameters are optional and you don't have
to pass it to the **run_persons_data_etl** CLI command because these parameters have defaults. You can run this command many times as you need,
also you can set a schedule to run this command or even deploy the package to any scheduler from your choice such as Airflow for examaple.<br />
The ETL extracts the data from the public FakerAPI, Trnasforms 
**Parameters**:-
- **data_size**:- Total amount of data  to be extracted, Default = 1000
- **batch_size**:- Because of the APIs maximum limit we need to tell the ETL to get the data in batches, Dfault = 100
- **retries**:- The number of ETL run attempts on failure
- **delay**:- Time to wait till the next ETL run, Default = 5 seconds
- **logging**:- Enable or disable the ETL run logging, Default = True <br />

**Examples**:-
- Run the help command to see the help and documentation of the run_persons_data_api command
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_persons_data_etl --help
    ```
- Run the ETL
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_persons_data_etl --data_size 10000 --batch_size 1000 --retries 3 --delay 10
    ```
## APP Service Usage
The App service aims to implement a set of REST APIs on top of the destination DB to get some metrics and KPIs out of the 
persisted data by the ETL. Mainly you will find **6** endpoint described as following.
- **/persons**:- This endpoint enables you of getting the data according to a pagination and masking parameters.
    - Parameters:
        - pageNo:- Integer, Default = 1
        - pageSize:- Integer, Default = 10
        - authorized:- Boolean, Default = True
        - mask_len:- Integer, Default = 4
    - Request: http://127.0.0.1:5000/persons?pageNo=1&pageSize=5&authorized=false
    - Response:
        ```json
        {
          "data": [
            {
              "age_range_end": 50, 
              "age_range_start": 40, 
              "building_number": "324", 
              "city": "Gutkowskitown", 
              "country": "Kuwait", 
              "county_code": "PY", 
              "created_at": "2022/05/10", 
              "email": "lkling@yahoo.com", 
              "email_provider": "yahoo.com", 
              "first_name": "Trevor", 
              "gender": "male", 
              "last_name": "Rogahn", 
              "lat": 39.527273, 
              "long": -120.079989, 
              "phone_number": "+4843620601938", 
              "street": "Edwina Villages", 
              "updated_at": "2022/05/10", 
              "zip_code": "92943-5362"
            },
            {},
            {},
          ], 
          "dataCount": 5, 
          "nextPageURL": "http://127.0.0.1:5000/persons?pageNo=2&pageSize=5&authorized=false", 
          "pagesCount": 200, 
          "prevPageURL": null, 
          "totalPersonsCount": 1000
        }
        ```
    - Request: http://127.0.0.1:5000/persons?pageNo=1&pageSize=5&authorized=true&mask_len=4
    - Response:
        ```json
        {
          "data": [
            {
              "age_range_end": 80, 
              "age_range_start": 70, 
              "building_number": "XXXX", 
              "city": "MohammadXXXX", 
              "country": "SwXXXX", 
              "county_code": "XX", 
              "created_at": "2022/05/12", 
              "email": "donato.kXXXX@hotmail.com", 
              "email_provider": "hotmail.com", 
              "first_name": "WilXXXX", 
              "gender": "male", 
              "last_name": "HomeXXXX", 
              "lat": -39.915544, 
              "long": 74.507826, 
              "phone_number": "+784564482XXXX", 
              "street": "Wintheiser DrXXXX", 
              "updated_at": "2022/05/12", 
              "zip_code": "7XXXX"
            },
            {},
            {}
          ], 
          "dataCount": 5, 
          "nextPageURL": "http://127.0.0.1:5000/persons?pageNo=2&pageSize=5&authorized=true&mask_len=4", 
          "pagesCount": 200, 
          "prevPageURL": null, 
          "totalPersonsCount": 1000
        }
        ```
- **/persons/total_count**:- Gets the total count of persons in the DB (total number of rows).
    - Parameters: None
    - Request: http://127.0.0.1:5000/persons/total_count
    - Response:
        ```json
        {
          "count": 1000
        }
        ```
- **/persons/filterByAgeAndEmailProvider**:- Get the total count of persons over a given age and use a given email provider.
    - Parameters:
        - age:- Integer, Default = 60
        - email_provider:- String, Default = 'gmail.com'
    - Request: http://127.0.0.1:5000/persons/filterByAgeAndEmailProvider?age=60&email_provider=gmail.com
    - Response:
        ```json
        {
          "count": 61
        }
        ```
- **/persons/percentageCountryAndEmailProvider**:- Get the percentage of users living in a given country and use a given email provider.
    - Parameters:
        - country:- String, Default = 'Germany'
        - email_provider:- String, Default = 'gmail.com'
    - Request: http://127.0.0.1:5000/persons/percentageCountryAndEmailProvider?country=Germany&email_provider=gmail.com
    - Response:
        ```json
        {
          "percentage": 0.1
        }
        ```
- **/persons/topCountriesByEmailProvider**:- Find the top N countries use the given email provider.
    - Parameters:
        - top_n:- Integer, Default = 3
        - email_provider:- String, Default = 'gmail.com'
    - Request: http://127.0.0.1:5000/persons/topCountriesByEmailProvider?top_n=3&email_provider=gmail.com
    - Response:
        ```json
        {
          "China": 4, 
          "Guinea": 3, 
          "Guyana": 3
        }
        ```
- **/report**:- This endpoint gathers up all the metrics described above in a single API call such that it returns all the values with respect to
the default values of each API.
    - Parameters: None
    - Request: http://127.0.0.1:5000/report
    - Response:
        ```json
        {
          "GmailTopThreeCountries": {
            "China": 4, 
            "Guinea": 3, 
            "Guyana": 3
          }, 
          "GmailUsersOverSixty": 61, 
          "GmailUsersPercentageInGermany": 0.1, 
          "totalUsersCount": 1000
        }
        ```
