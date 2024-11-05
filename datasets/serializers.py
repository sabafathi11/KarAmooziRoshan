from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Label, Dataset, Text, User


class LabelSerializer(serializers.ModelSerializer):

    dataset = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all(), required=False)

    class Meta:
        model = Label
        fields = ['id', 'name', 'dataset', 'is_active']


class DatasetSerializer(serializers.ModelSerializer):

    labels = LabelSerializer(many=True, required=False)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'title', 'created_by', 'labels', 'labeled_texts']
        read_only_fields = ['labeled_texts', 'created_by']

    def create(self, validated_data):
        labels_data = validated_data.pop('labels')
        user = self.context['request'].user
        dataset = Dataset.objects.create(created_by=user, **validated_data)
        for label_data in labels_data:
            Label.objects.create(dataset=dataset, **label_data)
        dataset.users_with_access.add(user)
        return dataset

    def update(self, instance, validated_data):
        if 'labels' in validated_data:
            labels_data = validated_data.pop('labels')
        else:
            labels_data = None
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        if labels_data:
            instance.labels.all().delete()
            instance.save()
            for label_data in labels_data:
                if 'dataset' not in label_data:
                    Label.objects.create(dataset=instance, **label_data)
                else:
                    Label.objects.create(**label_data)
        return instance


class TextSerializer(serializers.ModelSerializer):

    labels = serializers.SlugRelatedField(
        queryset=Label.objects.all(),
        many=True,
        allow_null=True,
        slug_field='name')
    dataset = serializers.SlugRelatedField(
        queryset=Dataset.objects.all(),
        allow_null=False,
        many=False,
        slug_field='title')

    class Meta:
        model = Text
        fields = ['id', 'content', 'dataset', 'labels']

    def create(self, validated_data):
        labels_data = validated_data.pop('labels')
        text = Text.objects.create(**validated_data)
        text.labels.set(labels_data)
        return text

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.dataset = validated_data.get('dataset', instance.dataset)
        labels_data = validated_data.pop('labels', None)
        if labels_data:
            instance.labels.set(labels_data)
        instance.save()
        return instance

    def validate(self, attrs):
        dataset = attrs.get('dataset')
        labels = attrs.get('labels')
        if labels and dataset:
            for label in labels:
                if label.dataset != dataset:
                    raise serializers.ValidationError(f"Label {label.name} does not belong to the dataset.")
                elif not label.is_active:
                    raise serializers.ValidationError(f"Label {label.name} is not active.")
        return attrs
