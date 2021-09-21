# WriteUp Coffee

Url du challenge: https://coffee.0xhorizon.eu/

On se retrouve sur une page de login.
On test des login/password classic pour voir(ex: admin/admin, root/root).Rien de bien fou toujours le même message.

## SQL Injection

Essayons une injection sql en **sqlite** pour bypass cette page de connexion:

- **login**: `1' or 1=1 --` -- sont présent pour commenter le reste de la requête.
- **password**: `a` champ obligatoire.

Message:

```bash
Hello user1
Your message: I want coffee...
```

Victoire on a reussit à faire une injection cependant on a pas le bon user.
Essayons la même avec le login admin:

- login: `admin' or 1=1 --`
- password: `a`

Message:

```bash
There is not any user with an username or a password so long :(
```

Ahhh on est limité en therme de caractère.
testons encore plus simple:

- login: `admin' --`
- password: `a`

Message:

```
Hello admin
Your message: Coffee code: horiz0nx{FLAG}
```

GG!