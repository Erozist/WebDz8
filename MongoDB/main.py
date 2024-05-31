from typing import List, Union
from models import Quote, Author

def search_quotes_by_author(author_name: str) -> Union[List[str], str]:
    author = Author.objects(fullname__iexact=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        return [quote.quote for quote in quotes]
    else:
        return "Author not found."

def search_quotes_by_tag(tag: str) -> List[str]:
    quotes = Quote.objects(tags__icontains=tag)
    return [quote.quote for quote in quotes]

def search_quotes_by_tags(tags: List[str]) -> List[str]:
    quotes = Quote.objects(tags__icontains=tags[0])
    for tag in tags[1:]:
        quotes = quotes.filter(tags__icontains=tag)
    return [quote.quote for quote in quotes]

def process_command(command: str) -> Union[List[str], str]:
    command = command.lower()
    if command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        return search_quotes_by_author(author_name)
    elif command.startswith("tag:"):
        tag = command.split(":")[1].strip()
        return search_quotes_by_tag(tag)
    elif command.startswith("tags:"):
        tags = command.split(":")[1].strip().split(",")
        return search_quotes_by_tags(tags)
    elif command == "exit":
        return "Exiting script..."
    else:
        return "Invalid command. Please try again."

def main() -> None:
    while True:
        try:
            command = input("Enter command: ")
            result = process_command(command)
            if isinstance(result, list):
                if result:
                    print("\n".join(result))
                else:
                    print("No quotes found.")
            else:
                print(result)
            if result == "Exiting script...":
                break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
