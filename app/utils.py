import nlp_analysis.constants as cs
import reviews as rv

FILE_PATH = '/Users/pranav/Desktop/comments_better.txt'


def provide_reviews(file_path):
    with open(file_path) as fr:
        for line in fr:
           yield line.split(':')[1]
import pdb;pdb.set_trace()
review_list = provide_reviews(FILE_PATH)
rv.EventReviews(review_list).generate_object()


def write_language_based_reviews(file_path):
    dir_path = os.path.split(file_path)[0]
    file_name = 'out_{}.txt'
    file_path = os.path.join(dir_path, file_name)

    file_objects = {language:open(file_path.format(language), 'w') for language in sc.LANGUAGES_LIST}

    with open(file_path) as fr:
        for line in fr:
            language = detect_language(line)
            if language not in cs.LANGUAGES_LIST:
                language = cs.SWEDISH
            file_objects[language].write(line)

    [file_obj.close() for file_obj in file_objects.values()]

def normalize_5_to_10(float_number):
    new_number = round(float_number*2)
    return new_number if new_number <= 10 else 10

def normalize_1_to_10(float_number):
    new_number = round(float_number*10)
    return new_number if new_number <= 10 else 10
