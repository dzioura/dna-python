import re

class SequenceDbClass:
    """
    Sequence Database Class

    Will implement in memory database of DNA sequences

    Public Methods
        find(sample)
            returns:
                List of sequence_ids that have DNA sequences that contain
                the sample sequence. Empty list if the sample sequence
                does not match.
            raises:
                ValueError, when illegal characters are passed in.    
        get(sequence_id)
            returns:
                DNA sequence associated with the id.
                If no match is found message to user will be displayed.
                'Inputed sequence_id does not match any sequence.'
            raises:
                ValueError, when sequence_id is not an integer.
        insert(sequence)
            returns:
                Dictionary containing sequence_id and message. If sequence was
                created or existing. Valid input is a string containing the
                following characters 'A','C','G' and 'T'. If sequence already
                exists the sequence_id will be returned, with message 'exists'.
            raises:
                ValueError, when illegal characters are passed in.
    """
    VALIDATION_REG = re.compile('^[ACGT]+$')
    NEXT_ID = 1
    _database = {}
    
    def __init__(self):
        self._database = {
            "by_id": {},
            "by_sequence": {}
        }

    def find(self, sample):
        """
            Find DNA sequences that contain provided sample.
            Attributes:
                sample (string): DNA sequence sample to find. Must only
                                 contain 'A','C','G' and 'T'.
            Return:
                List - List containing sequence_id that match the sample.
            Raises:
                ValueError when invalid input is provided
        """
        return_list = []
        if (self._validate_input(sample)):
            for sequence, sequence_id in self._database['by_sequence'].items():
                if (sample in sequence):
                    return_list.append(sequence_id)
        else:
            raise ValueError('Only A, C, G and T are allowed in sample.')

        return return_list


    def get(self, sequence_id):
        """
            Get DNA sequence that matches the sequence_id.
            Attributes:
                sequence_id (int): Sequence ID assigned to DNA sequence.
            Return:
                String - DNA sequence, on no sequence the following message
                'Inputed sequence_id does not match any sequence.'.
            Raises:
                ValueError when sequence_id is not a positive integer.
        """
        if (isinstance(sequence_id, int)):
            sequence = self._database['by_id'].get(sequence_id)
            if (sequence):
                return sequence
            else:
                return 'Inputed sequence_id does not match any sequence.'
        else:
            raise ValueError('Sequence ID must be an integer.')

    def insert(self, sequence):
        """
            Insert new sequence to the database
            Attributes:
                sequence (sting): DNA sequence must only contain 
                                  'A','C','G' and 'T'.
            Return:
                Dictionary with sequence_id and message.
            Raises:
                ValueError when invalid input is provided.
        """
        if (self._validate_input(sequence)):
            return_obj = {
                'sequence_id': self._database['by_sequence'].get(sequence),
                'message': 'created'
            }
            if (return_obj['sequence_id'] is None):
                return_obj['sequence_id'] = self.NEXT_ID
                self._database['by_id'][self.NEXT_ID] = sequence
                self._database['by_sequence'][sequence] = self.NEXT_ID
                self.NEXT_ID += 1
            else:
                return_obj['message'] = 'exists'
        else:
            raise ValueError('Only A, C, G and T are allowed in sequence.')

        return return_obj

    def _validate_input(self, sequence):
        """
            Validates that sequence only contains 'A', 'C', 'G' and 'T'.
            Return:
                True if valid, False if invalid.
        """
        if (self.VALIDATION_REG.match(sequence)):
            return True
        return False







