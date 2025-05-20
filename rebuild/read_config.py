def get_config(key):
    with open("config.cfg", "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith(key + "=") or line.startswith(key + " ="):
                return line.split("=", 1)[1].strip()
        return None
