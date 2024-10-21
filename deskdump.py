import re
import argparse
import subprocess


def dump_process(pid):
    try:
        dump_file_name = f'dump_{pid}'
        result = subprocess.run(['tools/procdump64.exe', '-accepteula', '-ma', str(pid), '-o', dump_file_name],
                                stdout=subprocess.PIPE)
        if "complete" in result.stdout.decode('utf-8'):
            print("dump complete!")
        else:
            print("dump failed!")
        # print(f"Dumping process {pid} to {dump_file_name}")
        return dump_file_name + ".dmp"
    except Exception as e:
        print(f"Failed to create dump file: {e}")
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pid', type=int, help='PID to dump')
    parser.add_argument('-a', '--app', type=str, help='app name')
    args = parser.parse_args()
    pid = args.pid
    app_name = args.app
    if pid is not None and app_name is not None:
        dump_file_name = dump_process(pid)
        if dump_file_name is not None:
            with open(dump_file_name, "rb") as f:
                contentByte = f.read()
                content = contentByte.decode("ascii", errors="ignore")
                result2 = re.compile(r'<f f=.+ c=color_edit >\w+</f>').findall(content)
                mima = []
                if result2 != 0:
                    print("[+]密码：")
                    for r in result2:
                        r = re.sub(r'<f f=.+ c=color_edit >', "", r).replace("</f>", "")
                        mima.append(r)
                    mima = list(set(mima))
                    for m in mima:
                        print(m)
                else:
                    print("[-]未找到密码")

    else:
        print("PID or app name must be specified")
