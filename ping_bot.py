import requests, time, json, logging, sys

# Set the config level
logging.basicConfig(level=logging.INFO)

# test_env
test_status_code = 500;
# failing boolean
failing = 0

# set the headers
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
}
# Set the data
data = {
    "username": "TEMU",
    "password": "aRt71111",
    "language": "en",
    "rememberUserName": False,
}
# Encode as json
data_e = json.dumps(data)
# Make the request
r = requests.post(
    "https://testmcl1.tbconline.ge/ibs/delegate/rest/auth/v1/login",
    headers=headers,
    data=data_e,
)

while True:
    if r.status_code == 200:
        logging.info("Ping is stable: Status code: %s", str(r.status_code))
        # if the systems recovers send notification
        if failing >= 1:
            # send notification and set failing to 0
            logging.info("Seems like system has recovered! Sending notification!")
            failing = 0;

            headers_slack = {"Content-Type": "application/json"}
            slack_payload = json.dumps(
                {
                    "attachments": [
                        {
                            "pretext": "MCL seem to have recovered! :innocent: :ghost: :man-cartwheeling:",
                            "title": "MCL has recovered!",
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
                "https://hooks.slack.com/services/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",
                headers=headers_slack,
                data=slack_payload,
            )
            if p_res.status_code != 200:
                raise ValueError(
                    "Send requuest to payload to slack failed! %s, respose: \n%s",
                    p_res.status_code,
                    p_res.text,
                )
    else:
        # logg the error and set failling flag to 1
        logging.warning("Issue encountered! Status code: %s", str(r.status_code))
        failing += 1
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
                "https://hooks.slack.com/services/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",
                headers=headers_slack,
                data=slack_payload,
            )
            if p_res.status_code != 200:
                raise ValueError(
                    "Send requuest to payload to slack failed! %s, respose: \n%s",
                    p_res.status_code,
                    p_res.text,
                )

    time.sleep(60)