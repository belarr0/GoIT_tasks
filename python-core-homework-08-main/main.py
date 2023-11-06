from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):
    today = date.today()
    current_year = today.year

    if not users:
        return {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }

    birthdays_per_week = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }

    for user in users:
        new_birthday_date = user["birthday"].replace(year=current_year)

        if new_birthday_date < today:
            continue

        day_of_week = new_birthday_date.weekday()
        #print(day_of_week)
        if 0 <= day_of_week <= 5:
            day_name = list(birthdays_per_week.keys())[day_of_week-1]
            birthdays_per_week[day_name].append(user["name"])
        elif 5 < day_of_week < 7:
            birthdays_per_week['Monday'].append(user["name"])

    return birthdays_per_week


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()},
        {"name": "Mark Zuckerberg", "birthday": datetime(1984, 5, 14).date()},
        {"name": "Ded", "birthday": datetime(1958, 12, 4).date()}
    ]

    result = get_birthdays_per_week(users)
    print(result)
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
