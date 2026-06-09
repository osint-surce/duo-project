class EventSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'artist', 'date', 'location', 'price', 
                 'description', 'image_url', 'is_active']

    def get_image_url(self, obj):
        return obj.image_url
