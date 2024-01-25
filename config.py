from configparser import ConfigParser


def config(key: str) -> str:
    c = ConfigParser()
    c.read("config")
    c.sections()
    return c["SECRETS"][key]
