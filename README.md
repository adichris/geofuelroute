# **Route and Fuel Cost API**

This is a Django-based API that calculates the optimal route and fuel costs between a start and end destination in the USA. The API determines the most cost-effective fuel stops along the route based on fuel prices, vehicle fuel efficiency, and range.

---

## **Features**

- Calculates total distance between two points.
- Determines fuel costs based on fuel efficiency and retail fuel prices.
- Recommends cost-effective fuel stops along the route.
- Returns route geometry for visualization.
- Built with Django 3.2.23 and Django REST Framework.

---

## **Requirements**

- Python 3.8+
- Django 3.2.23
- Django REST Framework
- OpenRouteService API Key
- database (for storing fuel data from csv file)

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone [https://github.com/adichris/geofuelroute.git](https://github.com/adichris/geofuelroute.git)
cd route-fuel-cost-api
```

### **2. Install Dependencies**
Set up a virtual environment and install required packages:

```bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### **3. Configure Database**
Update the database settings in settings.py to connect to your PostgreSQL database.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
**Apply migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **4. Add Fuel Data**
Load the provided fuel dataset into the database

```bash
python manage.py load_fuel_data 'asset/fuel-prices-for-be-assessment.csv'
```

### **5. Set OpenROuteService API KEY**
```python
# geofuel/settings.py

# OPEN ROUTE SERVICE API
OPEN_ROUTE_SERVICE_API = "******"
```

### **6. Run Development Server**
```bash
python3 manage.py runserver
```

<hr>

### **API ENDPOINTS**
Calculate Route and Fuel Costs <br>
Endpoint: <code>[/api/](http://127.0.0.1:8000/api/) </code>
<br>Method: <code>POST</code>
<br>Request <code>Body</code>
```json
{
    "start_lat": 38.9072,
    "start_lng": -77.0369,
    "end_lat": 40.7128,
    "end_lng": -74.0060
}
```
**Response**
```json
TTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "total_distance_miles": 227.51,
    "total_fuel_required_gallons": 22.75,
    "total_cost": 61.13,
    "stops": [
        {
            "opis_trucking_id": 66341,
            "truckstop_name": "7-ELEVEN #218",
            "address": "I-44, EXIT 4",
            "city": "Harrold",
            "state": "TX",
            "price_per_gallon": 2.687,
            "gallons_needed": 22.75,
            "cost": 61.13
        }
    ],
    "route_geometry": {
        "coordinates": [
            [ ... ],
            [ ... ],
            ...]
```

### Testing
Use Postman, cURL, builtin rest framework browsable to test the API:
```bash
curl -X POST http://127.0.0.1:8000/api/ \
-H "Content-Type: application/json" \
-d '{
    "start_lat": 38.9072,
    "start_lng": -77.0369,
    "end_lat": 40.7128,
    "end_lng": -74.0060
}'

```

### Technologies Used
Backend: Django 3.2.23, Django REST Framework
<br>Database: SQLITE
<br>Routing API: OpenRouteService

### Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.


### Acknowledgments
OpenRouteService for routing API.
<br>Fuel dataset sample provided in the project.
