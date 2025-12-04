from src.dashboard import KerneuralDashboard

if __name__ == "__main__":
    try:
        dashboard = KerneuralDashboard()
        dashboard.start()
    except KeyboardInterrupt:
        print("\nSystem stopped.")
