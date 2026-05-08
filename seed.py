import random
from faker import Faker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from db import SessionLocal, engine
from models import Base, Contact

fake = Faker()

def seed_database(num_contacts: int = 50):
    """
    Populates the database with random contact data.
    :param num_contacts: Number of contact records to create.
    """

    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        print("Starting the database seeding process...")
        
        existing_count = session.query(Contact).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} contacts.")

        new_contacts = []
        for _ in range(num_contacts):
            contact = Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:20],
                birthday=fake.date_of_birth(minimum_age=20, maximum_age=65),
                additional_data=fake.sentence(nb_words=4) if random.random() > 0.3 else None
            )
            new_contacts.append(contact)

        try:
            session.add_all(new_contacts)
            session.commit()
            print(f"Successfully added {num_contacts} new contacts!")
        except IntegrityError as e:
            session.rollback()
            print(f"Integrity error: likely a duplicate email. {e}")
        except Exception as e:
            session.rollback()
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    seed_database(100)