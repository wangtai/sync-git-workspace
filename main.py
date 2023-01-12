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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='set workspace path')
    parser.add_argument('--path', type=str, help='workspace path')
    args = parser.parse_args()
    # print(args.path)

    export(args.path)
