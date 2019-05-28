import traceback, sys
from pprint import pprint
import re

file_name = 'bad_code'

try:
    exec(f'import {file_name}')
except Exception:
    sag = traceback.format_exc()

error_msg = sag.split('\n')[4:-1]


# for i, err in enumerate(error_msg, start=0):
#     print(i, err.strip(), sep='--')


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

# print(err_dict[f'F-{F_num}']['script']
# [:6])
if err_dict[f'F-{F_num}']['script'][:6] == 'return':
    prev_script = err_dict[f'F-{F_num - 1}']['script']
    ind_1 = prev_script.index('(')
    # print(f'ind_1 : {type(ind_1)}')
    ind_2 = prev_script.index(')')
    # print(f'ind_2() : {type(ind_2)}')
    params = prev_script[ind_1 + 1 : ind_2].split(',')
    params = [x.strip().strip('"').strip("'") for x in params]




pprint(err_dict)
error_final = error_msg[-1]
error_type = error_final.split(':')[0]
if error_type == 'TypeError':
    types = error_final.split(':')[2].split('and')
    types = [x.strip().strip('"').strip("'")for x in types]
operation = error_final.split(':')[1][-1]
if operation == '/':
    operation = 'divide'

print(f"You've got a {error_type} because:")
print(f'You cannot {operation} a {types[0]}({params[0]}) by a {types[1]}({params[1]}) ! ')

print('Here is the problem chain:')



