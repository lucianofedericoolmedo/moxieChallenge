### Create an appointment

curl -X POST http://localhost:8000/api/appointments/ \
-H "Content-Type: application/json" \
-d '{
    "start_time": "2024-10-01T14:00:00Z",
    "med_spa": 1,
    "services": [1, 2]
}'

### Retrieve a Specific Appointment by ID

curl -X GET http://localhost:8000/api/appointments/1/


### Update an Appointment's Status

curl -X PATCH http://localhost:8000/api/appointments/1/ \
-H "Content-Type: application/json" \
-d '{
    "status": "COMPLETED"
}'

### List All Appointments

curl -X GET http://localhost:8000/api/appointments/


### Retrieve Appointments by Status

curl -X GET http://localhost:8000/api/appointments/?status='SCHEDULED'


### Retrieve Appointments by Start Date

curl -X GET http://localhost:8000/api/appointments/?start_time=2024-10-01

### Create a service

curl -X POST http://localhost:8000/api/services/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Botox",
    "description": "Anti-aging treatment",
    "price": 300.00,
    "duration": 30,
    "med_spa": 1
}'

### Update a service

curl -X PATCH http://localhost:8000/api/services/1/ \
-H "Content-Type: application/json" \
-d '{
    "price": 350.00,
    "description": "Updated anti-aging treatment"
}'

### Retrieve service by id

curl -X GET http://localhost:8000/api/services/1/

### Retrieve a List of All Services for a Given MedSpa

curl -X GET "http://localhost:8000/api/services/?medspa_id=1"
