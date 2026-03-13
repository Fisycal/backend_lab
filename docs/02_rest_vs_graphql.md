- REST is a style of designing APIs where:
    - Nouns are used in the URL to represent resources (e.g., /users)
    - HTTP methods to show the action (GET, POST, PUT, DELETE)
    - Standard status codes to explain what happened
    - REST is a way of building APIs where the URL shows what you want, and the HTTP method shows what you want to do.


1. What is a resource?
    - A resource is the "thing" my API is about. In this lab, users are a resource - a collection of users objescts that my API can list, create, updatem or delete.

    - Think of resource as: "The noun your API manages". In some cases, resource could be posts, products, orders, etc.

2. What are endpoints?
    - Endpoints are **specfic URLs** where clients can interact with a resource.
    - Endpoints are combination of:
        - a path (e.g., /users or /users/1)
        - an HTTP method (GET, POST, DELETE, etc.)
    - Together, they define what action the client can perform.
    - Endpoints are the "doors' into your API

3. Why are /users and /users/{id} REST-style?
    - Both /users and /users/{id} follow REST conventions:
        - /users: 
            - It represents the **collection** of all users.
            - Any actions taken here affect the whole group (list users, create a user).

        - /users/{id}:
            - It represents **a specific user** inside the collection users
            - Any actions taken here affect only that one item (get, update, delete, etc.)

    - In sum, this matches REST's idea of:
        - **Collections**: plural nouns (/users)
        - **Items**: collection + identifier (/users/123)
        - **Actions**: expressed through HTTP methods, not verbs in the URL
        - REST uses:
            - GET /users/1
            - DELETE /users/1
            - POST /users
        - The URL shows **what** you are acting on
        - The HTTP method shows **what action** you are taking