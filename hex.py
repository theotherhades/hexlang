import typer
import lang

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

    with open("dist/out.py", "w+") as f:
        for line in lines:
            if line[0]["token"] == "NAME":
                # Declare a variable
                if line[0]["name"] == "var":
                    idx = 0
                    varname = ""
                    for token in line:
                        idx += 1
                        if (idx == 1) or (token["token"] == "SPACE"):
                            continue

                        if (token["token"] == "name") and (varname == ""):
                            varname = token["name"]

app()