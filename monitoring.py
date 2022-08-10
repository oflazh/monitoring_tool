import paramiko
import yaml
import pandas as pd
import numpy as np
from multiprocessing import Pool

def monitor():
    cmd = "kubectl get nodes"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port, user, str(pw), timeout=10)
        isAvailable = "Yes"
        stdin, stdout, stderr = ssh.exec_command(cmd)

        output = stdout.readlines()
        isCluster = "0"
        isOld = []
        isOld.append(output)
        if len(output) > 2:
            isCluster = "Yes"
        if len(output) == 2:
            isCluster = "No"

        cmd2 = "kubectl get pods"
        stdin, stdout, stderr2 = ssh.exec_command(cmd2)

        output2 = stdout.read()

        if "alarm-manager" in str(output2):
            isCentral = "Yes"
        else:
            isCentral = "No"

        if "Evicted" in str(output2):
            isEvicted = "Yes"
        else:
            isEvicted = "No"

        wordlist = output2.split()[:10]
        isOld = wordlist[9].decode("utf-8")



    except:
        isAvailable = "No"
        isCluster = "-"
        isCentral = '-'
        isOld = '-'
        isEvicted = '-'

    name.append(vm_id)
    cluster.append(isCluster)
    central.append(isCentral)
    age.append(isOld)
    available.append(isAvailable)
    evicted.append(isEvicted)


with open('vm.yaml', 'r') as f:
    doc = yaml.load(f, Loader=yaml.FullLoader)

name = []
cluster = []
central = []
age = []
available = []
evicted = []

vms = doc["vms"]
for vm_id in vms:
    vm = vms[vm_id]

    ip = vm["ip"]
    user = vm["user"]
    pw = vm["pass"]
    port = 22
    monitor()


data = []
data.append(name)
data.append(cluster)
data.append(central)
data.append(age)
data.append(available)
data.append(evicted)

df = pd.DataFrame(np.transpose(data), columns=['VM_IDs', 'Cluster', 'Central', 'Age', 'Available', 'Evicted'])
print(df)


df.to_html(open(r'C:\Users\huseyinof\Desktop\VMs.html','w'))