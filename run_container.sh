# Run a container
# docker run -it -p 5000:5000 -p 5001:5001 -v "$PWD":/app --rm --name data_etl_app taxfix_data_app
docker run -it -d -p 5000:5000 -p 5001:5001 -v "$PWD":/app --name data_etl_app taxfix_data_app

