import pymssql
import datetime
import uuid

conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_cma115', password='6EF2nNdnMYfe62Mr', database='cma115354')

def login():
    while True:
        user_id = input("Enter your user ID: ")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_yelp WHERE user_id = %s", user_id)
        user = cursor.fetchone()
        if not user:
            print("Invalid user ID. Please try again.")
        else:
            # Stores the user ID
            current_user = user_id
            # Displays a message
            print(f"Welcome, {user[1]}!")
            return current_user
        
def search_business():
    # Gets user input for search criteria
    while True:
        name = input("Enter business name or partial name: ").lower()
        if name.isalpha() or name == "":
            break
        else:
            print("Invalid input. Please enter alphabets only.")

    while True:
        city = input("Enter city: ").lower()
        if city.isalpha() or city == "":
            break
        else:
            print("Invalid input. Please enter alphabets only.")

    while True:
        try:
            min_stars = int(input("Enter minimum number of stars (1-5): "))
            max_stars = int(input("Enter maximum number of stars (1-5): "))
            if min_stars > max_stars or min_stars < 1 or max_stars > 5:
                print("Invalid input. Please enter a valid range of stars (1-5).")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter numbers only.")

    # Executes SQL query to search for businesses
    cursor = conn.cursor()
    query = "SELECT business_id, name, address, city, stars FROM business WHERE name LIKE '%{}%' AND city LIKE '%{}%' AND stars >= {} AND stars <= {} ORDER BY name".format(name, city, min_stars, max_stars)
    cursor.execute(query)
    results = cursor.fetchall()

    # Displays search results
    if len(results) == 0:
        print("No businesses found.")
    else:
        print("Search results:")
        for result in results:
            print("ID: {}\nName: {}\nAddress: {}\nCity: {}\nStars: {}\n".format(result[0], result[1], result[2], result[3], result[4]))
            
def search_users():
    # Gets user input for search criteria
    while True:
        name = input("Enter user name or partial name: ").lower()
        if name.isalpha() or name == "":
            break
        else:
            print("Invalid input. Please enter alphabets only.")

    while True:
        useful = input("Enter 'yes' or 'no' for useful: ").lower()
        if useful in ['yes', 'no', '']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    while True:
        funny = input("Enter 'yes' or 'no' for funny: ").lower()
        if funny in ['yes', 'no', '']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    while True:
        cool = input("Enter 'yes' or 'no' for cool: ").lower()
        if cool in ['yes', 'no', '']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Executes SQL query to search for users
    cursor = conn.cursor()
    query = "SELECT user_id, name, useful, funny, cool, yelping_since FROM user_yelp WHERE name LIKE '%{}%'".format(name)
    if useful == 'yes':
        query += " AND useful > 0"
    elif useful == 'no':
        query += " AND useful = 0"
    if funny == 'yes':
        query += " AND funny > 0"
    elif funny == 'no':
        query += " AND funny = 0"
    if cool == 'yes':
        query += " AND cool > 0"
    elif cool == 'no':
        query += " AND cool = 0"
    query += " ORDER BY name"
    cursor.execute(query)
    results = cursor.fetchall()

    # Displays the search results
    if len(results) == 0:
        print("No users found.")
    else:
        print("Search results:")
        for result in results:
            useful_str = result[2]
            funny_str = result[3]
            cool_str = result[4]
            print("ID: {}\nName: {}\nUseful: {}\nFunny: {}\nCool: {}\nYelping Since: {}\n".format(result[0], result[1], useful_str, funny_str, cool_str, result[5]))

def make_friend(user_id):
    # Gets the ID of the friend to add
    friend_id = input("Enter the ID of the user you want to be friends with: ")

    # Checks if the friend ID is valid
    cursor = conn.cursor()
    query = "SELECT * FROM user_yelp WHERE user_id = %s"
    cursor.execute(query, (friend_id,))
    result = cursor.fetchone()

    if not result:
        print("Invalid user ID. Please try again.")
        return

    # Adds the friendship to the database
    query = "INSERT INTO friendship (user_id, friend) VALUES (%s, %s)"
    cursor.execute(query, (user_id, friend_id))
    conn.commit()

    print("You are now friends with user ID", friend_id)

def write_review(current_user):
    # Gets the user input for business ID and number of stars
    while True:
        try:
            business_id = input("Enter business ID: ")
            stars = int(input("Enter number of stars (1-5): "))
            if stars < 1 or stars > 5:
                print("Invalid input. Please enter a number between 1 and 5.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    # Checks if the business ID exists in database
    cursor = conn.cursor()
    query = "SELECT * FROM business WHERE business_id = '{}'".format(business_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        print("Business ID not found.")
        return

    # Gets the current date, logged-in user ID, and a unique review id
    now = datetime.datetime.now()
    user_id = current_user
    review_id = str(uuid.uuid4())[:22]


    # Inserts the review into Review table
    query = "INSERT INTO review (review_id, user_id, business_id, stars, date) VALUES (%s, %s, %s, %s, %s)"
    values = (review_id, user_id, business_id, stars, now)
    cursor.execute(query, values)
    conn.commit()

    print("Review added successfully.")

# Defines the menu options
menu_options = {
    "1": "Search Businesses",
    "2": "Search Users",
    "3": "Make Friend",
    "4": "Write Review",
    "5": "Exit"
}

# Defines the menu function
def menu(current_user):
    while True:
        print("\nMenu:")
        for option, description in menu_options.items():
            print(f"{option}: {description}")
        choice = input("Enter an option: ")

        if choice == "1":
            # Runs Search Businesses function
            search_business()

        elif choice == "2":
            # Runs Search Users function
            search_users()

        elif choice == "3":
            # Runs Make Friend function
            make_friend(current_user)

        elif choice == "4":
            # Runs Write Review function
            write_review(current_user)

        elif choice == "5":
            print("Exiting program.")
            break
            
        else:
            print("Invalid option. Please try again.")

# Main function
def main():
    # Asks user to login
    current_user = login()
    if current_user:
        # Displays the menu
        menu(current_user)

if __name__ == "__main__":
    main()

