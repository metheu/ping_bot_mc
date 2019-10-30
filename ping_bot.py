import requests, time, json, logging, sys, os
from dotenv import load_dotenv

# Set the config level
logging.basicConfig(level=logging.INFO)

# load dotenv file
load_dotenv(verbose=True)

#  Load env variables form file
username = os.getenv("USER_NAME")
password = os.getenv("USER_PASSWORD")
test_url = os.getenv("TEST_URL")
slack_hook = os.getenv("SLACK_HOOK_URL");

# check that necessary variables are loaded!
for i in username, password:
    if not i:
        raise ValueError("Seems like .env file is empty or didn't map correct values!")

# test_env
test_status_code = 500
# failing boolean
failing = 0

# set the params
params_payload = {"X-IBS-CHANNEL": "MBS"}

# set the headers
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
}

# Set the data
data = {
    "username": os.getenv("USER_NAME"),
    "password": os.getenv("USER_PASSWORD"),
    "language": "en",
    "rememberUserName": False,
}
# Encode as json
data_e = json.dumps(data)

# start the loop
while True:

    # clear request response or else it gets saved when looping
    r = ""

    # Make the request and handle it if no connection
    try:
        r = requests.post(
            test_url,
            params=params_payload,
            headers=headers,
            data=data_e,
        )
    except requests.ConnectionError:
        logging.error("Could not connect to server!")

    if not r == '' and r.status_code == 200:
        logging.info("Ping is stable: Status code: %s", str(r.status_code))
        # if the systems recovers send notification
        if failing >= 1:
            # send notification and set failing to 0
            logging.info("Seems like system has recovered! Sending notification!")
            failing = 0
            down_time = '{:02d}:{:02d}'.format(*divmod(failing, 60)), 

            headers_slack = {"Content-Type": "application/json"}
            slack_payload = json.dumps(
                {
                    "attachments": [
                        {
                            "pretext": "MCL seem to have recovered! :innocent: :ghost: :man-cartwheeling:",
                            "title": "MCL has recovered! Down time: " + str(down_time), 
                            "text": "Error code: "
                            + str(r.status_code)
                            + " Response: "
                            + r.text,
                            "color": "#7CD197",
                        }
                    ]
                }
            )

            p_res = requests.post(
                slack_hook,
                headers=headers_slack,
                data=slack_payload,
            )
            if p_res.status_code != 200:
                raise ValueError(
                    "Send requuest to payload to slack failed! %s, respose: \n%s",
                    p_res.status_code,
                    p_res.text,
                )
    elif not r == '' and r.status_code == 500:
        # logg the error and set failling flag to 1
        failing += 1
        logging.warning(
            "Issue encountered! Status code: %s failing #: %s",
            str(r.status_code),
            failing,
        )

        # if failed for first time
        if failing <= 1:
            headers_slack = {"Content-Type": "application/json"}
            slack_payload = json.dumps(
                {
                    "attachments": [
                        {
                            "pretext": "MCL down! :hankey: :skull_and_crossbones:",
                            "title": "Can't ping MCL!",
                            "text": "Error code: "
                            + str(r.status_code)
                            + " Response: "
                            + r.text,
                            "color": "#FF3232",
                        }
                    ]
                }
            )
            logging.info("Sending notification to slack!")
            p_res = requests.post(
                slack_hook,
                headers=headers_slack,
                data=slack_payload,
            )
            if p_res.status_code != 200:
                raise ValueError(
                    "Send requuest to payload to slack failed! %s, respose: \n%s",
                    p_res.status_code,
                    p_res.text,
                )

    # sleep for 1 min
    time.sleep(60)
