import logging
import os
import shutil
import sys

from behave.model import Scenario
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from methods.api import eps_api_methods

load_dotenv(override=True)
global _page
global _playwright
INTERNAL_QA_BASE_URL = "https://internal-qa.api.service.nhs.uk/"
INTERNAL_DEV_BASE_URL = "https://internal-dev.api.service.nhs.uk/"
INT_BASE_URL = "https://int.api.service.nhs.uk/"
SANDBOX_DEV_BASE_URL = "https://internal-dev-sandbox.api.service.nhs.uk/"
SANDBOX_INT_BASE_URL = "https://sandbox.api.service.nhs.uk/"
REF_BASE_URL = "https://ref.api.service.nhs.uk/"

LOCALHOST_URL = "http://localhost:3000/"

AWS_BASE_URL = ".eps.national.nhs.uk/"
PFP_AWS_PR_URL = "https://pfp-{{aws_pull_request_id}}.dev.eps.national.nhs.uk/"
PFP_AWS_SANDBOX_PR_URL = (
    "https://pfp-{{aws_pull_request_id}}-sandbox.dev.eps.national.nhs.uk/"
)
CPTS_UI_PR_URL = "https://cpt-ui-{{aws_pull_request_id}}.dev.eps.national.nhs.uk/"
CPTS_UI_SANDBOX_PR_URL = (
    "https://cpt-ui-{{aws_pull_request_id}}sandbox.dev.eps.national.nhs.uk/"
)

APIGEE_ENVS = {
    "INTERNAL-DEV": INTERNAL_DEV_BASE_URL,
    "INTERNAL-QA": INTERNAL_QA_BASE_URL,
    "INT": INT_BASE_URL,
    "REF": REF_BASE_URL,
    "INTERNAL-DEV-SANDBOX": SANDBOX_DEV_BASE_URL,
    "SANDBOX": SANDBOX_INT_BASE_URL,
    "LOCALHOST": LOCALHOST_URL,
}

AWS_ENVS = {
    "INTERNAL-DEV": f".dev{AWS_BASE_URL}",
    "INTERNAL-QA": f".qa{AWS_BASE_URL}",
    "INT": f".int{AWS_BASE_URL}",
    "REF": f".ref{AWS_BASE_URL}",
    "INTERNAL-DEV-SANDBOX": f".sandbox{AWS_BASE_URL}",
    "SANDBOX": f".sandbox.dev{AWS_BASE_URL}",
}

CIS2_USERS = {
    "prescriber": {"user_id": "656005750107", "role_id": "555254242105"},
    "dispenser": {"user_id": "555260695103", "role_id": "555265434108"},
}
LOGIN_USERS = {"user_id": "9449304130"}
MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES = "555043308597"
MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE = "555083343101"
MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE = "555043300081"
MOCK_CIS2_LOGIN_ID_NO_ROLES = "555073103101"
MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE = "555043304334"

REPOS = {
    "CPTS-UI": "https://github.com/NHSDigital/eps-prescription-tracker-ui",
    "EPS-FHIR": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "EPS-FHIR-PRESCRIBING": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "EPS-FHIR-DISPENSING": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "PFP-APIGEE": "https://github.com/NHSDigital/prescriptions-for-patients",
    "PFP-AWS": "https://github.com/NHSDigital/prescriptionsforpatients",
    "PSU": "https://github.com/NHSDigital/eps-prescription-status-update-api",
}

CERTIFICATE = os.getenv("CERTIFICATE")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_KID = os.getenv("JWT_KID")
HEADLESS = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")

CPTS_UI_PREFIX = "cpt-ui"
EPS_FHIR_SUFFIX = "electronic-prescriptions"
EPS_FHIR_PRESCRIBING_SUFFIX = "fhir-prescribing"
EPS_FHIR_DISPENSING_SUFFIX = "fhir-dispensing"
PFP_SUFFIX = "prescriptions-for-patients"
PSU_SUFFIX = "prescription-status-update"


def count_of_scenarios_to_run(context):
    tags = context.config.tags
    total_scenarios = sum(
        1
        for feature in context._runner.features
        for scenario in feature.walk_scenarios()
        if isinstance(scenario, Scenario)
        and (not tags or scenario.should_run_with_tags(tags))
    )

    print(f"Total scenarios to be run: {total_scenarios}")
    return total_scenarios


def before_scenario(context, scenario):
    product = context.config.userdata["product"].upper()
    if product == "CPTS-UI":
        global _playwright
        global _page
        context.browser = context.browser.new_context()
        context.page = context.browser.new_page()
        _page = context.page
        set_page(context, _page)


def after_scenario(context, scenario):
    if context.page is not None:
        global _page
        _page.close()


def before_all(context):
    product = context.config.userdata["product"].upper()
    if count_of_scenarios_to_run(context) != 0:
        env = context.config.userdata["env"].upper()
        print(f"Environment: {env}")

        # Currently, only the CPT-UI product is supported for local testing
        if env == "LOCALHOST":
            context.cpts_ui_base_url = LOCALHOST_URL

        else:
            context.cpts_ui_base_url = (
                f"https://{CPTS_UI_PREFIX}" + select_aws_base_url(env)
            )

        context.eps_fhir_base_url = os.path.join(
            select_apigee_base_url(env), EPS_FHIR_SUFFIX
        )
        context.eps_fhir_prescribing_base_url = os.path.join(
            select_apigee_base_url(env), EPS_FHIR_PRESCRIBING_SUFFIX
        )
        context.eps_fhir_dispensing_base_url = os.path.join(
            select_apigee_base_url(env), EPS_FHIR_DISPENSING_SUFFIX
        )
        context.pfp_base_url = os.path.join(select_apigee_base_url(env), PFP_SUFFIX)
        context.psu_base_url = os.path.join(select_apigee_base_url(env), PSU_SUFFIX)

        if PULL_REQUEST_ID and env != "LOCALHOST":
            print(f"--- Using pull request id: '{PULL_REQUEST_ID}'")
            pull_request_id = PULL_REQUEST_ID.lower()
            if "pr-" in pull_request_id:
                get_url_with_pr(context, env, product)

    else:
        raise RuntimeError("no tests to run. Check your tags and try again")
    if product == "CPTS-UI":
        global _playwright
        _playwright = sync_playwright().start()
        context.browser = _playwright.chromium.launch(
            headless=False, channel="chrome"
        )

    eps_api_methods.calculate_eps_fhir_base_url(context)
    print("CPTS-UI: ", context.cpts_ui_base_url)
    print("EPS: ", context.eps_fhir_base_url)
    print("EPS-PRESCRIBING: ", context.eps_fhir_prescribing_base_url)
    print("EPS-DISPENSING: ", context.eps_fhir_dispensing_base_url)
    print("PFP: ", context.pfp_base_url)
    print("PSU: ", context.psu_base_url)


def get_url_with_pr(context, env, product):
    assert PULL_REQUEST_ID is not None
    if product == "EPS-FHIR":
        context.eps_fhir_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{EPS_FHIR_SUFFIX}-{PULL_REQUEST_ID}"
        )
    if product in ["EPS-FHIR-PRESCRIBING", "EPS-FHIR-DISPENSING"]:
        context.eps_fhir_prescribing_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL,
            f"{EPS_FHIR_PRESCRIBING_SUFFIX}-{PULL_REQUEST_ID}",
        )
        context.eps_fhir_dispensing_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL,
            f"{EPS_FHIR_DISPENSING_SUFFIX}-{PULL_REQUEST_ID}",
        )
    if product == "PFP-APIGEE":
        context.pfp_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PFP_SUFFIX}-{PULL_REQUEST_ID}"
        )
    if product == "PSU":
        context.psu_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PSU_SUFFIX}-{PULL_REQUEST_ID}"
        )
    if product == "PFP-AWS":
        handle_pfp_aws_pr_url(context, env)
    if product == "CPTS-UI":
        handle_cpt_ui_pr_url(context, env)


def handle_cpt_ui_pr_url(context, env):
    assert PULL_REQUEST_ID is not None
    context.cpts_ui_base_url = (
        f"https://{CPTS_UI_PREFIX}-{PULL_REQUEST_ID}{select_apigee_base_url(env)}"
    )
    if env == "INTERNAL-DEV":
        context.cpts_ui_base_url = CPTS_UI_PR_URL.replace(
            "{{aws_pull_request_id}}", PULL_REQUEST_ID
        )
    if env == "INTERNAL-DEV-SANDBOX":
        context.cpts_ui_base_url = CPTS_UI_SANDBOX_PR_URL.replace(
            "{{aws_pull_request_id}}", PULL_REQUEST_ID
        )


def handle_pfp_aws_pr_url(context, env):
    assert PULL_REQUEST_ID is not None
    context.pfp_base_url = os.path.join(
        INTERNAL_DEV_BASE_URL, f"{PFP_SUFFIX}-{PULL_REQUEST_ID}"
    )
    if env == "INTERNAL-DEV":
        context.pfp_base_url = PFP_AWS_PR_URL.replace(
            "{{aws_pull_request_id}}", PULL_REQUEST_ID
        )
    if env == "INTERNAL-DEV-SANDBOX":
        context.pfp_base_url = PFP_AWS_SANDBOX_PR_URL.replace(
            "{{aws_pull_request_id}}", PULL_REQUEST_ID
        )


def after_all(context):
    # Add anything you want to happen after all the tests have completed here
    if count_of_scenarios_to_run(context) != 0:
        env = context.config.userdata["env"].upper()
        product = context.config.userdata["product"].upper()
        properties_dict = {"PRODUCT": product, "ENV": env}
        if PULL_REQUEST_ID:
            pull_request_id = PULL_REQUEST_ID.lower()
            if "pr-" in pull_request_id:
                env = os.path.join("PULL-REQUEST", PULL_REQUEST_ID)
                pull_request_link = os.path.join(
                    select_repository_base_url(product),
                    "pull",
                    PULL_REQUEST_ID.upper().replace("PR-", ""),
                )
                properties_dict = {
                    "PRODUCT": product,
                    "ENV": env,
                    "PULL-REQUEST": pull_request_link,
                }

        file_path = "./allure-results/environment.properties"
        write_properties_file(file_path, properties_dict)
    else:
        directory_path = "./allure-results"
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            print(f"Directory '{directory_path}' exists. Deleting...")
            shutil.rmtree(directory_path)
        if _page:
            _page.close()


def setup_logging(level: int = logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
        handlers=handlers,
    )


def select_apigee_base_url(env):
    if env in APIGEE_ENVS:
        return APIGEE_ENVS[env]
    else:
        raise ValueError(f"Unknown environment or missing base URL for: {env} .")


def select_aws_base_url(env):
    if env in AWS_ENVS:
        return AWS_ENVS[env]
    else:
        raise ValueError(f"Unknown environment or missing base URL for: {env} .")


def select_repository_base_url(product):
    if product in REPOS:
        return REPOS[product]
    else:
        raise ValueError(f"Unknown product or missing repository URL for: {product} .")


def write_properties_file(file_path, properties_dict):
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        for key, value in properties_dict.items():
            file.write(f"{key}={value}\n")


def get_page(self):
    return self._page


def set_page(self, _page):
    self._page = _page
