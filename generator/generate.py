import argparse
import os

import frontmatter
import markdown
import pdfkit


def process(path: str, output: str):
    with open(path) as f:
        metadata, content = frontmatter.parse(f.read())

        content = markdown.markdown(content)

        html = ""
        with open("document.html") as document:
            html = document.read()

        html = html.replace("%title%", metadata['title']) \
            .replace("%content%", content)

        pdfkit.from_string(html, output, options={
            "margin-top": "10", "margin-bottom": "10", "margin-left": "0", "margin-right": "0", "dpi": "300"})

    print(f"Processed {os.path.basename(path)}.")


def get_pdf_path(outdir: str, original_file: str):
    return outdir.rstrip("/") + "/" + os.path.splitext(os.path.basename(original_file))[0] + ".pdf"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--outdir', nargs='?', help='Output directory', default="./")
    parser.add_argument('-f', '--file', nargs='?', help='File to process')
    parser.add_argument('-d', '--dir', nargs='?', help='Directory to process')

    args = parser.parse_args()

    if args.file is None and args.dir is None:
        print("At least --file or --dir must be provided.")
        exit(1)
    elif args.file is not None and args.dir is not None:
        print("--file and --dir must not be present at the same time.")
        exit(1)

    if args.file is not None:
        process(str(args.file),
                get_pdf_path(str(args.outdir), str(args.file)))
    else:
        for file in os.listdir(str(args.dir)):
            if os.path.splitext(file)[1] in [".md", ".yaml", ".yml"]:
                process(str(args.dir).rstrip("/") + "/" + file,
                        get_pdf_path(str(args.outdir), str(file)))
