from account.models import Account
from household.models.book import Book
from household.models.tag import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class BookSerializer(serializers.ModelSerializer):
    account = serializers.ReadOnlyField(source='account.id')
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), write_only=True)
    tag = TagSerializer(read_only=True)
    tag_uid = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), write_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'money', 'date', 'tag',
                  'tag_uid', 'account', 'account_id', 'created_at',
                  'updated_at']

    def create(self, validated_data):
        validated_data['account'] = validated_data.get('account_id', None)
        validated_data['tag'] = validated_data.get('tag_uid', None)

        if validated_data['account'] is None:
            raise serializers.ValidationError("アカウントが選択されてません")

        if validated_data['tag'] is None:
            raise serializers.ValidationError("タグが選択されてません")

        del validated_data['account_id']
        del validated_data["tag_uid"]

        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['tag'] = validated_data.get('tag_uid', None)

        instance.title = validated_data.get('title', instance.title)
        instance.money = validated_data.get('money', instance.money)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()

        return instance


class TestSerializer(serializers.Serializer):
    total = serializers.IntegerField()


class TotalByDateSerializer(serializers.Serializer):
    date = serializers.DateField()
    total = serializers.IntegerField()


class TotalByTagSerializer(serializers.Serializer):
    tag__name = serializers.CharField()
    tag__color = serializers.CharField()
    total = serializers.IntegerField()


class PeriodSerializer(serializers.Serializer):
    date = serializers.DateField()
