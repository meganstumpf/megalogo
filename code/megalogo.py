'''
This software is written for display of presence/absence of amino acids at given positions in a logoplot.
Written by Tonya Brunetti and Megan Stumpf
'''

print("importing packages...")

import pandas as pd
import argparse
import math
import logomaker
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MultipleLocator

'''
def format_data()
    input needs a minimum of 3 columns (all others will be ignored)
        - POSITION: an integer of the codon position
        - AA: amino acid to plot, generally this is a single letter amino acid symbol
        - MERGE_FRAC: float [0-1] that shows the height/frequency of the amino acid symbol to plot on the logoplot
    output is a pandas dataframe that is formatted for logomaker in input into def generate_logo_plot()
'''

print("reading data...")

def format_data(data_input: str) -> pd.DataFrame:
    pandas_df = pd.read_csv(data_input)
    pandas_df['POSITION'] = pandas_df['POSITION'] - pandas_df['POSITION'].min() + 1
    info_df = pandas_df[['POSITION', 'AA', 'MERGE_FRAC']]
    info_pivot_matrix = info_df.pivot(index="POSITION", columns="AA", values="MERGE_FRAC")
    info_pivot_matrix.fillna(0, inplace=True)
    return info_pivot_matrix

def generate_logo_plot(matrix_input: pd.DataFrame, sample_name: str, annotations: str, increment: int, min_label_len: int, output_path: str, codon_start: int = None, codon_end: int = None, ref_aa_path: str = None) -> None:
    annot_data = pd.read_csv(annotations) if annotations else None
    if annot_data is not None:
        annot_data = annot_data.to_dict("index")
        breakpoints = {key: range(value['start'], value['end']) for key, value in annot_data.items()}

    ref_aa_data = pd.read_csv(ref_aa_path) if ref_aa_path else None

    def match_annotation(ax, position_start: int, position_end: int, min_label_len: int) -> None:
        annot_start = -1
        annot_end = -1

        for key, value in breakpoints.items():
            if position_start in value:
                annot_start = key
            if position_end in value:
                annot_end = key

        if annot_start == annot_end:
            ax.plot([position_start-1, position_end+1], [y+0.1, y+0.1], alpha=0.5, color=annot_data[annot_start]['color'], linewidth=12, solid_capstyle="butt")
            if (position_end - position_start) >= min_label_len:
                ax.text(((position_start-1 + position_end+1) / 2), 1.1, annot_data[annot_start]['region_name'], fontsize=10, color='black')
        else:
            for subannotations in enumerate(range(annot_start, annot_end + 1)):
                if subannotations[0] == 0:
                    begin = max(annot_data[annot_start]['start'], position_start)
                    end = annot_data[annot_start]['end']
                    ax.plot([begin-1, end+1], [y+0.1, y+0.1], alpha=0.5, color=annot_data[annot_start]['color'], linewidth=12, solid_capstyle="butt")
                    if (end - begin) >= min_label_len:
                        ax.text(((begin-1 + end+1) / 2), 1.1, annot_data[annot_start]['region_name'], fontsize=10, color='black')
                elif subannotations[0] == len(range(annot_start, annot_end)):
                    begin = annot_data[annot_end]['start']
                    end = min(annot_data[annot_end]['end'], position_end)
                    ax.plot([begin, end+1], [y+0.1, y+0.1], alpha=0.5, color=annot_data[annot_end]['color'], linewidth=12, solid_capstyle="butt")
                    if (end - begin) >= min_label_len:
                        ax.text(((begin + end+1) / 2), 1.1, annot_data[annot_end]['region_name'], fontsize=10, color='black')
                else:
                    begin = annot_data[subannotations[1]]['start']
                    end = annot_data[subannotations[1]]['end']
                    ax.plot([begin, end+1], [y+0.1, y+0.1], alpha=0.5, color=annot_data[subannotations[1]]['color'], linewidth=12, solid_capstyle="butt")
                    if (end - begin) >= min_label_len:
                        ax.text(((begin + end+1) / 2), 1.1, annot_data[subannotations[1]]['region_name'], fontsize=10, color='black')

    height_per_row = 2
    width_per_col = 15

    start = codon_start if codon_start is not None else matrix_input.index.min()
    end_pos = codon_end if codon_end is not None else matrix_input.index.max()
    end = start + increment - 1
    y = 1.05
    num_pos = end_pos - start + 1
    num_rows = math.ceil(num_pos / increment)

    fig = plt.figure(figsize=[width_per_col * 1, height_per_row * num_rows])
    fig.suptitle('{}\n'.format(sample_name), fontsize=15)
    fig.supylabel('amino acid diversity per codon')
    fig.supxlabel('codon position')

    for i in range(0, num_rows):
        tmp = matrix_input.loc[start:end]
        ax = plt.subplot2grid((num_rows, 1), (i, 0))
        logomaker.Logo(tmp, ax=ax, color_scheme="skylign_protein", show_spines=True, stack_order="fixed")
        ax.set_ylim([0, 1.5])
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['0.0', '1.0'])
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.xaxis.set_major_locator(MultipleLocator(5))  # Set tick marks every 5 positions

        if annotations is not None:
            match_annotation(ax, position_start=start, position_end=end, min_label_len=min_label_len)
        
        if ref_aa_data is not None:
            ref_aa_subset = ref_aa_data[(ref_aa_data['POSITION'] >= start) & (ref_aa_data['POSITION'] <= end)]
            for _, row in ref_aa_subset.iterrows():
                ax.text(row['POSITION'], 1.3, row['REF_AA'], fontsize=10, color='black', ha='center')

        start = end + 1
        if (end + increment) > end_pos:
            end = end_pos
        else:
            end = end + increment
    
    print("saving logoplot...")
    fig.tight_layout()
    fig.savefig(output_path, dpi=600, format='png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates logo plot for predefined input matrix",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, required=True, help="Path to input csv matrix containing data to plot")
    parser.add_argument('--sampleName', type=str, default="sample_1", help="String indicating the name to give to sample")
    parser.add_argument('--annotConfig', type=str, default=None, help="Path to csv containing annotations. Example file located in ref folder of github repo")
    parser.add_argument('--codonStartPos', type=int, default=None, help="The position of which codon position you want to start at (must be present in your csv matrix provided to --input; default is to plot every position in your matrix)")
    parser.add_argument('--codonEndPos', type=int, default=None, help="The position of which codon position you want to end at (must be present in your csv matrix provided to --input; default is to plot every position in your matrix)")
    parser.add_argument('--aaSpacing', type=int, default=65, help='The number of amino acids to show per line on the logo plot')
    parser.add_argument('--minAnnotLabel', type=int, default=7, help='The minimum length of consecutive amino acids under an annotation bar; anything smaller (non-inclusive) than this value will not have text written in the bar, to help prevent text from overflowing into margins')
    parser.add_argument('--refAA', type=str, default=None, help="Path to csv containing reference amino acids with POSITION and REF_AA columns")
    parser.add_argument('--output', type=str, required=True, help="Path to save the output logoplot image")

    args = parser.parse_args()

    formatted_input_matrix = format_data(data_input=args.input)
    generate_logo_plot(matrix_input=formatted_input_matrix, sample_name=args.sampleName,
                       annotations=args.annotConfig, increment=args.aaSpacing,
                       min_label_len=args.minAnnotLabel, output_path=args.output,
                       codon_start=args.codonStartPos, codon_end=args.codonEndPos, ref_aa_path=args.refAA)

print("megalogo has finished plotting")