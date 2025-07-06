from itertools import islice

stream_users = __import__('0-stream_users')


def main():
    """Main function to demonstrate the streaming of user data."""
    for user in islice(stream_users.stream_users(), 6):
        print(user)


if __name__ == "__main__":
    main()
