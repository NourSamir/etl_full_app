import math
from app_service.api_base import *
from app_service.utils import *


# http://127.0.0.1:5000/persons/total_count
@app.route("/persons/total_count", methods=['GET'])
def get_total_count():
	response = get_persons_total_count()
	return jsonify(
		response
	)


# http://127.0.0.1:5000/persons/filterByAgeAndEmailProvider?age=60&email_provider=gmail.com
@app.route("/persons/filterByAgeAndEmailProvider", methods=['GET'])
def get_count_age_by_email_provider():
	args = request.args
	age = int(args.get("age", 60))
	email_provider = args.get("email_provider", "gmail.com")
	response = get_persons_filtered_by_age_email_provider(age, email_provider)
	return jsonify(
		response
	)


# http://127.0.0.1:5000/persons/percentageCountryAndEmailProvider?country=Germany&email_provider=gmail.com
@app.route("/persons/percentageCountryAndEmailProvider", methods=['GET'])
def get_percentage():
	args = request.args
	country = args.get("country", "Germany")
	email_provider = args.get("email_provider", "gmail.com")

	response = get_percentage_of_country_by_email_provider(country, email_provider)
	return jsonify(
		response
	)


# http://127.0.0.1:5000/persons/topCountriesByEmailProvider?top_n=3&email_provider=gmail.com
@app.route("/persons/topCountriesByEmailProvider", methods=['GET'])
def get_top_countries():
	args = request.args
	top_n = int(args.get("top_n", 3))
	email_provider = args.get("email_provider", "gmail.com")

	response = get_top_countries_by_email_provider(top_n, email_provider)

	return jsonify(
		response
	)


# http://127.0.0.1:5000/report
@app.route("/report", methods=['GET'])
def get_full_report():
	total_count = get_persons_total_count()['count']
	age_per_email_provider = get_persons_filtered_by_age_email_provider(60, 'gmail.com')['count']
	percentage = get_percentage_of_country_by_email_provider('Germany', 'gmail.com')['percentage']
	top_countries = get_top_countries_by_email_provider(3, 'gmail.com')

	return jsonify(
		{
			"totalUsersCount": total_count,
			"GmailUsersOverSixty": age_per_email_provider,
			"GmailUsersPercentageInGermany": percentage,
			"GmailTopThreeCountries": top_countries
		}
	)

# http://127.0.0.1:5000/persons?pageNo=4&pageSize=30
@app.route("/persons", methods=['Get'])
def get_persons_data():
	args = request.args
	page_num = int(args.get('pageNo', 1))
	page_size = int(args.get('pageSize', 10))
	with_masking = False if args.get('authorized', "").lower() == 'true' else True
	
	offset = ((page_num - 1) * page_size)
	pages_count, next_page_url, prev_page_url = 0, None, None

	persons_data_generator = DBMS.get_data_generator()
	all_data_count = persons_data_generator.count()

	if page_size != 0 and all_data_count != 0:
		pages_count = math.ceil(all_data_count / page_size)

		if page_num > pages_count or page_num < 1:
			return make_response("Page Not Found", 404)

		if page_num < pages_count:
			next_page_url = f"{request.url_root}{request.path[1:]}?pageNo={page_num + 1}&pageSize={page_size}&authorized={not with_masking}"
		if page_num > 1:
			prev_page_url = f"{request.url_root}{request.path[1:]}?pageNo={page_num - 1}&pageSize={page_size}&authorized={not with_masking}"

	
	data = persons_data_generator.offset(offset).limit(page_size).all()
	serialized_data = list(map(lambda row: serialize_persons_obj(row, with_masking), data))

	response = {
		"data": serialized_data,
		"pagesCount": pages_count,
		"dataCount": len(serialized_data),
		"totalPersonsCount": all_data_count,
		"nextPageURL": next_page_url,
		"prevPageURL": prev_page_url,
	}

	return jsonify(
		response
	)

