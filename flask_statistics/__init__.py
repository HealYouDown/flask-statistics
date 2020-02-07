import datetime
import time

from flask import Flask, Response, g, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Table


class Statistics:
    def __init__(
        self,
        app: Flask = None,
        db: SQLAlchemy = None,
        model: Table = None
    ):

        if (app is not None and db is not None
                and model is not None):
            self.init_app(app, db, model)

    def init_app(
        self,
        app=None,
        db=None,
        model=None
    ) -> None:
        self.app = app
        self.db = db
        self.model = model

        # Register function that runs before / after each request
        # These functions are used to collect the data
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        self.app.teardown_request(self.teardown_request)

    def before_request(
        self
    ) -> None:
        # Take time when request started
        g.start_time = time.time()
        g.request_date = datetime.datetime.utcnow()
        # after_request, which is used to get the status code,
        # is skipped if an error occures, so we set a default
        # error code that is used when this happens
        g.request_status_code = 500

    def after_request(
        self,
        response: Response
    ) -> Response:
        g.request_status_code = response.status_code
        g.request_content_size = response.content_length

        return response

    def teardown_request(
        self,
        exception: Exception = None
    ) -> None:
        # Take time when request ended
        end_time = time.time()

        # Create object that is later stored in database
        obj = {}

        # the time to finish the request
        obj["response_time"] = end_time - g.start_time
        # the returned status code
        obj["status_code"] = g.request_status_code
        # body response size in bytes
        obj["size"] = g.request_content_size
        # used method (PUT, PATCH, GET, POST, ...)
        obj["method"] = request.method
        # ip address
        obj["remote_address"] = request.remote_addr
        # requested path (e.g. /homepage, /about, ...)
        obj["path"] = request.path
        # page that linked to requested page
        obj["referrer"] = request.referrer
        # browser and version
        obj["browser"] = "{browser} {version}".format(
            browser=request.user_agent.browser,
            version=request.user_agent.version)
        # platform (e.g. windows)
        obj["platform"] = request.user_agent.platform
        # complete user agent string
        obj["user_agent"] = request.user_agent.string
        # date when request was send
        obj["date"] = g.request_date
        # exception (if there was one)
        obj["exception"] = None if exception is None else repr(exception)

        """
        # Gets geo data based of ip
        url = "https://freegeoip.app/json/{0}".format(request.remote_addr)
        with requests.get(url) as req:
            if req.status_code != 403:  # 403 means rate limted was reached
                resp = req.json()

                none_if_empty = lambda s: None if resp.get(s) == "" else resp.get(s)  # noqa F731

                obj["country_code"] = none_if_empty("country_code")
                obj["country_name"] = none_if_empty("country_name")
                obj["region_code"] = none_if_empty("region_code")
                obj["region_name"] = none_if_empty("region_name")
                obj["city"] = none_if_empty("city")
                obj["zip_code"] = none_if_empty("zip_code")
                obj["time_zone"] = none_if_empty("time_zone")
        """

        # Adds object to db and saves
        self.db.session.add(
            self.model(**obj)
        )
        self.db.session.commit()
