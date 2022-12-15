import math
from dataclasses import dataclass
from decimal import Decimal
import uuid


@dataclass
class DocumentReference:
    file: str
    length: Decimal


@dataclass
class TokenOccurence:
    doc_ref: DocumentReference
    count: int


@dataclass
class TokenInfo:
    idf: Decimal
    occ_list: list[TokenOccurence]

    def __init__(self):
        self.occ_list = []


class InvertedFiles:

    def __init__(self):
        self.hash_map = {}

    def add(self, item, token_freq: dict[str, int]):
        files = item.getFiles()
        for file in files:
            for key in token_freq:
                if self.hash_map.get(key) in None:
                    token_info = TokenInfo()
                    self.hash_map[key] = token_info
                    doc_ref = DocumentReference()
                    doc_ref.file = file
                    token_occurence = TokenOccurence()
                    token_occurence.doc_ref = doc_ref
                    token_info.occ_list.append(token_occurence)

    @staticmethod
    def calculateIDF(files):
        files_len = len(files)

        idf_dict = dict.fromkeys(files[0].keys(), 0)
        for document in files:
            for token, val in document.items():
                if val > 0:
                    idf_dict[token] += 1

        for token, val in idf_dict.items():
            idf_dict[token] = math.log(files_len / float(val))

        return idf_dict

    @staticmethod
    def getCosineSimilarity(value1, value2):
        sum1, sum2, sum3 = 0, 0, 0
        for i in range(len(value1)):
            x = value1[i]
            y = value2[i]
            sum1 += x * x
            sum3 += y * y
            sum2 += x * y
        return sum2 / math.sqrt(sum1 * sum3)
