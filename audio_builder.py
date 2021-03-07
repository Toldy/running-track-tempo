from pydub import AudioSegment
from pydub.playback import play
from models import *
import logger

class AudioBuilder:

    output_name = 'result'
    sound = None

    def load(self, configuration):
        self.sound = empty_sound()

        # output_name is exercise_name
        self.output_name = configuration.exercise_name

        for exercise in configuration.exercises:
            self.sound = self.sound.append(self.__exercise_to_sound(exercise, configuration.piste_distance, configuration.beeps_per_lap), crossfade=0)
        self.sound = self.sound.append(AudioSegment.from_wav('resources/success.wav'), crossfade=0)

    def build(self):
        self.sound.export(f'{self.output_name}.mp3')

    def duration(self):
        return self.sound.duration_seconds

    def __exercise_to_sound(self, exercise: Exercise, piste_distance, beeps_per_lap):
        beep_of_1_second = build_beep(1)
        one_tour_duration = exercise.durationInMilliseconds * piste_distance / exercise.distance
        between_beeps_duration = one_tour_duration / beeps_per_lap

        print('+ [NEW STEP]')
        print(f'Goal: {exercise.distance} meters in {exercise.durationInMilliseconds / 1000} seconds')
        print(f'Lap time:  {round(one_tour_duration / 1000, 2)}s')
        print(f'Time between beeps: {round(between_beeps_duration / 1000, 2)}s')

        # Build audio
        sound = AudioSegment.silent(0)
        while (round(sound.duration_seconds) * 1000 < exercise.durationInMilliseconds):
            logger.verbose('Before', sound.duration_seconds)

            silent = AudioSegment.silent(between_beeps_duration - beep_of_1_second.duration_seconds * 1000)
            logger.verbose('Silent duration', silent.duration_seconds)

            sound = sound.append(beep_of_1_second, crossfade=0)
            sound = sound.append(silent, crossfade=0)

        sound = sound.append(beep_of_1_second, crossfade=0)
        return sound

def build_beep(seconds):
    return speed_change(AudioSegment.from_mp3('resources/beep.mp3'), 0.75)[:1 * 1000]

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def empty_sound():
    return AudioSegment.silent(0)