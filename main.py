# Cinema Manager Module - Cinema Ticket Booking and Management System
from datetime import datetime

# -----------Global Variables------------
data_file = "cinema_data.txt"
showtimes_file = "showtimes.txt"
DEFAULT_TICKET_PRICE = 25.0
DEFAULT_DISCOUNT = 0.0
ticket_price = DEFAULT_TICKET_PRICE
discount = DEFAULT_DISCOUNT
# Empty Lists
movies = []
showtimes = []
auditoriums = []

# writing data in the file
def save_data():
    try:
        with open(data_file, "w") as f:
            f.write("--MOVIES--\n")
            for m in movies:
                f.write(str(m["id"]) + "|" + m["title"] + "|" + str(m["duration"]) + "|" + "\n")

            f.write("--SHOWTIMES--\n")
            for s in showtimes:
                f.write(
                    str(s["id"]) + "|" +
                    str(s["movie_id"]) + "|" +
                    str(s["time"]) + "|" +
                    str(s.get("auditorium_id", "")) + "\n"
                )

            f.write("--AUDITORIUMS--\n")
            for a in auditoriums:
                f.write(str(a["id"]) + "|" + a["name"] + "|" + str(a["capacity"]) + "\n")

            f.write("--TICKETS--\n")
            f.write(str(ticket_price) + "|" + str(discount) + "\n")

        with open(showtimes_file, "w") as f:
            f.write("--SHOWTIMES--\n")
            for s in showtimes:
                f.write(
                    str(s["id"]) + "|" +
                    str(s["movie_id"]) + "|" +
                    str(s["time"]) + "|" +
                    str(s.get("auditorium_id", "")) + "\n"
                )

    except Exception as e:
        print("Something went wrong while saving data:", e)

# reading data from the file
def load_data():
    global movies, showtimes, auditoriums, ticket_price, discount
    # resetting the system memory before readinf a new one
    movies = []
    showtimes = []
    auditoriums = []
    ticket_price = DEFAULT_TICKET_PRICE
    discount = DEFAULT_DISCOUNT

    try:
        # starts loading the fresh file
        f = open(data_file, "r")
        section = ""
        # removing the hidden newlines
        for line in f:
            line = line.replace("\n", "")
            if line == "":
                continue

            if line == "--MOVIES--":
                section = "movies"
                continue
            elif line == "--SHOWTIMES--":
                section = "showtimes"
                continue
            elif line == "--AUDITORIUMS--":
                section = "auditoriums"
                continue
            elif line == "--TICKETS--":
                section = "config"
                continue

            if section == "movies":
                parts = line.split("|")
                if len(parts) >= 3:
                    movie_id = parts[0]
                    title = parts[1]
                    try:
                        duration = int(parts[2])
                    except:
                        duration = 0
                    movies.append({"id": movie_id, "title": title, "duration": duration})

            elif section == "showtimes":
                parts = line.split("|")
                if len(parts) >= 3:
                    sid = parts[0]
                    movie_id = parts[1]
                    time = parts[2]
                    aud_id = parts[3] if len(parts) >= 4 else ""
                    showtimes.append({"id": sid, "movie_id": movie_id, "time": time, "auditorium_id": aud_id})

            elif section == "auditoriums":
                parts = line.split("|")
                if len(parts) >= 3:
                    aid = parts[0]
                    name = parts[1]
                    try:
                        capacity = int(parts[2])
                    except:
                        capacity = 0
                    auditoriums.append({"id": aid, "name": name, "capacity": capacity})

            elif section == "config":
                parts = line.split("|")
                if len(parts) >= 2:
                    try:
                        ticket_price = float(parts[0])
                    except:
                        ticket_price = 0
                    try:
                        discount = float(parts[1])
                    except:
                        discount = 0
        f.close()
    except FileNotFoundError:
        print("The file is  not created yet, a new one will be created.")
    except:
        print("Error")
    # Then: if showtimes.txt exists, prefer its content for showtimes (override)
    try:
        # starts loading the dedicated showtimes file
        f = open(showtimes_file, "r")
        section = ""
        loaded_showtimes = []

        # removing the hidden newlines
        for line in f:
            line = line.replace("\n", "")
            if line == "":
                continue

            if line == "--SHOWTIMES--":
                section = "showtimes"
                continue

            if section == "showtimes":
                parts = line.split("|")
                if len(parts) >= 3:
                    sid = parts[0]
                    movie_id = parts[1]
                    time = parts[2]
                    aud_id = parts[3] if len(parts) >= 4 else ""
                    loaded_showtimes.append({
                        "id": sid,
                        "movie_id": movie_id,
                        "time": time,
                        "auditorium_id": aud_id
                    })

        f.close()

        if loaded_showtimes:
            showtimes[:] = loaded_showtimes  # override with dedicated file

    except FileNotFoundError:
        print("The file is not created yet, a new one will be created.")
    except:
        print("Error")

# -----------GENERAL - DEFS------------
def get_time():
    print("**Examples: 9am, 9:30pm, 11:45pm**")
    print("**Cinema Operation Hours Are Between 12pm and 1am**")

    tries = 0

    while tries < 5:
        time_input = input("Enter time: ").strip().lower()

        # must end with am/pm
        if not (time_input.endswith("am") or time_input.endswith("pm")):
            print("Time must end with am or pm for a clearer vision.")
            tries += 1
            continue

        # add :00 if minutes missing
        if ":" not in time_input:
            time_input = time_input[:-2] + ":00" + time_input[-2:]

        try:
            user_time = datetime.strptime(time_input, "%I:%M%p")
        except:
            print("Invalid time format.")
            tries += 1
            continue

        # allow 12pm–11:59pm, plus 12:00–1:59am
        if not ((12 <= user_time.hour <= 23) or user_time.hour in (0, 1)):
            print("Operation hours are between 12pm and 1am.")
            tries += 1
            continue

        accepted_time = user_time.strftime("%I:%M %p").lstrip("0")
        print("Time accepted:", accepted_time)
        return accepted_time

    print("Too many failed attempts. Please try again later.")
    return None

# -----------MAIN - MENU------------
def manager_menu():
    load_data()
    while True:
        print("\n--- Cinema Manager Menu ---")
        print("1. Manage Movies")
        print("2. Manage Showtimes")
        print("3. Manage Auditoriums")
        print("4. Manage Prices & Discounts")
        print("5. Statistics")
        print("6. Exit Program")
        entered_choice = input("Enter your choice: ").strip()

        if entered_choice == "1":
            movies_menu()
        elif entered_choice == "2":
            showtimes_menu()
        elif entered_choice == "3":
            auditoriums_menu()
        elif entered_choice == "4":
            price_menu()
        elif entered_choice == "5":
            statistics_menu()
        elif entered_choice == "6":
            print("Exiting Cinema Manager Module...")
            save_data()
            break
        else:
            print("Invalid choice, try again.")

# -----------MOVIES- MENU------------
def movies_menu():
    while True:
        print("\n--- Movies Menu ---")
        print("1. Add Movie")
        print("2. Update Movie")
        print("3. Remove Movie")
        print("4. List Movies")
        print("5. Back")

        entered_choice = input("Enter your choice: ").strip()

        if entered_choice == "1":
            add_movie()
        elif entered_choice == "2":
            update_movie()
        elif entered_choice == "3":
            remove_movie()
        elif entered_choice == "4":
            list_movies()
        elif entered_choice == "5":
            save_data()
            break
        else:
            print("Invalid choice, try again.")

def add_movie():
    global movies

    # Auto generating IDs, max number quantity is 99
    if len(movies) == 0:
        movie_id = "M001"
    else:
        last = movies[-1]["id"]
        try:
            num = int(last[1:]) + 1
        except:
            num = len(movies) + 1

        if num < 10:
            movie_id = "M00" + str(num)
        elif num < 100:
            movie_id = "M0" + str(num)
        else:
            movie_id = "M" + str(num)

    title = input("Enter Title: ").strip().upper()

    if len(title) < 1 or len(title) > 100:
        print("Title can't be less than one letter and more than 100 letters")
        return
    # limiting the times the end-user can add a not proper input
    tries = 0
    while tries < 3:
        try:
            duration = int(input("Enter Duration (minutes): "))
            if duration >= 30 and duration <= 300:
                break
            else:
                # a realistic duration limit for movies
                print("Duration must be between 30 and 300 minutes.")
                tries = tries + 1
        except:
            print("Please enter a whole number for minutes.")
            tries = tries + 1

    if tries >= 3:
        print("Many attempts, try again.")
        return

    movies.append({"id": movie_id, "title": title, "duration": duration})

    print("Movie added successfully. Movie ID:", movie_id)
    save_data()

def update_movie():
    movie_id = input("Enter Movie ID to update: ")
    for movie in movies:
        if movie["id"] == movie_id:
            new_title = input("New Title: ").strip().upper()
            if len(new_title) < 1 or len(new_title) > 100:
                print("Title can't be less than one letter and more than 100 letters")
                return
            movie["title"] = new_title

            attempts = 0
            while attempts < 3:
                try:
                    new_duration = int(input("New Duration (minutes): "))
                    if 30 <= new_duration <= 300:
                        movie["duration"] = new_duration
                        print("Movie updated.")
                        save_data()
                        return
                    else:
                        print("Duration must be between 30 and 300 minutes.")
                        attempts += 1
                except ValueError:
                    print("Please enter a whole number for minutes.")
                    attempts += 1

            print("Many attempts, try again.")
            return

    print("Movie not found.")

def remove_movie():
    movie_id = input("Enter Movie ID to remove: ").strip().upper()
    # block if referenced
    if any(s["movie_id"] == movie_id for s in showtimes):
        print("Cannot remove movie; it is used by existing showtimes. Reassign or delete those showtimes first.")
        return
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            print("Movie removed.")
            save_data()
            return
    print("Movie not found.")

def list_movies():
    if not movies:
        print("No movies available.")
        return
    print("\nList of Movies:")
    for m in movies:
        print(
            f"ID: {m['id']}, Title: {m['title']}, Duration: {m['duration']} min"
        )

# -----------AUDITORIUM - MENU------------
def auditoriums_menu():
    while True:
        print("\n--- Auditoriums Menu ---")
        print("1. Add Auditorium")
        print("2. Update Auditorium")
        print("3. Remove Auditorium")
        print("4. List Auditoriums")
        print("5. Back")

        entered_choice = input("Enter your choice: ")

        if entered_choice == "1":
            add_auditorium()
        elif entered_choice == "2":
            update_auditorium()
        elif entered_choice == "3":
            remove_auditorium()
        elif entered_choice == "4":
            list_auditoriums()
        elif entered_choice == "5":
            save_data()
            break
        else:
            print("Invalid choice, try again.")

def add_auditorium():
    global auditoriums

    # Auto-generate ID, starting from A001
    if len(auditoriums) == 0:
        aid = "A001"
    else:
        last = auditoriums[-1]["id"]
        try:
            num = int(last[1:]) + 1
        except:
            num = len(auditoriums) + 1

        if num < 10:
            aid = "A00" + str(num)
        elif num < 100:
            aid = "A0" + str(num)
        else:
            aid = "A" + str(num)

    name = input("Enter Auditorium Name: ").strip().upper()
    if len(name) < 1 or len(name) > 100:
        print("Auditorium Name can't be less than one letter and more than 100 letters")
        return

    try:
        capacity = int(input("Enter Capacity (number): "))
        if capacity < 30 or capacity > 1000:
            print(
                "The Capacity Of Auditoriums Can't be more than 1000 or less than 30, according to the company regulations and safety standards.")
            return
    except:
        print("Invalid capacity.")
        return

    auditoriums.append({"id": aid, "name": name, "capacity": capacity})
    print("Auditorium added successfully. Auditorium ID:", aid)
    save_data()

def update_auditorium():
    aid = input("Enter Auditorium ID to update: ").strip().upper()
    # ID length validation
    for a in auditoriums:
        if a["id"] == aid:
            new_name = input("New Auditorium Name: ").strip().upper()
            if len(new_name) < 1 or len(new_name) > 100:
                print("Name can't be less than one letter or more than 100 letters.")
                return
            a["name"] = new_name
            try:
                capacity = int(input("New Capacity (number): "))
                if capacity < 30 or capacity > 1000:
                    print("Capacity must be between 30 and 1000.")
                    return
            except ValueError:
                print("Invalid capacity. Update cancelled.")
                return
            print("Auditorium updated.")
            save_data()
            return
    else:
        print("Auditorium not found.")

def remove_auditorium():
    aid = input("Enter Auditorium ID to remove: ").strip().upper()
    for a in auditoriums:
        if a["id"] == aid:
            linked_shows = [s for s in showtimes if s.get("auditorium_id") == aid]
            if linked_shows:
                print(
                    "Cannot remove auditorium; it's used by existing showtimes. Reassign or delete those showtimes first.")
                return
            auditoriums.remove(a)
            print("Auditorium removed.")
            save_data()
            return
    print("Auditorium not found.")

def list_auditoriums():
    if not auditoriums:
        print("No Auditoriums Available.")
        return
    print("\nAuditoriums:")
    for a in auditoriums:
        print(f"ID: {a['id']}, Name: {a['name']}, Capacity: {a['capacity']}")

# -----------SHOWTIMES - MENU------------
def showtimes_menu():
    global showtimes, auditoriums

    while True:
        print("\n--- Showtimes Menu ---")
        print("1. Create Showtime")
        print("2. Edit Showtime")
        print("3. Delete Showtime")
        print("4. List Showtime")
        print("5. Back")

        entered_choice = input("Enter choice: ").strip()

        if entered_choice == "1":
            create_showtime()
        elif entered_choice == "2":
            edit_showtime()
        elif entered_choice == "3":
            delete_showtime()
        elif entered_choice == "4":
            list_showtimes()
        elif entered_choice == "5":
            save_data()
            break
        else:
            print("Invalid choice, try again.")

def create_showtime():
    global showtimes, auditoriums

    # Auto ID generation
    if len(showtimes) == 0:
        show_id = "SH001"
    else:
        last = showtimes[-1]["id"]
        try:
            num = int(last[2:]) + 1
        except:
            num = len(showtimes) + 1

        if num < 10:
            show_id = "SH00" + str(num)
        elif num < 100:
            show_id = "SH0" + str(num)
        else:
            show_id = "SH" + str(num)

    movie_id = input("Enter Movie ID: ").strip().upper()

    # find the movie
    found = False
    for movie in movies:
        if movie["id"] == movie_id:
            found = True
            break

    if not found:
        print("Movie not found.")
        return

    time = get_time()
    if time is None:
        print("Many Attempts~. Returning to Showtimes Menu...")
        return

    # Choose auditorium
    if len(auditoriums) == 0:
        print("No Auditoriums Available. Please add one first.")
        return
    else:
        print("\nAvailable Auditoriums:")
        for a in auditoriums:
            print("-", a["id"], a["name"])
        aud_id = input("Enter Auditorium ID: ").strip().upper()

    # Validate auditorium ID
    found = False
    for a in auditoriums:
        if a["id"] == aud_id:
            found = True
            break

    if not found:
        print("Invalid Auditorium ID. Please enter an existing ID.")
        return

    # Save showtime
    exists = False
    for s in showtimes:
        if s["id"] == show_id:  # make sure show_id is defined earlier
            exists = True
            break

    if exists:
        print("Showtime ID already exists. Try again.")
    else:
        showtimes.append({
            "id": show_id,
            "movie_id": movie_id,
            "time": time,
            "auditorium_id": aud_id
        })
        print("Showtime added. ID:", show_id, "Movie:", movie_id, "Auditorium:", aud_id, "Time:", time)
        save_data()

def edit_showtime():
    global showtimes, auditoriums, movies

    # Show list first
    if not showtimes:
        list_showtimes()  # prints "No showtimes available."
        return
    else:
        list_showtimes()

    show_id = input("Enter Showtime ID to edit: ").strip().upper()
    for s in showtimes:
        if s["id"] == show_id:
            # --- Movie selection (optional, validated) ---
            print("\nAvailable Movies:")
            list_movies()  # shows ID / Title / Duration
            new_movie = input("New Movie ID (press Enter to keep current): ").strip().upper()
            if new_movie:
                if any(m["id"] == new_movie for m in movies):
                    s["movie_id"] = new_movie
                else:
                    print("Invalid Movie ID. Edit cancelled.")
                    return  # stop edit if invalid

            # --- Time edit (optional, validated via get_time) ---
            change_time = input("Change start time? (y/N): ").strip().lower()
            if change_time == "y":
                print("Enter New Start Time:")
                new_time = get_time()
                if new_time is None:
                    print("Edit cancelled (too many invalid attempts).")
                    return
                s["time"] = new_time

            # --- Auditorium selection (optional, validated) ---
            if not auditoriums:
                print("No Auditoriums Available. Please add one first.")
                return

            print("\nAvailable Auditoriums:")
            list_auditoriums()  # shows ID / Name / Capacity
            new_aud = input("New Auditorium ID (press Enter to keep current): ").strip().upper()
            if new_aud:
                if any(a["id"] == new_aud for a in auditoriums):
                    s["auditorium_id"] = new_aud
                else:
                    print("Invalid Auditorium ID. Edit cancelled.")
                    return  # stop edit if invalid

            print("Showtime updated.")
            save_data()
            return
    print("Showtime not found.")

def delete_showtime():
    global showtimes

    show_id = input("Enter Showtime ID to delete: ").strip().upper()
    found = False
    for s in showtimes:
        if s["id"] == show_id:
            showtimes.remove(s)
            print("Showtime deleted.")
            save_data()
            found = True
            break
    if not found:
        print("Showtime not found.")

def list_showtimes():
    if not showtimes:
        print("No showtimes available.")
        return
    print("\nShowtimes List:")
    for s in showtimes:
        print(f"ID: {s['id']}, Movie ID: {s['movie_id']}, Time: {s['time']}, Auditorium ID: {s['auditorium_id']}")


# -----------TICKETS - MENU------------
def price_menu():
    global ticket_price, discount
    print("\n--- Price Menu ---")

    print("Current ticket price: RM", ticket_price)
    print("Current discount:", discount * 100, "%")

    while True:
        try:
            new_price = input("Enter new base ticket price: ").strip()
            new_price = float(new_price)

            if new_price < 5 or new_price > 500:
                print("Ticket price must be between RM5 and RM500.")
                continue

            ticket_price = new_price
            print("New Ticket price set to: RM", ticket_price)
            save_data()
            break
        except ValueError:
            print("Please enter a valid number like 20 or 50.")

    while True:
        try:
            new_discount_input = input("Enter discount percentage (20 for 20%): ").strip()
            new_discount = float(new_discount_input)

            if new_discount >= 0 and new_discount <= 50:
                discount = new_discount / 100
                print("Discount set to:", new_discount, "%")
                save_data()
                break
            else:
                print("Discount Max Limit Is 50%.")

        except ValueError:
            print("Please enter a valid number like 10 or 25.")

    print("Prices updated. Base: RM", ticket_price, ", Discount:", new_discount, "%")
    print("Final price after discount: RM", ticket_price * (1 - discount))

# -----------STATISTICS - MENU------------
def statistics_menu():
    print("\n--- Statistics Section ---")

    print("\n--- Movies ---")
    list_movies()

    print("\n--- Auditoriums ---")
    list_auditoriums()

    print("\n--- Showtimes ---")
    list_showtimes()

    print("\n--- Tickets ---")
    print(f"Ticket Price: RM{ticket_price}")
    print(f"Discount: {discount * 100}%")
    print(f"Price After Discount: RM{ticket_price * (1 - discount)}")

    print("\nReturning To Cinema Management Menu...")
    save_data()



# -----------PROGRAM ENTRY POINT------------
def main():
    print("**************************************")
    print("Welcome to the Cinema Manager Module")
    print("**************************************")
    manager_menu()
    print("Thank you for using the Cinema Manager Module.")

if __name__ == "__main__":
    main()
