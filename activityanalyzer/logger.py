import logging
import os


def get_logger(file_name, logger_name):
    directory = os.path.join(os.path.curdir, 'log')
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.mkdir(directory)

    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(file_path)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add handlers to the logger
    if not len(log.handlers):
        log.addHandler(fh)
        log.addHandler(ch)

    return log


if __name__ == '__main__':
    log = get_logger('test.log', __name__)

