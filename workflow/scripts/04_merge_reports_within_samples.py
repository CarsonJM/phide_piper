import os
import pandas as pd
from Bio import SeqIO


# extract diamond virus sequences
if os.stat(str(snakemake.input.genomad_results)).st_size != 0:
    genomad_results = pd.read_csv(str(snakemake.input.genomad_results), sep='\t')
    if len(genomad_results['seq_name'].str.split('|', expand=True)) > 1:
        genomad_results['seq_source'] = genomad_results['seq_name'].str.split('|', expand=True)[0]

# extract diamond virus sequences
if os.stat(str(snakemake.input.external_results)).st_size != 0:
    external_results = pd.read_csv(str(snakemake.input.external_results), sep='\t', names=['identity', 'shared-hashes', 'median-multiplicity', 'p-value', 'seq_source', 'query-comment'])
    external_results['shared-hashes'] = external_results['shared-hashes'].str.partition('/')[0].astype(int)
    external_results = external_results[(external_results['identity'] >= snakemake.params.min_mash_score) & (external_results['shared-hashes'] >= snakemake.params.min_mash_hashes) & (external_results['median-multiplicity'] >= snakemake.params.min_mash_multiplicity)]
    virus_report = genomad_results.merge(external_results, on='seq_source', how='left') 

virus_report['assembly'] = snakemake.params.assembly
virus_report['vls_id'] = virus_report['assembly'] + "|" + virus_report["seq_name"]

virus_report.to_csv(str(snakemake.output), sep='\t', index=False)

