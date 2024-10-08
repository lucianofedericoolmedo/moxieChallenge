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

### Create a service (Optional not required but offers you to add services products, category)

curl -X POST http://localhost:8000/api/services/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Botox 3",
    "description": "Anti-aging treatment 12",
    "price": 300.00,
    "duration": 30,
    "med_spa": 1,
    "service_product": 1,
    "service_category": 1,
    "service_type": 1
}'

### Create a service (Optional not required but offers you to add services products, category and product supplier)
curl -X POST http://localhost:8000/api/services/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Facial Treatment",
    "description": "A relaxing facial treatment to rejuvenate your skin.",
    "price": 99.99,
    "duration": 60,
    "med_spa": 1,
    "service_product": 1,
    "service_category": 1,
    "service_type": 1,
    "service_product_supplier": 1
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

### Create an appointment

curl -X POST http://localhost:8000/api/appointments/ \
-H "Content-Type: application/json" \
-d '{
    "start_time": "2024-10-01T14:00:00Z",
    "med_spa": 1,
    "services": [1, 2]
}'

### Failing to Create an appointment

curl -X POST http://localhost:8000/api/appointments/ \
-H "Content-Type: application/json" \
-d '{
    "start_time": "2024-10-01T17:30:00Z",
    "med_spa": 1,
    "services": [1, 2,3]
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
