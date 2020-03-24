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
        overlap(sample, sequence_id)
            returns:
                Boolean. True if sample overlaps the sequence represented by
                sequence_id. False otherwise
            raises:
                ValueError, when illegal characters are passed in.
                ValueError, when sequence_id is not an integer.
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
                ValueError when illegal characters are present in sample.
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
                ValueError when illegal characters are present in sequence.
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

    def overlap(self, sample, sequence_id):
        """
            Checks to see if provided sample overlaps the sequence
            represented by sequence_id.
            Attributes:
                sample (string): DNA sequence sample to find. Must only
                                 contain 'A','C','G' and 'T'.
                sequence_id (int): Sequence ID assigned to DNA sequence.
            Return:
                Boolean. True if sample overlaps the sequence represented by
                sequence_id. False otherwise
            Raises:
                ValueError, when illegal characters are present in sample.
                ValueError, when sequence_id is not an integer.
        """
        overlapped = False
        if (self._validate_input(sample)):
            if (isinstance(sequence_id, int)):
                sequence = self.get(sequence_id)
                if (len(sample) > len(sequence)):
                    if (sequence in sample):
                        overlapped = True
                else:
                    if (sample in sequence):
                        overlapped = True

                    elif self._overlap_front(sample, sequence):
                        overlapped = True

                    elif self._overlap_back(sample, sequence):
                        overlapped = True
            else:
                raise ValueError('Sequence ID must be an integer.')
        else:
            raise ValueError('Only A, C, G and T are allowed in sample.')

        return overlapped

    def _overlap_front(self, sample, sequence):
        """
            Check in sample overlaps sequence in the front
            Attributes:
                sample (string): DNA sequence sample to find. Must only
                                 contain 'A','C','G' and 'T'.
                sequence_id (int): Sequence ID assigned to DNA sequence.
            Return:
                Boolean. True if sample overlaps the sequence. False otherwise
        """
        overlaps = False
        # Get length of sample
        count = len(sample)
        # Get length of sample from the beginning of the sequence
        substring = sequence[:count]
        while(count > 0):
            # Check if we have a match
            if (sample == substring):
                overlaps = True
                break
            else:
                # When there is no match remove a character from beginning of
                # the sample and the end of the sequence substring
                count -= 1
                sample = sample[1:]
                substring = substring[:count]
        return overlaps

    def _overlap_back(self, sample, sequence):
        """
            Check in sample overlaps sequence from the back
            Attributes:
                sample (string): DNA sequence sample to find. Must only
                                 contain 'A','C','G' and 'T'.
                sequence_id (int): Sequence ID assigned to DNA sequence.
            Return:
                Boolean. True if sample overlaps the sequence. False otherwise
        """
        overlaps = False
        # Get length of sample
        count = len(sample)
        # Get length of sample from the end of the sequence
        substring = sequence[-count:]
        while(count > 0):
            # Check if we have a match
            if (sample == substring):
                overlaps = True
                break
            else:
                # When there is no match remove a character from the end of
                # the sample and the beginning of the sequence substring
                count -= 1
                sample = sample[:-1]
                substring = substring[-count:]
        return overlaps

    def _validate_input(self, sequence):
        """
            Validates that sequence only contains 'A', 'C', 'G' and 'T'.
            Return:
                True if valid, False if invalid.
        """
        if (self.VALIDATION_REG.match(sequence)):
            return True
        return False







