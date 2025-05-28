# Wave Function Collapse
### Simple Tiled Model / ESTM
First pass at adjacency-rule WFC. It does the job, at present adjacency rules don't take into consideration rotation or reflection data because the domain reduction was minimal, based on how I'm already interpreting data in a cell. Ex: If a cell has data ABC, and another cell has data ABC, they both hash to the same identity despite being two separate objects... this and similar optimizations I think are what the original WFC algorithm solves with rotation and reflection data.

Derived from the following resources: <br>
https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/ <br>
https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/ <br>
https://paulmerrell.org/model-synthesis/

<img src="images/ESTM.png" width="80%">

### Overlapping WFC
https://www.gridbugs.org/wave-function-collapse/ <br>
https://www.youtube.com/watch?v=5iSAvzU2WYY <br>