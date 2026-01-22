# subscription-app


## Step1- git clone https://github.com/leettobtech-blip/subscription-app.git

## Step-2 Build image and run application in container

docker-compose up --build

## step3- login on admin using this (http://127.0.0.1:8000/admin/login/?next=/admin/) with below email and password to add dummy data

Email: admin@example.com
Password: admin123

## then test below endpoints


## Register new user 

http://127.0.0.1:8000/api/accounts/register/

### body
{
"email": "dk@gmail.com",
"password": "123"
}

### response

{    "detail": "User created"}



## Login with a device

http://127.0.0.1:8000/api/accounts/login/

### body
{
"email": "dk@gmail.com",
"password": "123",
"device_id":"1"
}

### Response
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY5MTA0MTI4LCJpYXQiOjE3NjkxMDMyMjgsImp0aSI6IjM0N2JkNmIyYTExODQ1MzA4ZTI4MWU0YjZjNGU2Yjc2IiwidXNlcl9pZCI6IjcifQ.7rH3KK5610OljFKelAH9UevWwzf_UXQgBUqDgWVvrMA",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2OTcwODAyOCwiaWF0IjoxNzY5MTAzMjI4LCJqdGkiOiI3NDkzNDliMmRmZjc0YWZkYTRiNThlMWFmZjY5YWY1NCIsInVzZXJfaWQiOiI3In0.d5ZmwibbO2rRhg0oJsPKwvy98DTN_6ln9n3Kb4jyX_0",
    "detail": "Login successful"
}



## Access contents

http://127.0.0.1:8000/api/content/

### response:
{
    "content": [
        {
            "id": 1,
            "title": "content1",
            "is_premium": false
        }
    ]
}



## buy subscription

http://127.0.0.1:8000/api/subscriptions/subscribe/

### body is null just pass token in authentication header
### response
{
    "plan": "paid",
    "is_active": true,
    "max_devices": 4,
    "price": "99.00"
}



## logout from one device

http://127.0.0.1:8000/api/accounts/logout/device/

### pass access token in body
{"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2OTcwOTQ0MSwiaWF0IjoxNzY5MTA0NjQxLCJqdGkiOiIzYTBmY2ZiZGYyMTk0NDUzOTAyMDZkYWUzMjBjYTM2MCIsInVzZXJfaWQiOiI3In0.Cv3pAQ6Cdgid_ShKrYDYK-85o5CJWlwCTbpaI-83nHY"}

### pass token in authentication header 




## Logout from all device
http://127.0.0.1:8000/api/accounts/logout/all/

### pass access token in body
{"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2OTcwOTQ0MSwiaWF0IjoxNzY5MTA0NjQxLCJqdGkiOiIzYTBmY2ZiZGYyMTk0NDUzOTAyMDZkYWUzMjBjYTM2MCIsInVzZXJfaWQiOiI3In0.Cv3pAQ6Cdgid_ShKrYDYK-85o5CJWlwCTbpaI-83nHY"}


### pass token in authentication header
