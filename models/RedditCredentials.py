import os, json

class RedditCredentials:
    def __init__(self, client_id=None, client_secret=None, username=None, user_agent=None, password=None, twofa=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.user_agent = user_agent
        self.password = password
        self.twofa = twofa
        
    def to_dict(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "user_agent": self.user_agent,
            "password": self.password,
            "twofa": self.twofa
        }
        
    def save_to_file(self, filename='reddit.json'):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

            
    def update_from_env(self, filename=".env"):
        with open(filename, "r") as file:
            lines = file.readlines()
            self.client_id = lines[0].split("=")[1].strip("\"").strip("\"").strip("\n")
            self.client_secret = lines[1].split("=")[1].strip("\"").strip("\n")
            self.username = lines[2].split("=")[1].strip("\"").strip("\n")
            self.user_agent = lines[3].split("=")[1].strip("\"").strip("\n")
            self.password = lines[4].split("=")[1].strip("\"").strip("\n")
            self.twofa = lines[5].split("=")[1].strip("\"").strip("\n") == "true"

    def update_from_new_credentials(self, new_credentials):
        for attr in ["client_id", "client_secret", "username", "user_agent", "password", "twofa"]:
            value = getattr(new_credentials, attr, None)
            if value is not None and value != "":
                setattr(self, attr, value)

    @staticmethod
    def from_file(filename="reddit_credentials.json"):
        try:
            with open(filename) as f:
                data = json.load(f)
                return RedditCredentials(
                    data["client_id"],
                    data["client_secret"],
                    data["username"],
                    data["user_agent"],
                    data["password"],
                    data["twofa"]
                )
        except FileNotFoundError:
            return None

    # def __str__(self):
    #     return f"client_id={self.client_id}, client_secret={self.client_secret}, username={self.username}, user_agent={self.user_agent}, password={self.password}, twofa={self.twofa}"

    # def get_client_id(self):
    #     return self.client_id

    # def get_client_secret(self):
    #     return self.client_secret

    # def get_username(self):
    #     return self.username

    # def get_user_agent(self):
    #     return self.user_agent

    # def get_password(self):
    #     return self.password

    # def get_twofa(self):
    #     return self.twofa

# my_credentials = RedditCredentials(
#     client_id="SJqugNR-9LBzv1rnCCYqvg",
#     client_secret="clZkhlnsyb6yyS3LGN3gdwebwzo85w",
#     username="reddit88t",
#     user_agent="reddit88t",
#     password="Ht@08082002",
#     twofa="false"
# )

# my_credentials.save_to_file("my_credentials.txt")
# my_credentials = RedditCredentials.from_file("my_credentials.txt")

# if __name__ == "__main__":
#     print("Testing RedditCredentials.py")
#     myCred = RedditCredentials.from_file(".env")
#     print(myCred)