import os.path
import subprocess

from config.const import ROOT_PATH


def main():
    exact_location = os.path.join(ROOT_PATH, 'output', 'novel.jsonl')
    command = f"scrapy crawl novel -o {exact_location}"
    subprocess.run(command, check=True, shell=True)


if __name__ == "__main__":
    main()
