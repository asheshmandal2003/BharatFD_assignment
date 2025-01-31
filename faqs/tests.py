import pytest
from rest_framework.test import APIClient
from faqs.models import FAQ
from django.core.cache import cache
import time


# Create your tests here.
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_faq(db):
    return FAQ.objects.create(
        question='What is your name?',
        answer='My name is John Doe'
        )


def create_faq(api_client, db):
    response = api_client.post(
        '/api/v1/faqs',
        {
            'question': 'Test Question',
            'answer': 'Test Answer'
        },
        format='json')
    assert response.status_code == 201
    assert response.data['question'] == 'Test Question'


def test_get_faq_list(api_client, sample_faq):
    response = api_client.get('/api/v1/faqs/')
    assert response.status_code == 200
    assert len(response.data["results"]) > 0


def test_get_faq_with_translation(api_client, sample_faq):
    response = api_client.get('/api/v1/faqs/?lang=hi')
    assert response.status_code == 200
    assert "question" in response.data["results"][0]


@pytest.mark.django_db
def test_faq_pagination(api_client):
    cache.clear()
    for i in range(15):
        FAQ.objects.create(question=f"Question {i}", answer="Answer")

    response = api_client.get("/api/v1/faqs/?lang=en&page=1&page_size=10")
    assert response.status_code == 200
    assert len(response.json()["results"]) == 10
    assert "next" in response.json()


def test_cache_behavior(api_client, sample_faq):
    cache.set("faqs_en",
              [{"id": sample_faq.id,
                "question": "Cached question?",
                "answer": "Cached answer"}],
              timeout=180)
    response = api_client.get('/api/v1/faqs/')
    assert response.data["results"][0]["question"] == "Cached question?"


@pytest.mark.django_db
def test_faq_cache_expiry(api_client):
    cache.clear()
    faq = FAQ.objects.create(question="Cached question",
                             answer="Cached answer")
    cache.set("faqs_en",
              [{"id": faq.id, "question": faq.question, "answer": faq.answer}],
              timeout=5)
    response = api_client.get("/api/v1/faqs/?lang=en")
    assert response.status_code == 200
    assert response.json()['results'][0]['question'] == "Cached question"
    time.sleep(6)
    response = api_client.get("/api/v1/faqs/?lang=en")
    assert response.status_code == 200
    assert response.json()['results'][0]['question'] == "Cached question"
