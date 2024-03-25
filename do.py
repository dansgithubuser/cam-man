#! /usr/bin/env python3

#===== imports =====#
import argparse
import datetime
import glob
import os
import re
import signal
import string
import subprocess
import sys

#===== args =====#
parser = argparse.ArgumentParser()
parser.add_argument('--run', '-r', metavar='<script invocation>')
parser.add_argument('--systemd-install', metavar='<script path>')
parser.add_argument('--systemd-ls', '-l', action='store_true')
args = parser.parse_args()

#===== consts =====#
DIR = os.path.dirname(os.path.realpath(__file__))

#===== setup =====#
os.chdir(DIR)

#===== helpers =====#
def blue(text):
    return '\x1b[34m' + text + '\x1b[0m'

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def invoke(
    *args,
    quiet=False,
    env_add={},
    handle_sigint=True,
    popen=False,
    check=True,
    out=False,
    err=False,
    **kwargs,
):
    if len(args) == 1 and type(args[0]) == str:
        args = args[0].split()
    if not quiet:
        print(blue('-'*40))
        print(timestamp())
        print(os.getcwd()+'$', end=' ')
        if any([re.search(r'\s', i) for i in args]):
            print()
            for i in args: print(f'\t{i} \\')
        else:
            for i, v in enumerate(args):
                if i != len(args)-1:
                    end = ' '
                else:
                    end = ';\n'
                print(v, end=end)
        if kwargs: print(kwargs)
        if popen: print('popen')
        print()
    if env_add:
        env = os.environ.copy()
        env.update(env_add)
        kwargs['env'] = env
    if out or err: kwargs['capture_output'] = True
    p = subprocess.Popen(args, **kwargs)
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    if popen:
        return p
    p.wait()
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    if check and p.returncode:
        raise Exception(f'invocation {repr(args)} returned code {p.returncode}.')
    if out:
        stdout = p.stdout.decode('utf-8')
        if out != 'exact': stdout = stdout.strip()
        if not err: return stdout
    if err:
        stderr = p.stderr.decode('utf-8')
        if err != 'exact': stderr = stderr.strip()
        if not out: return stderr
    if out and err: return [stdout, stderr]
    return p

#===== main =====#
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if args.run:
    invoke(args.run, env_add={'PYTHONPATH': '.'})

if args.systemd_install:
    print('short unique description:')
    desc = input()
    print()
    print('script args:')
    script_args = input()
    print()
    script_path = os.path.abspath(args.systemd_install)
    exec_start = f'{sys.executable} -u {script_path} {script_args}'
    with open('systemd/template.service') as f:
        template = f.read()
    service_text = template.format(
        description=desc,
        python_path=DIR,
        exec_start=exec_start,
    )
    remove_punctuation = str.maketrans('', '', string.punctuation)
    service_file_name = 'camman_' + desc.translate(remove_punctuation).replace(' ', '_').lower() + '.service'
    service_path = f'/etc/systemd/system/{service_file_name}'
    print(f"I will write the following to '{service_path}':")
    print()
    print(service_text)
    print()
    print('OK? Enter to proceed, ctrl-c to abort.')
    input()
    with open('.service.tmp', 'w') as f:
        f.write(service_text)
    invoke(f'sudo systemd/install.sh {service_path} {service_file_name}')

if args.systemd_ls:
    for i in glob.glob('/etc/systemd/system/camman_*'):
        print(i)
