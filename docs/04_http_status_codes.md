1. 200 OK
    - It means everything worked normally
    - In the app, when someone does:
        - GET /users/ and the server successfully returns the list of all users, you send 200 OK because it means:
        - "Here is the data you requested for, Everything is fine."

2. 201 Created
    - A new resource was successfully created
    - In the app, when someone calls:
        - POST /users/ and witha valid users detail in dict, you return 201 because it means:
        - "I successfully created a new user and added it to the list."
        - It tells the client something new now exists.

3. 204 No content
    - The action worked, but there is nothing to return.
    - In the app, when someone calls:
        - DELETE /users/3 and the user exist and is successfully deleted, you return 204 because: 
            - "The user is gone, I deleted the user, but nothing to show you."
        - No JSON body, just success.

4. 400 Bad Request
    - The client sent somrthing invalid
    - In your app, when someone tries to create a user but forgets a field, you return 400 because: 
        - "You did not provide me with the required fields. Fix your request."
    - The problem is with the client's input

5. 404 Not Found
    - The thing they requested for does not exist.
    - In the app, if someone calls GET /users/1002, whereby user 1002 is not in the users list, you return 404 because:
        - "I looked, but that user doesn't exist."
    - This tells the client the resource is missing
