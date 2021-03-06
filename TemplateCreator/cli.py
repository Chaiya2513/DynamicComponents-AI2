import click
import zipfile
import sys
import json

from TemplateCreate import GenerateTemplate

@click.command()
@click.argument('file', nargs = 1, required = True, type = click.File("r"))
@click.option('--screen', default="Screen1", prompt='Type a screen name that template will generated for.', help='Screen name that template will generated for.')
def main(file, screen):
    project = {}
    extensions = {}
    # Read the AIA.
    with zipfile.ZipFile(file.name, "r") as z:
        for filename in z.namelist():
            # Read SCM file.
            if filename.startswith("src/") and filename.endswith(".scm") and filename.split("/")[-1][:-4] == screen:
                # Read the file
                with z.open(filename) as f:
                    count = 0
                    for line in f:
                        # Only third line contains the JSON in AIA files.
                        if count == 2:
                            project = json.loads(line)
                            break
                        count = count + 1
            # Learn the package name of the extensions to use with schema.
            elif filename.startswith("assets/external_comps/") and filename.endswith("/components.json"):
                with z.open(filename, "r") as f:
                    componentdata = json.loads(f.read())
                    if componentdata[0]["type"] != "com.yusufcihan.DynamicComponents.DynamicComponents":
                        extensions[componentdata[0]["name"]] = componentdata[0]["type"]


    if project == {}:
        sys.exit(f"{screen} doesn't exists in the project.")
    else:
        template = json.dumps(GenerateTemplate(project, extensions), indent=4)
        filen = str(file.name).split(".")
        filen[:] = [x.replace("\\", "") for x in filen if x.strip()]
        file = open(filen[0] + ".json", "w")
        file.write(template)
        file.close()


if __name__ == '__main__':
    main()