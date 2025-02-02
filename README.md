# FAQ Management System Using Django

This is a Django-based FAQ application with multi-language support, designed to serve dynamic FAQs to users in different languages.
It uses PostgreSQL for database management and Redis for caching frequently accessed data.

## Preview

### 1. FAQs List:

![Screenshot from 2025-02-02 05-31-34](https://github.com/user-attachments/assets/5d21e1e7-4832-4cd1-8348-aa70c7a9eede)

### 2. Admin Interface:

![Screenshot from 2025-02-02 05-31-23](https://github.com/user-attachments/assets/759de2be-e7ed-482a-a577-63bc4fea3906)
![Screenshot from 2025-02-02 05-51-52](https://github.com/user-attachments/assets/298333af-0e16-4250-a669-2abf97b7f795)


## Features

- **Multi-language Support** (English, Hindi, Bengali) powered by `googletrans`.
- **REST API** implemented using `django-restframework` for easy integration.
- **Pagination** for efficient browsing of large FAQ sets.
- **WYSIWYG Editor** with `django-ckeditor` integration.
- **Redis for caching** to optimize response times.
- **Enhanced Admin Interface** with `django-jazzmin`.
- **Quick Deployment** with a pre-configured `docker-compose` file.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/asheshmandal2003/BharatFD_assignment.git
cd BharatFD_assignment
```

### 2. Setup Environment Vriables

Create a `.env.dev` file in the root directory of the project and add the following environment variables:

```bash
# Django Secret Key
SECRET_KEY=your-secret-key

# Debug Mode
DEBUG=True

# Database Configuration
DATABASE_NAME=faqs
DATABASE_USER=user
DATABASE_PASSWORD=pass
DATABASE_HOST=db
DATABASE_PORT=5432

# Redis Configuration
CACHE_URL=redis://redis:6379/1

# Test Database Configuration
TEST_DATABASE_NAME=faqs_test
```
Replace `your-secret-key` with a secure secret key for Django.

### 3. Build and Run the Application

Use Docker Compose to build and start the application:
```bash
docker-compose --env-file .env.dev up --build
```

This will:

- Build the Docker images for the server, db, and redis services.

- Start the containers and link them together.

### 4. Access the Application

Once the containers are running, you can access the Django application at:

  ```bash
  http://localhost:8000/api/v1/faqs
  ```

### 5. Create a Superuser

To create a superuser for the Django admin interface, run the following command:

  ```bash
  docker compose exec server python manage.py createsuperuser
  ```

Follow the prompts to enter a username, email, and password.

###  6. Access the Admin Interface

You can access the Django admin interface at:

  ```bash
  http://localhost:8000/admin
  ```
Log in using the superuser credentials you created earlier and add some FAQs.

## Project Structure

  ```bash
BharatFD_assignment
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── faqs
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-311.pyc
│   │       └── __init__.cpython-311.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-311.pyc
│   │   ├── apps.cpython-311.pyc
│   │   ├── __init__.cpython-311.pyc
│   │   ├── models.cpython-311.pyc
│   │   ├── tests.cpython-311-pytest-8.3.4.pyc
│   │   └── views.cpython-311.pyc
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── fetchFAQs.js
│   ├── templates
│   │   ├── base.html
│   │   └── faq.html
│   ├── tests.py
│   └── views.py
├── manage.py
├── pytest.ini
├── requirements.txt
├── server
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── settings.cpython-311.pyc
│   │   ├── urls.cpython-311.pyc
│   │   └── wsgi.cpython-311.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static
└── templates
  ```

## API Endpoints:

### 1. GET http://localhost:8000/api/v1/faqs/

Default API for fectching FAQs in `english`.

### Response
  ```bash
  {
      "count": 3,
      "next": null,
      "previous": null,
      "results": [
          {
              "id": 1,
              "question": "Why should I use a digital platform like BharatFD for fixed deposits instead of going directly to a bank?",
              "answer": "<p>Digital platforms often offer higher interest rates, provide a convenient way to compare different FD options, and ensure faster processing times. With BharatFD, you can manage multiple fixed deposits from different banks in one place without the need to visit each bank physically.</p>"
          },
          {
              "id": 2,
              "question": "How can I be sure that my money is safe with BharatFD?",
              "answer": "<p>BharatFD collaborates with trusted banks and financial institutions to offer fixed deposit products. The platform ensures that all investments are made directly with these institutions, adhering to regulatory standards. However, it&#39;s always advisable to review the terms and conditions of the specific bank or financial institution before investing.</p>"
          },
          {
              "id": 3,
              "question": "Who is eligible to open a Fixed Deposit through BharatFD?",
              "answer": "<p>Any individual who meets the eligibility criteria set by the respective banks or financial institutions can open a fixed deposit through BharatFD. This typically includes being at least 18 years old and complying with the Know Your Customer (KYC) requirements.</p>"
          }
      ]
  }
  ```

### 2. GET http://localhost:8000/api/v1/faqs/?lang={preffered_lang}

Language-specific API for fetching FAQs. If you use `bn` in the place of `preffered_lang` then the response will be as follows:

### Response

```bash
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "question": "আমি কেন সরাসরি কোনও ব্যাঙ্কে যাওয়ার পরিবর্তে স্থির আমানতের জন্য ভারতফডের মতো ডিজিটাল প্ল্যাটফর্ম ব্যবহার করব?",
            "answer": "<p>Digital platforms often offer higher interest rates, provide a convenient way to compare different FD options, and ensure faster processing times. With BharatFD, you can manage multiple fixed deposits from different banks in one place without the need to visit each bank physically.</p>"
        },
        {
            "id": 2,
            "question": "আমি কীভাবে নিশ্চিত হতে পারি যে আমার অর্থ ভরটিএফডি দিয়ে নিরাপদ?",
            "answer": "<p>BharatFD collaborates with trusted banks and financial institutions to offer fixed deposit products. The platform ensures that all investments are made directly with these institutions, adhering to regulatory standards. However, it&#39;s always advisable to review the terms and conditions of the specific bank or financial institution before investing.</p>"
        },
        {
            "id": 3,
            "question": "ভারতফডের মাধ্যমে একটি নির্দিষ্ট আমানত খোলার যোগ্য কে?",
            "answer": "<p>Any individual who meets the eligibility criteria set by the respective banks or financial institutions can open a fixed deposit through BharatFD. This typically includes being at least 18 years old and complying with the Know Your Customer (KYC) requirements.</p>"
        }
    ]
}
```











