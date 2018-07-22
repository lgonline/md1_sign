from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from sign.models import Guest,Event

# 创建ModelTest类，继承django.test.TestCase
class ModelTest(TestCase):
    # 初始化方法，创建一条Event数据和一条Guest数据
    def setUp(self):
        Event.objects.create(id=1,name='oneplus 3 event',status=True,limit=2000,address='beijing',start_time='2018-7-20 9:18:00')
        Guest.objects.create(id=1,event_id=7,realname='alex',phone='13711001101',email='alex@jd.com',sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address,'beijing')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname,'alex')
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'sign/index.html')


