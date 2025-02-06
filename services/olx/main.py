import argparse
import logging

from pprint import pprint, pformat

from requests import OLX

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OLX GetLinks")

def main():
    logger.debug("foi")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Integração com a API OLX.")
    parser.add_argument('action', choices=['get', 'post'], help="Ação a ser executada (get ou post)")
    args = parser.parse_args()
    pprint(pformat(args))
    main(args.action)
