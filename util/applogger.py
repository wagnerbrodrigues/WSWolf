import logging

class AppLogger:
    logger = None

    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self):
        # Criar o objeto logger
        logger = logging.getLogger('AppLogger')
        logger.setLevel(logging.DEBUG)

        # Definir o formato do log
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Criar o handler do arquivo de log
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)

        # Criar o handler de console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)

        # Adicionar os handlers ao logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Redirecionar warnings para o logger
        logging.captureWarnings(True)

        return logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)
