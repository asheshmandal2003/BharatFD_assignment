from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class FAQPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = FAQPagination

    def list(self, request, *args, **kwargs):
        lang = request.GET.get('lang', 'en')
        cached_faqs = cache.get(f'faqs_{lang}')

        if cached_faqs:
            faqs_data = cached_faqs
        else:
            if lang not in ['hi', 'bn']:
                lang = 'en'
                faqs = FAQ.objects.all().values(
                    'id',
                    'question',
                    'answer'
                )
            else:
                faqs = FAQ.objects.all().values(
                    'id',
                    f'question_{lang}',
                    'answer'
                )
            faqs_data = [
                {
                    'id': faq['id'],
                    'question': faq.get(f'question_{lang}')
                    if lang != 'en'
                    else faq['question'],
                    'answer': faq['answer'],
                }
                for faq in faqs
            ]
            cache.set(f'faqs_{lang}', faqs_data, timeout=180)

        page = self.paginate_queryset(faqs_data)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(faqs_data)


def faq_page(request):
    return render(request, "faq.html")
