import argparse
import zipfile
from pathlib import Path

def unzip_archive(zip_file: Path, extract_to: Path, delete_archives: bool = False):
    # Step 1: Unzip the initial archive
    print(f"Unzipping main archive: {zip_file}")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Step 2: Recursively unzip any nested zip files
    for nested_zip in extract_to.rglob("*.zip"):
        print(f"Unzipping nested archive: {nested_zip}")
        try:
            with zipfile.ZipFile(nested_zip, 'r') as zip_ref:
                zip_ref.extractall(nested_zip.parent)
        except zipfile.BadZipFile:
            print(f"Skipping invalid zip file: {nested_zip}")

    # Optional: Step 3 — Delete all zip files
    if delete_archives:
        for zip_path in extract_to.rglob("*.zip"):
            print(f"Deleting: {zip_path}")
            zip_path.unlink()

    print("All done.")


def main():
    parser = argparse.ArgumentParser(description="Recursively unzip an archive and all nested zip files.")
    parser.add_argument(
        "--zip_file",
        type=Path,
        required=True,
        help="Path to the main zip file."
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("unzipped_data"),
        help="Directory to extract files to (default: ./unzipped_data)."
    )
    parser.add_argument(
        "--delete_zips",
        action="store_true",
        help="If set, deletes all zip files after extraction."
    )
    args = parser.parse_args()
    unzip_archive(args.zip_file, args.output_dir, args.delete_zips)


if __name__ == "__main__":
    main()