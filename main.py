from exercise_loader import load_configuration
from exercise_loader import Exercise
from audio_builder import AudioBuilder
import logger

configuration = load_configuration('exercise.csv')

print(f'Track length: {configuration.piste_distance} meters')
print(f'{configuration.beeps_per_tour} beeps per lap\n')


audio_builder = AudioBuilder()
audio_builder.output_name = ''
audio_builder.load(configuration)

print('\nBuilding audio file... This may take several seconds...')
audio_builder.build()
print(f'✅ Audio created: ./result.mp3 Duration: {audio_builder.duration()}s')
