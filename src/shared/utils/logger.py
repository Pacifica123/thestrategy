import logging
from logging.handlers import RotatingFileHandler


def configure_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        fmt = logging.Formatter(
            "%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s"
        )

        # В консоль
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        # В файл с ротацией
        fh = RotatingFileHandler(
            filename="app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
