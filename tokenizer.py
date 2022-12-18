from __future__ import annotations
import re
from collections import defaultdict
from data_retriveal import RepoRetriveal

class Tokenizer:

    PHYTHONREGEX = r"^\s*from\s+(\w+)\s+import\s+([\w\.]+(?:\s*,\s*\w+)*)|\
                    ^\s*import\s+([\w\.]+(?:\s*,\s*\w+)*)"
    
    @staticmethod
    def getTokenFreqs(file_list: list[RepoRetriveal.RepoFile]):
        import_pattern = re.compile(Tokenizer.PHYTHONREGEX, re.MULTILINE)
        tokenFreqs = defaultdict(lambda: 0)
        for file in file_list:
            tokens = file.filepath.split('/')
            for token in tokens:
                tokenFreqs[token] += 1

            if not file.filepath.endswith('.py'): continue

            matches = import_pattern.findall(file.content)
            listTokens = []
            for match in matches:
                for token in match:
                    if not token: continue
                    listTokens.extend(re.split(r'\W+', token)) 
            
            for token in listTokens:
                if not token: continue
                tokenFreqs[token] += 1

        return tokenFreqs