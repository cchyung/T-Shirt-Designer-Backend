from rest_framework import serializers
from api import models


class StyleColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StyleColor
        fields = (
            'color',
            'slug',
            'hex'
        )


class StyleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StyleImage
        fields = (
            'front',
            'back',
        )


class StyleSerializer(serializers.ModelSerializer):
    colors = StyleColorSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        image_set = models.StyleImage.objects.filter(style=obj)
        if image_set.count > 0:
            # get first non null image in set
            for image in image_set:
                if image.front is not None:
                    return StyleImageSerializer(image).data
            return StyleImageSerializer(image_set.first()).data
        else:
            return None

    class Meta:
        model = models.Style
        fields = (
            'uuid',
            'style_id',
            'name',
            'brand',
            'description',
            'colors',
            'images'
        )


class AddonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Addon
        fields = (
            'id',
            'name'
        )
