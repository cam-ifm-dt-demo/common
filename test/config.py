from pprint import pprint

from cam_ifm_dt_demo.common.config import config

pprint(config.model_dump(), sort_dicts=False)
