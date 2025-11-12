# 🏢 Company Management System (Django + DRF)

A complete **Company Management System** built with **Django REST Framework (DRF)** and a dynamic HTML frontend.  
It allows you to **add, edit, delete, search, filter, and order** company records — all powered by Django APIs.  

---

## 🚀 Features

- 🔍 **Search**, **Filter**, and **Order** company data directly via URL  
- 🧠 **Dynamic frontend** that interacts with DRF APIs using `fetch()`  
- 🖋️ Add / Edit companies without full page reloads  
- 🧾 Logo upload, form validation, and real-time UI updates  
- 🔗 URL-based filtering: e.g.  

http://127.0.0.1:8000/companyv2/?ordering=name

http://127.0.0.1:8000/companyv2/?search=tech

http://127.0.0.1:8000/companyv2/?status=active


---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django + Django REST Framework |
| Frontend | HTML + CSS + JavaScript (Fetch API) |
| Database | SQLite (default) |
| Filtering | `django-filter` + `OrderingFilter` + `SearchFilter` |
| Serializer | DRF `ModelSerializer` |
| View | Custom `APIView` |
| Templates | Django Template Engine |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/company-management-system.git
cd company-management-system

python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

Then open your browser and visit:
👉 http://127.0.0.1:8000/companyv2/

🧩 Example API Usage (via Postman or Browser)
Get all companies
GET http://127.0.0.1:8000/companyv2/

Get company by ID
GET http://127.0.0.1:8000/companyv2/1/

Filter & Order
GET http://127.0.0.1:8000/companyv2/?ordering=name
GET http://127.0.0.1:8000/companyv2/?search=tech
GET http://127.0.0.1:8000/companyv2/?status=active

Add a new company (via API)
POST http://127.0.0.1:8000/companyv2/
Content-Type: application/json

{
  "name": "Tech Sphere",
  "address": "Lahore, PK",
  "status": "active",
  "total_workers": 45
}
