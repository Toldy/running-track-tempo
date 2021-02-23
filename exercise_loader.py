import logger
import csv
from pytimeparse.timeparse import timeparse
from models import *

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