"""ReviewParser.

This module searches for a product and fetchs all the reviews
associated.
"""
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup as bs
import requests
import plotly
import plotly.graph_objects as go
from logger import AppLogger

# url to search in flipkart
FLIPKART_SEARCH = "https://www.flipkart.com/search?q="

# flipkart main url
FLIPKART = "https://www.flipkart.com"


class ReviewParser:
    """Fetch and parse reviews."""

    def __init__(self) -> None:
        """Intialize required variables."""
        self.__content = "None"
        self.__product_list = []
        self.__name = "name"
        self.__rating = 5
        self.__comment_head = "Super"
        self.__comment = "wonderful product"
        self.__logger_class = AppLogger()
        self.__logger = self.__logger_class.get_logger(name="review_parser")
        self.__all_reviews = []

    def fetch_main_data(self, product_to_search) -> None:
        """Search for a product  on flipkart and get metadata.

        Args:
            product_to_search (str): product to be searched
        """
        client = urlopen(FLIPKART_SEARCH + str(product_to_search))
        self.__content = client.read()
        client.close()

    def parse_data(self) -> None:
        """Parse the html data."""
        parsed_content = bs(self.__content, "html.parser")
        self.__product_list = parsed_content.findAll("div", {"class": "_2kHMtA"})

    def extract_product_review(self, product) -> list:
        """Extract product review.

        Args:
            product : All the data regarding a product

        Returns:
            list: list of required data
        """
        list_data = []
        product_link = product.a["href"]
        self.__logger.debug("opening product link: %s", FLIPKART + product_link)
        prod_res = requests.get(FLIPKART + product_link, timeout=10)
        prod_res_parse = bs(prod_res.text, "html.parser")
        product_reviews = prod_res_parse.findAll("div", {"class": "_16PBlm"})
        for review in product_reviews:
            flag = False
            try:
                self.__name = review.div.div.find_all(
                    "p", {"class": "_2sc7ZR _2V5EHH"}
                )[0].text
            except Exception as name_exception:
                self.__logger.debug(str(name_exception))
                flag = True
            try:
                self.__rating = review.div.div.div.div.text
            except Exception as rating_exception:
                self.__logger.debug(str(rating_exception))
                flag = True
            try:
                self.__comment_head = review.div.div.div.p.text
            except Exception as comm_head_exception:
                self.__logger.debug(str(comm_head_exception))
                flag = True
            try:
                comment_tag = review.div.div.find_all("div", {"class": ""})
                self.__comment = comment_tag[0].div.text
            except Exception as comment_exception:
                self.__logger.debug(str(comment_exception))
                flag = True
            if flag is False:
                list_data.append(
                    [self.__name, self.__rating, self.__comment_head, self.__comment]
                )
        return list_data

    def extract_all_reviews_to_db(self, database) -> None:
        """Extract all reviews to database.

        Args:
            database (DataBase): DataBase object
        """
        self.__all_reviews = []
        for product in self.__product_list:
            reviews = self.extract_product_review(product=product)
            for review in reviews:
                self.__all_reviews.append(review)
                database.add_to_db(review)

    def fetch_all_reviews(self, product_to_search, database) -> list:
        """Extract all the reviews.

        Extracts all the reviews of specified product to given database

        Args:
            product_to_search (str): product to be searched
            database (DataBase): DataBase object
        """
        if database.check_if_table_exists(product_to_search.replace("+", "")) is True:
            reviews = database.get_data(product_to_search.replace("+", ""))
            if reviews is not None and len(reviews) > 0:
                self.__all_reviews = list(reviews)
            else:
                self.fetch_main_data(product_to_search=product_to_search)
                self.parse_data()
                self.extract_all_reviews_to_db(database=database)
        else:
            database.create_table(tablename=product_to_search.replace("+", ""))
            self.fetch_main_data(product_to_search=product_to_search)
            self.parse_data()
            self.extract_all_reviews_to_db(database=database)
        return self.__all_reviews

    def get_pie_chart(self) -> str:
        """Plot a pie charts of all ratings.

        Returns:
            str: json data
        """
        labels = ["5 ⭐", "4 ⭐", "3 ⭐", "2 ⭐", "1 ⭐"]
        values = []
        for review in self.__all_reviews:
            values.append(review[1])
        data = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    hoverinfo="label+value",
                    title="User Rating",
                )
            ]
        )
        graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
