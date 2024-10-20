from rest_framework import serializers
from .models import Marathon, Racer, Checkpoint


class RacerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Racer
        fields = ['uid', 'number', 'name', 'team_name', 'km_group', 'age_gender_group']

class MarathonSerializer(serializers.ModelSerializer):
    racers = RacerSerializer(many=True)

    class Meta:
        model = Marathon
        fields = ['marathon_name', 'laps', 'race_date', 'racers']

class MarathonListSerializer(serializers.ModelSerializer):
    marathonUID = serializers.IntegerField(source='id')  # Map the database ID to marathonUID

    class Meta:
        model = Marathon
        fields = ['marathon_name', 'marathonUID', 'laps', 'race_date']


class CheckpointSerializer(serializers.ModelSerializer):
    racerUID = serializers.IntegerField(source='racer.uid')
    stationNumber = serializers.IntegerField(source='station_number')
    checkpointTimes = serializers.DateTimeField(source='checkpoint_time')

    class Meta:
        model = Checkpoint
        fields = ['racerUID', 'stationNumber', 'checkpointTimes']