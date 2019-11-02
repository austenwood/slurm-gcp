import subprocess
import time
import re

cmd = subprocess.Popen("gcloud auth list", shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
# cmd_err = cmd.stderr.read()
lst = re.findall('\S+@\S+', str(cmd_out))
email = lst[0]
print(email.rstrip().lstrip())

cluster_conf = open("slurm-cluster.yaml")
for line in cluster_conf:
    if "zone" in line:
        # print(line.split(":")[1].rstrip().lstrip())
        zone = line.split(":")[1].rstrip().lstrip()
print(zone)
# quit()

print("Enabling Compute Engine API")
cmd = subprocess.Popen("gcloud services enable compute.googleapis.com",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
print(cmd_out.decode())

print("Enabling Cloud Deployment Manager V2 API")
cmd = subprocess.Popen("gcloud services enable deploymentmanager.googleapis.com",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
print(cmd_out.decode())

print("Deploying GCP Slurm Cluster")
cmd = subprocess.Popen("gcloud deployment-manager deployments create google1 --config slurm-cluster.yaml",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
print(cmd_out.decode())

# Does a list of files, and

print("Waiting for slurm and other packages to be installed")
start = time.perf_counter()
cmd = subprocess.Popen("gcloud compute ssh g1-login1 --zone="+zone+" --command 'sinfo'",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
# cmd_out = cmd.stdout.read()
cmd_err = cmd.stderr.read()
# print(str(cmd_err))
# quit()
while "command not found" in cmd_err.decode() or "Permission denied" in cmd_err.decode():
    time.sleep(60)
    cmd = subprocess.Popen("gcloud compute ssh g1-login1 --zone="+zone+" --command 'sinfo'",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd.wait()
    # cmd_out = cmd.stdout.read()
    cmd_err = cmd.stderr.read()
    # print(cmd_err)
end = time.perf_counter()
print("Ready")
print("Took time: " + str(end-start))
cmd = subprocess.Popen("gcloud compute scp ./code g1-login1:~/ --recurse --zone=" +
                       zone, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
cmd_err = cmd.stderr.read()
print(cmd_out.decode())
print(cmd_err.decode())
cmd = subprocess.Popen("gcloud compute ssh g1-login1 --zone="+zone+" --command 'cd ~/code && mpicc hello.c -o hello'",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
cmd_err = cmd.stderr.read()
print(cmd_out.decode())
print(cmd_err.decode())
cmd = subprocess.Popen("gcloud compute ssh g1-login1 --zone="+zone+" --command 'cd ~/code && sbatch slurmscript.sh'",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
cmd_err = cmd.stderr.read()
print(cmd_out.decode())
print(cmd_err.decode())


def check_squeue():
    cmd = subprocess.Popen("gcloud compute ssh g1-login1 --zone="+zone+" --command 'squeue'",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd.wait()
    cmd_out = cmd.stdout.read()
    cmd_err = cmd.stderr.read()
    print(cmd_out.decode())
    print(cmd_err.decode())
    if cmd_out.decode() != "             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)":
    print("Waiting for job to finish")
    time.sleep(10)
    check_squeue()


check_squeue()

cmd = subprocess.Popen("gcloud compute scp g1-login1:~/code/test-srun.out . --zone=" +
                       zone, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd.wait()
cmd_out = cmd.stdout.read()
cmd_err = cmd.stderr.read()
print(cmd_out.decode())
print(cmd_err.decode())

answer = None
while answer not in ("yes", "no"):
    answer = input(
        "Job executed successfully. Would you like to delete the deployment?\n Enter yes or no:")
    if answer == "yes":
        quit()
    elif answer == "no":
        print("Destroying Slurm Cluster")
        cmd = subprocess.Popen("gcloud deployment-manager deployments delete google1 -q",
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd.wait()
        cmd_out = cmd.stdout.read()
        cmd_err = cmd.stderr.read()
        print(cmd_out.decode())
        print(cmd_err.decode())
    else:
        print("Please enter yes or no.")
