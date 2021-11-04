import os
import datetime
import time
import shutil

import numpy as np
import pandas as pd
import requests


try:
    from modules.config import append_log_info, CLASSIFICATION_MODELS, DEFAULT_CLASSIFICATION_MODEL, ensure_directory_exists, get_log_filepath, get_servo_url, save_plot, write_log_info, LOG_DIR_BASES, SAVE_IMAGE_DIR
    from modules.image_module import process_image, save_image
    from modules.process_image_for_servo import calculate_image_clarity, extend_image, get_person_position_x_from_image
    from modules.server_module import handle_default_server_response
    from modules.servo_module import calculate_duty_from_image_position
    from modules.image_classification import load_classification_model_by_name
except ModuleNotFoundError:
    from config import append_log_info, CLASSIFICATION_MODELS, DEFAULT_CLASSIFICATION_MODEL, ensure_directory_exists, get_log_filepath, get_servo_url, save_plot, write_log_info, LOG_DIR_BASES, SAVE_IMAGE_DIR
    from image_module import process_image, save_image
    from process_image_for_servo import calculate_image_clarity, extend_image, get_person_position_x_from_image
    from server_module import handle_default_server_response
    from servo_module import calculate_duty_from_image_position
    from image_classification import load_classification_model_by_name

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True


SAVE_PLOT_OF_PROCESSING_TIMES = False

servo_url = get_servo_url(IS_TEST)

MAX_ITEMS_FOR_TOTAL_TIMES = 10
SAVE_IMAGES_CONTINUOUS_DIR = os.path.join(SAVE_IMAGE_DIR, 'images_continous')

PLOT_FILEPATH = 'image_processor_time'

def get_log_filename():
    time_log_filename_base = 'processing_time_log'
    timestamp = str(datetime.datetime.now())
    return '{}_{}.csv'.format(time_log_filename_base, timestamp)
TIME_LOG_FILENAME = get_log_filename()

def get_stats_filepath():
    return get_log_filepath(LOG_DIR_BASES.IMAGE_PROCESSING_TIME, TIME_LOG_FILENAME)

def get_stats_df():
    filepath = get_stats_filepath()
    if not os.path.isfile(filepath):
        return pd.DataFrame()
    return pd.read_csv(filepath, sep='\t')

def save_plot_of_times(df=None):
    if df is None:
        df = get_stats_df()
    plot = df.drop('objects_detected_count_found', axis=1).plot.line(ylim=(0, 0.6), figsize=(10, 6), grid=True)
    save_plot(PLOT_FILEPATH, plot)

def print_aggregated_stats(send_output):
    df = get_stats_df()

    aggregated_stats = df.median().sort_values()

    output_text = '\n'.join((
        'Median value of stats',
        str(aggregated_stats),
        ''
    ))
    send_output(output_text)


def setup_continous_photos_directory():
    try:
        shutil.rmtree(SAVE_IMAGES_CONTINUOUS_DIR)
        print('Cleaned (removed) directory with continuous images')
    except FileNotFoundError:
        pass
    ensure_directory_exists(SAVE_IMAGES_CONTINUOUS_DIR)
setup_continous_photos_directory()

def save_image_with_objects_detected(img, objects_detected, person_position_x, duty_change, clarity):
    texts = [
        'Person Position: {}'.format(person_position_x),
        'Clarity (anti-blur): {}'.format(int(clarity))
    ]
    if duty_change is not None:
        texts.append('Duty Change: {}'.format(duty_change))
    img_with_objects_detected = extend_image(img, show_objects_detected=True, show_vertical_lines=True, texts=texts, objects_detected=objects_detected)

    # save_image(img, 'image-raw.jpg')
    save_image(img_with_objects_detected, 'test-objects-detected-image.jpg')
    filepath = os.path.join('images_continous', 'img-{}.jpg'.format(str(datetime.datetime.now())))
    save_image(img_with_objects_detected, filepath)


def call_and_get_time(function, args):
    time_start = time.time()
    response = function(*args)

    time_end = time.time()
    time_total = time_end - time_start

    return (response, time_total)

def fps(times):
    total_time = np.sum(times)

    if total_time == 0:
        return 0

    _fps = len(times) / total_time

    return int(_fps)

def calculate_time_spent_average(total_times):
    if len(total_times) == 0:
        return -1
    
    avg = np.mean(total_times)
    return np.round(avg, 2)

def get_stats_text(stats_info):
    text = []
    headers = []
    for (field, value) in stats_info:
        if type(value) == float:
            value = np.round(value, 2)
        if value is None:
            value = ''
        text.append(str(value))
        headers.append(field)

    return text, headers

# TODO: Move global variable to class
time_without_object_detected = None
def set_time_with_out_object_detected():
    global time_without_object_detected
    time_without_object_detected = time.time()

def reset_time_with_out_object_detected():
    global time_without_object_detected
    time_without_object_detected = None

def has_too_much_time_passed_without_object_detected():
    global time_without_object_detected
    if time_without_object_detected is None:
        set_time_with_out_object_detected()
        return False

    new_time = time.time()
    time_diff = new_time - time_without_object_detected

    if time_diff > 3:
        set_time_with_out_object_detected()
        return True

    return False

def get_servo_url_path(path):
    global servo_url
    url = '/'.join([servo_url, path])

    return url

def send_reset_servo():
    url = get_servo_url_path('resetServo')
    print('resetting servo')
    try:
        response = requests.post(url)
        handle_default_server_response(response)
    except requests.exceptions.ConnectionError:
        print('Could not send duty to servo server')

def send_servo_duty(duty_change):
    url = get_servo_url_path('setServoPosition')

    print('Sending request to "{}"'.format(url))
    
    try:
        response = requests.post(url, json={
            "duty": duty_change
        })

        handle_default_server_response(response)
    except requests.exceptions.ConnectionError:
        print('Could not send duty to servo server')

def move_servo_based_on_person_position_x(person_position_x):
    # TODO: Make this available from a config
    center_position = [-0.1, 0.1]
    # No object_detected
    if person_position_x is None:
        if has_too_much_time_passed_without_object_detected():
            send_reset_servo()
        return
    
    reset_time_with_out_object_detected()
    # if dead center, then stay there
    if person_position_x >= center_position[0] and person_position_x <= center_position[1]:
        return
    
    duty_change = calculate_duty_from_image_position(person_position_x)
    
    send_servo_duty(duty_change)
    
    return duty_change

def get_time_delta(time1, time2):
    if time1 is None:
        return None
    
    time_delta = time2 - time1

    return float('{}.{}'.format(time_delta.seconds, time_delta.microseconds))


# This class performs processing on an image and will output various metrics of performance
class Image_Processor:
    stats_info = []
    total_time_list_objects_detected = []
    total_time_list_no_objects_detected = []
    last_image_run_time = None
    images_processed_count = 0
    classification_model = None
    loaded_classification_models = {}
    
    def use_classification_model(self, model_name: CLASSIFICATION_MODELS):
        if model_name not in self.loaded_classification_models:
            self.loaded_classification_models[model_name] = load_classification_model_by_name(model_name)
        
        self.classification_model = self.loaded_classification_models[model_name]
    
    def use_default_classification_model(self):
        self.use_classification_model(DEFAULT_CLASSIFICATION_MODEL)
    
    def add_stat(self, field, value, index=-1):
        if index == -1:
            index = len(self.stats_info)
        self.stats_info.insert(index, (field, value))

    def limit_total_time_stored(self):
        if len(self.total_time_list_objects_detected) > MAX_ITEMS_FOR_TOTAL_TIMES:
            del self.total_time_list_objects_detected[0] # Delete oldest item
        if len(self.total_time_list_no_objects_detected) > MAX_ITEMS_FOR_TOTAL_TIMES:
            del self.total_time_list_no_objects_detected[0] # Delete oldest item

    def print_processing_time_all(self):
        mean_time_objects_detected = calculate_time_spent_average(self.total_time_list_objects_detected)
        mean_time_no_objects_detected = calculate_time_spent_average(self.total_time_list_no_objects_detected)

        fps_objects_detected = fps(self.total_time_list_objects_detected)

        sum_total_time_objects_detected = np.round(np.sum(self.total_time_list_objects_detected), 2)

        print('Takes {} seconds total (average  of {} seconds) to run {} images with objects_detected ({} fps) and {} to run {} imags WITHOUT objects_detected'.format(sum_total_time_objects_detected, mean_time_objects_detected, len(self.total_time_list_objects_detected), fps_objects_detected, mean_time_no_objects_detected, len(self.total_time_list_no_objects_detected)))
    
    def log_processing_time(self, objects_detected):
        last_image_run_time = self.last_image_run_time
        is_first_image = self.last_image_run_time is None
        self.last_image_run_time = datetime.datetime.now()

        time_passed = get_time_delta(last_image_run_time, self.last_image_run_time)

        self.add_stat('objects_detected_count_found', len([] if objects_detected is None else objects_detected))
        self.add_stat('time_passed', time_passed, index=0)
        self.add_stat('ended_at', self.last_image_run_time)

        cells, headers = get_stats_text(self.stats_info)
        if is_first_image:
            write_log_info(LOG_DIR_BASES.IMAGE_PROCESSING_TIME, TIME_LOG_FILENAME, '\t'.join(headers))

        append_log_info(LOG_DIR_BASES.IMAGE_PROCESSING_TIME, TIME_LOG_FILENAME, '\t'.join(cells))

    
    def set_initial_time(self, time_passed_for_image):
        self.add_stat('get_image', time_passed_for_image, index=0)

    def process_image(self, img):
        img, total_time = call_and_get_time(process_image, (img,))
        self.add_stat('process_image', total_time)

        return img
    
    def calculate_image_clarity(self, img):
        clarity, total_time = call_and_get_time(calculate_image_clarity, (img,))
        self.add_stat('calculate_image_clarity', total_time)

        return clarity

    def find_objects_in_image(self, img):
        if self.classification_model is None:
            self.use_default_classification_model()

        objects_detected, total_time = call_and_get_time(self.classification_model.predict, (img,))
        print('objects_detected', objects_detected)
        print()
        self.add_stat('find_objects_in_image', total_time, index=0)

        return objects_detected
    
    def get_people_from_objects_detected(self, objects_detected):
        people = []
        for object_detected in objects_detected:
            if object_detected['name'] in ('person', 'face'):
                people.append(object_detected)
        return people

    # TODO: Draw line in box based on duty change position
    def get_person_position(self, img, objects_detected):
        # TODO: Clean image (make sharper perhaps) to better find objects_detected
        # TODO: Try to find pedestrians as well
        # TODO: Why do we need to pass img in here?
        people_detected = self.get_people_from_objects_detected(objects_detected)
        person_position_x, total_time = call_and_get_time(get_person_position_x_from_image, (img, people_detected))
        self.add_stat('get_objects_detected', total_time)

        return person_position_x
    
    def move_servo(self, person_position_x):
        if IS_TEST:
            return None

        # TODO: Get duty from a seperate method
        duty_change, total_time = call_and_get_time(move_servo_based_on_person_position_x, (person_position_x,))
        self.add_stat('turn_servo', total_time)

        return duty_change
    
    def set_time_to_run_all_stat(self, time_start, objects_detected):
        time_all_end = time.time()
        time_all_total = (time_all_end - time_start)
        if objects_detected is not None and len(objects_detected) > 0:
            self.total_time_list_objects_detected.append(time_all_total)
        else:
            self.total_time_list_no_objects_detected.append(time_all_total)

        self.add_stat('time_total', time_all_total, index=0)
    
    def save_image_with_objects_detected(self, img, objects_detected, person_position_x, duty_change, clarity):
        _, total_time = call_and_get_time(save_image_with_objects_detected, (img, objects_detected, person_position_x, duty_change, clarity))
        self.add_stat('save_images', total_time, index=1)
    
    def save_plot_of_times(self):
        if self.images_processed_count > 0:
            _, total_time = call_and_get_time(save_plot_of_times, [])
        else:
            total_time = 0
        self.add_stat('save_plot_of_times', total_time, index=1)
    
    def print_aggregated_stats(self, send_output):
        if self.images_processed_count > 0:
            _, total_time = call_and_get_time(print_aggregated_stats, (send_output,))
        else:
            total_time = 0
        self.add_stat('print_aggregated_stats', total_time, index=1)

    def process_message_immediately(self, img, time_passed_for_image, time_all_start, send_output=print):
        self.set_initial_time(time_passed_for_image)        

        img = self.process_image(img)

        # TODO: Use this to determine if we should keep the image or get a new image - if the image is too blurry, that means the servo is probably moving
        clarity = self.calculate_image_clarity(img)

        objects_detected = self.find_objects_in_image(img)

        person_position_x = self.get_person_position(img, objects_detected)

        duty_change = self.move_servo(person_position_x)

        self.save_image_with_objects_detected(img, objects_detected, person_position_x, duty_change, clarity)

        if SAVE_PLOT_OF_PROCESSING_TIMES:
            self.save_plot_of_times()

        self.print_aggregated_stats(send_output)
        self.set_time_to_run_all_stat(time_all_start, objects_detected)
        self.limit_total_time_stored()

        self.log_processing_time(objects_detected)
        # self.print_processing_time_all()
        self.stats_info = []

        self.images_processed_count += 1
        
        # Give time for the servo server to change before getting a new image
        # TODO: Make this smarter
        if duty_change is not None:
            time.sleep(0.1)
