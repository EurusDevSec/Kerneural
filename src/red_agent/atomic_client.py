import yaml
import requests
from typing import List, Dict, Any

class AtomicClient:
    """
    Client to fetch and parse Atomic Red Team tests directly from GitHub.
    """
    BASE_URL = "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics"

    def fetch_technique(self, technique_id: str) -> List[Dict[str, Any]]:
        """
        Fetches and parses the Atomic Red Team YAML for a given technique ID.
        Returns a list of executable tests for Linux.
        """
        # Handle sub-techniques (e.g., T1059.004)
        # The URL structure is .../T1059.004/T1059.004.yaml
        url = f"{self.BASE_URL}/{technique_id}/{technique_id}.yaml"
        
        print(f"[*] Fetching Atomic Test from: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                print(f"[!] Technique {technique_id} not found in Atomic Red Team library.")
                return []
            
            response.raise_for_status()
            data = yaml.safe_load(response.text)
            
            linux_tests = []
            for test in data.get('atomic_tests', []):
                if 'linux' in test.get('supported_platforms', []):
                    # Extract executor details
                    executor = test.get('executor', {})
                    command = executor.get('command', '')
                    cleanup = executor.get('cleanup_command', '')
                    
                    # Check if it requires manual input (arguments)
                    # For automation, we might need to replace default args
                    args = test.get('input_arguments', {})
                    if args:
                        for arg_name, arg_data in args.items():
                            default_val = arg_data.get('default', 'test_value')
                            # Replace #{arg_name} with default value
                            command = command.replace(f"#{{{arg_name}}}", str(default_val))
                            if cleanup:
                                cleanup = cleanup.replace(f"#{{{arg_name}}}", str(default_val))

                    linux_tests.append({
                        'name': test.get('name'),
                        'description': test.get('description'),
                        'commands': command.strip(),
                        'cleanup': cleanup.strip() if cleanup else None
                    })
            
            print(f"[+] Found {len(linux_tests)} Linux tests for {technique_id}")
            return linux_tests
            
        except Exception as e:
            print(f"[!] Error fetching Atomic Test {technique_id}: {e}")
            return []
