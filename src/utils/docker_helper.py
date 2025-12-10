import subprocess
import sys

class DockerHelper:
    @staticmethod
    def restart_container(container_name):
        try:
            subprocess.run(["docker", "restart", container_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def exec_command(container_name, command):
        """
        Executes a command inside a running container.
        Returns (exit_code, output)
        """
        try:
            # Use 'sh -c' to handle complex commands with pipes/redirects
            cmd = ["docker", "exec", container_name, "sh", "-c", command]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return -1, str(e)

    @staticmethod
    def is_container_running(container_name):
        try:
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
                capture_output=True, text=True
            )
            return result.stdout.strip() == "true"
        except:
            return False
