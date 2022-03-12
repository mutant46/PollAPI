from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from polls import views


class PollTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com', password='test')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()

    def test_list(self):
        ''' Using APiREquestFactory to create a request '''
        request = self.factory.get(
            self.uri, HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_list2(self):
        ''' Using APIClient to create a request '''
        self.client.login(username='test', password='test')
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,)

    def test_create(self):
        self.client.login(username='test', password='test')
        data = {'question': 'How are you?',
                'created_by': self.user.id}
        response = self.client.post(self.uri, data, format='json')
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_create_bad_request(self):
        self.client.login(username='test', password='test')
        data = {'question': 'How are you?'}
        response = self.client.post(self.uri, data, format='json')
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))
