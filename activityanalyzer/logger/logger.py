import logging


def get_logger(file_name, logger_name):
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    if not len(log.handlers):
        log.addHandler(fh)
        log.addHandler(ch)
    return log


if __name__ == '__main__':
    log = get_logger('test.log', __name__)
