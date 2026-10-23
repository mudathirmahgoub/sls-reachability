| Configuration | unsat | sat | unknown | timeout | error | solved | median time |
|---|---|---|---|---|---|---|---|
| cvc5, sets solver | 89 | 140 | 0 | 11 | 0 | 229 | 0.019 s |
| cvc5, sets solver, `--fmf-bound` | 89 | 0 | 140 | 11 | 0 | 89 | 0.016 s |
| cvc5, `--sets-to-bags=setof`, stock bags solver | 24 | 52 | 0 | 164 | 0 | 76 | 0.023 s |
| cvc5, `--sets-to-bags=relaxed`, stock bags solver | 24 | 0 | 109 | 107 | 0 | 24 | 0.016 s |
| cvc5, `--sets-to-bags=setof --bags-to-liastar` | 92 | 136 | 11 | 1 | 0 | 228 | 0.035 s |
| cvc5, `--sets-to-bags=relaxed --bags-to-liastar` | 92 | 0 | 146 | 2 | 0 | 92 | 0.021 s |
| sls-reachability, BAPA | 72 | 117 | 0 | 51 | 0 | 189 | 0.196 s |
| sls-reachability, MAPA (`--mapa`) | 69 | 110* | 0 | 61 | 0 | 179 | 0.184 s |
| sls-reachability, MAPA, `--unfold=5` | 65 | 115* | 0 | 60 | 0 | 180 | 0.269 s |
| sls-reachability, MAPA, `--no-interp` | 59 | 112* | 0 | 69 | 0 | 171 | 0.136 s |
