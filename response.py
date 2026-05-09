import re

class Response():
    """ 
    This calss is for the response object to simplfy
    the way that the user deal with the low level
    details 

    """

    def __init__(self, status_code="404 NOT FOUND", text="Route Not Found") -> None:
        self.status_code = status_code
        self.text = text
        self.headers = []


    def as_wsgi(self, start_response):
        start_response(self.status_code, headers=self.headers)
        return [self.text.encode()]
        
    def send(self, text, status_code="200 OK"):
        """handel the data that passed by the user"""

        self.text = str(text) + "\n"
        self.status_code = status_code

        if isinstance(self.status_code, int):
            self.status_code = str(status_code)
        elif isinstance(self.status_code, str):
            self.status_code = status_code
        else:
            raise ValueError("Status Code should be ing or str type")
        
    def render(self, template_name, context={}):
        path = f"{template_name}.html"

        with open(path) as fp:
            template = fp.read()

            for key, value in context.items():
                template = re.sub(r'{{\s*' + re.escape(key) + r'\s*}}', str(value), template)

        self.headers.append(('content_type', 'text/html'))
        self.text = template
        self.status_code = "200 OK"
