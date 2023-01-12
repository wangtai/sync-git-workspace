#!/usr/bin/env python3

# This is a sample Python script.

# Press ⌃F5 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import argparse


def export(path):
    import os

    repos = {}
    for dir in os.listdir(path):
        # print(dir)
        full_path = os.path.join(path, dir)
        import git

        g = git.cmd.Git(full_path)
        try:
            repo_url = g.execute(["git", "remote", "get-url", "origin"])
            repos[dir] = repo_url
        except git.exc.GitCommandError:
            if not os.path.isdir(full_path):
                continue
            for dir2 in os.listdir(full_path):
                full_path2 = os.path.join(full_path, dir2)
                if not os.path.isdir(full_path2):
                    continue
                # print(full_path)
                g = git.cmd.Git(full_path2)
                try:
                    repo_url = g.execute(["git", "remote", "get-url", "origin"])
                    repos[dir + '/' + dir2] = repo_url
                except git.exc.GitCommandError:
                    continue
            continue

    print(repos)

    with open('export.json', 'w') as f:
        f.write(str(repos).replace("'", '"'))


def import_repos(path):
    import json
    with open('import.json', 'r') as f:
        repos = json.load(f)
        print(repos)
        for name, url in repos.items():
            print(name, url)
            import os
            os.makedirs(os.path.join(path, name), exist_ok=True)
            os.chdir(os.path.join(path, name))
            os.system('git clone ' + url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='set workspace path')
    parser.add_argument('--action', type=str, help='export or import')
    parser.add_argument('--path', type=str, help='workspace path')
    args = parser.parse_args()
    # print(args.path)
    if args.action == 'export':
        export(args.path)
    elif args.action == 'import':
        import_repos(args.path)
