import os
import sys
import subprocess

def print_header():
    print("=" * 50)
    print("       ESIM AUTOMATED TOOL MANAGER (TASK 5)")
    print("=" * 50)

def check_python():
    print("\n[INFO] Checking Python installation and version...")
    try:
        version = sys.version.split()[0]
        print(f"[SUCCESS] Python is installed. Version: {version}")
    except Exception as e:
        print(f"[ERROR] Python check failed: {e}")

def check_ngspice():
    print("\n[INFO] Checking Ngspice installation...")
    try:
        result = subprocess.run(["ngspice", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Ngspice is installed and available in system path.")
            print(result.stdout.splitlines()[0])
        else:
            print("[WARNING] Ngspice command executed but returned non-zero status. Make sure it is added to environment variables.")
    except FileNotFoundError:
        print("[ERROR] Ngspice is NOT found on your system path. Please install Ngspice for eSim simulation support.")
    except Exception as e:
        print(f"[ERROR] An error occurred while checking Ngspice: {e}")

def run_dependency_checker():
    print("\n" + "-" * 30)
    print("   RUNNING DEPENDENCY CHECKER")
    print("-" * 30)
    check_python()
    check_ngspice()
    print("-" * 30)

def main():
    while True:
        print_header()
        print("1. Check Python and Ngspice Versions")
        print("2. Run Full Dependency Checker")
        print("3. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            check_python()
            check_ngspice()
        elif choice == '2':
            run_dependency_checker()
        elif choice == '3':
            print("\nExiting Automated Tool Manager. Goodbye!")
            break
        else:
            print("\n[INVALID CHOICE] Please enter a valid option between 1 and 3.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
