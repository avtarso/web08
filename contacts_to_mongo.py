import random
from faker import Faker

from models import Contact
import connect_to_mongo_db


number_of_contacts = 10

fake = Faker('UK_UA')

def create_phone():
    pref = ['99', '98', '97', "96", "95", "94", "93", "92", "91", "68", "67", "66", "63","50"]
    return "+380" + random.choice(pref) + str(random.randint(1111111, 9999999))


if __name__ == "__main__":

    connect_to_mongo_db
    
    for _ in range(number_of_contacts):
        contact = Contact()
        contact.fullname = fake.name()
        contact.email = fake.email()
        contact.phone = create_phone()
        contact.send_email = False
        contact.send_sms = False
        contact.born_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
        contact.save()

    print("Data successfully loaded into MongoDB!")
