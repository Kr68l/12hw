from collections import UserDict
from datetime import date, timedelta


 class AddressBook(UserDict):
     def __init__(self, records_per_page=5):
     def __init__(self, data, records_per_page=5):
         super().__init__()
         self.data = data
         self.records_per_page = records_per_page

     def add_record(self, record):
        self.data[record.name.value] = record
     def __iter__(self):
         sorted_data = sorted(self.data.values(), key=lambda r: r.name.get_value())
         pages = [sorted_data[i:i+self.records_per_page] for i in range(0, len(sorted_data), self.records_per_page)]
         page_num = 0
         while page_num < len(pages):
             page = pages[page_num]
         for page in pages:
             for record in page:
                 yield f"{record.name}: {', '.join(record.phones)} ({record.birthday})" 
             page_num += 1
             if page_num < len(pages):
                 input(f"Press Enter to show next {self.records_per_page} records")
         return

                 yield f"{record.name}: {', '.join(record.phones)} ({record.birthday})"
             input(f"Press Enter to show next {self.records_per_page} records")

     def search(self, search_string):
     results = []
     for record in self.data.values():
        if search_string.lower() in record.name.get_value().lower() or search_string.lower() in ''.join(record.phones) in record.has_phone(phone):
            results.append(record)
    return results

    def delete_record(self, name):  
        if name in self.data:
            del self.data[name]
        else:
             raise ValueError(f"No record found with name {name}")

class Record():
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday
    def add_phone(self, phone):
        self.phones.append(phone)
    def edit_phone(self, phone_index, new_phone):
        self.phones[phone_index] = new_phone
    def delete_phone(self, phone_index):
        del self.phones[phone_index]
    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            bday = self.birthday.get_value().replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            return (bday - today).days
    def has_phone(self, phone):
        return phone in self.phones


class Birthday(Field):
    def set_value(self, value):
        try:
            dt = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use dd.mm.yyyy")
        today = date.today()
        if dt < today:
            raise ValueError("Birthday date should be in the future")
        self.value = dt
    def days_to_birthday(self): 
        if not self.value:
            return None
        today = date.today()
        bday = self.value.replace(year=today.year)
        if bday < today:
            bday = bday.replace(year=today.year + 1)
        return (bday - today).days 

 class Field:
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return str(self.value)
     def __repr__(self):
         return str(self.value)
     def __eq__(self, other):
         return self.value == other.value
     def __hash__(self):
         return hash(self.value)
     def get_value(self):
         return self.value
     def set_value(self, value):
         self.value = value
class Name(Field):
     pass
class Phone(Field):
    def set_value(self, value):
        if not re.match(r'^\+?\d{1,3}\s?\(?\d{1,3}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}$', value):
            raise ValueError("Invalid phone number format. Please use international format.")
        self.value = value
# address_book = {}
address_book = AddressBook()
def input_error(func):
      def inner(*args, **kwargs):
          try:
              return func(*args, **kwargs)
          except KeyError:
              return "Contact not found"
          except ValueError:
              return "Please enter name and phone number separated by space"
          except IndexError:
              return "Please enter contact name"
          except:
              return "An error occurred"
      return inner
@input_error
def add_contact(name, phone):
     name = Name(name.lower())
     phone = Phone(phone)
     rec = Record(name, phone)
     address_book.add_record(rec)
     return f"Contact {name} with phone number {phone} has been added"
@input_error
def change_contact(name, phone):
     address_book[name.lower()] = phone
     return f"Phone number for {name} has been changed to {phone}"
@input_error
def get_phone(name):
     return address_book[name.lower()]
def show_all():
     if not address_book:
         return "Phone book is empty"
     else:
         return "\n".join(f"{name}: {phone}" for name, phone in address_book.items())
def handle_command(command):
      command = command.lower()
      if command == "hello":
          return "How can I help you?"
      elif command in ("good bye", "close", "exit"):
          return "Good bye!"
      elif command.startswith("add"):
          parts = command.split()
          if len(parts) < 3:
              return "Please enter contact name and phone number"
          _, name, phone = parts
          return add_contact(name, phone)
      elif command.startswith("change"):
          parts = command.split()
          if len(parts) < 3:
              return "Please enter contact name and phone number"
          _, name, phone = parts
          return change_contact(name, phone)
      elif command.startswith("phone"):
          parts = command.split()
          if len(parts) < 2:
              return "Please enter contact name"
          _, name = parts
          return get_phone(name)
      elif command == "show all":
          return show_all()
      else:
          return "Unknown command"
def main():
      while True:
          command = input("Enter command: ")
          result = handle_command(command)
          print(result)
          if result == "Good bye!":
              break


 if name == '__main__':
     main()

     
     #82/31