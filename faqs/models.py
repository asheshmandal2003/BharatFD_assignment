from django.db import models
from ckeditor.fields import RichTextField
import hashlib
from googletrans import Translator
from django.core.cache import cache

# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            question_hash = hashlib.md5(self.question.encode('utf-8')).hexdigest()
            cached_hi = cache.get(f'{question_hash}_hi')
            cached_bn = cache.get(f'{question_hash}_bn')
            
            if cached_hi and cached_bn:
                self.question_hi = cached_hi
                self.question_bn = cached_bn
            else:
                translator = Translator()
                try:
                    self.question_hi = translator.translate(self.question, src='en', dest='hi').text
                    self.question_bn = translator.translate(self.question, src='en', dest='bn').text
                    
                    cache.set(f'{question_hash}_hi', self.question_hi, timeout=3600*24)
                    cache.set(f'{question_hash}_bn', self.question_bn, timeout=3600*24)
                except Exception as e:
                    print(f"Translation failed for question: {self.question}, error: {e}")
                    self.question_hi = self.question_bn = None

        super().save(*args, **kwargs)


    def __str__(self):
        return self.question
