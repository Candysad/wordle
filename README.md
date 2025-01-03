# Wordle

### word list

- find from [this](https://github.com/3b1b/videos/tree/master/_2022/wordle) repository



### wordle games

- [New York Times](https://www.nytimes.com/games/wordle/index.html)
- [wordly](https://wordly.org/)



### solutions

- enumerate

  ```python
  guesser = Guesser()
  guesser.update("audio", "02222")
  guesser.update("bench", "20222")
  guesser.candidate()
  ```

  - `update(word:str, stat:str)`
    - call this after each guess you made
    - `stat`
      - is a string of 5 characters, each of them implicates the state of characters at the same position
      - 1 stands for correct
      - 0 stands for not correct at this position while the target has this character
      - other character stands for the character at this position in `word` is not in the target
  - `candidate()`
    - returns candidate words for after update

- pytorch

  - `game_core`:  python class of the game of wordle
  - `model.ipynb`: a simple pytorch model without codes and data for training  
