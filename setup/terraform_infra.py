# setup/terraform_infra.py
import subprocess
from pathlib import Path

TERRAFORM_DIR = Path(__file__).parent  # adjust to your .tf file location

def terraform_init():
    subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR, check=True)

def terraform_apply():
    subprocess.run(
        ["terraform", "apply", "-auto-approve"],
        cwd=TERRAFORM_DIR,
        check=True
    )

def provision_infra():
    terraform_init()
    terraform_apply()
    print("Infrastructure provisioned")

if __name__ == "__main__":
    provision_infra()