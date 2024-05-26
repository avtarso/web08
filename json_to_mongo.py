import json
import logging
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import ReferenceField, DateField
from models import Quote, Author
import connect_to_mongo_db


def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def filter_data_by_keys(item_data, model):
    """Filters the data, leaving only those keys that are present in the model."""
    valid_keys = model._fields.keys()
    return {key: value for key, value in item_data.items() if key in valid_keys}

def convert_field_types(filtered_data, model):
    '''Converting a date from a string to a date object'''
    for field_name, field in model._fields.items():
        if isinstance(field, DateField) and field_name in filtered_data:
            try:
                filtered_data[field_name] = datetime.strptime(filtered_data[field_name], '%B %d, %Y')
            except ValueError as e:
                logging.error(f"Date conversion error for field {field_name}: {e}")
                raise
    return filtered_data

def filter_data(item_data, model):
    '''general data filtering before entering'''
    filtered_data = filter_data_by_keys(item_data, model)
    filtered_data = convert_field_types(filtered_data, model)
    return filtered_data

def update_reference_fields(filtered_data, model):
    """searching and updating links to objects"""
    for field_name, field in model._fields.items():
        if isinstance(field, ReferenceField):
            reference_model = field.document_type
            reference_value = filtered_data.get(field_name)
            if reference_value:
                try:
                    # Try to find one author by full name
                    reference_instance = reference_model.objects.get(fullname=reference_value)
                    filtered_data[field_name] = reference_instance
                except reference_model.DoesNotExist:
                    logging.error(f"Reference {reference_model.__name__} with value '{reference_value}' does not exist.")
                except reference_model.MultipleObjectsReturned:
                    logging.error(f"Multiple authors found with fullname '{reference_value}'.")
    return filtered_data

def save_data(filtered_data, model):
    try:
        item = model(**filtered_data)
        item.save()
    except (ValueError, TypeError) as e:
        error = f"Error while saving data:"
        print(f"{error}: {e}")
        logging.error(f"Error while saving data: {e}")
    except Exception as e:
        error = f"Unexpected error:"
        print(f"{error}: {e}")
        logging.error(f"{error} {e}")

def save_data_to_db(data, model: Document):
    for item_data in data:
        filtered_data = filter_data(item_data, model)
        filtered_data = update_reference_fields(filtered_data, model)
        save_data(filtered_data, model)


if __name__ == "__main__":

    connect_to_mongo_db
    
    # Setting up downloadable json-files and models
    data_sources = [
        ('source/authors.json', Author),
        ('source/quotes.json', Quote)
    ]

    # Setting up logging
    logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    for file_path, model in data_sources:
        data = load_data_from_json(file_path)
        save_data_to_db(data, model)

    print("Data successfully loaded into MongoDB!")
