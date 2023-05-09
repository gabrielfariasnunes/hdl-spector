import subprocess


def build(portname):
    command = ["java", "-jar", "./lib/hdl.jar", portname]
    results = subprocess.run(command, capture_output=True, text=True)
    return results.stdout
