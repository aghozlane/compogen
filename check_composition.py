import sys
import os
import argparse
import json


def isfile(path):
    """Check if path is an existing file.
      :Parameters:
          path: Path to the file
    """
    if not os.path.isfile(path):
        if os.path.isdir(path):
            msg = "{0} is a directory".format(path)
        else:
            msg = "{0} does not exist.".format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def get_arguments():
    """Retrieves the arguments of the program.
      Returns: An object that contains the arguments
    """
    # Parsing arguments
    parser = argparse.ArgumentParser(description=__doc__, usage=
                                     "{0} -h".format(sys.argv[0]))
    parser.add_argument('-i', dest='protein_file', type=isfile, required=True,
                        help="Protein fasta file")
    parser.add_argument('-o', dest='output_file', type=str, required=True,
                        help='Output json file')
    return parser.parse_args()


def get_statistics(protein_file, amino_acid):
    """Count elements
    """
    try:
        with open(protein_file, "rt") as protein:
            for line in protein:
                #print(line)
                if not line.startswith(">"):
                    for aa in line.replace("\n", ""):
                        amino_acid[aa] += 1
    except IOError:
        sys.exit("Error cannot open {0}".format(protein_file))
    return amino_acid



def write_result(output_file, amino_acid, total_aa):
    """Write statistics
    """
    try:
        with open(output_file, 'wt') as fp:
            json.dump(amino_acid, fp)
    except IOError:
        sys.exit("Error cannot open {0}".format(output_file))

#==============================================================
# Main program
#==============================================================
def main():
    """
    Main program function
    """
    amino_acid = {'A':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'K':0,
                  'L':0, 'M':0, 'N':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0, 'V':0, 
                  'W':0, 'Y':0, 'X':0, 'Z':0, 'B':0, 'U':0, 'O':0}
    # Get arguments
    args = get_arguments()
    # read
    amino_acid = get_statistics(args.protein_file, amino_acid)
    print(amino_acid)
    sum_aa = sum(amino_acid.values())
    for aa in amino_acid:
        amino_acid[aa] = amino_acid[aa] / float(sum_aa)
    write_result(args.output_file, amino_acid)


if __name__ == '__main__':
    main()