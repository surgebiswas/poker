# Johnny Harv's Bodacious Poker Tour Goes Computational
*Before machines take over the world, they will play poker.*

Staying true to it's name, the folks at Johnny Harv's are making a bodaciously outrageous new move into the world of computational poker. We challenge **you** to build your own poker mean-machine and submit it for battle in the form of no-limit Texas Hold'em. 

This repository contains:

1. Code to manage poker (no-limit Texas Hold'em) games between multiple agents. Games are managed, in large part, using the API made available by the Annual Computer Poker Competition (ACPC) [1]. This API was written in C by the Computer Poker Research Group at the University of Alberta [2]. This code was edited by Surge Biswas to simplify the interface for compatibility with higher level languages (e.g. R and Python). This code is contained in the "project_acpc_server" folder. 

2. Community submitted computational poker agents. Details below on how to program and submit your agent for competition.

## Programming your agent

When programming your agent, you do not need to worry about directly interfacing with the ACPC API and so you can ignore the contents of the "project_acpc_server" folder. However your agent must meet the following interface:

1. Be command line executable
2. Take two arguments as input:
  - 'Match State' string that describes the full state of the match up until the agent's current turn. More details below.
  - An output file destination to which the player's action is written.
3. Output a valid action by writing to the specified output file above. More details below.

The agent will be invoked using a command of the following form `/path/to/your/agent_executable <MATCH_STATE> <OUTPUT_FILE>`. Note that if your agent is written in e.g. Python, the call to your agent may be something like `python /path/to/your/agent.py <MATCH_STATE> <OUTPUT_FILE>`, but that this does NOT meet the above interface. In this situation you should create a wrapper shell script for your program. This wrapper might have the name `/path/to/your/agent.sh` and have the following contents:

```
#!/bin/bash/
python /path/to/your/agent.py $1 $2
```

**MATCH STATE STRING** - The match state string specification is as described in the communication protocol document published by the ACPC [3]. The following is an edited excerpt that provides the relevant information for understanding the match state string for No Limit Texas Hold'em. The match state string has the following format:

```
'MATCHSTATE:' <position>:<handNumber>:<nolimitbetting>:<cards>

<position> := <unsigned integer>

<handNumber> := <unsigned integer>

<nolimitBetting> := <round1NolimitBetting> '/' <round2NolimitBetting> ...
  <roundXNolimitBetting> := <fold> or <call/check> or <nolimitRaise> 
    <fold> := 'f'
    <call/check> := 'c'
    <nolmitRaise> := 'r'<unsigned integer>

<cards> := <holeCards>'/'<boardCards>
  <holeCards> := <player1Cards> '|' <player2Cards> '|' ...
    <playerXCards> := '' or <card><card>
  <boardCards> := <round1BoardCards>'/'<round2BoardCards>
    <roundXBoardCards> := <card>...
    
      <card> := <rank><suit>
      <rank> := '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'T' | 'J' | 'Q' | 'K' | 'A' 
      <suit> := 's' | 'h' | 'd' | 'c'
```
A few things to note:
- The `<position>` field tells the client their position relative to the dealer button. A value of 0 indicates that for the current hand, the client is the first player after the button (the small blind in ring games, or the big blind in reverse-blind heads-up games.)
- The `<handNumber>` is simply an identifier for the current hand. Clients should make no assumption about these values, other than that it will be unique across hands within a match, and that it will not change within a single hand.
- `<betting>` is a list of actions taken by all players. There is no distinction made between calling and checking, or betting and raising. The raise action includes a size, which indicates the total number of chips the player will have put into the pot after raising (*i.e. the value they are raising to, not the value they are raising by.*) 
- `<cards>` is the complete set of cards visible to the player, given their `<position>`. `<holecards>` describes the view of the private cards, and the number of `<playerCards>` sections is determined by the game being player. For example, heads-up games will have two sections, 3 player ring games will have 3 sections, and so on. Each `<playerCard>` section will either be an empty string, indicating that the player does not know what those cards are, or a number of `<card>` strings determined by the game. A `<card>` is simply two characters, one for the rank and one for the suit. The `<boardCards>` description will also have a number of sections, one for each round, up to the current round as indicated by the `<nolimitbetting>`. The number of `<cards>` in each section is fixed, and determined by the game. 

Here are two example sequences from a two player no-limit game:

```
MATCHSTATE:0:30::9s8h| <=> This is the 30th hand. You are the first person after the dealer and are dealt a 9 of spades and 8 of hearts.
MATCHSTATE:0:30:c:9s8h| <=> You call
MATCHSTATE:0:30:cc/:9s8h|/8c8d5c <=> Villain (other person) calls. Flop is 8 of clubs, 8 of diamonds, 5 of clubs.
MATCHSTATE:0:30:cc/r250:9s8h|/8c8d5c <=> You raise 250
MATCHSTATE:0:30:cc/r250c/:9s8h|/8c8d5c/6s <=> Villain calls. Turn is 6 of spades. 
MATCHSTATE:0:30:cc/r250c/r500:9s8h|/8c8d5c/6s <=> You raise 500. 
MATCHSTATE:0:30:cc/r250c/r500c/:9s8h|/8c8d5c/6s/2d <=> Villain calls. River is 2 of diamonds.
MATCHSTATE:0:30:cc/r250c/r500c/r1250:9s8h|/8c8d5c/6s/2d <=> You raise 1250
MATCHSTATE:0:30:cc/r250c/r500c/r1250c:9s8h|9c6h/8c8d5c/6s/2d <=> Villain calls. At showdown Villain reveals 9c6h. You win with trip 8's.

MATCHSTATE:1:31::|JdTc <=> You are second after the dealer, and were dealt a Jack of diamonds and a ten of clubs.
MATCHSTATE:1:31:r300:|JdTc <=> Villain raises 300.
MATCHSTATE:1:31:r300r900:|JdTc <=> You re-raise to 900.
MATCHSTATE:1:31:r300r900c/:|JdTc/6dJc9c <=> Villain calls, flop is 6 of diamonds, Jack of clubs, and 9 of clubs.
MATCHSTATE:1:31:r300r900c/r1800:|JdTc/6dJc9c <=> Villain raises to 1800. 
MATCHSTATE:1:31:r300r900c/r1800r3600:|JdTc/6dJc9c <=> You re-raise to 3600.
MATCHSTATE:1:31:r300r900c/r1800r3600r9000:|JdTc/6dJc9c <=> Villain re-raises to 9000.
MATCHSTATE:1:31:r300r900c/r1800r3600r9000c/:|JdTc/6dJc9c/Kh <=> You Call. King of hearts on the turn.
MATCHSTATE:1:31:r300r900c/r1800r3600r9000c/r20000:|JdTc/6dJc9c/Kh <=> Villain goes all in.
MATCHSTATE:1:31:r300r900c/r1800r3600r9000c/r20000c/:KsJs|JdTc/6dJc9c/Kh/Qc <-> You call. Queen of clubs on the river. You lose to villain who has a two pair, Kings and Jacks. 
```
Everything before the '<=>' is the match state string, and everything after is an explanation of what's going on.

## Submitting your agent

1. Before you get started programming your agent, you should clone this repository. 
2. Then create a folder that is named after what will be your username. Write all of your code in this folder. 
3. For your agent(s) specifically, create an executable that meets the interface described above. This executable should be directly under your user folder (e.g. `./poker/your_user_folder/your_agent.sh` NOT `./poker/your_user_folder/agents/your_agent.sh`).
4. Create a file `agents.txt` directly under your user folder. This file should contain the names of your agent scripts one line after another. For example,
```
my_agent1.sh
my_agent2.sh
```

## References
[1] http://www.computerpokercompetition.org

[2] http://poker.cs.ualberta.ca

[3] http://www.computerpokercompetition.org/downloads/documents/protocols/protocol.pdf





