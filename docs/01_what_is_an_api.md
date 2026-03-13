An API stands for APplication Programming Interface. It is a set of rules that lets one program communicate to another program.

This makes communication possible between client and server and vice-versa. When the client sends a request, the server sends a response.

When a FastAPI backend is built, endpoints (URLs) are created that other apps can call to.

/users routes are example of API because:
1. They serve as doors that other programs can knock to ask the server to do some things.

2. They follow API rules:
    - Use URLs to identify things
    - Use HTTP methods (GET, POST, DELETE) to say what you want
    - Send and receive data in JSON
    - Return proper status codes (200, 201, 204, 400, 404) to expalin what happened

3. It is a resource in my API. In REST terminologies:
    - "users" is a resource
    - /users is the collection
    - /users/{id is an item}
    
