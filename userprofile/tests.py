import datetime
from calendar import MONDAY
from random import randint

from django.contrib.auth import get_user_model
from django.test import TestCase

from userprofile.models import DutyTime, Profile


class DutyTimeTestCase(TestCase):
    now = (DutyTime.t0 + datetime.timedelta(hours=1)).time()
    later = (DutyTime.t0 + datetime.timedelta(hours=3)).time()
    earlier = (DutyTime.t0 - datetime.timedelta(hours=1)).time()

    def setUp(self):
        d = DutyTime.objects.create(day=MONDAY, start_time=DutyTime.t0, end_time=DutyTime.t1)
        u = get_user_model().objects.create(username=str(randint(0, 100000)))
        p = Profile.objects.create(user=u)
        p.dutytime.add(d)
        p.save()

    def test_now(self):
        self.assertEqual(Profile.get_profiles_for_dutytime(day=MONDAY, time=self.now).count(), 1)

    def test_later(self):
        self.assertEqual(Profile.get_profiles_for_dutytime(day=MONDAY, time=self.later).count(), 0)

    def test_earlier(self):
        self.assertEqual(Profile.get_profiles_for_dutytime(day=MONDAY, time=self.earlier).count(), 0)

    def test_now_with_two_people(self):
        u = get_user_model().objects.create(username=str(randint(0, 100000)))
        d = DutyTime.objects.get(day=MONDAY, start_time=DutyTime.t0, end_time=DutyTime.t1)
        p = Profile.objects.create(user=u)
        p.dutytime.add(d)
        p.save()

        self.assertEqual(Profile.get_profiles_for_dutytime(day=MONDAY, time=self.now).count(), 2)
