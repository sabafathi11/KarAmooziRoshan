from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Dataset, Text, Label
from accounts.models import ActivityLog
from .serializers import DatasetSerializer, TextSerializer, LabelSerializer
from rest_framework import permissions
import csv
from django.db import transaction


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Dataset.objects.all()
        else:
            return Dataset.objects.filter(users_with_access=user)

    @action(detail=True, methods=['get'], url_path='search')
    def search_texts(self, request, *args, **kwargs):
        dataset = self.get_object()
        query = request.query_params.get('q', None)
        if query:
            search_results = Text.objects.filter(
                dataset=dataset,
                content__icontains=query
            )
            serializer = TextSerializer(search_results, many=True)
            return Response(serializer.data)
        return Response({"error": "A search query 'q' must be provided"}, status=400)

    @action(detail=False, methods=['post'], url_path='import-csv')
    def import_csv(self, request):
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must be .csv extension"}, status=400)
        if not csv_file:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            with transaction.atomic():
                dataset = Dataset.objects.create(
                    title=csv_file.name,
                    created_by=request.user)
                for row in reader:
                    text_content = row.get('text')
                    # if multiple labels, put '/' between
                    label_names = row.get('label').split('/')
                    text = Text.objects.create(dataset=dataset, content=text_content)
                    if label_names:
                        for label_name in label_names:
                            label_names_of_dataset = [lab.name for lab in dataset.labels.all()]
                            if label_name not in label_names_of_dataset:
                                label = Label.objects.create(dataset=dataset, name=label_name)
                            else:
                                label = Label.objects.get(name=label_name)
                            text.labels.add(label)
                dataset.users_with_access.add(request.user)
            return Response({"detail": "Dataset imported successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Failed to import dataset: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Created a dataset")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Updated a dataset")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Deleted a dataset")
        return response


class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Text.objects.all()
        else:
            return Text.objects.filter(dataset__users_with_access=user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Created a text")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Updated a text")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Deleted a text")
        return response


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Created a label")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Updated a label")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        ActivityLog.objects.create(user=request.user, action="Deleted a label")
        return response
