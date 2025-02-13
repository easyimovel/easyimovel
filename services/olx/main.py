import argparse
import logging

from dotenv import load_dotenv
from pprint import pprint, pformat
from requests_olx import OLX

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OLX GetLinks")

def main(action: str):
    olx = OLX(logger)

    if action == "get":
        olx.get_links()

    if action == "scrap":
        olx.get_data_from_urls()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Integração com a API OLX.")
    parser.add_argument('action', choices=['get', 'scrap'], help="Ação a ser executada (get ou post)")
    args = parser.parse_args()
    main(args.action)
