import logger
import csv
from pytimeparse.timeparse import timeparse

class Exercise:

    def __init__(self, duration: int, distance: int):
        super().__init__()
        self.durationInMilliseconds = duration * 1000
        self.distance = distance

class Configuration:
    beeps_per_tour = 0
    piste_distance = 0
    exercises = []

def load_configuration(filename='exercise.csv'):
    configuration = Configuration()
    first = True
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            logger.verbose(row)
            if first:
                configuration.beeps_per_tour = int(row['time'])
                configuration.piste_distance = int(row['distance'])
                first = False
                continue
            configuration.exercises.append(Exercise(timeparse(row['time']), int(row['distance'])))
    
    return configuration