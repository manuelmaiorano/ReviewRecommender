import re

class Tokenizer:
    
    @staticmethod
    # conta le occorrenze dei metodi
    def method_occurrences(file_list):
        method_pattern = re.compile(r'def\s+(\w+)\(')
        method_dict = {}
        for file in file_list:
            file_content = file.content
            for method_name in method_pattern.findall(file_content):
                if method_name in method_dict:
                    method_dict[method_name] += 1
                else:
                    method_dict[method_name] = 1
        return method_dict

    @staticmethod
    # conta le occorrenze delle classi
    def class_occurrences(file_list):
        class_pattern = re.compile(r'class\s+(\w+)(?:\(.*\))?\s?:')
        class_dict = {}
        for file in file_list:
            file_content = file.content
            for class_name in class_pattern.findall(file_content):
                if class_name in class_dict:
                    class_dict[class_name] += 1
                else:
                    class_dict[class_name] = 1
        return class_dict

    @staticmethod
    # conta le occorrenze delle classi e dei metodi
    def class_method_occurrences(file_list):
        method_dict = Tokenizer.method_occurrences(file_list)
        class_dict = Tokenizer.class_occurrences(file_list)
        all_dict = {**method_dict, **class_dict}
        return all_dict
