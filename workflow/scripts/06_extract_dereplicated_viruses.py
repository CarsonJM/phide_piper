import pandas as pd
from Bio import SeqIO

# open clustering results
clusters = open(str(snakemake.input.clusters), 'r')

votu_reps= []
for line in clusters:
    stripped = line.strip()
    centroid, nodes = stripped.split('\t')
    votu_reps.append(centroid)

votu_reps_set = set(votu_reps)

# extract representative sequences from fasta file
votu_rep_sequences = []
for record in SeqIO.parse(str(snakemake.input.viruses), "fasta"):
    if record.id in votu_reps_set:
        votu_rep_sequences.append(record)

votu_reps_set = set(votu_reps)

# extract representative sequences from fasta file
votu_rep_sequences_untrimmed = []
for record in SeqIO.parse(str(snakemake.input.untrimmed_viruses), "fasta"):
    if record.id in votu_reps_set:
        votu_rep_sequences_untrimmed.append(record)

# save all sequences to specified file
SeqIO.write(votu_rep_sequences, str(snakemake.output.viruses), "fasta")
SeqIO.write(votu_rep_sequences_untrimmed, str(snakemake.output.untrimmed_viruses), "fasta")