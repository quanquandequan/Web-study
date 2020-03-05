from django.test import TestCase, Client
from sign.models import Event, Guest
import unittest
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.


class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1,
                             name="iphoneX event",
                             status=True, limit=2000,
                             address='Beijing',
                             start_time='2019-08-31 10:30:00')
        Guest.objects.create(id=1,
                             event_id=1,
                             guest_name='alen',
                             phone='13811001101',
                             email='alen@mail.com',
                             sign=False)

    def tearDown(self):
        pass

    def test_event_models(self):
        result = Event.objects.get(id=1)
        self.assertEqual(result.address, "Beijing")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13811001101')
        self.assertEqual(result.guest_name, "Panpan")
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):

    """
        测试index 登录首页
    """

    def test_index_page_renders_index_template(self):
        """
            测试index 视图
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class LoginActionTest(TestCase):
    """
        测试登录函数
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.c = Client()

    def test_login_action_username_password_null(self):
        """
            用户名密码为空
        """
        test_data = {'username': '', 'password': ''}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        """
            用户名密码错误
        """
        test_data = {'username': 'abc', 'password': '123'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        """
            登录成功
        """
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """
        发布会管理
        运行时，需要将views中，event_manage()和search_name()中的@login_required去掉
    """
    def setUp(self):
        Event.objects.create(id=2,
                             name='世界园艺博览会',
                             limit=2000,
                             status=True,
                             address='beijing',
                             start_time=datetime(2019, 10, 1, 10, 30, 0))
        self.c = Client()

    def test_event_manage_success(self):
        """
            测试发布会:世界园艺博览会
        """
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("世界园艺博览会", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_search_success(self):
        """
            测试发布会搜索
        """
        response = self.c.post('/search_name/', {"name": "世界园艺博览会"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("世界园艺博览会", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    """
        嘉宾管理
        运行时，需要将views中，guest_manage()和search_phone()中的@login_required去掉
    """
    def setUp(self):
        Event.objects.create(id=1,
                             name="世界园艺博览会",
                             limit=2000,
                             address='beijing',
                             status=1,
                             start_time=datetime(2019, 10, 1, 10, 30, 0))
        Guest.objects.create(guest_name="alen",
                             phone=18611001100,
                             email='alen@mail.com',
                             sign=0,
                             event_id=1)
        self.c = Client()

    def test_event_manage_success(self):
        """
            测试嘉宾信息: alen
        """
        response = self.c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

    def test_guest_manage_search_success(self):
        """
            测试嘉宾搜索
        """
        response = self.c.post('/search_phone/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)


class SignIndexActionTest(TestCase):
    """
        发布会签到
    """
    def setUp(self):
        Event.objects.create(id=1,
                             name="世界园艺博览会",
                             limit=2000,
                             address='beijing',
                             status=1,
                             start_time=datetime(2019, 10, 1, 10, 30, 0))
        Event.objects.create(id=2,
                             name="婚博会",
                             limit=2000,
                             address='shanghai',
                             status=1,
                             start_time=datetime(2019, 12, 1, 10, 30, 0))
        Guest.objects.create(guest_name="alen",
                             phone=18611001100,
                             email='alen@mail.com',
                             sign=0,
                             event_id=1)
        Guest.objects.create(guest_name="una",
                             phone=18611001101,
                             email='una@mail.com',
                             sign=1,
                             event_id=2)
        self.c = Client()

    def test_sign_index_action_phone_null(self):
        """
            手机号为空
        """
        response = self.c.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        """
            手机号或发布会id 错误
        """
        response = self.c.post('/sign_index_action/2/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        """
            用户已签到
        """
        response = self.c.post('/sign_index_action/2/', {"phone": "18611001101"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        """
            签到成功
        """
        response = self.c.post('/sign_index_action/1/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ModelTest("test_event_models"))
    suite.addTest(ModelTest("test_guest_models"))
    runner = unittest.TextTestRunner()
    runner.run(suite)