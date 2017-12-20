import sys
import os
import git
import re
import subprocess

from optparse import OptionParser
from time import sleep

LAST_COMMITS_MASTER=30
ITERATIONS = 3
TIME = 15


class WebSeverCommand:
    def __init__(self, server_path=None):
        self.server_path = server_path if server_path else os.path.join(os.getcwd(), "web_uvloop.py")

    def __str__(self):
        return str(self.command())

    def command(self):
        return (
            "python3",
            self.server_path
        )

class WrkCommand:
    def __init__(self, connections=20, time=TIME, threads=20, uri='http://localhost:5000/', wrk_path=None):
        self.connections = connections
        self.time = time
        self.threads = threads
        self.uri = uri
        self.wrk_path = wrk_path if wrk_path else "wrk"

    def __str__(self):
        return str(self.command())

    def command(self):
        return (
            self.wrk_path,
            "-c",
            str(self.connections),
            "-d",
            str(self.time),
            "-t" ,
            str(self.threads),
            self.uri
        )

def find_req_sec(data):
    return float(re.search(".*(Requests/sec:)\s+([0-9]*\.[0-9]*).*", str(data)).groups()[1])

def run_web_server(aiohttp_git_path):
    env = os.environ.copy()
    env['PYTHONPATH'] = aiohttp_git_path
    cmd = WebSeverCommand()
    process = subprocess.Popen(
        cmd.command(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env)

    sleep(2)
    return process

def run_benchmark(wrk_path=None):
    cmd = WrkCommand(wrk_path=wrk_path)
    return subprocess.check_output(
        cmd.command()
    )

def run_reference_benchmark(aiohttp_git_path, reference, wrk_path=None):
    repo = git.Git(aiohttp_git_path)
    repo.checkout(reference)
    process = run_web_server(aiohttp_git_path)
    try:
        ret = []
        for i in range(0, ITERATIONS):
            output = str(run_benchmark(wrk_path=wrk_path))
            assert "Non-2xx" not in output
            ret.append(find_req_sec(output))
        print("[{}] Benchmark req/sec {}".format(reference, round(sum(ret)/3), 2))
    finally:
        process.kill()

def run_tag_benchmark(aiohttp_git_path, tag_re, wrk_path=None):
    repo = git.Git(aiohttp_git_path)
    tags = filter(lambda tag: re.search(tag_re, tag), repo.tag().split("\n"))
    for tag in tags:
        run_reference_benchmark(aiohttp_git_path, tag, wrk_path=wrk_path)

def run_v3_benchmark(aiohttp_git_path, wrk_path=None):
    repo = git.Git(aiohttp_git_path)
    repo.checkout("master")
    output = subprocess.check_output(
        ('git', 'log', '--oneline', '-n', str(LAST_COMMITS_MASTER)),
        cwd=aiohttp_git_path
    )
    for l in output.decode().split("\n")[:-1]:
        commit = l.split(" ")[0]
        run_reference_benchmark(aiohttp_git_path, commit, wrk_path=wrk_path)

USAGE = """usage: %prog [options] <aiohttp_git_path>
Without options will run the test against the master reference
"""
if __name__ == "__main__":
    parser = OptionParser(usage=USAGE)
    parser.add_option(
        "--server-path",
        action="store",
        dest="server_path",
        type=str,
        help="Alternative Server path, default to",
        default=None)
    parser.add_option(
        "--wrk-path",
        action="store",
        dest="wrk_path",
        type=str,
        help="Alternative WRK path, default delegates to be find by the system",
        default=None)
    parser.add_option(
        "--reference",
        action="store",
        dest="reference",
        type=str,
        help="Checkout a specific reference and run the tests within",
        default=None)
    parser.add_option(
        "--v1",
        action="store_true",
        dest="v1",
        help="Test all aiohttp v1 releases",
        default=False)
    parser.add_option(
        "--v2",
        action="store_true",
        dest="v2",
        help="Test all aiohttp v2 releases",
        default=False)
    parser.add_option(
        "--v3",
        action="store_true",
        dest="v3",
        help="Test last {} commits in master".format(LAST_COMMITS_MASTER),
        default=False)

    try:
        (options, args) = parser.parse_args()
        aiohttp_git_path = args[0]
    except IndexError:
        parser.print_help()
        sys.exit(1)

    if options.reference:
        run_reference_benchmark(aiohttp_git_path, options.reference, wrk_path=options.wrk_path)
    elif options.v1:
        run_tag_benchmark(aiohttp_git_path, "^(v?)1.*", wrk_path=options.wrk_path)
    elif options.v2:
        run_tag_benchmark(aiohttp_git_path, "^(v?)2.*", wrk_path=options.wrk_path)
    elif options.v3:
        run_v3_benchmark(aiohttp_git_path, wrk_path=options.wrk_path)
    else:
        print("Default using master reference")
        run_reference_benchmark(aiohttp_git_path, "master", wrk_path=options.wrk_path)
