from main import SlowAPI

def global_middleware(request):
    print("Hello from the global middlware")

def local_middleware(request):
    print(" Hello from the local middlware")

slowapi = SlowAPI(middlewares=[global_middleware])

@slowapi.get("/users/{id}", middlewares=[local_middleware])
def get_users(request, response, id, ):
    response.send([id], 200) 
    print(request.queries)

@slowapi.post("/users")
def post_users(request, response):
    response.send("Hey, There", 200)


@slowapi.route("/usersc")
class users():
    def __init__(self):
        pass

    def get(request, response):
        response.send("Hello From Class", 200)

    def post(requeset, response):
        response.render('example', {"name" : "Ahmed", "message" : "Hello from html"})
