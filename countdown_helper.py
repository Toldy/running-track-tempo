import pyttsx3
import os

import logger

class CountdownHelper:

    file_name = 'countdown.mp3'

    @staticmethod
    def new_countdown(starting_number=5):
        engine = pyttsx3.init()

        countdown_numbers = reversed(range(1, starting_number + 1))
        full_countdown_array = [str(num) for num in countdown_numbers] + ['GO!']
        full_countdown = ', '.join(full_countdown_array)

        engine.save_to_file(full_countdown, CountdownHelper.file_name)
        engine.runAndWait()
        
        logger.verbose(f'Countdown is: {full_countdown}')
        logger.verbose(f'Countdown saved to {CountdownHelper.file_name}')
    
    @staticmethod
    def clear_resources():
        os.remove(CountdownHelper.file_name)
