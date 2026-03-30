1. GET: It is used to retrieve data in the resource
    - In the project, the endpoint GET/users/:
        - Returns the list of all users.
            -   [
                    {
                        "id": 1,
                        "name": "Alice",
                        "email": "alice111@learning.com"
                    },
                    {
                        "id": 2,
                        "name": "Bobby",
                        "email": "bobby123@learning.com"
                    }
                ]
        -   Status code returned:
            -   200 OK

        - No changes, no side effects - just reading

    - for endpoint, GET/users/1:
        - Returned:
            -   {
                    "id": 1,
                    "name": "Alice",
                    "email": "alice111@learning.com"
                }
        
        -   Status code: 200 Ok

    - for endpoint, GET/users/999:
        - Returned:
            -   {
                    "detail": "User not found"
                }
        
        -   Status code:404 Not Found

2. POST: It is used to create a new resource or an object
    - In this project, POST/users/:
        - Creates a new user in users_db
        - Returned:
            -   {
                    "id":3,
                    "name":"Charlie",
                    "email":"charlie@learning.com"
                }

        - Status code:
            -   201 Created

    - For a bad request:
        -   {
                "id":4,
                "name":"David"
            }

        - Returned:
            -   {
                    "detail": "id, name, and email are required"
                }

            -   Status code: 400 Bad Request

3. PUT: It is used to update/modify a resource **completely**
    - In the app, PUT/users/1:
        - Would replace user #1 with a completely new resource
        - Anything missing in the body who be overwritten.

4. PATCH: It is used to update/modify a part of a resource
    - In the app, PATCH/users/1:
        - Would replace only the specified fields in user #1 

5. DELETE: To completely remove a resorce
    - In the app, DELETE/users/1:
        - Deletes user #1 from your users_db

6. HEAD: To show all the headers. It behaves like GET but without the body. It is good for a quick peek to see if something exist. Also good for seeing metadata (e.g., content length) without downloading the whole response.
    - In the app, HEAD /users/:
        - FastAPI would respond with:
            - The same headers as GET /users/
            - But no JSON list of users
        - It is very useful for: 
            - Checking if the endpoint is alive
            - Checking caching info
            - Checking if a resource exists

       
7. OPTIONS: To see all HTTP methods that are allowed on the endpoint. Browsers uses OPTIONS for CORS preflight checks and to understand what actions the server supports.
    - In the app, OPTIONS /users/: 
        - FastAPI would respond with things such as:
            - Allow: GET, POST. HEAD, OPTIONS

    - In the app, OPTIONS /users/{id}: 
        - FastAPI would respond with things such as:
            - Allow: GET, DELETE, PUT, PATCH, HEAD, OPTIONS

- NOTE: **fetch()** is not an HTTP method; it is a JavaScript browser API