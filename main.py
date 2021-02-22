from pydub import AudioSegment
from pydub.playback import play
from exercise_loader import load_configuration
from exercise_loader import Exercise
import logger


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

BEEP_1_SECOND = speed_change(AudioSegment.from_mp3('resources/beep.mp3'), 0.75)[:1 * 1000]


def exercie_to_sound(exercise: Exercise, piste_distance, beeps_per_tour):
    one_tour_duration = exercise.durationInMilliseconds * piste_distance / exercise.distance
    between_beeps_duration = one_tour_duration / beeps_per_tour

    print('+ [NEW STEP]')
    print(f'Goal: {exercise.distance} meters in {exercise.durationInMilliseconds / 1000} seconds')
    print(f'Lap time:  {one_tour_duration / 1000}s')
    print(f'Time between beeps: {between_beeps_duration / 1000}s')

    # Build audio
    sound = AudioSegment.silent(0)
    while (round(sound.duration_seconds) * 1000 < exercise.durationInMilliseconds):
        logger.verbose('Before', sound.duration_seconds)

        beep = BEEP_1_SECOND
        silent = AudioSegment.silent(between_beeps_duration - beep.duration_seconds * 1000)
        logger.verbose('Silent duration', silent.duration_seconds)

        sound = sound.append(beep, crossfade=0)
        sound = sound.append(silent, crossfade=0)

    sound = sound.append(BEEP_1_SECOND, crossfade=0)
    return sound

configuration = load_configuration('exercise.csv')


print(f'Track length: {configuration.piste_distance} meters')
print(f'{configuration.beeps_per_tour} beeps per lap\n')

sound = empty_sound()
for exercise in configuration.exercises:
    sound = sound.append(exercie_to_sound(exercise, configuration.piste_distance, configuration.beeps_per_tour), crossfade=0)
sound = sound.append(AudioSegment.from_wav('resources/success.wav'), crossfade=0)

print('\nBuilding audio file... This may take several seconds...')
sound.export('result.mp3')
print(f'✅ Audio created: ./result.mp3 Duration: {sound.duration_seconds}s')
# play(sound)