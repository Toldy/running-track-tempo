class Exercise:

    def __init__(self, duration: int, distance: int):
        super().__init__()
        self.durationInMilliseconds = duration * 1000
        self.distance = distance

class Configuration:
    beeps_per_lap = 0
    piste_distance = 0
    exercises = []