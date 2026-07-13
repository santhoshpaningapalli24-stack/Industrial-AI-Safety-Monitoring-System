import logging


def get_logger(name):

    logging.basicConfig(

        level=logging.INFO,

        format=(
            "%(asctime)s "
            "[%(levelname)-8s] "
            "%(name)-20s | "
            "%(message)s"
        )

    )

    return logging.getLogger(name)