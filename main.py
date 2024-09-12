from toolz.curried import pipe, get
from service.assigned_service import get_top_7_unique_targets
from service.assigned_service import load_json

from repository.json_repository import read_pilots_from_json, read_aircraft_from_json, read_targets_from_json
pilots = load_json("./assets/pilots.json")
print(pilots)
pilots = []
aircraft = []
targets = []

def display_menu():
    print("\n--- Air Strike Simulation Menu ---")
    print("1. Load files (Pilots, Aircraft, Targets) from JSON")
    print("2. Display mission recommendations")
    print("3. Save mission recommendations to CSV")
    print("4. Exit")

def load_files():
    global pilots, aircraft, targets
    pilots = read_pilots_from_json('./assets/pilots.json')
    print(pilots)
    aircraft = read_aircraft_from_json('./assets/aircraft.json')
    print(aircraft)
    targets = read_targets_from_json('./assets/targets.json')
    print(targets)

def display_mission_recommendations():
    if not pilots or not aircraft or not targets:
        print("Please load the files first!")
        return
    print("\n--- Mission Recommendations ---")

def save_mission_recommendations_to_csv():
    if not pilots or not aircraft or not targets:
        print("Please load the files first!")
        return
    print("\n--- save mission recommendations to csv ---")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-4): ")
        if choice == '1':
            load_files()
        elif choice == '2':
            display_mission_recommendations()
        elif choice == '3':
            save_mission_recommendations_to_csv()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()


