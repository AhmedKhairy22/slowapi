import types
import inspect
from typing import Any
from parse import parse

from response import Response
from request import Request

SUPPORTED_REQ_METHODS = {"GET", "POST", "DELETE"}

class SlowAPI():
    
    def __init__(self, middlewares=[]) -> None:
        self.routes = dict()
        self.middlewares = middlewares
        self.routes_middlewares = dict()

        # {
        #     "/route" : {
        #         "GET" : handler,
        #         "POST" : handler
        #     }
        # }

    
    def __call__(self, environ, start_response) -> Any:
        response = Response()
        request = Request(environ)

        # running the middlewares
        for middleware in self.middlewares:
            if isinstance(middleware, types.FunctionType):
                middleware(request)
            else:
                raise TypeError("You Can Only Pass Functions as middlewares")

        for path, handler_dict in self.routes.items():
            res = parse(path, request.path_info)

            for request_method, handler in handler_dict.items():

                if request.request_method == request_method and res:
                    for middleware in self.routes_middlewares[path][request_method]:
                         if isinstance(middleware, types.FunctionType):
                             middleware(request)
                         else:
                              raise TypeError("You Can Only Pass Functions as middlewares")

                    handler(request, response, **res.named)
                    return response.as_wsgi(start_response)
                 
        return response.as_wsgi(start_response)
    
    # this is the base route function for implementing the other HTTP methods
    def route_base(self, method, path, middlewares):
        def wrapper(handler):
            path_name = path or f"/{handler.__name__}"

            if path_name not in self.routes:
                self.routes[path_name] = {}
            self.routes[path_name][method] = handler

            if path_name not in self.routes_middlewares:
                self.routes_middlewares[path_name] = {}
            self.routes_middlewares[path_name][method] = middlewares
            
            return handler
        
        return wrapper
    

    def get(self, path=None, middlewares=[]):
        return self.route_base("GET", path, middlewares)
    
    def post(self, path=None, middlewares=[]):
        return self.route_base("POST", path, middlewares)
    
    def delete(self, path=None, middlewares=[]):
        return self.route_base("DELETE", path, middlewares)
    

    def route(self, path=None, middlewares=[]):
        def wrapper(handler):
            if isinstance(handler, type):
                class_members = inspect.getmembers(handler, lambda x: inspect.isfunction(x) and not 
                    x.__name__.startswith("__") and not x.__name__.endswith("__") and
                    x.__name__.upper() in SUPPORTED_REQ_METHODS
                    )
                for fn_name, fn_handler in class_members:
                    self.route_base(fn_name.upper(), path or f"/{fn_handler.__name__}", middlewares)(fn_handler)

            else:
                raise ValueError("@route can only be used with Classes")
            
        return wrapper
