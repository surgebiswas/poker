# Johnny Harv's Bodacious Poker Tour Goes Computational
Poker AI

Our goal is to further our understanding of how we make decisions under pressure with imperfect information by studying the game of poker. Even if you play the game a lot, it's difficult to crystallize exactly why and how you make certain decisions in different situations. Are there other strategies you, or people in general, might be missing? Our hope is that in the process of programming an agent to play, or learn how to play, poker we might improve our understanding of the game and our own decision making processes.

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
S-> MATCHSTATE:0:30:cc/:9s8h|/8c8d5c

'MATCHSTATE:' <position>:<handNumber>:<nolimitbetting>:<cards>
<position> := <unsigned integer>

<handNumber> := <unsigned integer>

<nolimitBetting> := <round1NolimitBetting> '/' <round2NolimitBetting> ...
  <roundXNolimitBetting> := <fold> | <call/check> | <nolimitRaise> 
    <fold> := 'f'
    <call/check> := 'c'
    <nolmitRaise> := 'r'<unsigned integer>

<cards> := <holeCards> <boardCards>
  <holeCards> := <player1Cards> '|' <player2Cards> '|' ...
    <playerXCards> := '' | <card> { <card> ... } 
  <boardCards> := <round1BoardCards> { '/' <round2BoardCards> ... }


<roundXBoardCards> := { <card> ... }
<card> := <rank> <suit>
<rank> := '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'T' | 'J' | 'Q' | 'K' | 'A' <suit> := 's' | 'h' | 'd' | 'c'
```

## References
[1] http://www.computerpokercompetition.org

[2] http://poker.cs.ualberta.ca

[3] http://www.computerpokercompetition.org/downloads/documents/protocols/protocol.pdf





