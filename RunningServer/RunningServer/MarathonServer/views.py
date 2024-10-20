from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Marathon, Racer, Checkpoint, Station, Summary
from .serializers import MarathonSerializer, RacerSerializer, MarathonListSerializer, CheckpointSerializer
from django.db import transaction
from django.db.models import Min
import random
from datetime import timedelta

@api_view(['POST'])
def new_marathon(request):
    data = request.data
    marathon_name = data.get('marathonName')
    station_number = data.get('stationNumber')
    race_date = request.data.get('raceDate')
    gun_time = request.data.get('gunTime')  # Make sure gun_time is passed as a datetime
    status = request.data.get('status', 'upcoming')
    racers_data = request.data.get('racers', [])

    try:
        # Create or update the marathon
        marathon, created = Marathon.objects.get_or_create(
            marathon_name=marathon_name,
            race_date=race_date,
            defaults={'station_number': station_number, 'gun_time': gun_time, 'status': status}
        )

        if not created:
            print(f"Marathon already exists with ID {marathon.id}")
            return Response({'marathon_id': marathon.id}, status=200)

        # Process each racer independently
        with transaction.atomic():
            for racer_data in racers_data:
                racer_serializer = RacerSerializer(data=racer_data)

                if racer_serializer.is_valid():
                    racer = racer_serializer.save(marathon=marathon)

                    # Initialize a summary for each racer
                    summary = Summary.objects.create(
                        racer=racer,
                        gun_time=gun_time,  # This should be a datetime object
                        start_time=gun_time,  # Placeholder
                        end_time=gun_time,  # Placeholder
                        personal_record=timedelta(hours=random.randint(2, 4), minutes=random.randint(0, 59)),  # Placeholder
                        marathon_record=timedelta(hours=random.randint(2, 4), minutes=random.randint(0, 59))  # Placeholder
                    )
                    print(f"Summary created for racer {racer.uid}")

                else:
                    print(f"Invalid racer data: {racer_serializer.errors}")
                    return Response(racer_serializer.errors, status=400)

        return Response({'marathon_id': marathon.id}, status=201)

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': str(e)}, status=400)
@api_view(['POST'])
def modify_gun_time(request):
    try:
        # Extract the marathon ID and new gun time from the request
        marathon_id = request.data.get('marathonUID')
        new_gun_time = request.data.get('gunTime')

        # Ensure both fields are present in the request
        if not marathon_id or not new_gun_time:
            return Response({"error": "Marathon ID and Gun Time are required."}, status=400)

        # Parse the new gun time string into a datetime object
        parsed_gun_time = parse_datetime(new_gun_time)
        if not parsed_gun_time:
            return Response({"error": "Invalid Gun Time format. Use ISO 8601 format."}, status=400)

        # Fetch the marathon by ID
        marathon = Marathon.objects.get(id=marathon_id)

        # Update the gun time
        marathon.gun_time = parsed_gun_time
        marathon.save()

        return Response({"status": "Gun Time updated successfully", "new_gun_time": marathon.gun_time}, status=200)

    except Marathon.DoesNotExist:
        return Response({"error": "Marathon not found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def update_status(request):
    try:
        # Extract the marathon ID and new status from the request data
        marathon_id = request.data.get('marathon_id')
        new_status = request.data.get('status')

        # Ensure the status is either 'start' or 'end'
        if new_status not in ['start', 'end']:
            return Response({"error": "Invalid status. Status must be 'start' or 'end'."}, status=400)

        # Find the marathon by ID
        try:
            marathon = Marathon.objects.get(id=marathon_id)
        except Marathon.DoesNotExist:
            return Response({"error": "Marathon not found."}, status=404)

        # Update the marathon's status
        marathon.status = new_status
        marathon.save()

        return Response({"status": "success", "new_status": marathon.status}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def get_marathon(request):
    try:
        # Retrieve all marathon records from the database
        marathons = Marathon.objects.all()

        # Serialize the marathon data
        serializer = MarathonListSerializer(marathons, many=True)

        # Return serialized data as a response
        return Response(serializer.data, status=200)

    except Exception as e:
        # Handle any unexpected errors
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
def delete_marathon(request):
    # Extract marathon ID from the request data
    marathon_id = request.data.get('marathonUID')

    if not marathon_id:
        return Response({"error": "Marathon ID is required"}, status=400)

    try:
        # Try to find the marathon by its ID
        marathon = Marathon.objects.get(id=marathon_id)

        # Delete the marathon
        marathon.delete()

        # Return success message
        return Response({"status": "succeed"}, status=200)

    except Marathon.DoesNotExist:
        # Handle the case where the marathon does not exist
        return Response({"error": "Marathon not found"}, status=404)

    except Exception as e:
        # Handle any other unexpected errors
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def modify_station_name(request):
    try:
        # Extract station_number, marathon_id, and new station_name from the request
        marathon_id = request.data.get('marathonUID')
        station_number = request.data.get('stationNumber')
        new_station_name = request.data.get('stationName')

        # Ensure all fields are present in the request
        if not marathon_id or not station_number or not new_station_name:
            return Response({"error": "Marathon ID, Station Number, and Station Name are required."}, status=400)

        # Find the station by marathon and station number
        station = Station.objects.get(marathon__id=marathon_id, station_number=station_number)

        # Update the station name
        station.station_name = new_station_name
        station.save()

        return Response({"status": "Station Name updated successfully", "new_station_name": station.station_name}, status=200)

    except Station.DoesNotExist:
        return Response({"error": "Station not found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def modify_km_group(request):
    try:
        # Extract data from the request
        racer_uid = request.data.get('uid')
        marathon_id = request.data.get('marathonUID')
        new_km_group = request.data.get('kmGroup')

        # Ensure all required fields are present
        if not racer_uid or not marathon_id or not new_km_group:
            return Response({"error": "Racer UID, Marathon ID, and KM Group are required."}, status=400)

        # Fetch the racer using the uid and marathon ID
        racer = Racer.objects.get(uid=racer_uid, marathon__id=marathon_id)

        # Update the km_group
        racer.km_group = new_km_group
        racer.save()

        return Response({"status": "KM Group updated successfully", "new_km_group": racer.km_group}, status=200)

    except Racer.DoesNotExist:
        return Response({"error": "Racer not found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def modify_age_gender_group(request):
    try:
        # Extract data from the request
        racer_uid = request.data.get('uid')
        marathon_id = request.data.get('marathonUID')
        new_age_gender_group = request.data.get('ageGenderGroup')

        # Ensure all required fields are present
        if not racer_uid or not marathon_id or not new_age_gender_group:
            return Response({"error": "Racer UID, Marathon ID, and Age/Gender Group are required."}, status=400)

        # Fetch the racer using the uid and marathon ID
        racer = Racer.objects.get(uid=racer_uid, marathon__id=marathon_id)

        # Update the age_gender_group
        racer.age_gender_group = new_age_gender_group
        racer.save()

        return Response({"status": "Age/Gender Group updated successfully", "new_age_gender_group": racer.age_gender_group}, status=200)

    except Racer.DoesNotExist:
        return Response({"error": "Racer not found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def update_checkpoints(request):
    try:
        # Extract marathon ID and racers from the request
        marathon_id = request.data.get('marathonUID')
        racers_data = request.data.get('racers')  # Expecting multiple racers

        # Find the marathon
        try:
            marathon = Marathon.objects.get(id=marathon_id)
        except Marathon.DoesNotExist:
            return Response({"error": "Marathon not found."}, status=404)

        # Track missing racers
        missing_racers = []

        # Process each racer
        for racer_data in racers_data:
            racer_uid = racer_data.get('racerUID')
            station_number = racer_data.get('stationNumber')
            checkpoint_time = racer_data.get('checkpointTimes')

            # Find the racer
            try:
                racer = Racer.objects.get(uid=racer_uid, marathon=marathon)
            except Racer.DoesNotExist:
                missing_racers.append(racer_uid)  # Add to the missing racers list
                continue  # Skip the rest of the processing for this racer

            # Update checkpoint for the racer
            Checkpoint.objects.create(
                marathon=marathon,
                racer=racer,
                station_number=station_number,
                checkpoint_time=checkpoint_time
            )

            # If this is the final station, update the Summary table
            if station_number == marathon.station_number:  # Final station reached
                first_checkpoint = Checkpoint.objects.filter(
                    marathon=marathon, racer=racer, station_number=1
                ).first()

                final_checkpoint = Checkpoint.objects.filter(
                    marathon=marathon, racer=racer, station_number=station_number
                ).first()

                if first_checkpoint and final_checkpoint:
                    start_time = first_checkpoint.checkpoint_time
                    end_time = final_checkpoint.checkpoint_time

                    personal_time = end_time - start_time
                    marathon_time = end_time - marathon.gun_time

                    # Update the Summary table for the racer
                    summary, created = Summary.objects.get_or_create(racer=racer)
                    summary.start_time = start_time
                    summary.end_time = end_time
                    summary.personal_record = personal_time
                    summary.marathon_record = marathon_time
                    summary.save()

        # If there are missing racers, return their UIDs
        if missing_racers:
            return Response({"error": f"Racers not found: {', '.join(map(str, missing_racers))}"}, status=404)

        return Response({"status": "success", "message": "Checkpoints updated for all racers"}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def get_racer_results(request):
    # Extract marathon and racer IDs from the request
    marathon_id = request.data.get('marathonUID')
    racer_uid = request.data.get('racerUID')

    if not marathon_id or not racer_uid:
        return Response({"error": "Marathon ID and Racer UID are required"}, status=400)

    try:
        # Fetch marathon and racer details
        marathon = Marathon.objects.get(id=marathon_id)
        racer = Racer.objects.get(uid=racer_uid, marathon=marathon)

        # Fetch all checkpoints for the racer in this marathon
        checkpoints = Checkpoint.objects.filter(marathon=marathon, racer=racer).order_by('station_number')

        # Calculate overall rank based on the last checkpoint time of each racer
        overall_ranks = (
            Checkpoint.objects
            .filter(marathon=marathon)
            .values('racer')
            .annotate(last_time=Min('checkpoint_time'))
            .order_by('last_time')
        )

        # Get the racer's overall rank by enumerating over sorted results
        overall_rank = next((index + 1 for index, rank in enumerate(overall_ranks) if rank['racer'] == racer.id), None)

        # Calculate gender rank by filtering racers of the same group
        gender_ranks = (
            Checkpoint.objects
            .filter(marathon=marathon, racer__group=racer.group)
            .values('racer')
            .annotate(last_time=Min('checkpoint_time'))
            .order_by('last_time')
        )

        # Get the racer's gender rank by enumerating over sorted results
        gender_rank = next((index + 1 for index, rank in enumerate(gender_ranks) if rank['racer'] == racer.id), None)

        # Prepare station times
        station_times = [{'time': checkpoint.checkpoint_time.isoformat()} for checkpoint in checkpoints]

        # Prepare response data
        response_data = {
            "marathonName": marathon.marathon_name,
            "laps": marathon.laps,
            "raceDate": marathon.race_date.isoformat(),
            "group": racer.group,
            "rank": overall_rank,
            "genderRank": gender_rank,
            "station": station_times,
        }

        return Response(response_data, status=200)

    except Marathon.DoesNotExist:
        return Response({"error": "Marathon not found"}, status=404)
    except Racer.DoesNotExist:
        return Response({"error": "Racer not found in this marathon"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)