from typing import List, Tuple

import torch
from torch import Tensor

class WordsIndexError(Exception):
    def __init__(self, answerlen:int, targetlen:int) -> None:
        super().__init__()
        self.info = f"length of answer: {answerlen} is not same with those of target: {targetlen}"
    def __str__(self) -> str:
        return self.info

class Wordle:
    # encode a word into vector
    def encode(self, word) -> List[int]:
        result = []
        for c in word:
            result.append(ord(c) - ord('a'))
        return result
    
    # init and save target word 
    def __init__(self, target: str, training:bool=False) -> None:
        self.targetstr = target
        target = self.encode(target)
        self.target = target
        self.targetset = set((target))
        self.n = len(self.target)
        
        self.training = training
        self.success = False
        
        # 1 : correct at this position
        # 0 : unknown 
        self.correct = [0] * self.n

        # 1: this position is not the letter
        # 0: unknown
        self.notcorrect = [[0] * 26 for _ in range(self.n)]
        
        # 1: the letter is not in this word
        # 0: unknown
        self.hasnot = [0] * 26

        # 1: the letter is in this word
        # 0: unknown
        self.has = [0] * 26
    
    # check an answer
    def check(self, answer: str) -> None:
        n = self.n
        if answer == self.targetstr:
            self.success = True
        answer = self.encode(answer)
        target = self.target
        targetset = self.targetset
        correct = self.correct
        notcorrect = self.notcorrect
        hasnot = self.hasnot
        has = self.has

        if len(answer) != n:
            raise WordsIndexError(len(answer), len(target))
        
        for i in range(self.n):
            ac, tc = answer[i], target[i]
            
            if ac == tc:
                correct[i] = 1
                has[ac] = 1
            else:
                notcorrect[i][ac] = 1
                if ac in targetset:    
                    has[ac] = 1
                else:
                    hasnot[ac] = 1

    '''
    Return a tensor as [n + 1, 26]
    The former n-dimensions stand for each position
    The last one dimension stands for all characters
    '''
    def query(self):
        correct, notcorrect, hasnot, has = self.correct, self.notcorrect, self.hasnot, self.has
        n = self.n
        target = self.targetstr
        if not self.training:
            return correct, notcorrect, hasnot, has
        
        tensor = torch.zeros(n + 1, 26)
        for i in range(n):
            result = {}
            if correct[i]:
                result["correct"] = target[i]
                tensor[i][self.target[i]] = 1
            else:
                result["correct"] = "unkown"
            
            result["not"] = set()
            for j in range(26):
                if notcorrect[i][j]:
                    result['not'].add(chr(ord('a') + j))
                    tensor[i][j] = -1
            if not self.training:
                print("position:", i)
                print(result)
                print()
        
        t = set()
        for j in range(26):
            if has[j]:
                t.add(chr(ord('a') + j))
                tensor[-1][j] = 1
        if not self.training:
            print('has:', sorted(t))
        
        t = set()
        for j in range(26):
            if hasnot[j]:
                t.add(chr(ord('a') + j))
                tensor[-1][j] = -1
        if not self.training:
            print('has not:', sorted(t))

        return tensor.reshape((1, n + 1, 26))    
    
    def get_target(self) -> Tuple[str, Tensor]:
        n = self.n
        target = self.target
        
        tensor = -1 * torch.ones(self.n, 26)
        for i in range(n):
            tensor[i][target[i]] = 1
        
        return self.targetstr, tensor.reshape((1, n, 26))
     

if __name__ == "__main__":
    wordle = Wordle("scone")
    print(wordle.get_target())
    
    while wordle.success == False:
        print(f"enter a word of lengh: {wordle.n}")
        line = input()
        line.strip()
        
        try:
            wordle.check(line)
            wordle.query()
        except WordsIndexError as e:
            print(e)
        print()
    print("success!")
