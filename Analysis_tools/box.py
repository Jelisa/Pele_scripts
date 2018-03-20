import sys
import os
import shutil
import argparse
from string import Template

KEYWORDS = ["CENTER_X", "CENTER_Y", "CENTER_Z", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]
COORD = "{:>11.3f}{:>8.3f}{:>8.3f}"
CENTER = "{:.3f}"
DIR=os.path.dirname(os.path.abspath(__file__))
BOX=os.path.join(DIR,"box_template.pdb")


def parse_args():
    parser = argparse.ArgumentParser(description="Create pdb-box from center and radius")
    parser.add_argument("center", nargs='+', type=float,  help='center of the box')
    parser.add_argument("radius",  type= int, help='radius of the box')
    parser.add_argument("-f", "--file", default= "box.pdb", help='output file')
    args = parser.parse_args()


    return args.center, args.radius, args.file


class TemplateBuilder(object):

    def __init__(self, file, keywords):

        self.file = file
        self.keywords = keywords
        self.fill_in()

    def fill_in(self):
        """
        Fill the control file in
        """
        with open(os.path.join(self.file), 'r') as infile:
            confile_data = infile.read()

        confile_template = Template(confile_data)

        confile_text = confile_template.safe_substitute(self.keywords)

        with open(os.path.join(self.file), 'w') as outfile:
            outfile.write(confile_text)


def build_box(center, radius, file):
   

    cx, cy, cz = center
    v1 = COORD.format(cx-radius,cy-radius, cz-radius)
    v2 = COORD.format(cx+radius,cy-radius, cz-radius)
    v3 = COORD.format(cx+radius,cy-radius, cz+radius)
    v4 = COORD.format(cx-radius,cy-radius, cz+radius)
    v5 = COORD.format(cx-radius,cy+radius, cz-radius)
    v6 = COORD.format(cx+radius,cy+radius, cz-radius)
    v7 = COORD.format(cx+radius,cy+radius, cz+radius)
    v8 = COORD.format(cx-radius,cy+radius, cz+radius)
    cx = CENTER.format(cx)
    cy = CENTER.format(cy)
    cz = CENTER.format(cz)

    values = [cx, cy, cz, v1, v2, v3, v4,
                   v5, v6, v7, v8]
 
    replace =  {keyword : value for keyword, value in zip(KEYWORDS, values)}

    shutil.copy(BOX, file)

    TemplateBuilder(file, replace)

    return file

if __name__ == "__main__":
    center, radius, box_file = parse_args()
    box = build_box(center, radius, box_file)
    print("Box created in {}".format(os.path.abspath(box)))
