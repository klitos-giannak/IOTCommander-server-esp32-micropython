import json
import os
import sys
import time

import web
import executables

REST_API_PORT = 9977
CONFIG_FILENAME = 'commands_config.json'

PARAM_EXEC_COMMAND = "execute"
PARAM_INTEGER = "int"
PARAM_FLOAT = "float"
PARAM_TEXT = "text"
PARAM_BOOLEAN = "boolean"
ACCEPTED_PARAMETER_TYPES = [PARAM_INTEGER, PARAM_FLOAT, PARAM_BOOLEAN, PARAM_TEXT]
ACCEPTED_BOOLEAN_TRUE_VALUES = ["true", "t", "1"]
ACCEPTED_BOOLEAN_FALSE_VALUES = ["false", "f", "0"]
COMMAND_RESPONSE_OK_BODY = "<html><body><h1>[200] OK</h1><p>Command successful</p></body></html>\n"

should_continue = True
web_server = web.WebApp()

supported_commands = {}


def get_boolean_value(value):
    if value.lower() in ACCEPTED_BOOLEAN_TRUE_VALUES:
        return True
    elif value.lower() in ACCEPTED_BOOLEAN_FALSE_VALUES:
        return False
    else:
        return None


@web_server.route('/commands', method='GET')
def supported_commands_query(request, response):
    print("Supported commands requested. Sending Back Commands config.")

    commands_dict = json.loads(json.dumps(supported_commands))
    for command in commands_dict:
        commands_dict[command].pop(PARAM_EXEC_COMMAND)

    yield from web.jsonify(response, commands_dict)

import re
@web_server.route(re.compile('/command/'), method='GET')
def command_requested(request, response):
    command_name = ''
    command_parts = request.path.split('/')
    if len(command_parts) > 2:
        command_name = command_parts[2]
    print("Command <" + command_name + "> requested. Trying to parse parameters.")
    
    if not isinstance(command_name, str):
        yield from web.http_error(response, '400')
    
    if len(command_name) == 0:
        yield from web.http_error(response, '400')

    command = supported_commands.get(command_name)
    if command is None:
        # retry but case-insensitive
        for key in supported_commands:
            if key.lower() == command_name:
                command = supported_commands[key]
                break

    if command is None:
        yield from web.http_error(response, '404')
        
    executable_command = command[PARAM_EXEC_COMMAND]
    
    request.parse_qs()
    
    for param in command:
        if param == PARAM_EXEC_COMMAND:
            continue

        expected_type = command[param]
        try:
            value = request.form.get(param)
            if value is None:
                reason = "missing param " + param
                print(reason + ". Responding with an error.")
                yield from web.http_error(response, '400')

            if expected_type == PARAM_INTEGER:
                # we don't want to save the result, just validate the type
                if int(value) is None:
                    reason = "Unable to convert value of param " + param + " to type " + expected_type
                    print(reason + ". Responding with an error.")
                    yield from web.http_error(response, '400')

            elif expected_type == PARAM_FLOAT:
                # we don't want to save the result, just validate the type
                if float(value) is None:
                    reason = "Unable to convert value of param " + param + " to type " + expected_type
                    print(reason + ". Responding with an error.")
                    yield from web.http_error(response, '400')

            elif expected_type == PARAM_BOOLEAN:
                # we don't want to save the result, just validate the type
                if get_boolean_value(value) is None:
                    reason = "Unable to convert value of param " + param + " to type " + expected_type
                    print(reason + ". Responding with an error.")
                    yield from web.http_error(response, '400')

        except ValueError:
            reason = "Invalid param " + param
            print(reason + ". Responding with an error.")
            yield from web.http_error(response, '400')

        executable_command = executable_command.replace("$" + param, value, 1)

    print("Parameters parsed successfully, responding OK")

    print("trying to execute: '" + executable_command + "'")
    exec(executable_command, {"executables":executables})
    print()
    yield from web.jsonify(response, COMMAND_RESPONSE_OK_BODY)


def validate_config() -> bool:
    try:
        if sys.implementation.name == "micropython":
            file = CONFIG_FILENAME
        else:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            file = os.path.join(__location__, CONFIG_FILENAME)

        with open(file) as json_file:
            global supported_commands
            supported_commands = json.load(json_file)
            for command in supported_commands:
                parameters = supported_commands[command]
                executable_command = parameters.get(PARAM_EXEC_COMMAND)
                if executable_command is None:
                    print('"' + PARAM_EXEC_COMMAND + '" not found for command "' + command + '"')
                    return False

                for (key, value) in parameters.items():
                    if not (key == PARAM_EXEC_COMMAND or value in ACCEPTED_PARAMETER_TYPES):
                        print('Unknown parameter value: "' + value + '" for key "' + key + '"')
                        return False

            return True
    except OSError:
        return False


def print_commands_summary():
    output = "\nSupported commands summary: ["
    # noinspection PyUnboundLocalVariable
    for command in supported_commands:
        output = output + command + ", "
    output = output[:-2]
    output = output + "]"
    print(output)


def start():
    if not validate_config():
        print("commands_config validation failed")
        return False
    else:
        print_commands_summary()

    print("-- Running commands server at port " + str(REST_API_PORT) + " --\n")

    #global web_server
    import uasyncio
    
    loop = uasyncio.get_event_loop()

    loop.create_task(uasyncio.start_server(web_server.handle, '0.0.0.0', REST_API_PORT))
    loop.run_forever()
    return True


def stop():
    web_server.Stop()
    print("\n-- Commands server terminated --")



