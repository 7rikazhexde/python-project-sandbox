import argparse
import subprocess


def get_user_input() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=False, help="Enter a string")
    args = parser.parse_args()
    user_input = args.input
    return user_input


if __name__ == "__main__":
    user_input = get_user_input()

    if user_input:
        print(f"User input: {user_input}")
        subprocess.run(
            ["echo", "Hello, world!"], capture_output=True, text=True, input=user_input
        )
