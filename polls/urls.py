from django.urls import path
from .views import PollViewSet, ChoiceList, VoteCreate, CreateUser, LoginView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

urlpatterns = [
    # used for generic views List, and Detail
    # path("polls/", PollList.as_view(), name="polls_list"),
    # path("polls/<int:pk>/", PollDetail.as_view(), name="polls_detail"),
    path('users/', CreateUser.as_view(), name='users_create'),
    path('login/', LoginView.as_view(), name='login'),
    path('polls/<int:pk>/choices/', ChoiceList.as_view(), name='choice_results'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote/',
         VoteCreate.as_view(), name='create_vote'),
]


urlpatterns += router.urls
