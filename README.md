# 🐢 SlowAPI

A lightweight Python web framework inspired by FastAPI, but deliberately **slow** (for now).

SlowAPI runs on synchronous WSGI with [Gunicorn](https://gunicorn.org/), so it doesn't support `async`/`await` yet. That's where the name comes from, we're slow, and we own it 🐢. ASGI support may come in the future.

---

## ✨ Features

- 🎨 **Decorator-style routing** — `@app.get`, `@app.post`, `@app.delete`
- 🔗 **Dynamic URL parameters** — capture path variables like `{id}`
- 🛡️ **Middleware support** — global or per-route middleware functions
- 🏛️ **Class-based routing** — group HTTP methods under a single class
- 🖼️ **Simple HTML templating** — render HTML with `{{ variable }}` placeholders

---

## 📦 Installation

```bash
git clone https://github.com/your-username/slowapi.git
cd slowapi
pip install -r requirements.txt
```

---

## 🚀 Quick Start

```python
from main import SlowAPI

slowapi = SlowAPI()

@slowapi.get("/hello")
def hello(request, response):
    response.send("Hello, World!", 200)
```

```bash
gunicorn example:slowapi
```

---

## 🗺️ Routing

### Dynamic URL Parameters

```python
@slowapi.get("/users/{id}")
def get_user(request, response, id):
    response.send(f"User ID: {id}", 200)
```

### Query String Parameters

```python
@slowapi.get("/search")
def search(request, response):
    term = request.queries.get("q", "")
    response.send(f"Searching for: {term}", 200)
```

---

## 🛡️ Middlewares

```python
def logging_middleware(request):
    print(f"{request.request_method} {request.path_info}")

def auth_middleware(request):
    print("Checking auth...")

# Global — runs on every request
slowapi = SlowAPI(middlewares=[logging_middleware])

# Per-route — runs only on this route
@slowapi.get("/protected", middlewares=[auth_middleware])
def protected(request, response):
    response.send("Secret content", 200)
```

---

## 🏛️ Class-Based Routing

```python
@slowapi.route("/users")
class Users:
    def get(request, response):
        response.send("Get all users", 200)

    def post(request, response):
        response.send("Create a user", 200)
```

Method names must match HTTP verbs (`get`, `post`, `delete`).

---

## 🖼️ HTML Templating

**`profile.html`:**
```html
<h1>Hello, {{ name }}!</h1>
<p>{{ message }}</p>
```

```python
@slowapi.get("/profile")
def profile(request, response):
    response.render("profile", context={"name": "Ahmed", "message": "Welcome!"})
```

---

## 📁 Project Structure

```
slowapi/
├── main.py       # Core framework
├── request.py    # Request object
├── response.py   # Response object
├── example.py    # Example app
└── example.html  # Example template
```
