tokens = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "=": "EQUALS",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACK",
    "}": "RBRACK",
    " ": "SPACE",
    "\"": "QUOTE",
    ";": "SEMICOLON",
    ",": "COMMA",
    ":": "COLON",
    "?": "QUESTION-POINT",
    "!": "EXCLAMATION-POINT",
    "\n": "NEWLINE"
}
abc = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
digits = list("0123456789")
operators = ["PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQUALS"]
reserved_names = [
    "var"
]

def lex(code: str):
    """
    Returns an array of <code> but tokenized, in chronological order.

    Tokens are individual dicts, structured like:
    {
        "token": ["NAME", "INTEGER", or one of the symbol tokens],
        "value": the value of the token if one is required,
        "name": the name of the token if it is required (currently only with NAME tokens)
    }
    """
    name = ""
    num = ""
    out = list()
    
    idx = 0
    for char in code:
        if (char not in tokens.keys()) and (char not in abc) and (char not in digits):
            print(f"Illegal character: {char} (at index {idx})") # Raise error later

        elif char in abc:
            name += char
            
            try:
                if code[idx + 1] not in abc:
                    out.append({"token": "NAME", "name": name, "value": name})
                    name = ""

            except IndexError:
                out.append({"token": "NAME", "name": name, "value": name})
                name = ""

        elif char in digits:
            num += char

            try:
                if code[idx + 1] not in digits:
                    out.append({"token": "INTEGER", "value": num})
                    num = ""

            except IndexError:
                out.append({"token": "INTEGER", "value": num})
                num = ""
        
        else:
            out.append({"token": tokens[char], "value": char})

        idx += 1

    return out