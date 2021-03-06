import re
import json
import sys
import ntpath

# Used to mark the start and end of templatized sections
# The lines on which the opening and closing comments appear will be discarded.
TMPL_BLOCK_OPEN = '/** +-+'
TMPL_BLOCK_CLOSE = '-+- **/'

# Used to mark the start and end of individual template tags.
# Template tags cannot be nested.
TMPL_TAG_OPEN = '{:'
TMPL_TAG_CLOSE = ':}'

def find_template_block( text ):
    try:
        start_idx = text.index(TMPL_BLOCK_OPEN)
        end_idx = text.index(TMPL_BLOCK_CLOSE)

        block = text[start_idx:end_idx].split('\n')
        block = '\n'.join(block[1:-1])
        return (block, start_idx, end_idx+len(TMPL_BLOCK_CLOSE))
    except ValueError:
        return (None, -1, -1)

def find_template_tag( text ):
    try:
        start_idx = text.index(TMPL_TAG_OPEN)
        end_idx = text.index(TMPL_TAG_CLOSE)

        return (text[start_idx+len(TMPL_TAG_OPEN):end_idx].strip(), start_idx, end_idx+len(TMPL_TAG_CLOSE))
    except ValueError:
        return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("You MUST specify input and output files!")
        print("Usage:\n\t" + sys.argv[0] + "template_file graph_file output_file")

    with open(sys.argv[1], 'r') as input:
        in_template = input.read()

    with open(sys.argv[2], 'r') as input:
        in_graph = input.read()

    out_file = sys.argv[3]

    # find template block
    template, boundsmin, boundsmax = find_template_block(in_template)
    while template is not None:
        tag = find_template_tag(template)
        while tag is not None:
            param = tag[0]
            if tag[0] == 'graph':
                param = in_graph
            elif tag[0] == 'graph_name':
                param = ntpath.basename(sys.argv[2])
            else:
                print("Unknown Template Parameter: '" + tag[0] + "'")

            template = template[0:tag[1]] + param + template[tag[2]:]
            tag = find_template_tag(template)

        in_template = in_template[0:boundsmin] + template + in_template[boundsmax:]

        # get next template block if there is one
        template, boundsmin, boundsmax = find_template_block(in_template)

    with open(out_file, 'w') as output:
        output.write(in_template)
