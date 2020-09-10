from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tweet

User = get_user_model()


# Create your tests here.
class TweetTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='andrei', password='1111')
        User.objects.create_user(username='andrei2', password='2222')
        Tweet.objects.create(content="my tweet 1", user=User.objects.first())
        Tweet.objects.create(content="my tweet 2", user=User.objects.first())
        Tweet.objects.create(content="my tweet 3", user=User.objects.get(id=2))
        Tweet.objects.create(content="my tweet 5", user=User.objects.first())

    def get_client(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='andrei', password='1111')
        client.force_authenticate(user=User.objects.first())
        # token = Token.objects.get(user__username='andrei')
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def test_tweet_created(self):
        tweet = Tweet.objects.create(content="my tweet 4", user=User.objects.first())
        self.assertEqual(tweet.id, 4)
        self.assertEqual(tweet.user, User.objects.first())

    def test_api_login(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)

    def test_tweet_create_api_view(self):
        request_data = {"content": "This is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertNotEqual(2, new_tweet_id)

    def test_tweet_detailed_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        response_delete_second = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response_delete_second.status_code, 500)
        response_incorrect_owner = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)

