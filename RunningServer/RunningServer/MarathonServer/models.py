from django.db import models
from django.utils import timezone
import uuid
class Marathon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Automatically generates unique UUIDs
    marathon_name = models.CharField(max_length=255, unique=True)
    station_number = models.IntegerField() # Renamed from 'laps' to 'station'
    race_date = models.DateTimeField()
    gun_time = models.DateTimeField()  # New field for Gun Time
    status = models.CharField(max_length=50, default="upcoming")  # New field for marathon status (e.g., upcoming, ongoing, completed)

class Station(models.Model):
    marathon = models.ForeignKey(Marathon, related_name='stations', on_delete=models.CASCADE)
    station_number = models.IntegerField()
    station_name = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f'Station {self.station_number}: {self.station_name}'

class Racer(models.Model):
    uid = models.IntegerField()  # Racer UID (number within marathon)
    marathon = models.ForeignKey(Marathon, related_name='racers', on_delete=models.CASCADE)  # Moved to second position
    number = models.IntegerField()  # Bib number
    name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    km_group = models.CharField(max_length=255, blank=True, null=True)  # Renamed from 'group' to 'km_group'
    age_gender_group = models.CharField(max_length=255, blank=True, null=True)  # Renamed from 'note' to 'age_gender_group'
    class Meta:
        unique_together = ('marathon', 'uid')
class Checkpoint(models.Model):
    marathon = models.ForeignKey(Marathon, related_name='checkpoints', on_delete=models.CASCADE)
    racer = models.ForeignKey(Racer, related_name='checkpoints', on_delete=models.CASCADE)
    station_number = models.IntegerField()
    checkpoint_time = models.DateTimeField()

class Summary(models.Model):
    racer = models.OneToOneField('Racer', on_delete=models.CASCADE, primary_key=True)  # Primary key linked to Racer
    gun_time = models.DateTimeField()  # Fetched from the Marathon table
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    personal_record = models.DurationField()  # Duration of personal best time
    marathon_record = models.DurationField()  # Duration of this marathon's record

    def __str__(self):
        return f"Summary for Racer {self.racer.uid}"