import argparse
import json
import os
import sys
from configparser import ConfigParser
from nss import NSSProxy
from termcolor import colored


profile_path = "~/.mozilla/firefox"
DEFAULT_ENCODING = "utf-8"
password_list = list[dict[str, str]]


class Firefox:
    def __init__(self):
        self.profile = None
        self.proxy = NSSProxy()

    def load_profile(self, profile):
        self.profile = profile
        self.proxy.initialize(self.profile)

    def unload_profile(self):
        self.proxy.shutdown()

    def getCredentialsJson(self):
        db = os.path.join(self.profile, "logins.json")

        if not os.path.isfile(db):
            print(colored(f"[ - ] O usuário [{self.profile}] não tem senhas salvas: logins.json\n",'red') ,file=sys.stderr,)
            return

        with open(db) as fh:
            data = json.load(fh)
            logins = data["logins"]
            for i in logins:
                yield (i["hostname"], i["encryptedUsername"],
                       i["encryptedPassword"], i["encType"])

    def decrypt_passwords(self) -> password_list:
        credentials = self.getCredentialsJson()

        outputs: list[dict[str, str]] = []

        for url, user, passw, enctype in credentials:
            if enctype:
                try:
                    user = self.proxy.decrypt(user)
                    passw = self.proxy.decrypt(passw)
                except (TypeError, ValueError) as e:
                    continue

            output = {"url": url, "user": user, "password": passw}
            outputs.append(output)

        return outputs

    def printOutput(self, pwstore: password_list):
        for output in pwstore:
            if output['url'] == 'chrome://FirefoxAccounts':
                continue
            record: str = (
                f"\nWebsite:  '{output['url']}'\n"
                f"Username: '{output['user']}'\n"
                f"Password: '{output['password']}'"
            )
            print(colored(record, 'green'))

    def get_sections(self, profiles):
        sections = {}
        i = 1
        for section in profiles.sections():
            if section.startswith("Profile"):
                sections[str(i)] = profiles.get(section, "Path")
                i += 1
            else:
                continue
        return sections

    def read_profiles(self, basepath):
        profileini = os.path.join(basepath, "profiles.ini")

        if not os.path.isfile(profileini):
            print("File not found: profiles.ini", file=sys.stderr)
            sys.exit(1)

        profiles = ConfigParser()
        profiles.read(profileini, encoding=DEFAULT_ENCODING)

        return profiles
        
    def get_profile(self, section, basepath):
        section = section
        profile = os.path.join(basepath, section)

        return profile

def profile_connect(firefox, profile):
    
    firefox.load_profile(profile)

    outputs = firefox.decrypt_passwords()

    firefox.printOutput(outputs)

    firefox.unload_profile()
    
def main() -> None:
    basepath = input("Enter the path to the Firefox profile directory (default: ~/.mozilla/firefox): ")
    basepath = os.path.expanduser(basepath.strip() or "~/.mozilla/firefox")

    if not os.path.isdir(basepath):
        print(colored(f"[{basepath}] is invalid Path", 'red'))
        sys.exit(1)
    
    firefox = Firefox()
    
    profiles: ConfigParser = firefox.read_profiles(basepath)
    sections = firefox.get_sections(profiles)
    
    while True:
        print(colored("=============================================================", 'magenta'))
        print(colored("Select a option: ", 'magenta'))
        print(colored("     Option -1: Sair", 'cyan'))
        print(colored("     Option 0: Todos os Perfis", 'cyan'))
        for s in sections:
            print(colored(f"     Option {s}: {sections[s]}", 'cyan'))
        print(colored("=============================================================", 'magenta'))
        op = input(colored("Option: ", 'magenta'))
        
        if op == '-1':
            print(colored("=============================================================", 'magenta'))
            print(colored("Saindo...", 'red'))
            print(colored("=============================================================", 'magenta'))
            sys.exit(0)
        
        if op == '0':
            if sections is not None:
                for s in sections:
                    profile = firefox.get_profile(sections[s], basepath)
                    print(colored("=============================================================", 'magenta'))
                    print(colored("Using profile: "+sections[s], 'green'))
                    profile_connect(firefox, profile)
            else:
                print(colored("Sections Is empty", 'red'))
        elif op in sections:
            section = sections[op]
            profile = firefox.get_profile(section, basepath)
            print(colored("Using profile: "+section, 'green'))
            profile_connect(firefox, profile)
        else:
            print(colored("Invalid Option", 'red'))


if __name__ == "__main__":
    main()