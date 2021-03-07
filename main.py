from exercise_loader import load_configuration
from exercise_loader import Exercise
from audio_builder import AudioBuilder
import sys
import logger

exercice_filename = sys.argv[-1] if len(sys.argv) == 2 else "exercise.csv"

configuration = load_configuration(exercice_filename)

print(f'Track length: {configuration.piste_distance} meters')
print(f'{configuration.beeps_per_lap} beeps per lap\n')

audio_builder = AudioBuilder()
audio_builder.load(configuration)

print('\nBuilding audio file... This may take several seconds...')
audio_builder.build()
print(f'✅ Audio created: ./{audio_builder.output_name}.mp3 Duration: {round(audio_builder.duration(), 2)}s')
