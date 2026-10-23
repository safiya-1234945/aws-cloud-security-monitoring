import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4



PROJECT_FOLDER = "."


OUTPUT_FILE = "Cloud_Security_Artefact_Code.pdf"



EXCLUDE_FOLDERS = [

    "__pycache__",

    ".git",

    "venv",

    "env"

]



def collect_python_files():


    python_files = []


    for root, dirs, files in os.walk(PROJECT_FOLDER):


        dirs[:] = [

            d for d in dirs

            if d not in EXCLUDE_FOLDERS

        ]


        for file in files:


            if file.endswith(".py"):

                python_files.append(

                    os.path.join(

                        root,

                        file

                    )

                )


    return sorted(python_files)




def create_pdf():


    files = collect_python_files()


    print(

        f"Found {len(files)} Python files"

    )


    doc = SimpleDocTemplate(

        OUTPUT_FILE,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=40

    )


    styles = getSampleStyleSheet()


    content = []



    content.append(

        Paragraph(

            "Cloud Security Artefact - Source Code",

            styles["Title"]

        )

    )


    content.append(

        Spacer(

            1,

            20

        )

    )



    for index, filepath in enumerate(files):


        print(

            "Adding:",

            filepath

        )


        content.append(

            Paragraph(

                filepath,

                styles["Heading2"]

            )

        )


        content.append(

            Spacer(

                1,

                10

            )

        )


        try:


            with open(

                filepath,

                "r",

                encoding="utf-8"

            ) as f:


                code = f.read()



        except Exception as e:


            code = (

                "Could not read file:\n"

                + str(e)

            )



        content.append(

            Preformatted(

                code,

                styles["Code"]

            )

        )



        content.append(

            PageBreak()

        )



    doc.build(

        content

    )


    print()

    print(

        "PDF created:",

        OUTPUT_FILE

    )




if __name__ == "__main__":

    create_pdf()