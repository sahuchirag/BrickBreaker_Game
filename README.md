# Brick-Breaker
The classic brick breaker game in terminal from scratch without any special libraries such as pygame. It has 3 levels where the final level is the boss level with a UFO!

## Setup

1. <b>Installation</b><br />
pip3 install -r requirements.txt

2. <b>Execution</b><br />
python3 main.py

## Controls

1. `A` to move the paddle left.
2. `D` to move the paddle right.
3. `Space` to release the ball from the paddle.
4. `Q` to quit the game.
5. `N` to skip a level.

## Rules
1. You get 3 lives in the game.
2. Increase your score by breaking bricks.
3. Brick Color Scheme:
    * Green: Breakable but full health brick.
    * Orange: Breakable but half health brick.
    * Red: Breakable but quarter health brick.
    * Magenta: Unbreakable brick.
    * Blue: Exploding brick.
    * Special rainbow brick retains/fixes on the health level it has when ball collides with it. 
4. Hitting a green brick brings it to orange level. Orange turns to red. Red breaks/disappears.
5. Hitting an exploding brick makes it explode and directly break any other bricks close to it including unbreakable bricks.
6. Powerup Scheme:
    * "<=>" - Paddle Expand: Paddle width increases
    * ">=<" - Paddle Shrink: Padd width decreases
    * "2xO" - Ball Multiplier: Number of balls doubles
    * ">>>" - Fast Ball: Ball speed increases
    * "XXX" - Thru Ball: Ball can break any brick(even unbreakable) in 1 shot
    * "|_|" - Paddle Grab: Ball sticks to paddles when collides with paddle.
    * "^_^" - Paddle Shoot: Paddle periodically shoots a pair of bullets with strength of a normal ball(no special effects such as "Thru Ball").
    * "\<O\>" - Fire Ball: Ball that produces exploding effect on any brick it touches, i.e, all neighboring bricks are also destroyed.
7. The above powerups can be active simultaneously in any combination as well. 
8. Each powerup lasts for about 15 seconds.
9. The game ends when player breakes all the breakable bricks in all the levels or loses all lives.
10. The lesser the time taken per level, the higher the final score will be!
11. Bricks begin to move down everytime ball collides with paddle after a certain time limit is reached.
12. UFO in boss level drops bombs periodically. When a bomb collides with the paddle, the player loses 1 life.
