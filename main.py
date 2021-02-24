from exercise_loader import load_configuration
from exercise_loader import Exercise
from audio_builder import AudioBuilder
import sys
import logger

if len(sys.argv) == 2:
    configuration = load_configuration(sys.argv[-1])
else:
    configuration = load_configuration('exercise.csv')


print(f'Track length: {configuration.piste_distance} meters')
print(f'{configuration.beeps_per_lap} beeps per lap\n')


audio_builder = AudioBuilder()
audio_builder.output_name = 'exercice'
audio_builder.load(configuration)

print('\nBuilding audio file... This may take several seconds...')
audio_builder.build()
print(f'✅ Audio created: ./result.mp3 Duration: {round(audio_builder.duration(), 2)}s')
