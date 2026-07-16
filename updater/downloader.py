from pathlib import Path
import subprocess

REPO_URL = "https://gitlab.com/Dimbreath/animegamedata2.git"
REPO_DIR = Path("animegamedata2")

SPARSE_PATHS = [
    "/Readable/EN/",
    "/Readable/CHS/",
    "/Subtitle/EN/",
    "/Subtitle/CHS/",
    "/TextMap/TextMapEN.json",
    "/TextMap/TextMapCHS.json",
    "/TextMap/TextMap_MediumEN.json",
    "/TextMap/TextMap_MediumCHS.json",
]


def run_git(*args):
    process = subprocess.Popen(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None

    for line in process.stdout:
        print(line, end="", flush=True)

    process.wait()

    if process.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(args)}")


def configure_sparse_checkout():
    print("\nConfiguring sparse checkout...\n")

    run_git(
        "-C",
        str(REPO_DIR),
        "sparse-checkout",
        "init",
        "--no-cone",
    )

    sparse_file = REPO_DIR / ".git" / "info" / "sparse-checkout"

    with sparse_file.open("w", encoding="utf-8") as file:
        for path in SPARSE_PATHS:
            file.write(path + "\n")

    run_git(
        "-C",
        str(REPO_DIR),
        "sparse-checkout",
        "reapply",
    )

def update_repository():
    print("Hi")
    if REPO_DIR.exists():
        print("Repository found. Updating only required files...\n")

        run_git(
            "-C",
            str(REPO_DIR),
            "pull",
            "--progress",
        )

        run_git(
            "-C",
            str(REPO_DIR),
            "sparse-checkout",
            "reapply",
        )

    else:
        print("Repository not found. Cloning required files only...\n")

        run_git(
            "clone",
            "--depth=1",
            "--filter=blob:none",
            "--no-checkout",
            REPO_URL,
            str(REPO_DIR),
        )

        configure_sparse_checkout()

        run_git(
            "-C",
            str(REPO_DIR),
            "checkout",
            "main",
        )

    print("\nRepository is up to date.")


