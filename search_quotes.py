import json
import logging
from bson import ObjectId
from datetime import datetime
from mongoengine import Document
from models import Quote, Author
import connect_to_mongo_db


def check_command(raw_command, command_list):
    for command in command_list:
        if raw_command.startswith(command):
            return command
    help_text = f"You can start command from one of next commands {comand_list} + find text"  
    print(help_text)

def extract_parametr(raw_command):
    return raw_command.partition(":")[2]

def extract_tags(raw_tags):
    tags = raw_tags.split(",")
    return tags

def get_quotes_by_author(fullname):
    author = Author.objects(fullname=fullname).first()
    if author:
        quotes = Quote.objects(author=author)
        return quotes
    else:
        return []
    

if __name__ == "__main__":

    connect_to_mongo_db

    welcome_message = "Welcome"
    print(welcome_message)

    input_message = "input your request ->>"

    comand_list = ("name", "tags", "tag", "exit")

    while True:
        choice_text = input(input_message)
        command = check_command(choice_text, comand_list)
        print(command)
        if command == "exit":
            quit()
        else:
            if choice_text.find(":") > -1:

                if command == "name":
                    author_name = extract_parametr(choice_text)
                    result = get_quotes_by_author(author_name)
                    if result:
                        for item in result:
                            try:
                                print(f"{item.quote} - {item.author.fullname}")
                            except Exception as e:
                                print(f"Error processing quote '{quote.quote}': {e}")
                    else:
                        print(f"Quotes from author - '{author_name}' is not exist")

                elif command == "tags":
                    find_tags = extract_tags(extract_parametr(choice_text))
                    quotes = Quote.objects(tags__in=list(find_tags))
                    if quotes :
                        for quote in quotes:
                            try:
                                print(quote.quote)
                            except Exception as e:
                                print(f"Error processing quote '{quote.quote}': {e}")
                    else:
                        print(f"Quotes from tags - '{find_tags}' is not exist")


                elif command == "tag":
                    find_tag = extract_parametr(choice_text)
                    quotes = Quote.objects(tags=find_tag)
                    if quotes :
                        for quote in quotes:
                            try:
                                print(quote.quote)
                            except Exception as e:
                                print(f"Error processing quote '{quote.quote}': {e}")
                    else:
                        print(f"Quotes from tag - '{find_tag}' is not exist")
            
            else:
                print(f"You must separate command from list {comand_list} and find text, by ':'")

