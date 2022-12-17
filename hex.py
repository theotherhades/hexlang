import typer
import lang
import os

app = typer.Typer()

@app.command()
def compile(file: str):
    with open(file, "r") as f:
        # print(lang.lex(f.read()))
        token_seq = lang.lex(f.read())
        lines = list()
        line = list()
        
        for token in token_seq:
            line.append(token)
            if token["token"] == "SEMICOLON":
                lines.append(line)
                line = list()

    if not os.path.exists(f"{os.getcwd()}/dist"):
        os.mkdir(f"{os.getcwd()}/dist")

    with open(f"{os.getcwd()}/dist/out.py", "w+") as f:
        for line in lines:
            if line[0]["token"] == "NAME":
                match line[0]["name"]:
                    case "var":
                        """
                        Declare a variable.
                        All of the below fields must be assigned otherwise an error should be thrown:
                        name (string): The variable's name.
                        assigned (bool): A control field to make sure the variable has been declared correctly, with a '=' symbol.
                        value (any): The value of the variable, more on that later.
                        type (string): The type of the variable. Implicit typing for now; explicit typing will be implemented later.
                        """
                        var = {
                            "name": "",
                            "assigned": False,
                            "value": None,
                            "type": ""
                        }

                        for idx, token in enumerate(line[:-1]):
                            if (var["name"] != "") and (var["assigned"] == True) and (var["value"] != None) and (var["type"] != ""):
                                break
                            else:
                                match token["token"]:
                                    case "SPACE":
                                        # Ignore spaces
                                        continue

                                    case "NAME":
                                        if token["name"] in lang.reserved_names:
                                            # Skip the "var" keyword
                                            continue
                                        elif var["name"] == "":
                                            var["name"] = token["name"]
                                        elif var["assigned"] == True:
                                            # Point to another object
                                            pass

                                    case "EQUALS":
                                        if var["name"] == "":
                                            # Syntax error (unexpected char)
                                            pass
                                        else:
                                            var["assigned"] = True

                                    case "QUOTE":
                                        if (var["name"] == "") and (var["assigned"] == False):
                                            # Syntax error (unexpected char)
                                            pass
                                        else:
                                            for subidx, subtoken in enumerate(line[-(len(line) - idx):]):
                                                if subidx == 0:
                                                    continue

                                                if subtoken["token"] == "QUOTE":
                                                    var["type"] = "string"
                                                    break

                                            else:
                                                # Syntax error (unmatched quote)
                                                pass

                                            if var["type"] != "":
                                                var["value"] = ""
                                                string = line[-(len(line) - idx):]
                                                string_length = len(string) - 1

                                                for i, subtoken in enumerate(string):
                                                    char = ""
                                                    if i == 0 or i == string_length - 1 or i == string_length:
                                                        continue
                                                    elif subtoken["value"] == "\"":
                                                        char = "\""
                                                    else:
                                                        char = subtoken["value"]

                                                    var["value"] += char

                        f.write(f"""_{var['name']} = {{ "value": "{var['value']}", "type": "{var['type']}" }}\n""")

app()