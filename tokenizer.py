from __future__ import annotations
import re
from collections import defaultdict
from data_retriveal import RepoRetriveal

class Tokenizer:
    
    @staticmethod
    def getTokenFreqs(file_list: list[RepoRetriveal.RepoFile]):
        import_pattern = re.compile(r'^\s*(?:from|import)\s+([\w\.]+(?:\s*,\s*\w+)*)', re.MULTILINE)
        tokenFreqs = defaultdict(lambda: 0)
        for file in file_list:
            tokens = file.filepath.split('/')
            for token in tokens:
                tokenFreqs[token] += 1

            if not file.filepath.endswith('.py'): continue

            matches = import_pattern.findall(file.content)
            for match in matches:
                for token in match.split('.'):
                    tokenFreqs[token] += 1

        return tokenFreqs