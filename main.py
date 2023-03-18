import os
import datetime
from github import Github
import dotenv

dotenv.load_dotenv()
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
USERNAME = os.environ["USERNAME"]
REPOSITORY = os.environ["REPOSITORY"]

class GithubFile:
    def __init__(self):
        self.g = Github(
            ACCESS_TOKEN, 
        )
        self.repo = self.g.get_repo(f'{USERNAME}/{REPOSITORY}')

    def create_or_update_file(self, file_path, content, message):
        try:
            file_contents = self.repo.get_contents(file_path)
            commit = f"Update {message}"
            self.repo.update_file(file_path, commit, content, file_contents.sha, branch="main")
            print(f"File {message} updated.")
        except Exception as e:
            print(f"Create a file: {e}")
            commit = f"Add {message}"
            self.repo.create_file(file_path, commit, content, branch="main")
            print(f"File {message} created.")

    def create_file(self, content):
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+9), 'JST'))
        if now.hour < 4:
            now = now - datetime.timedelta(days=1)
        message = f"{now.year}.{now.month}.{now.day}"
        file_path = f"{now.year}/{now.month:02d}{now.day:02d}.md"
        self.create_or_update_file(file_path, content, message)

file = GithubFile()
file.create_file("""
# Test

This is a test.

""")
