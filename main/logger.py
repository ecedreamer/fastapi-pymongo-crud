import logging

logging.basicConfig(level=logging.INFO, filename="application.log", format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)
