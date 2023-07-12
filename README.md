# CS 5150 Final Project `GobangAgent`

This repo represents the coursework for CS 5150 Game AI, the Spring 2022 Edition!

**Name:** Andy(Xiang-yu) Cui


**Email:** cui.xiangyu@northeastern.edu

**Preferred Name:** Andy Cui



### About/Overview

* Gobang is a very popular ancient culture in China, its also called Gomoku and Five in a Row, is an abstract strategy board game. It is traditionally played with Go pieces (black and white stones) on a Go board. It is played using a 15×15 board while in the past a 19×19 board was standard. Because pieces are typically not moved or removed from the board, Gobang may also be played as a paper-and-pencil game. The game is known in several countries under different names. Go bang have different name and play policy, I just want to design a Chinese version. Its only get five chess pieces, and then that player will win. 

  


### Game rule

* Player: put chess first (Black)

* Agent: put second (White)

* Turn one by one 

* Like big Tic-tac-toe, different from Tic-tac-toe, game need to have five chess pieces. Go-Bang chess On 15 x 15 game board.

* Win: player get five chess first.

* Fail: Agent get five chess first.

  


### Project performance 

#### Code structure

* Code use two main directory `src` and `res`
  * `src` store code
    * `gobangAgent.py` The AI game agent.
  
    * `gobangBoard.py` The Game board.
  
    * `gobangGui.py` The game GUI.
  
    * `startGame.py` The main of the project.  
  * `res` store the game materials
    * `img` store the game png stickers file
    * `sound` store the game sound file
  
* `demoShow` the example video for game agent works.



#### Project feature

* 15 x 15 game board with PNG.
* The arrow identifies location for Agent actions.
* Refer to Chinese gobang strategy analysis player’s action choose Agent action.
* Win or Lose game can restart or exit the game.
* Game sound with put chess actions.



#### Arithmetic & main logic

##### Arithmetic:

* Battle game Tree: Minimax Tree

* Pruning: Alpha–beta pruning

* Search: Depth First Search(DFS)

* Fusion concepts: Monte Carlo tree search (MCTS) 


##### Basic chess piece shape:

1. 冲二(STWO): If you add one more son to your side, only one point can become one of two.
   
2. 冲三(STHREE): If you add one more son to your side, only one point can make two of three.

3. 冲四(SFOUR): Means If you add one more son to your side, 
                only one point can be made into four of five. 
                Including continuous punch four and jump punch four, 
                jump punch four is also known as "embedded five"
            
4. 活二(TWO): Add one son to your side to form two of three living three.

5. 活三(THREE): Add one more son to your side, and you can form a three of a living four.

6. 活四(FOUR): Add one son to your side, and there are two points that can be a single four of five.

7. 活五(Five): Five chess pieces of the same color that are closely connected on a positive or negative line.

8. 双四(DFOUR): When a pawn falls, 2 rushing fours are formed at the same time.

9. 四三(FOURT): When rushing to the fourth, a live three is formed, and the next move is a live four to win.

10. 双三(DTHREE): When a pawn falls, 2 live threes are formed at the same time.


#### Some shape example:

![image-20220424050227175](C:\Users\Andy Cui\AppData\Roaming\Typora\typora-user-images\image-20220424050227175.png)



### How to Run

* The project main function is `startGame.py` which located `Gobang/src/startGame.py`.
  Open the repo directory and then open project use IDE PyCharm. Choose the `startGame.py` and click the green button to run it. 




### How to Use the Program

#### Program Environment requirement
  * python 3.9
  * PyQt5



### Example Runs

* ![image-20220423143140617](C:\Users\Andy Cui\AppData\Roaming\Typora\typora-user-images\image-20220423143140617.png)

  




### Limitations

I think the limitations is that:

* The game have only difficult game agent.  
* Can not choose who first in game GUI, it should change at code. `gobangGui.py` line 86-87.
* It only can do small game board, if board bigger, it will use more time, but gobang only have 5 in line win rules, so it good for this game.



### Citations

[1] (2020, October 06). GoBangChinese. *GobangTerm.*  Retrieved April 24, 2022, from http://www.wuziqi123.com/jiangzuo/zhuanti/168.html