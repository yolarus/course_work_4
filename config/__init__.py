import logging

main_logger = logging.getLogger("main_logger")
main_file_formater = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "%d.%m.%Y %H:%M:%S")
main_file_handler = logging.FileHandler("logs/main.log", "a")
main_file_handler.setFormatter(main_file_formater)
main_logger.setLevel(logging.DEBUG)
main_logger.addHandler(main_file_handler)
