import random
import string
import numpy as np

from datetime import datetime
from datetime import timedelta

from one_hot import dense_to_one_hot

START_DATE = datetime.strptime('1950-01-01', '%Y-%m-%d')
END_DATE = datetime.strptime('2050-12-31', '%Y-%m-%d')
FORMAT_TOKENS = ('%a', '%A', '%d', '%b', '%B', '%m', '%y', '%Y')
INPUT_FORMATS = ['%Y %B, %d', '%B %d, %Y', '%b %d %y']
OUTPUT_FORMAT = '%Y-%m-%d'

PAD_SYMBOL = 'PAD'
INPUT_LETTERS = string.ascii_lowercase + string.digits + ',- .:/'
INPUT_SYMBOLS = list(INPUT_LETTERS) + [PAD_SYMBOL]
INPUT_SYMBOL_TO_IDX = dict((l, i) for i, l in enumerate(INPUT_SYMBOLS))
INPUT_SEQ_LEN = 20

OUTPUT_LETTERS = string.digits + '-'
OUTPUT_SYMBOLS = list(OUTPUT_LETTERS)
OUTPUT_SYMBOL_TO_IDX = dict((l, i) for i, l in enumerate(OUTPUT_SYMBOLS))
OUTPUT_SEQ_LEN = 10


def random_datetime(start=START_DATE, end=END_DATE):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_date_format(date):
    # random_format_tokens = random.sample(FORMAT_TOKENS, 5)
    # date_format = '-'.join(random_format_tokens)

    date_format = random.choice(INPUT_FORMATS)
    return date.strftime(date_format)


def encode_sequences(sequences, symbol_to_idx, sequence_len, pad_symbol=PAD_SYMBOL, reverse=False):
    """
    Given a set of symbols and their index/label encoded the given list of sequences
    input numeric target sequences.
    """

    if pad_symbol is None:
        pad_idx = 0
    else:
        pad_idx = symbol_to_idx[pad_symbol]

    assert sequence_len >= len(max(sequences, key=len))

    encoded_sequences = np.full((len(sequences), sequence_len),
                                fill_value=pad_idx,
                                dtype=np.int32)

    for i, sequence in enumerate(sequences):
        idxs = [symbol_to_idx[symbol] for symbol in sequence]
        if reverse:
            encoded_sequences[i, -len(idxs):] = idxs[::-1]
        else:
            encoded_sequences[i, :len(idxs)] = idxs

    return encoded_sequences


def generate_training_data(batch_size=32):

    while True:

        datetimes = [random_datetime() for _ in range(batch_size)]
        input_date_strings = [dt.strftime(random.choice(INPUT_FORMATS)).lower() for dt in datetimes]
        target_date_strings = [dt.strftime(OUTPUT_FORMAT) for dt in datetimes]

        input_sequences = encode_sequences(input_date_strings,
                                           symbol_to_idx=INPUT_SYMBOL_TO_IDX,
                                           sequence_len=INPUT_SEQ_LEN)
        input_sequences = dense_to_one_hot(input_sequences,
                                           num_classes=len(INPUT_SYMBOL_TO_IDX))

        target_sequences = encode_sequences(target_date_strings,
                                            symbol_to_idx=OUTPUT_SYMBOL_TO_IDX,
                                            sequence_len=OUTPUT_SEQ_LEN,
                                            pad_symbol=None)
        target_sequences = dense_to_one_hot(target_sequences,
                                            num_classes=len(OUTPUT_SYMBOL_TO_IDX))

        yield input_sequences, target_sequences
