import sys
import os
import argparse
import json
import numpy as np
import random
import math


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
    parser.add_argument('-i', dest='aa_stat_file', type=isfile, required=True,
                        help="Protein stat json file")
    parser.add_argument('-n', dest='num_protein', type=int, required=True,
                        help='Number of protein')
    parser.add_argument('-min', dest='minlen', type=int,
                        help='Minimum length of protein (for uniform law)')
    parser.add_argument('-max', dest='maxlen', type=int,
                        help='Maximum length of protein (for uniform law)')
    parser.add_argument('-mean', dest='meanlen', type=float,
                        help='Mean of length distribution (for normal law)')
    parser.add_argument('-sd', dest='sdlen', type=float,
                        help='Standard deviation of length distribution (for normal law)')
    parser.add_argument('-lambda', dest='lamb', type=float,
                        help='Lambda of length distribution (for exponential law)')
    parser.add_argument('-o', dest='output_file', type=str, required=True,
                        help='Output fasta file')
    return parser.parse_args()


def load_json(aa_stat_file):
    """Load stat
    """
    data = {}
    try:
        with open(aa_stat_file, "rt") as aa_stat:
            data = json.load(aa_stat)
    except IOError:
        sys.exit("Error cannot open {0}".format(json_file))
    return data


def fill(text, width=80):                                                        
    """Split text"""                                                             
    return os.linesep.join(text[i:i+width] for i in xrange(0, len(text), width))


def generate_protein(aa_list, aa_prob, minlen, maxlen, meanlen, sdlen, lamb):
    """
    """
    protlen = 0
    while protlen <= 19:
        if minlen and maxlen:
            protlen = np.random.random_integers(minlen, maxlen)
        elif meanlen and sdlen:
            protlen = int(math.exp(round(random.normalvariate(meanlen, sdlen), 0)))
        elif lamb:     
            protlen = int(round(random.expovariate(lamb), 0))
    #assert(protlen > 0)
    return "".join(np.random.choice(aa_list, protlen, p=aa_prob))


def simulate_protein(aa_list, aa_prob, num_protein, minlen, maxlen,
                     meanlen, sdlen, lamb, output_file):
    """
    """
    try:
        with open(output_file, "wt") as output:
            for i in xrange(1, num_protein + 1):
                output.write(">protein_{1}{0}{2}{0}".format(os.linesep, i, 
                    fill(generate_protein(aa_list, aa_prob, minlen, maxlen,
                                          meanlen, sdlen, lamb))))
    except IOError:
        sys.exit("Error cannot open {0}".format(output_file))

#==============================================================
# Main program
#==============================================================
def main():
    """
    Main program function
    """
    # Get arguments
    args = get_arguments()
    # Load proportion
    stat_prot = load_json(args.aa_stat_file)
    # cumulated
    item = stat_prot.items()
    aa_list = [i[0] for i in item]
    aa_prob = [i[1] for i in item]
    # Start simulating
    simulate_protein(aa_list, aa_prob, args.num_protein, args.minlen,
                     args.maxlen, args.meanlen, args.sdlen, args.lamb,
                     args.output_file)


if __name__ == '__main__':
    main()