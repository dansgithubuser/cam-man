import os
import signal
import subprocess

def invoke(
    *args,
    env_add={},
    env_add_secrets=set(),
    handle_sigint=True,
    popen=False,
    check=True,
    put_in=False,
    get_out=False,
    get_err=False,
    **kwargs,
):
    if len(args) == 1 and type(args[0]) == str and not kwargs.get('shell'):
        args = args[0].split()
    if env_add:
        env = os.environ.copy()
        env.update(env_add)
        kwargs['env'] = env
    if put_in and 'stdin' not in kwargs: kwargs['stdin'] = subprocess.PIPE
    if get_out: kwargs['stdout'] = subprocess.PIPE
    if get_err: kwargs['stderr'] = subprocess.PIPE
    p = subprocess.Popen(args, **kwargs)
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    if put_in:
        if type(put_in) == str:
            put_in = put_in.encode()
        p.stdin.write(put_in)
        if popen:
            p.stdin.flush()
    if popen:
        return p
    stdout, stderr = p.communicate()
    p.out = stdout
    p.err = stderr
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    if check and p.returncode:
        e = Exception(f'invocation {repr(args)} returned code {p.returncode}.')
        e.p = p
        raise e
    if get_out:
        stdout = stdout.decode('utf-8')
        if get_out != 'exact': stdout = stdout.strip()
        if not get_err: return stdout
    if get_err:
        stderr = stderr.decode('utf-8')
        if get_err != 'exact': stderr = stderr.strip()
        if not get_out: return stderr
    if get_out and get_err: return stdout, stderr
    return p
