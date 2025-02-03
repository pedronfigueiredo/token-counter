#!/usr/bin/env python3
import argparse
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """
    Returns the number of tokens in a text string using the specified encoding.
    See https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

def main():
    parser = argparse.ArgumentParser(
        description="Count the number of tokens in a text string or in a file using tiktoken."
    )
    # Using a mutually exclusive group so the user can either provide a text string or a file path.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--text",
        type=str,
        help="The text string to count tokens for."
    )
    group.add_argument(
        "--file",
        type=str,
        help="Path to a text file whose contents will be used for token counting."
    )

    parser.add_argument(
        "--encoding",
        type=str,
        default="cl100k_base",
        help=("The encoding name to use. "
              "Options include: o200k_base, cl100k_base, p50k_base, r50k_base. "
              "Default is cl100k_base.")
    )
    args = parser.parse_args()

    # Get the text content either from the '--text' argument or by reading the file specified in '--file'.
    if args.text:
        content = args.text
    else:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            return

    tokens_count = num_tokens_from_string(content, args.encoding)
    print(f"Number of tokens: {tokens_count}")

if __name__ == "__main__":
    main() 