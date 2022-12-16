import re
from collections import defaultdict
from data_retriveal import RepoRetriveal

class Tokenizer:
    
    @staticmethod
    def getTokenFreqs(file_list: list[RepoRetriveal.RepoFile]):
        import_pattern = re.compile('import +(.*?)[ \r\n]')
        class_pattern = re.compile(r'class\s+(\w+)(?:\(.*\))?\s?:')
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
            
            matches = class_pattern.findall(file.content)
            for match in matches:
                tokenFreqs[match] += 1

        return tokenFreqs
