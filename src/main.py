#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kx"""

import sys
import typing as t
from warnings import filterwarnings as filter_warnings

SPECIAL_TOKENS: t.Final[t.Set[str]] = {
    ";",
    ",",
    ".",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "+",
    "-",
    "*",
    "/",
    "=",
    "<",
    ">",
    "!",
    "&",
    "|",
    "^",
    "%",
    "~",
}


def tokenize(code: str) -> list[str]:
    """Tokenize given code into a list of tokens, ignoring comments."""

    idx: int = 0
    tokens: list[str] = []
    length: int = len(code)

    while idx < length:
        start: int = idx  # Start of the token.

        # Skip whitespace.
        if code[idx].isspace():
            idx += 1
            continue

        # Handle line comments (//).
        if code[idx : idx + 2] == "//":
            idx = code.find("\n", idx)

            if idx == -1:  # No newline found, end of file.
                break

            continue

        # Handle block comments (/* ... */).
        if code[idx : idx + 2] == "/*":
            end_comment: int = code.find("*/", idx + 2)

            if end_comment == -1:
                raise ValueError("Block comment not closed")

            idx: int = end_comment + 2
            continue

        # Handle strings with(out) prefixes u, l.
        if code[idx] in "'\"" or (
            code[idx] in "ul" and idx + 1 < length and code[idx + 1] in "'\""
        ):
            if code[idx] in "ul" and code[idx + 1] in "'\"":
                idx += 2  # Skip prefix and opening quote.
                end_char = code[idx - 1]
            else:
                end_char = code[idx]
                idx += 1  # Skip opening quote

            while idx < length and code[idx] != end_char:
                if code[idx] == "\\":
                    idx += 2  # Skip escaped character.
                else:
                    idx += 1

            if idx < length:
                idx += 1  # Skip closing quote

            tokens.append(code[start:idx])
            continue

        # Handle identifiers and keywords.
        if code[idx].isalpha() or code[idx] == "_":
            while idx < length and (code[idx].isalnum() or code[idx] == "_"):
                idx += 1

            tokens.append(code[start:idx])
            continue

        # Handle numbers (integers, hex, octal, binary, floats).
        if (
            code[idx].isdigit()
            or (code[idx] == "-" and idx + 1 < length and code[idx + 1].isdigit())
            or (code[idx] == "." and idx + 1 < length and code[idx + 1].isdigit())
            or (code[idx] == "0" and idx + 1 < length and code[idx + 1] in "xobXOB")
        ):
            if code[idx] == "-":
                idx += 1

            if code[idx] == "0" and idx + 1 < length:
                # Prefixes.
                if code[idx + 1] in "xX":  # Hexadecimal
                    idx += 2
                elif code[idx + 1] in "oO":  # Octal
                    idx += 2
                elif code[idx + 1] in "bB":  # Binary
                    idx += 2

            # Continue until a non-space, non-underscore, non-dot, and non-exponent character is found.
            while idx < length and ((not code[idx].isspace()) or code[idx] in "._eE+-"):
                if code[idx] == "_":
                    idx += 1  # Skip underscore
                    continue

                idx += 1

            tokens.append(
                code[start:idx].replace("_", "")
            )  # Remove underscores from the token
            continue

        # Handle special symbols.
        if code[idx] in SPECIAL_TOKENS:
            tokens.append(code[idx])
            idx += 1
            continue

        # Handle other operators.
        while (
            idx < length
            and not code[idx].isspace()
            and not code[idx].isalnum()
            and code[idx] not in SPECIAL_TOKENS
        ):
            idx += 1

        tokens.append(code[start:idx])

    return tokens


def main() -> int:
    """entry/main function"""

    if len(sys.argv) < 2:
        print("Please supply the Kx file to compile.", file=sys.stderr)
        return 1

    with open(sys.argv[1], "r") as fp:
        print(tokenize(fp.read()))

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())
