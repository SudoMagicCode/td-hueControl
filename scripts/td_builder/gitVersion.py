import subprocess


# NOTE define any supporting functions
def GetVersioningInfo():
    # grab git information...
    # print("-> Version info")
    git_branch_process = subprocess.run(
        "git rev-parse --abbrev-ref HEAD", shell=True, capture_output=True)
    branch = str(git_branch_process.stdout, 'utf-8').strip()
    git_tag_process = subprocess.run(
        "git describe --tags", shell=True, capture_output=True)
    last_full_tag = str(git_tag_process.stdout, 'utf-8').strip()
    print(f"-> last full tag {last_full_tag}")

    tag_parts = last_full_tag.split('-')
    major_minor = tag_parts[0]
    major = major_minor.split('.')[0][1:]
    minor = major_minor.split('.')[1]

    num_commits = "0"
    current_commit_hash = None
    if len(tag_parts) > 2:
        num_commits = tag_parts[1]
        current_commit_hash = tag_parts[2][1:]

    semver = major_minor+"."+num_commits

    if branch != "main":
        if current_commit_hash is not None:
            semver = semver + "+"+branch+"-"+current_commit_hash
        else:
            semver = semver + "+"+branch

    dist_info = {
        "commit": current_commit_hash,
        "semver": semver,
        "major_minor": major_minor,
        "major": major,
        "minor": minor,
        "major_minor": major_minor,
        "patch": num_commits,
        "branch": branch
    }
    return dist_info
