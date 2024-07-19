from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        user = self.context["request"].user

        # Проверка на количество открытых объявлений
        open_ads_count = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN).count()
        if self.instance:
            # Если объявление обновляется, не учитываем его в подсчете
            open_ads_count -= 1

        if data.get('status') == AdvertisementStatusChoices.OPEN and open_ads_count >= 10:
            raise serializers.ValidationError("Вы не можете иметь больше 10 открытых объявлений.")

        # Проверка статуса при обновлении
        if self.instance and self.instance.status == AdvertisementStatusChoices.CLOSED and data.get(
                'status') == AdvertisementStatusChoices.OPEN:
            raise serializers.ValidationError("Нельзя менять статус с 'Закрыто' на 'Открыто'.")

        return data
