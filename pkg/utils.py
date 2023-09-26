import importlib.resources as pkg_resources
import subprocess

def get_data_path(dir):
    if __package__:
        return str(pkg_resources.files(__package__).joinpath(dir))
    else:
        return dir
    
def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.output