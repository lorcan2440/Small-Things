from typing import NamedTuple


class InvalidCodonError(Exception): ...


class AminoAcid(NamedTuple):
    '''
    Represents a single amino acid, by name, symbol and character.
    If it is a start or stop codon, the start_stop attribute is set.
    '''
    name: str
    symbol: str
    char: str
    start_stop: str = None


RNA_TO_AMINO_ACID_MAPPING = {
    'UUU': AminoAcid('Phenylalanine', 'Phe', 'F'),  'UUC': AminoAcid('Phenylalanine', 'Phe', 'F'),
    'UUA': AminoAcid('Lecine', 'Leu', 'L'),         'UUG': AminoAcid('Lecine', 'Leu', 'L'),
    'UCU': AminoAcid('Serine', 'Ser', 'S'),         'UCC': AminoAcid('Serine', 'Ser', 'S'),
    'UCA': AminoAcid('Serine', 'Ser', 'S'),         'UCG': AminoAcid('Serine', 'Ser', 'S'),
    'UAU': AminoAcid('Tyrosine', 'Tyr', 'Y'),       'UAC': AminoAcid('Tyrosine', 'Tyr', 'Y'),
    'UAA': AminoAcid('Stop', 'Ochre', '*', 'stop'), 'UAG': AminoAcid('Stop', 'Amber', '*', 'stop'),
    'UGU': AminoAcid('Cysteine', 'Cys', 'C'),       'UGC': AminoAcid('Cysteine', 'Cys', 'C'),
    'UGA': AminoAcid('Stop', 'Opal', '*', 'stop'),  'UGG': AminoAcid('Tryptophan', 'Trp', 'W'),
    'CUU': AminoAcid('Leucine', 'Leu', 'L'),        'CUC': AminoAcid('Leucine', 'Leu', 'L'),
    'CUA': AminoAcid('Leucine', 'Leu', 'L'),        'CUG': AminoAcid('Leucine', 'Leu', 'L'),
    'CCU': AminoAcid('Proline', 'Pro', 'P'),        'CCC': AminoAcid('Proline', 'Pro', 'P'),
    'CCA': AminoAcid('Proline', 'Pro', 'P'),        'CCG': AminoAcid('Proline', 'Pro', 'P'),
    'CAU': AminoAcid('Histidine', 'His', 'H'),      'CAC': AminoAcid('Histidine', 'His', 'H'),
    'CAA': AminoAcid('Glutamine', 'Gln', 'Q'),      'CAG': AminoAcid('Glutamine', 'Gln', 'Q'),
    'CGU': AminoAcid('Arginine', 'Arg', 'R'),       'CGC': AminoAcid('Arginine', 'Arg', 'R'),
    'CGA': AminoAcid('Arginine', 'Arg', 'R'),       'CGG': AminoAcid('Arginine', 'Arg', 'R'),
    'AUU': AminoAcid('Isoleucine', 'Ile', 'I'),     'AUC': AminoAcid('Isoleucine', 'Ile', 'I'),
    'AUA': AminoAcid('Isoleucine', 'Ile', 'I'),     'AUG': AminoAcid('Methionine', 'Met', 'M', 'start'),
    'ACU': AminoAcid('Threonine', 'Thr', 'T'),      'ACC': AminoAcid('Threonine', 'Thr', 'T'),
    'ACA': AminoAcid('Threonine', 'Thr', 'T'),      'ACG': AminoAcid('Threonine', 'Thr', 'T'),
    'AAU': AminoAcid('Asparagine', 'Asn', 'N'),     'AAC': AminoAcid('Asparagine', 'Asn', 'N'),
    'AAA': AminoAcid('Lysine', 'Lys', 'K'),         'AAG': AminoAcid('Lysine', 'Lys', 'K'),
    'AGU': AminoAcid('Serine', 'Ser', 'S'),         'AGC': AminoAcid('Serine', 'Ser', 'S'),
    'AGA': AminoAcid('Arginine', 'Arg', 'R'),       'AGG': AminoAcid('Arginine', 'Arg', 'R'),
    'GUU': AminoAcid('Valine', 'Val', 'V'),         'GUC': AminoAcid('Valine', 'Val', 'V'),
    'GUA': AminoAcid('Valine', 'Val', 'V'),         'GUG': AminoAcid('Valine', 'Val', 'V'),
    'GCU': AminoAcid('Alanine', 'Ala', 'A'),        'GCC': AminoAcid('Alanine', 'Ala', 'A'),
    'GCA': AminoAcid('Alanine', 'Ala', 'A'),        'GCG': AminoAcid('Alanine', 'Ala', 'A'),
    'GAU': AminoAcid('Aspartic acid', 'Asp', 'D'),  'GAC': AminoAcid('Aspartic acid', 'Asp', 'D'),
    'GAA': AminoAcid('Glutamic acid', 'Asp', 'D'),  'GAG': AminoAcid('Glutamic acid', 'Asp', 'D'),
    'GGU': AminoAcid('Glycine', 'Gly', 'G'),        'GGC': AminoAcid('Glycine', 'Gly', 'G'),
    'GGA': AminoAcid('Glycine', 'Gly', 'G'),        'GGG': AminoAcid('Glycine', 'Gly', 'G')
}


RNA_STRING = 'AUGGUAAACUCACCUAAUCUAUCCGGAUGGABAGCC'
CODON_LENGTH = 3


def convert_rna_to_amino_acids(rna: str):

    rna_codons = (rna[i : i + CODON_LENGTH] for i in range(0, len(rna), CODON_LENGTH))

    yield from (RNA_TO_AMINO_ACID_MAPPING.get(codon, None) for codon in rna_codons)


for i, amino_acid in enumerate(convert_rna_to_amino_acids(RNA_STRING)):
    if amino_acid is not None:
        print(amino_acid.name)
    else:
        raise InvalidCodonError(
            f'Bad codon found at position {CODON_LENGTH * i} in RNA string. Sequence '
            f'"{RNA_STRING[CODON_LENGTH * i : min([len(RNA_STRING), CODON_LENGTH * (i + 1)])]}" '
            'does not map to any amino acid.')
