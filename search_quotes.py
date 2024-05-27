from models import Quote, Author
import connect_to_mongo_db

import redis
from redis_lru import RedisLRU


redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)


def check_command(raw_command, command_list):
    for command in command_list:
        if raw_command.startswith(command):
            return command
    help_text = f"You can start command from one of next commands {command_list} + find text"  
    print(help_text)
    return None

def extract_parametr(raw_command):
    return raw_command.partition(":")[2].strip()

def extract_tags(raw_tags):
    return [tag.strip() for tag in raw_tags.split(",")]

@cache
def get_quotes_by_author(fullname):
    authors = Author.objects(fullname__icontains=fullname)   #string field contains value (case insensitive)
    #author = Author.objects(fullname=fullname).first()              #exact occurrence 
    if authors:
        return Quote.objects(author__in=authors)
    else:
        return []

@cache    
def get_quotes_by_tag(tag):
    #quotes = Quote.objects(tags=tag)              #exact occurrence
    return Quote.objects(tags__icontains=tag)       #string field contains value (case insensitive)

@cache
def get_quotes_by_tags(*tags):
    quotes = Quote.objects(tags__in=list(tags))
    return quotes

def print_quotes(quotes):
    if quotes:
        for quote in quotes:
            try:
                print(f"{quote.quote} - {quote.author.fullname}")
            except Exception as e:
                print(f"Error processing quote '{quote.quote}': {e}")
    else:
        print("No quotes found.")

def main():

    connect_to_mongo_db

    welcome_message = "Welcome"
    print(welcome_message)

    input_message = "input your request ->>"

    comand_list = ("name", "tags", "tag", "exit")

    while True:
        choice_text = input(input_message).strip()
        command = check_command(choice_text, comand_list)

        if command == "exit":
            quit()

        else:

            if ":" in choice_text:

                if command == "name":
                    author_name = extract_parametr(choice_text)
                    result = get_quotes_by_author(author_name)
                    print_quotes(result)


                elif command == "tags":
                    find_tags = extract_tags(extract_parametr(choice_text))
                    result = get_quotes_by_tags(*find_tags)
                    print_quotes(result)

                elif command == "tag":
                    find_tag = extract_parametr(choice_text)
                    result = get_quotes_by_tag(find_tag)
                    print_quotes(result)
            
            else:
                print(f"You must separate command from list {comand_list} and find text, by ':'")


if __name__ == "__main__":

    main()