# classes.py

class Employee:
    def __init__(self, emp_id, first_name, last_name, position, department):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.department = department

    def __str__(self):
        return (f"Employee(id={self.emp_id}, name={self.first_name} {self.last_name}, "
                f"position={self.position}, department={self.department})")

    def __eq__(self, other):
        return isinstance(other, Employee) and self.emp_id == other.emp_id


class Shift:
    def __init__(self, date, hours):
        self.date = date
        self.hours = hours

    def __str__(self):
        return f"Shift(date={self.date}, hours={self.hours})"

    def __eq__(self, other):
        return isinstance(other, Shift) and self.date == other.date and self.hours == other.hours


class Department:
    def __init__(self, name, people_count):
        self.name = name
        self.people_count = people_count

    def __str__(self):
        return f"Department(name={self.name}, people_count={self.people_count})"

    def __eq__(self, other):
        return isinstance(other, Department) and self.name == other.name and self.people_count == other.people_count
