import streamlit as st
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from io import StringIO

# Function to convert FASTA sequence to amino acid sequence
def fasta_to_amino_acid(fasta_seq, wild_type):
    data = []

    # T7 tag sequence
    t7_tag = "MGSSHHHHHHSSGLVPRGSHMASMTGGQQMGRGSEF"

    # Create a sequence record from the fasta sequence
    seq_record = SeqIO.read(StringIO(fasta_seq), "fasta")

    # Translate the nucleotide sequence to amino acid sequence
    amino_acid_seq = str(seq_record.seq.translate(to_stop=False))

    # Split the sequence by '*' which is the stop codon
    proteins = amino_acid_seq.split('*')

    # Loop through the proteins and add them to the list
    for protein in proteins:
        # Find the index of the first 'M'
        m_index = protein.find('M')
        if m_index != -1:
            # If 'M' is found, add the protein from 'M' to the end to the list
            protein = protein[m_index:]

            # Check if the protein starts with the T7 tag
            if protein.startswith(t7_tag):
                # If it does, remove the tag and add the remaining protein to the list
                protein = protein[len(t7_tag):]

                # Compare the protein with the wild-type
                mutations = []
                for i in range(min(len(protein), len(wild_type))):
                    if protein[i] != wild_type[i]:
                        # If the amino acids don't match, record the mutation
                        mutations.append(f'{wild_type[i]}{i+1}{protein[i]}')

                data.append({"id": seq_record.id, "protein": protein, "mutations": ", ".join(mutations)})

    # Create a dataframe from the list
    df = pd.DataFrame(data)

    return df

# Streamlit code
st.title('Protein Sequence Analysis')

# Input for the wild-type sequence
wild_type = st.text_area('Enter the wild-type amino acid sequence:')

# Input for the FASTA sequence
fasta_seq = st.text_area('Enter the FASTA DNA sequence:')

if st.button('Analyze'):
    if wild_type and fasta_seq:
        # Convert FASTA sequence to amino acid sequence and compare with wild-type
        df = fasta_to_amino_acid(fasta_seq, wild_type)

        # Display the results
        st.write(df)
    else:
        st.write('Please enter both the wild-type and FASTA sequences.')
