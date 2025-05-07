

def get_config(str):
    with open("config.cfg", "r", encoding='utf-8') as file:
        line = file.readline()
        if line.startswith(str):
            return line.split("=")[1]
        else:
            return None