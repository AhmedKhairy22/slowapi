from collections import defaultdict

class Request:
    def __init__(self, environ):
        self.queries = defaultdict()
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)

        if self.query_string:
            req_queries = self.query_string.split("&")

            for query in req_queries:
                qur_key ,qur_value = query.split("=")

                self.queries[qur_key] = qur_value
