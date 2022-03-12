from django.shortcuts import render
from .models import Poll, Choice
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from .serializers import ChoiceSerializer, PollSerializer, VoteSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from .perissions import IsOwnerOrReadOnly
# Create your views here.


''' Creating API with ViewSet '''


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    ''' overiding base permission class '''
    permission_classes = (IsOwnerOrReadOnly,)

    ''' Explicit way of adding permission '''
    # def destroy(self, request, *args, **kwargs):
    #     poll = Poll.objects.get(pk=self.kwargs["pk"])
    #     if not request.user == poll.created_by:
    #         raise PermissionDenied("You can not delete this poll.")
    #     return super().destroy(request, *args, **kwargs)


''' Creating API with Generic views '''

# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


# class PollDetail(generics.RetrieveAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


class CreateUser(generics.CreateAPIView):
    authenticaiton_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong Credentials'})


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def post(self, request, *args, **kwargs):
        voted_by = request.data.get('voted_by')
        data = {'choice': request.data.get(
            'choice'), 'poll': request.data.get('poll'), 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


''' Creting API with django rest framework + APIView '''


# class PollList(APIView):

#     def get(self, request, *args, **kwargs):
#         polls = Poll.objects.all()[:20]
#         serializer = PollSerializer(polls, many=True)
#         return Response(serializer.data)


# class PollDetail(APIView):

#     def get(self, request, *args, **kwargs):
#         poll = get_object_or_404(Poll, pk=self.kwargs.get('pk'))
#         serializer = PollSerializer(poll)
#         return Response(serializer.data)


''' Creating simple API with pure django  '''


# def polls_list(request):
#     polls = Poll.objects.all()[:20]
#     data = {"results": list(polls.values(
#         "question", "created_by__username", "pub_date"))}
#     return JsonResponse(data)


# def polls_detail(request, pk):
#     poll = get_object_or_404(Poll, pk=pk)
#     data = {"results": {
#         "question": poll.question,
#         "created_by": poll.created_by.username,
#         "pub_date": poll.pub_date
#     }}
#     return JsonResponse(data)
