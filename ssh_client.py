from fabric import Connection

class SSHClient:
    def __init__(self, config):
        self.hostname = config.get('hostname').strip('/')
        self.port = config.get('port', 22)  # Default to port 22 if not provided
        self.username = config.get('username')
        self.password = config.get('password')
        self.client = None

    def connect(self):
        try:
            self.client = Connection(
                host=self.hostname,
                user=self.username,
                port=self.port,
                connect_kwargs={
                    "password": self.password,
                }
            )
            print("Connected to the server")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")

    def execute_command(self, command):
        if self.client is None:
            print("Connection not established. Call connect() first.")
            return None, None

        try:
            result = self.client.run(command, hide=True)
            output = result.stdout.strip()
            error = result.stderr.strip()
            return output, error
        except Exception as e:
            print(f"Failed to execute command: {e}")
            return None, None

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            print("Connection closed")


class SASServerClient(SSHClient):
    CONFIG = {
        'hostname': 'sasserver.demo.sas.com',
        'username': 'root',
        'password': 'Orion123'
    }

    CERT = '/tmp/trustedcerts.pem'

    def __init__(self):
        super().__init__(self.CONFIG)
        self.connect()

    def update_path(self):
        if self.client is None:
            print("Connection not established. Call connect() first.")
            return None, None

        try:
            additional_paths = [
                '/root/bin',
                '/root/project/deploy/Scripts',
                '/mnt/viya-share/lua/luarocks-3.8.0',
                '/root/.istioctl/bin'
            ]
            additional_paths_str = ":".join(additional_paths)

            # Get current PATH value
            current_path, error = self.execute_command('echo $PATH', update_path=False)
            if error:
                print(f"Failed to get current PATH: {error}")
                return None, None

            # Update PATH
            new_path = f'{current_path.strip()}:{additional_paths_str}'

            # Set environment variables
            export_commands = [
                f'export PATH={new_path}',
                f'export SSL_CERT_FILE={self.CERT}',
                f'export REQUESTS_CA_BUNDLE={self.CERT}'
            ]
            full_command = ' && '.join(export_commands)
            return full_command, None
        except Exception as e:
            print(f"Failed to update PATH: {e}")
            return None, None

    def execute_command(self, command, update_path=True):
        if self.client is None:
            print("Connection not established. Call connect() first.")
            return None, None

        try:
            if update_path:
                print("=================")
                print("command:\033[94m", command,"\033[0m")
                update_command, _ = self.update_path()
                full_command = f'{update_command} && {command}'
            else:
                full_command = command

            result = self.client.run(full_command, hide=True)
            output = result.stdout.strip()
            error = result.stderr.strip() if result.stderr else None
            return output, error
        except Exception as e:
            print(f"Failed to execute command: {e}")
            return None, None

    def list_files(self, dir):
        command = f"ls -lrt {dir}"
        output, error = self.execute_command(command)
        return output, error

    def setup_cli_certs(self):
        try:
            command = """
            kubectl -n sas_viya cp $(kubectl get pod -n sas_viya | grep "sas-logon-app" | head -1 | 
            awk -F" " '{print $1}'):security/trustedcerts.pem /tmp/trustedcerts.pem
            """
            out, err = self.execute_command(command)
            print(out, "\nDone setting up certificate!\n") if out else print(err, "\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def setup_cli_sas_profile(self, profile):
        try:
            command = f"sas-viya --profile {profile} profile init --sas-endpoint https://sasserver.demo.sas.com --output json --colors-enabled y"
            out, err = self.execute_command(command)
            print(out, "\nDone creating Profile!\n") if out else print(err, "\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def login_cli_sas_viya(self, profile, password):
        try:
            command = f'sas-viya auth login --user {profile} --password {password}'
            out, err = self.execute_command(command)
            print(out, "\nDone logging in profile!\n") if out else print(err, "\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def setup_cli_config(self):
        try:
            command = 'python3 /opt/pyviyatools/setup.py --clilocation /opt --cliexecutable sas-viya'
            out, err = self.execute_command(command)
            print(out, "\nDone CLI Configuration!\n") if out else print(err, "\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def setup_cli_install_packages(self):
        try:
            command = 'pip3 install -r /opt/pyviyatools/requirements.txt'
            out, err = self.execute_command(command)
            print(out, "\nSuccessfully setting up python packages\n") if out else print(err, "\n")
        except Exception as e:
            print(f"Error: {e}\n")

    def verify_cli_setup(self):
        try:
            command = 'python3 /opt/pyviyatools/showsetup.py -h'
            out, err = self.execute_command(command)
            print(out, "\n") if out else print(err, "\n")
        except Exception as e:
            print(f"Error: {e}\n")