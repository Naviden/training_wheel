import traceback, sys
from pprint import pprint
import re

file_name = 'bad_code'

try:
    exec(f'import {file_name}')
except Exception:
    sag = traceback.format_exc()

error_msg = sag.split('\n')[4:-1]
error_final = error_msg[-1]
error_type = error_final.split(':')[0]

def find_operation(text):
    if '-' in text:
        return 'subtract'
    elif '+' in text:
        return 'add'
    elif '/' in text:
        return 'divide'
    elif '*' in text:
        return 'multiply'
    
def find_type(text):
    found = []
    for t in ['str', 'int', 'float', 'list', 'dict', 'bool']:
        if t in text:
            found.append(t)
    return found


F_num = 0
err_dict = {}
for err in error_msg:
    err_orig = err
    err = err.strip()
    if err[:4] == 'File':
        F_num += 1
        err_dict[f'F-{F_num}'] = {}
        err_dict[f'F-{F_num}']['file'] = err.split('"')[1].split('/')[-1]
        err_dict[f'F-{F_num}']['line'] = err.split('"')[2].split()[2]
        err_dict[f'F-{F_num}']['script'] = error_msg[error_msg.index(err_orig) + 1].strip()
        err_dict[f'F-{F_num}']['env'] = err.split()[6].rstrip('>').lstrip('<')

last_env = err_dict[f'F-{F_num}']['env']
if last_env != 'module':
    prev_script = err_dict[f'F-{F_num - 1}']['script']
    ind_1 = prev_script.index('(')
    # print(f'ind_1 : {type(ind_1)}')§
    ind_2 = prev_script.index(')')
    # print(f'ind_2() : {type(ind_2)}')
    params = prev_script[ind_1 + 1 : ind_2].split(',')
    params = [x.strip().strip('"').strip("'") for x in params]
    print(f'Check out the {last_env} function.')
    if len(params) > 2:
        print(
            f"In the line {err_dict[f'F-{F_num - 1}']['line']} you called the {last_env} function with the following arguments:")
        for p in params:
            print(f'\t* {p}')
        print(
            f'Inside these {len(params)} inputs you have a {find_type(error_final)[0]} and {find_type(error_final)[1]} which you cannot {find_operation(error_final)} from/to each other.')
else:
    print(
        f"In the line {err_dict[f'F-{F_num}']['line']} You wrote {err_dict[f'F-{F_num}']['script']} which means you are trying to {find_operation(error_final)} a {find_type(error_final)[0]} and {find_type(error_final)[1]} from/to each other.")
    print('Such an operation is not allowed in Python!')

# pprint(err_dict)

# if last call is function


# pprint(err_dict)

# if error_type == 'TypeError':
#     types = error_final.split(':')[2].split('and')
#     types = [x.strip().strip('"').strip("'")for x in types]
# operation = error_final.split(':')[1][-1]
# if operation == '/':
#     operation = 'divide'

# print(f"You've got a {error_type} because:")
# print(f'You cannot {operation} a {types[0]}({params[0]}) by a {types[1]}({params[1]}) ! ')

# print('Here is the problem chain:')



