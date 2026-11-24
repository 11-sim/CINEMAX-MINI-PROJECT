"""
=============================================================================
CINEMAX - Advanced Movie Ticket Booking System
Python Mini Project | Inspired by BookMyShow
Author: First Year Computer Science & Engineering Student
Technologies: Python 3 (CLI, 2D Lists, Dictionaries, Loops, Functions, Random)
=============================================================================
"""

import datetime
import random
import sys

# =============================================================================
# GLOBAL CONFIGURATION & DATA STRUCTURES
# =============================================================================

# GST Rate applicable on cinema tickets (18% - 9% CGST + 9% SGST)
GST_RATE = 0.18

# Seat Pricing Categories
SEAT_PRICES = {
    "Silver": 150,    # Rows A - D
    "Gold": 200,      # Rows E - H
    "Platinum": 300   # Rows I - J
}

# Theatres Database (Dictionary with names and addresses)
THEATRES = {
    "PVR Cinemas: Forum Mall": "4th Floor, Forum Mall, Koramangala",
    "INOX: City Centre": "Level 3, City Centre Mall, MG Road",
    "Cinepolis: Nexus Grand": "5th Floor, Nexus Mall, Whitefield",
    "PVR Superplex: Horizon": "Horizon Walkway, Indiranagar"
}

# Movies Database (Dictionary of dictionaries storing 8 detailed sample movies)
MOVIES = {
    1: {
        "id": 1,
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "language": "English",
        "duration": "2h 49m",
        "rating": 8.7,
        "release_date": "07 Nov 2014",
        "description": "Explorers travel through a wormhole in space to ensure humanity's survival.",
        "theatres": ["PVR Cinemas: Forum Mall", "INOX: City Centre", "Cinepolis: Nexus Grand"]
    },
    2: {
        "id": 2,
        "title": "Inception",
        "genre": "Thriller",
        "language": "English",
        "duration": "2h 28m",
        "rating": 8.8,
        "release_date": "16 Jul 2010",
        "description": "A thief who steals corporate secrets through dream-sharing is given a final mission.",
        "theatres": ["PVR Cinemas: Forum Mall", "PVR Superplex: Horizon"]
    },
    3: {
        "id": 3,
        "title": "3 Idiots",
        "genre": "Comedy",
        "language": "Hindi",
        "duration": "2h 50m",
        "rating": 8.4,
        "release_date": "25 Dec 2009",
        "description": "Two friends embark on a quest for a lost college buddy who challenged the education system.",
        "theatres": ["INOX: City Centre", "Cinepolis: Nexus Grand", "PVR Superplex: Horizon"]
    },
    4: {
        "id": 4,
        "title": "RRR",
        "genre": "Action",
        "language": "Telugu",
        "duration": "3h 07m",
        "rating": 7.8,
        "release_date": "25 Mar 2022",
        "description": "A fearless revolutionary and an officer in the British army forge an unbreakable friendship.",
        "theatres": ["PVR Cinemas: Forum Mall", "Cinepolis: Nexus Grand"]
    },
    5: {
        "id": 5,
        "title": "Coco",
        "genre": "Animation",
        "language": "English",
        "duration": "1h 45m",
        "rating": 8.4,
        "release_date": "22 Nov 2017",
        "description": "Aspiring musician Miguel confronts his family's ancestral ban on music in the Land of the Dead.",
        "theatres": ["INOX: City Centre", "PVR Superplex: Horizon"]
    },
    6: {
        "id": 6,
        "title": "La La Land",
        "genre": "Romance",
        "language": "English",
        "duration": "2h 08m",
        "rating": 8.0,
        "release_date": "09 Dec 2016",
        "description": "A jazz pianist and an aspiring actress fall in love while pursuing their passions in Los Angeles.",
        "theatres": ["PVR Cinemas: Forum Mall", "INOX: City Centre"]
    },
    7: {
        "id": 7,
        "title": "Avengers: Endgame",
        "genre": "Action",
        "language": "English",
        "duration": "3h 01m",
        "rating": 8.4,
        "release_date": "26 Apr 2019",
        "description": "The surviving Avengers assemble once more to reverse Thanos's devastating actions.",
        "theatres": ["PVR Cinemas: Forum Mall", "INOX: City Centre", "Cinepolis: Nexus Grand", "PVR Superplex: Horizon"]
    },
    8: {
        "id": 8,
        "title": "Hera Pheri",
        "genre": "Comedy",
        "language": "Hindi",
        "duration": "2h 36m",
        "rating": 8.2,
        "release_date": "31 Mar 2000",
        "description": "Three down-on-their-luck men find a wrong number call leading to a hilarious kidnapping ransom plan.",
        "theatres": ["INOX: City Centre", "Cinepolis: Nexus Grand"]
    }
}

# Standard Showtimes Available
SHOWTIMES = ["10:00 AM", "01:30 PM", "04:45 PM", "07:30 PM", "10:15 PM"]

# Session storage
# Maps unique show key -> 10x10 2D List of seats
SHOW_SEATS = {}

# Maps booking_id -> booking record dictionary
BOOKINGS = {}


# =============================================================================
# HELPER & UTILITY FUNCTIONS
# =============================================================================

def get_show_dates():
    """Generates 3 available show dates starting from today."""
    today = datetime.date.today()
    return [(today + datetime.timedelta(days=i)).strftime("%d %b %Y (%a)") for i in range(3)]


def get_seat_category(row_idx):
    """Returns seat category based on row index (0-9 for A-J)."""
    if row_idx <= 3:      # Rows A, B, C, D
        return "Silver"
    elif row_idx <= 7:    # Rows E, F, G, H
        return "Gold"
    else:                 # Rows I, J
        return "Platinum"


def get_seat_price(row_idx):
    """Returns ticket price for a given row index."""
    category = get_seat_category(row_idx)
    return SEAT_PRICES[category]


# =============================================================================
# SEATING ARRANGEMENT FUNCTIONS (2D LISTS)
# =============================================================================

def initialize_seats():
    """
    Creates a new 10x10 two-dimensional list.
    '[O]' represents an available seat.
    Simulates real cinema occupancy by randomly booking 8 to 15 seats.
    """
    rows = 10
    cols = 10
    # Create empty 10x10 grid of Available seats [O]
    seats = [["[O]" for _ in range(cols)] for _ in range(rows)]

    # Use random module to simulate pre-booked seats
    num_prebooked = random.randint(8, 15)
    booked_count = 0
    while booked_count < num_prebooked:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if seats[r][c] == "[O]":
            seats[r][c] = "[X]"
            booked_count += 1

    return seats


def get_or_create_show_seats(show_key):
    """Retrieves or initializes seating layout for a specific show."""
    if show_key not in SHOW_SEATS:
        SHOW_SEATS[show_key] = initialize_seats()
    return SHOW_SEATS[show_key]


def display_seats(seat_grid, temp_selected=None):
    """
    Displays the 10x10 theatre seating arrangement with categories,
    row identifiers (A-J), column numbers (1-10), and screen direction.
    """
    if temp_selected is None:
        temp_selected = []

    print("\n" + "=" * 65)
    print("                      SCREEN THIS WAY                     ")
    print("=" * 65)
    print("       1   2   3   4     5   6     7   8   9  10")
    print("     " + "-" * 47)

    row_letters = "ABCDEFGHIJ"
    for r in range(10):
        row_str = f" {row_letters[r]} | "
        category = get_seat_category(r)
        for c in range(10):
            seat_code = f"{row_letters[r]}{c + 1}"
            if seat_code in temp_selected:
                symbol = "[S]"  # Currently selected
            else:
                symbol = seat_grid[r][c]

            # Visual gangway spacing between seats 4-5 and 6-7
            if c in (4, 6):
                row_str += "  " + symbol
            else:
                row_str += " " + symbol

        row_str += f" | {category:<8} (₹{SEAT_PRICES[category]})"
        print(row_str)

        # Draw tier separator after Row D (Silver) and Row H (Gold)
        if r == 3:
            print("     " + "·" * 47 + " [ SILVER TIER - ₹150 ]")
        elif r == 7:
            print("     " + "·" * 47 + " [ GOLD TIER   - ₹200 ]")

    print("     " + "-" * 47 + " [ PLATINUM    - ₹300 ]")
    print("\n Legend: [O] Available   [X] Booked   [S] Selected")
    print("=" * 65)


def select_seats(seat_grid, ticket_qty):
    """
    Interactively selects valid seats matching requested ticket quantity.
    Returns list of seat codes (e.g., ['E5', 'E6']) or None if cancelled.
    """
    selected = []
    print(f"\nPlease select exactly {ticket_qty} seat(s). (e.g. E5 or enter '0' to cancel)")

    while len(selected) < ticket_qty:
        display_seats(seat_grid, selected)
        remaining = ticket_qty - len(selected)
        prompt = f"Enter seat code for ticket #{len(selected) + 1} ({remaining} remaining, '0' to back): "
        seat_input = input(prompt).strip().upper()

        if seat_input == '0':
            print("Seat selection cancelled.")
            return None

        # Validation: Format Check (Letter A-J followed by number 1-10)
        if len(seat_input) < 2 or len(seat_input) > 3:
            print("[!] Invalid seat format. Use Letter+Number like A1, F5, J10.")
            continue

        row_char = seat_input[0]
        col_str = seat_input[1:]

        if row_char not in "ABCDEFGHIJ" or not col_str.isdigit():
            print("[!] Row must be A-J and Column must be 1-10.")
            continue

        row_idx = ord(row_char) - ord('A')
        col_idx = int(col_str) - 1

        if col_idx < 0 or col_idx > 9:
            print("[!] Column number must be between 1 and 10.")
            continue

        # Check for duplicate selection in the current transaction
        if seat_input in selected:
            print(f"[!] You have already selected seat {seat_input}.")
            continue

        # Check if already booked
        if seat_grid[row_idx][col_idx] == "[X]":
            print(f"[!] Seat {seat_input} is ALREADY BOOKED. Please pick another seat.")
            continue

        category = get_seat_category(row_idx)
        price = SEAT_PRICES[category]
        selected.append(seat_input)
        print(f"[✓] Added {seat_input} ({category} - ₹{price})")

    # Final review of selected seats
    display_seats(seat_grid, selected)
    print(f"\nYou have selected {len(selected)} seat(s): {', '.join(selected)}")
    confirm = input("Confirm this seat selection? (Y/N): ").strip().upper()
    if confirm == 'Y':
        return selected
    else:
        print("Selection discarded.")
        return None


# =============================================================================
# PRICING, BILLING & PAYMENT SIMULATION
# =============================================================================

def calculate_bill(seat_codes):
    """
    Calculates subtotal, GST (18%), and final payable amount.
    Returns breakdown dictionary.
    """
    breakdown = []
    subtotal = 0

    for seat in seat_codes:
        row_char = seat[0]
        row_idx = ord(row_char) - ord('A')
        category = get_seat_category(row_idx)
        price = SEAT_PRICES[category]
        subtotal += price
        breakdown.append({
            "seat": seat,
            "category": category,
            "price": price
        })

    gst_amount = round(subtotal * GST_RATE, 2)
    grand_total = round(subtotal + gst_amount, 2)

    return {
        "items": breakdown,
        "ticket_count": len(seat_codes),
        "subtotal": subtotal,
        "gst_rate": int(GST_RATE * 100),
        "gst_amount": gst_amount,
        "grand_total": grand_total
    }


def display_price_breakdown(bill):
    """Prints a neat, itemized commercial invoice breakdown."""
    print("\n" + "=" * 55)
    print("               BOOKING PRICE BREAKDOWN                  ")
    print("=" * 55)
    print(f" {'Seat':<8} {'Category':<15} {'Base Price (₹)':>18}")
    print("-" * 55)
    for item in bill["items"]:
        print(f" {item['seat']:<8} {item['category']:<15} {item['price']:>18.2f}")
    print("-" * 55)
    print(f" Total Tickets: {bill['ticket_count']}")
    print(f" Subtotal:                              ₹{bill['subtotal']:>10.2f}")
    print(f" GST ({bill['gst_rate']}% Entertainment Tax):            ₹{bill['gst_amount']:>10.2f}")
    print("=" * 55)
    print(f" FINAL PAYABLE AMOUNT:                  ₹{bill['grand_total']:>10.2f}")
    print("=" * 55)


def process_payment(amount):
    """
    Simulates secure payment through UPI, Card, or Cash at Counter.
    Returns payment method string if successful, None if cancelled.
    """
    print("\n" + "=" * 45)
    print("             PAYMENT GATEWAY (SIMULATION)    ")
    print("=" * 45)
    print(f" Payable Amount: ₹{amount:.2f}\n")
    print(" Select Payment Method:")
    print("  1. UPI (Google Pay / PhonePe / Paytm)")
    print("  2. Debit / Credit Card")
    print("  3. Cash at Cinema Box-Office Counter")
    print("  0. Cancel Transaction")

    choice = input("\nEnter payment option (0-3): ").strip()

    if choice == '1':
        vpa = input("Enter your UPI ID (e.g., yourname@okhdfcbank): ").strip()
        if not vpa or "@" not in vpa:
            print("[!] Invalid UPI ID format. Payment aborted.")
            return None
        print(f"\n[→] Sending payment request of ₹{amount:.2f} to {vpa}...")
        otp = random.randint(1000, 9999)
        print(f"[Simulation] Verification code sent to your UPI App: {otp}")
        entered_otp = input(f"Enter the 4-digit code ({otp}) to approve: ").strip()
        if entered_otp == str(otp):
            print("[✓] UPI Payment Verified & Successful!")
            return f"UPI ({vpa})"
        else:
            print("[X] Incorrect OTP! Payment failed.")
            return None

    elif choice == '2':
        card = input("Enter 16-digit Card Number: ").strip().replace(" ", "")
        if len(card) != 16 or not card.isdigit():
            print("[!] Invalid Card Number. Must be 16 digits.")
            return None
        cvv = input("Enter 3-digit CVV: ").strip()
        if len(cvv) != 3 or not cvv.isdigit():
            print("[!] Invalid CVV.")
            return None
        masked_card = f"Card ending in {card[-4:]}"
        print(f"\n[✓] Card Payment of ₹{amount:.2f} Approved!")
        return masked_card

    elif choice == '3':
        print(f"\n[✓] Selected 'Cash at Counter'.")
        print(f"    Please collect your physical ticket by paying ₹{amount:.2f} at Audi Box Office.")
        return "Cash at Counter"

    elif choice == '0':
        print("Payment cancelled by user.")
        return None
    else:
        print("[!] Invalid choice. Payment failed.")
        return None


# =============================================================================
# TICKET GENERATION & FORMATTING
# =============================================================================

def generate_ticket(booking):
    """Displays a professionally formatted e-ticket with ASCII borders."""
    b_id = booking["booking_id"]
    movie = booking["movie_title"]
    theatre = booking["theatre"]
    location = booking["theatre_location"]
    date_str = booking["date"]
    time_str = booking["time"]
    audi = booking["audi"]
    seats_str = ", ".join(booking["seats"])
    qty = booking["ticket_count"]
    total = booking["grand_total"]
    pay_mode = booking["payment_method"]
    status = booking["status"]
    booked_on = booking["booking_time"]

    ticket = f"""
╔════════════════════════════════════════════════════════════════════════╗
║                          C I N E M A X                                 ║
║                    OFFICIAL DIGITAL E-TICKET                           ║
╠════════════════════════════════════════════════════════════════════════╣
║ BOOKING ID  : {b_id:<20} STATUS     : {status:<18} ║
║ BOOKED ON   : {booked_on:<48} ║
╠════════════════════════════════════════════════════════════════════════╣
║ MOVIE       : {movie:<48} ║
║ THEATRE     : {theatre:<48} ║
║ LOCATION    : {location:<48} ║
╠════════════════════════════════════════════════════════════════════════╣
║ DATE        : {date_str:<20} TIME       : {time_str:<18} ║
║ AUDITORIUM  : {audi:<20} TICKETS    : {str(qty) + ' Seat(s)':<18} ║
║ SEATS       : {seats_str:<48} ║
╠════════════════════════════════════════════════════════════════════════╣
║ TOTAL PAID  : ₹{total:<19.2f} PAYMENT    : {pay_mode:<18} ║
╠════════════════════════════════════════════════════════════════════════╣
║   Please present this digital e-ticket at the entrance. Enjoy movie!   ║
╚════════════════════════════════════════════════════════════════════════╝
"""
    print(ticket)


# =============================================================================
# NAVIGATION & MOVIE DISCOVERY FUNCTIONS
# =============================================================================

def display_banner():
    """Renders CINEMAX ASCII-art branding and current date & time."""
    now_str = datetime.datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")
    banner = f"""
  ██████╗██╗███╗   ██╗███████╗███╗   ███╗ █████╗ ██╗  ██╗
 ██╔════╝██║████╗  ██║██╔════╝████╗ ████║██╔══██╗╚██╗██╔╝
 ██║     ██║██╔██╗ ██║█████╗  ██╔████╔██║███████║ ╚███╔╝ 
 ██║     ██║██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══██║ ██╔██╗ 
 ╚██████╗██║██║ ╚████║███████╗██║ ╚═╝ ██║██║  ██║██╔╝ ██╗
  ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
             Premium Cinema Experience Platform
=============================================================================
 Current Date & Time: {now_str}
=============================================================================
"""
    print(banner)


def display_main_menu():
    """Prints the main system options."""
    print("┌" + "─" * 45 + "┐")
    print("│               MAIN NAVIGATION               │")
    print("├" + "─" * 45 + "┤")
    print("│  1. Explore All Movies                      │")
    print("│  2. Search & Filter Movies                  │")
    print("│  3. View Movie Details                      │")
    print("│  4. Book Tickets                            │")
    print("│  5. View My Bookings                        │")
    print("│  6. Cancel Booking                          │")
    print("│  7. Exit CINEMAX                            │")
    print("└" + "─" * 45 + "┘")


def explore_movies(movies_dict=None):
    """Displays a clean table listing movies."""
    if movies_dict is None:
        movies_dict = MOVIES

    if not movies_dict:
        print("\n[!] No movies found matching the criteria.")
        return

    print("\n" + "=" * 76)
    print(f" {'ID':<4} {'Title':<24} {'Genre':<12} {'Language':<10} {'Duration':<10} {'Rating':<6}")
    print("=" * 76)
    for mid, m in movies_dict.items():
        print(f" {m['id']:<4} {m['title']:<24} {m['genre']:<12} {m['language']:<10} {m['duration']:<10} ⭐ {m['rating']}")
    print("=" * 76)


def display_movie_details(movie_id=None):
    """Shows complete synopsis, ratings, and theatres for a selected movie."""
    if movie_id is None:
        explore_movies()
        try:
            movie_id = int(input("\nEnter Movie ID to view full details (0 to back): ").strip())
        except ValueError:
            print("[!] Please enter a valid numerical ID.")
            return

    if movie_id == 0:
        return

    if movie_id not in MOVIES:
        print(f"[!] Movie with ID #{movie_id} does not exist.")
        return

    m = MOVIES[movie_id]
    print("\n" + "#" * 60)
    print(f"   {m['title'].upper()} ({m['release_date']})")
    print("#" * 60)
    print(f" Genre       : {m['genre']}")
    print(f" Language    : {m['language']}")
    print(f" Duration    : {m['duration']}")
    print(f" IMDb Rating : ⭐ {m['rating']}/10")
    print(f"\n Synopsis:\n   {m['description']}")
    print("\n Available Theatres:")
    for idx, t in enumerate(m['theatres'], 1):
        print(f"   {idx}. {t} -> {THEATRES.get(t, 'Central')}")
    print("#" * 60)


def search_movies():
    """Allows searching by title keyword, genre filter, or language filter."""
    print("\n--- Search & Filter Movies ---")
    print("1. Search by Movie Name")
    print("2. Filter by Genre (Action, Comedy, Thriller, Romance, Sci-Fi, Animation)")
    print("3. Filter by Language (English, Hindi, Telugu)")
    print("0. Back to Main Menu")

    choice = input("\nEnter choice (0-3): ").strip()
    results = {}

    if choice == '1':
        query = input("Enter movie name keyword: ").strip().lower()
        if not query:
            print("[!] Query cannot be empty.")
            return
        for mid, m in MOVIES.items():
            if query in m['title'].lower():
                results[mid] = m

    elif choice == '2':
        genre = input("Enter genre to filter: ").strip().lower()
        for mid, m in MOVIES.items():
            if genre in m['genre'].lower():
                results[mid] = m

    elif choice == '3':
        lang = input("Enter language to filter: ").strip().lower()
        for mid, m in MOVIES.items():
            if lang in m['language'].lower():
                results[mid] = m

    elif choice == '0':
        return
    else:
        print("[!] Invalid search option.")
        return

    print(f"\nResults Found: {len(results)}")
    explore_movies(results)


# =============================================================================
# THEATRE & SHOWTIME SELECTION
# =============================================================================

def select_theatre(movie):
    """Lets user select an available cinema theatre for the chosen movie."""
    print(f"\nTheatres screening '{movie['title']}':")
    for idx, th in enumerate(movie['theatres'], 1):
        loc = THEATRES.get(th, "City Center")
        print(f"  {idx}. {th}")
        print(f"     Location: {loc}")

    while True:
        choice = input("\nSelect Theatre Number (0 to cancel): ").strip()
        if choice == '0':
            return None
        if choice.isdigit():
            c = int(choice)
            if 1 <= c <= len(movie['theatres']):
                selected_th = movie['theatres'][c - 1]
                return selected_th
        print("[!] Invalid selection. Please choose a valid theatre number.")


def select_showtime():
    """Lets user pick from available dates and standard showtimes."""
    dates = get_show_dates()
    print("\nAvailable Dates:")
    for idx, d in enumerate(dates, 1):
        print(f"  {idx}. {d}")

    selected_date = None
    while True:
        ch = input("\nSelect Date (1-3, 0 to cancel): ").strip()
        if ch == '0':
            return None, None
        if ch in ('1', '2', '3'):
            selected_date = dates[int(ch) - 1]
            break
        print("[!] Please enter 1, 2, or 3.")

    print("\nAvailable Showtimes:")
    for idx, t in enumerate(SHOWTIMES, 1):
        print(f"  {idx}. {t}")

    selected_time = None
    while True:
        ch = input("\nSelect Showtime (1-5, 0 to cancel): ").strip()
        if ch == '0':
            return None, None
        if ch.isdigit() and 1 <= int(ch) <= len(SHOWTIMES):
            selected_time = SHOWTIMES[int(ch) - 1]
            break
        print("[!] Please select a valid showtime number.")

    return selected_date, selected_time


# =============================================================================
# CORE BOOKING FLOW
# =============================================================================

def book_tickets():
    """Coordinates entire booking journey from movie pick to ticket output."""
    explore_movies()
    movie_choice = input("\nEnter Movie ID to book (0 to cancel): ").strip()
    if movie_choice == '0':
        return

    if not movie_choice.isdigit() or int(movie_choice) not in MOVIES:
        print("[!] Invalid Movie ID.")
        return

    movie = MOVIES[int(movie_choice)]

    # Theatre Selection
    theatre = select_theatre(movie)
    if not theatre:
        print("Booking process cancelled.")
        return

    # Showtime & Date Selection
    show_date, show_time = select_showtime()
    if not show_date or not show_time:
        print("Booking process cancelled.")
        return

    # Unique show key ensures separate seating maps per show
    show_key = f"{movie['id']}_{theatre}_{show_date}_{show_time}"
    seat_grid = get_or_create_show_seats(show_key)

    # Quantity Selection
    while True:
        qty_input = input("\nEnter number of tickets to book (1-10, 0 to cancel): ").strip()
        if qty_input == '0':
            print("Booking cancelled.")
            return
        if qty_input.isdigit() and 1 <= int(qty_input) <= 10:
            ticket_qty = int(qty_input)
            break
        print("[!] Enter a valid number between 1 and 10.")

    # Interactive Seat Selection
    selected_seats = select_seats(seat_grid, ticket_qty)
    if not selected_seats:
        return

    # Billing & Breakdown
    bill = calculate_bill(selected_seats)
    display_price_breakdown(bill)

    # Final User Confirmation
    confirm = input("\nProceed to payment? (Y/N): ").strip().upper()
    if confirm != 'Y':
        print("Booking abandoned by user.")
        return

    # Payment Simulation
    payment_mode = process_payment(bill["grand_total"])
    if not payment_mode:
        print("\n[!] Transaction could not be completed. Seats have not been booked.")
        return

    # Mark seats as BOOKED [X] in the 2D grid
    for seat in selected_seats:
        r = ord(seat[0]) - ord('A')
        c = int(seat[1:]) - 1
        seat_grid[r][c] = "[X]"

    # Generate unique Booking ID using random module
    random_num = random.randint(100000, 999999)
    booking_id = f"CNX-{random_num}"
    audi_name = f"Audi {random.choice([1, 2, 3, 4])}"

    # Store in BOOKINGS dictionary
    booking_record = {
        "booking_id": booking_id,
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "theatre": theatre,
        "theatre_location": THEATRES.get(theatre, "City Centre"),
        "date": show_date,
        "time": show_time,
        "audi": audi_name,
        "show_key": show_key,
        "seats": selected_seats,
        "ticket_count": ticket_qty,
        "bill": bill,
        "grand_total": bill["grand_total"],
        "payment_method": payment_mode,
        "booking_time": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "status": "CONFIRMED"
    }

    BOOKINGS[booking_id] = booking_record

    print("\n" + "*" * 50)
    print("      🎉 BOOKING CONFIRMED SUCCESSFULLY! 🎉      ")
    print("*" * 50)
    generate_ticket(booking_record)


# =============================================================================
# BOOKING HISTORY & CANCELLATION
# =============================================================================

def display_bookings_summary():
    """Prints a clean tabular summary of all session bookings and total spend."""
    print("\n" + "=" * 78)
    print("                            MY BOOKINGS                               ")
    print("=" * 78)
    print(f" {'Booking ID':<12} {'Movie':<20} {'Show Date':<15} {'Seats':<15} {'Total (₹)':<10} {'Status':<10}")
    print("-" * 78)

    total_spent = 0.0
    for b_id, b in BOOKINGS.items():
        seats_display = ", ".join(b["seats"])
        if len(seats_display) > 13:
            seats_display = seats_display[:11] + ".."
        print(f" {b_id:<12} {b['movie_title'][:18]:<20} {b['date'][:13]:<15} {seats_display:<15} {b['grand_total']:<10.2f} {b['status']:<10}")
        if b["status"] == "CONFIRMED":
            total_spent += b["grand_total"]

    print("=" * 78)
    print(f" Cumulative Money Spent on Active Bookings: ₹{total_spent:.2f}")
    print("=" * 78)


def view_bookings():
    """Lists all confirmed and cancelled bookings with full lookup."""
    if not BOOKINGS:
        print("\n[i] No bookings found in this session.")
        return

    display_bookings_summary()

    # Sub-menu to view specific ticket
    sub = input("\nEnter Booking ID to view e-ticket (or Press Enter to return): ").strip().upper()
    if sub:
        if sub in BOOKINGS:
            generate_ticket(BOOKINGS[sub])
        else:
            print(f"[!] Booking ID '{sub}' not found.")


def cancel_booking():
    """
    Cancels an active booking, updates status, and releases seats back to [O].
    """
    if not BOOKINGS:
        print("\n[i] No active bookings available to cancel.")
        return

    display_bookings_summary()
    b_id = input("\nEnter Booking ID to cancel (0 to return): ").strip().upper()
    if b_id == '0':
        return

    if b_id not in BOOKINGS:
        print(f"[!] Booking ID '{b_id}' does not exist.")
        return

    booking = BOOKINGS[b_id]

    if booking["status"] == "CANCELLED":
        print(f"[!] Booking '{b_id}' is ALREADY CANCELLED.")
        return

    print(f"\nFound Booking for: '{booking['movie_title']}' | Seats: {', '.join(booking['seats'])}")
    print(f"Paid Amount: ₹{booking['grand_total']:.2f}")
    confirm = input("Are you sure you want to cancel this booking? (Y/N): ").strip().upper()

    if confirm != 'Y':
        print("Cancellation aborted.")
        return

    # Release seats back to available [O] in the 2D grid
    show_key = booking["show_key"]
    if show_key in SHOW_SEATS:
        seat_grid = SHOW_SEATS[show_key]
        for seat in booking["seats"]:
            r = ord(seat[0]) - ord('A')
            c = int(seat[1:]) - 1
            seat_grid[r][c] = "[O]"

    # Update status
    booking["status"] = "CANCELLED"
    refund_amount = booking["grand_total"]

    print("\n" + "=" * 55)
    print("               CANCELLATION CONFIRMATION                  ")
    print("=" * 55)
    print(f" Booking ID       : {b_id}")
    print(f" Status           : CANCELLED")
    print(f" Released Seats   : {', '.join(booking['seats'])}")
    print(f" Refund Simulated : ₹{refund_amount:.2f} refunded via {booking['payment_method']}.")
    print(" Seats are now available for other cinema guests.")
    print("=" * 55)


# =============================================================================
# MAIN CONTROLLER LOOP
# =============================================================================

def main():
    """Main application loop with robust error handling."""
    while True:
        display_banner()
        display_main_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == '1':
            explore_movies()
            input("\nPress Enter to return to main menu...")
        elif choice == '2':
            search_movies()
            input("\nPress Enter to return to main menu...")
        elif choice == '3':
            display_movie_details()
            input("\nPress Enter to return to main menu...")
        elif choice == '4':
            book_tickets()
            input("\nPress Enter to return to main menu...")
        elif choice == '5':
            view_bookings()
            input("\nPress Enter to return to main menu...")
        elif choice == '6':
            cancel_booking()
            input("\nPress Enter to return to main menu...")
        elif choice == '7':
            print("\n" + "=" * 55)
            print("   Thank you for choosing CINEMAX! Have a great day!   ")
            print("=" * 55)
            sys.exit(0)
        else:
            print("\n[!] Invalid selection! Please enter a number from 1 to 7.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()