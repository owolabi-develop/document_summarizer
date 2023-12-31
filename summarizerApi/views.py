from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from . summarizer import (
    get_elasticsearch_similarity_search,
    get_summarizer_question_query,
    )
from . serializers import SummarizerSerializer
from rest_framework import status
# Create your views here.



class SummarizerView(GenericAPIView):
    serializer_class = SummarizerSerializer
    #permission_classes = [permissions.IsAuthenticated]
    @extend_schema(summary='Send a Message', methods=["GET"],description='Query Your Csv Files',filters=True,tags=['Summarizer'])
    def post(self,request,format=None):
        serializer = SummarizerSerializer(data=self.request.data)
        if serializer.is_valid():
            query = serializer.validated_data.get('query')
            openai_api_key = serializer.validated_data.get('openai_api_key')
            index_name = serializer.validated_data.get('index_name')
            es_cloud_id = serializer.validated_data.get('es_cloud_id')
            es_user = serializer.validated_data.get('es_user')
            es_password = serializer.validated_data.get('es_password')
            es_api_key = serializer.validated_data.get('es_api_key')
            question_answer = get_elasticsearch_similarity_search(
                openai_api_key=openai_api_key,
                index_name=index_name,
                es_cloud_id=es_cloud_id,
                es_user=es_user,
                es_password=es_password,
                es_api_key=es_api_key
                )
            query_response =  get_summarizer_question_query(query,question_answer,openai_api_key=openai_api_key)
            return Response(dict(message=query_response[0],source=query_response[1]),status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()



class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

