from yaml import safe_load
import json
from pathlib import Path


def lambda_handler(event, context):

    config = safe_load(Path("config.yml").read_text())
    current_intent_name = event["currentIntent"]["name"]
    previous_intent_name = event['sessionAttributes'].get('previous_intent_name')

    intent_config = config[current_intent_name]

    # standalone response
    if previous_intent_name is None:
        intent_config = config[current_intent_name]
        response_message = intent_config["message"]
        response_buttons = intent_config.get("buttons", [])
        session_attributes = {
            "previous_intent_name": current_intent_name
        }
        return build_response(response_message, response_buttons, session_attributes)

    # chained response
    intent_config = config[current_intent_name]["previousIntent"][previous_intent_name]
    response_message = intent_config["message"]
    response_buttons = intent_config.get("buttons", [])
    session_attributes = {
        "previous_intent_name": current_intent_name
    }
    return build_response(response_message, response_buttons, session_attributes)



def build_response(message, buttons=None, session_attributes=None):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {"contentType": "PlainText", "content": message},
        },
    }

    return response


def main():

    event1 = {"currentIntent": {"name": "Account"}, "sessionAttributes": {}}
    print(json.dumps(lambda_handler(event1, {}), indent=4))

    event2 = {"currentIntent": {"name": "CreditCardAccount"}, "sessionAttributes": {}}
    print(json.dumps(lambda_handler(event2, {}), indent=4))

    event3 = {"currentIntent": {"name": "Complaints"}, "sessionAttributes": {}}
    print(json.dumps(lambda_handler(event3, {}), indent=4))

    event3a = {"currentIntent": {"name": "Account"}, "sessionAttributes": {'previous_intent_name': "Complaints"}}
    print(json.dumps(lambda_handler(event3a, {}), indent=4))
    
    event3b = {"currentIntent": {"name": "CreditCardAccount"}, "sessionAttributes": {'previous_intent_name': "Complaints"}}
    print(json.dumps(lambda_handler(event3b, {}), indent=4))



if __name__ == "__main__":
    main()
