from models import Contact

import connect_to_mongo_db

if __name__ == "__main__":
    
    connect_to_mongo_db

    contacts = Contact.objects(send_email=True)
    for contact in contacts:
        contact.send_email = False
        contact.save()

    print('Contact.send_email - switch off')
 