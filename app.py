"""Flask app.

This module contains the code for flask app.
"""
from flask import Flask, render_template, request
from flask_cors import cross_origin
from database import DataBase
from logger import AppLogger
from review_parser import ReviewParser
from read_config import read_config
from generate_config import CONFIG_FILE, DATABASE, HOST, USERNAME, PASSWORD

app = Flask(__name__)

app_log = AppLogger().get_logger(name="app_log")


@cross_origin()
@app.route("/", methods=["GET", "POST"])
def homepage():
    """Render homepage."""
    return render_template("index.html")


@app.route("/scrap", methods=["POST"])
def scrap():
    """Scraps the reiews and sends back html response."""
    if request.method == "POST":
        search = str(request.form["search_content"].replace(" ", "+"))
        app_log.debug("Searching for %s", search)
        try:
            review_parser_obj = ReviewParser()
            database_obj = DataBase()
            config = read_config(CONFIG_FILE)
            host = config[DATABASE][HOST]
            user_name = config[DATABASE][USERNAME]
            password = config[DATABASE][PASSWORD]
            database_obj.db_connect(host=host, user=user_name, passwd=password)
            reviews = review_parser_obj.fetch_all_reviews(
                product_to_search=search, database=database_obj
            )
            pie_chart = review_parser_obj.get_pie_chart()
            database_obj.close_db()

            review_dict = []
            for review in reviews:
                review_dict.append(
                    {
                        "Product": search.replace("+", " "),
                        "Name": review[0],
                        "Rating": review[1],
                        "CommentHead": review[2],
                        "Comment": review[3],
                    }
                )

            return render_template(
                "result.html",
                reviews=review_dict,
                pie_chart=pie_chart,
                total_reviews_=len(reviews),
            )

        except Exception as scrap_exception:
            app_log.exception(scrap_exception)
            return "<h1>Sorry! Something Went Wrong !</h1>"


if __name__ == "__main__":
    app.run(debug=False)
