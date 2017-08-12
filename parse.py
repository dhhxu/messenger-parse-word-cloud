"""
Parse Messenger chat logs.

Chat logs are HTML files with the following structure:

Thread 1 block
User A block
Message A block
User B block
Message B block
...
Thread 2 block
...

All messages between a set of people will be associated with only one thread.
"""

import argparse
import os
import sys

from lxml import etree


def parse_chat_logs(input_path, user, self):
    """
    Get messages from a person, or between that person and yourself.

    "self" does not necessarily have to be your name.

    Args:
        input_path (str): Path to chat log HTML file
        user (str): Full name of person, as appears in Messenger app
        self (str): Your name, as appears in Messenger app

    Returns:
        list[str]: Each element is a message, i.e. what gets sent when the
                   enter key is pressed
    """ 
    data = []
    current_user = None
    user_found = False
    skip_thread = False
    for element in etree.parse(input_path).iter():
        tag = element.tag
        content = element.text
        cls = element.get("class")
        if tag == "div" and cls == "thread":
            # Do not parse threads with more than two people
            skip_thread = content.count(",") > 1
            if user_found:
                user_found = False
        elif tag == "span" and cls == "user" and not skip_thread:
            current_user = content
            if current_user == user:
                user_found = True
        elif tag == "p" and not skip_thread:
            if (current_user == user) or (current_user == self and user_found):
                data.append(content)
    return data


def main():
    parser = argparse.ArgumentParser(description="Parse Messenger chat logs")
    parser.add_argument("-p", "--person", dest="person", type=str, required=True,
                        help="Full name of person to get messages for")
    parser.add_argument("-i", "--input", default="raw/messages.htm",
                        help="Path to Facebook chat log HTML file")
    parser.add_argument("-o", "--output", type=str, default="output",
                        help="Output directory for parsed messages (default: output/)")
    parser.add_argument("-s", "--self", type=str,
                        help="Full name of chat log owner")
    args = parser.parse_args()
    data = parse_chat_logs(args.input, args.person, args.self)

    if not data:
        print("No messages found. Exiting.")
        sys.exit(1)

    basename = os.path.join(args.output, args.person.replace(" ", ""))
    if args.self:
        basename += ("_" + args.self.replace(" ", ""))

    with open("{}.txt".format(basename), "w") as f:
        for line in data:
            if line:
                f.write("{}\n".format(line)) 
    

if __name__ == "__main__":
    main()
