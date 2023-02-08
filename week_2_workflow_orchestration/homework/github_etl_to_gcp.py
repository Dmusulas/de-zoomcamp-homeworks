from prefect.filesystems import GitHub

github_block = GitHub.load("github-storage")
