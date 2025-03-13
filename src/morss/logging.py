import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s::%(levelname)s:%(module)s:%(lineno)d - %(message)s")
    # fh = RotatingFileHandler(filename="logs/morss.log", maxBytes=10 * 1024 * 1024, backupCount=10)
    # fh.level = logging.DEBUG
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
