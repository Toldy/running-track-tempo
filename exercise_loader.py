import logger
import csv
import json
import os

from pytimeparse.timeparse import timeparse
from models import *

def load_configuration(filename='exercise.csv'):
    if filename.endswith('.csv'):
        configuration = load_csv(filename)
    elif filename.endswith('.json'):
        configuration = load_json(filename)

    # exercise_name is exercise's filename
    configuration.exercise_name = os.path.splitext(filename)[0]

    return configuration

def load_csv(filename):
    configuration = Configuration()
    first = True

    with open(filename) as configuration_file:
        reader = csv.DictReader(configuration_file)
        for row in reader:
            logger.verbose(row)
            if first:
                configuration.beeps_per_lap = int(row['time'])
                configuration.piste_distance = int(row['distance'])
                first = False
                continue
            configuration.exercises.append(Exercise(timeparse(row['time']), int(row['distance'])))

    return configuration

def load_json(filename):
    with open(filename) as configuration_file:
        data = json.load(configuration_file)

        configuration = Configuration()
        configuration.beeps_per_lap = data['track']['beeps_per_lap']
        configuration.piste_distance = data['track']['length']

        for exercise in data['exercices']:
            configuration.exercises.append(Exercise(timeparse(exercise['time']), int(exercise['distance'])))

    return configuration