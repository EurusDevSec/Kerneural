from src.red_agent.attacker import RedAgent
import time

def main():

    attacker = RedAgent(target_container="victim")
    attacker.execute_attack("T1059.004")
    time.sleep(2)

    attacker.execute_attack("T1555")


if __name__ == "__main__":
    main()