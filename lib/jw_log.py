import os
import json
import datetime
import logging
import logging.config

def jw_make_logger(SCRIPT_NAME):
    LOG_PATH = os.path.join('log', SCRIPT_NAME)
    os.makedirs(LOG_PATH, exist_ok=True)

    # log module setting
    formatter = logging.Formatter(u"[%(asctime)-10s][%(name)s][%(levelname)s](%(funcName)s, %(lineno)d) : %(message)s")
    cur_date = datetime.datetime.today().strftime('%Y-%m-%d')

    log = logging.getLogger("main")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    file_handler = logging.FileHandler(filename=LOG_PATH +'/'+cur_date+'.log', encoding='utf8')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    log.setLevel(logging.INFO)

    return log

if __name__ == "__main__":
    test_logger, test_fail_logger = jw_make_logger("log_test")

    test_logger.debug("log_test")
    test_logger.info("log_test")
    test_logger.error("log_test")
    test_fail_logger.debug("log_test")
    test_fail_logger.info("log_test")
    test_fail_logger.error("log_test")
