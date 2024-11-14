import datetime
from termcolor import colored
from src.database import sqlcontroller

def user_captcha():
    """
    This function prompts the user to enter the current day of the week.
    It returns False if the user's input does not match the actual current day of the week.

    Returns:
        bool: True if the user's input matches the current day of the week, False otherwise.
    """
    # Get the current day of the week
    current_day = datetime.datetime.now().strftime('%A').lower()

    # Prompt the user to enter the current day of the week
    user_input = input("Please enter the current day of the week: ").lower()

    # Return False if the user's input does not match the current day
    if user_input != current_day:
        return False

    return True

def drop_all_tables():
    """ Remove every table in the database """

    sql_fetch = """
        SELECT tablename FROM pg_tables WHERE schemaname='public'
    """
    tables = sqlcontroller.db_run(sql_fetch, multi=True)
    for table_name in tables:
        sql_drop = f"""
            DROP TABLE IF EXISTS {table_name[0]} CASCADE
        """
        sqlcontroller.db_run(sql_drop, fetch=False)

if __name__ == "__main__":
    
    import os
    print(os.getcwd())
    
    
    print(colored("WARNING: This will drop all tables. Please be sure you know what you're doing!", "red"))
    if user_captcha():
        print("Dropping all tables, no regrets")
        drop_all_tables()
    else:
        print("Captcha failed. Aborting.")
