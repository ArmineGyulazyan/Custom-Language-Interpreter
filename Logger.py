import logging

def setup_logging():
    logging.basicConfig(filename='interpreter_log.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



logger = logging.getLogger(__name__)
setup_logging()
