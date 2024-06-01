#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kx"""

import sys
import typing as t
from dataclasses import dataclass
from enum import Enum, auto
from warnings import filterwarnings as filter_warnings

SPECIAL_TOKENS: t.Final[t.Set[str]] = {
    ";",
    ",",
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
    "!",
    "^",
    "%",
    "~",
}
STRING_PREFIXES: t.Final[str] = "nl"


class TokenType(Enum):
    type = auto()
    aname = auto()  # A name.
    function = auto()
    string = auto()
    number = auto()
    operator = auto()
    elipsis = auto()


@dataclass
class Token:
    type: TokenType
    token: str
    char: int
    line: int
    info: t.Optional[t.Any]


class TypeType(Enum):
    u8 = auto()
    i8 = auto()
    char = auto()
    bool = auto()
    u16 = auto()
    i16 = auto()
    char16 = auto()
    u32 = auto()
    i32 = auto()
    f32 = auto()
    char32 = auto()
    u64 = auto()
    i64 = auto()
    f64 = auto()
    ptr = auto()
    any = auto()


@dataclass
class Type:
    qualifiers: t.List[Token]
    type: TypeType
    pdepth: int  # Pointer depth


@dataclass
class Name:
    type: Type
    name: str


@dataclass
class Function:
    name: Name
    args: t.List[Name]
    variadic: bool
    body: t.List[Token]


def log(*args: str) -> None:
    print(*args)


def info(file: str, line: int, char: int, *args: str) -> None:
    print(f"{file}:{line}:{char}: \033[1m\033[34mInfo:\033[0m", *args)


def success(file: str, line: int, char: int, *args: str) -> None:
    print(f"{file}:{line}:{char}: \033[1m\033[32mSuccess:\033[0m", *args)


def warn(file: str, line: int, char: int, *args: str) -> None:
    print(
        f"{file}:{line}:{char}: \033[1m\033[33mWarning:\033[0m", *args, file=sys.stderr
    )


def err(file: str, line: int, char: int, *args: str) -> None:
    print(
        f"{file}:{line}:{char}: \033[1m\033[31mWarning:\033[0m", *args, file=sys.stderr
    )


def fatal(file: str, line: int, char: int, *args: str) -> t.NoReturn:
    print(
        f"{file}:{line}:{char}: \033[1m\033[31mFatal error:\033[0m",
        *args,
        file=sys.stderr,
    )
    sys.exit(1)


def tokenize(code: str) -> t.Tuple[int, int, t.List[t.Tuple[int, int, str]]]:
    """Tokenize given code into a list of tokens, ignoring comments."""

    idx: int = 0
    tokens: t.List[t.Tuple[int, int, str]] = []
    length: int = len(code)
    line: int = 1

    while idx < length:
        start: int = idx  # Start of the token.

        # Count lines
        if code[idx] == "\n":
            line += 1

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
                raise ValueError(f"Block comment not closed at line {line}.")

            idx: int = end_comment + 2
            continue

        # Handle strings with(out) prefixes n (non-null, no NULL at the end), l (literal).
        if code[idx] in "'\"" or (
            code[idx] in STRING_PREFIXES and idx + 1 < length and code[idx + 1] in "'\""
        ):
            if code[idx] in STRING_PREFIXES and code[idx + 1] in "'\"":
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

            tokens.append((line, start, code[start:idx]))
            continue

        # Handle identifiers and keywords.
        if code[idx].isalpha() or code[idx] == "_":
            while idx < length and (code[idx].isalnum() or code[idx] == "_"):
                idx += 1

            tokens.append((line, start, code[start:idx]))
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
                (line, start, code[start:idx].replace("_", ""))
            )  # Remove underscores from the token.
            continue

        # Handle special symbols.
        if code[idx] in SPECIAL_TOKENS:
            tokens.append((line, start, code[idx]))
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

        tokens.append((line, start, code[start:idx]))

    return line, idx, tokens


def build_ast(tokens: t.List[t.Tuple[int, int, str]], file: str) -> t.List[Token]:
    """Parse given tokens into a list of tokens(?)"""

    ast: t.List[Token] = []
    idx: int = 0

    type_tokens: t.Set[str] = {typ.name for typ in TypeType}

    while idx < len(tokens):
        char, line, token = tokens[idx]
        start: int = idx

        if token in type_tokens:  # Type
            typ: Type = Type(qualifiers=[], type=TypeType[token], pdepth=0)

            if tokens[idx + 1][2] == "*":  # Parse pointer depth
                idx += 1  # Skip the type

                while tokens[idx][2] == "*":
                    typ.pdepth += 1
                    idx += 1

            ast.append(
                Token(
                    type=TokenType.type,
                    token=token,
                    char=char,
                    line=line,
                    info=typ,
                )
            )
        elif token == "(": # Function definition
            fatal(file, char, line, f"Todo: {token!r}")
        else:
            if ast and ast[-1].type == TokenType.type:
                typ_tok: Token = ast.pop()

                if typ_tok.info is None:
                    warn(file, typ_tok.line, typ_tok.char, "Type has no type attribute.")
                    fatal(file, char, line, f"Unknown type for {token!r}")

                ast.append(
                    Token(
                        type=TokenType.aname,
                        token=token,
                        char=char,
                        line=line,
                        info=Name(type=typ_tok.info, name=token),
                    )
                )
            else:
                print(ast)
                fatal(file, char, line, f"Unknown token {token!r}")

        idx += 1

    return ast


def main() -> int:
    """entry/main function"""

    if len(sys.argv) < 2:
        print("Please supply the Kx file to compile.", file=sys.stderr)
        return 1

    file: str = sys.argv[1]

    info(file, 0, 0, f"Tokenizing {file} ...")

    lines, chars, tokens = 0, 0, []

    with open(file, "r") as fp:
        lines, chars, tokens = tokenize(fp.read())

    if len(tokens) == 0:
        fatal(file, 0, 0, "No tokens found.")

    print(tokens)
    success(
        file,
        lines,
        chars,
        f"Found {len(tokens)} tokens - processed {lines} line(s) and {chars} character(s). Building an AST ...",
    )

    ast: t.List[Token] = build_ast(tokens, sys.argv[1])

    print(ast)
    success(file, line, char, f"Found {len(ast)} ast element(s).")

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())
