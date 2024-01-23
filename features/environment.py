import logging
import os
import sys
from logging import DEBUG, INFO

if not os.getenv("BASE_URL"):
    raise EnvironmentError(
        """BASE_URL environment variable is not set on this machine. Tests will not run.
        See 'readme.md' for more information on how to set this variable"""
    )
EPS_BASE_URL = os.getenv("BASE_URL")
EPS_PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")


def before_all(context):
    if is_debug(context):
        setup_logging(level=DEBUG)
    else:
        setup_logging(level=INFO)
        
    eps_pr_suffix = build_pull_request_id(EPS_PULL_REQUEST_ID)

    context.base_url = EPS_BASE_URL + "electronic-prescriptions"
    
    logging.info("Using BASE_URL: '%s'", context.base_url)

def after_all(context):
    return
    # Add anything you want to happen after all the tests have completed here


def setup_logging(level: int = logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
        handlers=handlers,
    )


def is_debug(context):
    try:
        debug = context.config.userdata["debug"]
    except KeyError:
        print("Running in Normal mode")
        return False
    if str(debug) == "True":
        print("Running in DEBUG mode")
        return True
    print("Running in Normal mode")
    return False

def build_pull_request_id(id):
    pr_suffix = f"-pr-{id}" if id else ""
    return pr_suffix