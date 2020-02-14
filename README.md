# Stolen Cars US
Projet de Threat Intelligence, dont le but est d'extraire les informations du site https://www.stolencar.com/Report/Search, afin d'utiliser l'API PyMisp, et de créer un fichier JSON global pour référencer chaque véhicule volé qui est listé dans le site, ainsi que la position à laquelle le véhicule a été vu la dernière fois.

Prérequis :
- Python3 ;
- BeautifulSoup ;
- API PyMisp ;

### Comment ça marche
- Lancer  `extract_links.py ` pour lancer le script, tout est automatisé, et un fichier JSON sera créé une fois tous les véhicules analysés ;
- Si on souhaite relancer le script 1 ou 2 jours après, ou seulement sur une plage de pages réduites (par exemple, entre les pages 4 et 7), ou simplement en ne commençant pas à la 1ère page, alors lancer `extract_linksJourn.py` ;
- Dans le cas contraire, et que l'on souhaite relancer le script sur une "longue" période après (1 semaine par exemple), alors relancer `extract_links` ;

*Nota : lors du premier lancement (donc si aucun fichier JSON existe), il n'y pas de réelle importance entre `extract_links.py` et `extract_linksJourn.py`.*

*Un fichier JSON est laissé à titre d'exemple sur le projet GitHub.*

### Script extract_links :
Il s'agit du main de notre programme. On récupère premièrement la toute première page afin d'avoir le nombre total de véhicules sur le site. Ce nombre nous servira à calculer combien de pages comporte le site pour boucler dessus (à raison de 25 véhicules par page).

Afin de savoir si l'état du véhicule est Stolen ou Recovered, nous regardons s'il y a une balise rouge, caractéristique d'un véhicule retrouvé (Recovered).

### Script getOnePage :
3 dictionnaires différents :
- websiteToMisp : permet de corréler le langage du site avec celui de l'objet misp pour l'objet vehicle;
- websiteToMisp2 = permet de corréler la date avec l'attribut last-seen ;
- websiteToMisp3 = permet de corréler les informations de géolocalisation ;

Différentes fonctions :
- `extractFeatureName` : spliter une variable (remplie avec les fonctions de bs4) en fonction d'un tag html spécifique pour extraire le nom de la caractéristique du véhicule ;
- `extractInfosVehicle` : il s'agit là de la partie la plus importante du parser. En fonction des features parsées, on renseigne itérativement l'objet véhicule qui est en cours. Pour chaque event, on va lui ajouter un objet vehicule et un objet geoLocation. Avec ceci, on arrive répertorier toutes les informations importantes d'un véhicule sur ce site. Afin de faire correspondre entre eux les objets vehicle et geoLocation, la méthode `add_reference` est utilisée. De cette sorte, chaque objet vehicle aura une catégorie ObjectReference dans le fichier json, avec un champ `referenced_uuid` correspondant à un `uuid` de la géolocalisation référencée ;
- `printMispEvent` : afficher l'event MispVehicles ;

### Script mispVehicles :
C'est ici que nous créons l'event sur lequel sera attaché le véhicule et sa localisation.

Différentes fonctions :
- `createMispVehicle` : créer le misp objet vehicle ;
- `addComment` : ajouter un commentaire. Ici le numéro de rapport est choisi comme commentaire ;
- `addMispVehicle` : ajouter l'objet passé en paramètre à l'event courant ;
- `addAttributeMispVehicle` : ajouter la valeur val à l'attribut attr du mispObject vehicle ;
- `createMispGeolocation` : créer le misp objet geolocation ;
- `addMispGeolocation` : ajouter l'objet passé en paramètre à l'event courant ;
- `addAttributeMispGeolocation` : ajouter la valeur val à l'attribut attr du mispObject geolocation ;
- `printEvent` : permet d'imprimer le résultat de tout le processus dans un fichier Json. Créer un fichier json s'il n'existe pas, sinon remplace l'existant avec un nouveau Json avec les nouvelles valeurs ;

## Scripts alternatifs
Dans la version telle que présentée, nous faisons l'hypothèse que nous lançons le script à intervalle plus ou moins long (1 semaine environ), et **toujours depuis la 1ère page**. Dans ces conditions, après avoir analysé l'activité du site, il est quasi-certain que de nouveaux véhicules soient ajoutés sur le site entre la fin du run précédent, et le début du run suivant. C'est la raison pour laquelle nous mettons à jour les données systématiquement en remplaçant l'ancien Json.

Nous avons implémenté une autre méthode, avec les scripts `extract_linksJourn`,, `mispVehiclesJourn.py` et `getOnePageJourn.py` (pour journalier), qui sont davantage destinés à une utilisation "journalière" des scripts, ou du moins à une fréquence régulière. En utilisant ces 3 scripts, nous vérifions si le fichier Json existe, et si oui, nous regardons si les valeurs récoltées sont conformes ou déjà présentes dans le Json. Dans le cas où rien ne change (il est très fréquent qu'aucune donnée ne soit ajoutée d'un jour à l'autre sur le site), alors l'ancien Json est laissé en place. Sinon nous récupérons les données de l'ancien Json, et y ajoutons les nouvelles, ou modifions celles qui ont changé.

Pour utiliser ces scripts, il faut lancer le fichier `extract_linksJourn.py`. **Avec ces scripts, on peut le lancer depuis une autre page que la 1ère page** (par exemple page 2, 10, 152, etc.). Les changements détectés par rapport au Json existant ne se font alors que sur l'état (Stolen, Recovered) du véhicule. C'est la raison pour laquelle, après une "longue" période sans avoir lancé le script, il vaut mieux lancer `extract_links.py` car, par exemple, ce script est en mesure de mettre dans le Json la nouvelle date "last-seen".

A titre de comparaison, nous avons fait tourner les 2 méthodes parallèlement, et le temps d'exécution semble identique entre les 2 versions (Attention, le script `extract_links` refait un Json à partir de la borne des pages inférieures, donc toujours la position à 1).

## Pull request sur Misp
Nous avont fait des pull request sur les misp-objects du GitHub officiel de Misp.

Nous avons changé les `definition.json` des objets vehicle et geolocation pour leur ajouter des champs utiles à notre projet.

### Les difficultés relevées pendant le projet :

- Réussir à parser les données intéressantes du site. En effet, nous avons dû trouver des enchaînements répétitifs dans le code HTML afin de condenser le code du parser, et de l'écrire de la façon la plus générale possible selon le modèle du site. Le site n'a clairement pas été construit de façon à faciliter son parsing ;
- Comprendre le fonctionnement de l'API PyMisp, et notamment comprendre les concepts d'events, d'objets et d'attributs ;
- Implémenter le parsing en prenant en compte les exigences liées aux objets de Misp ;
- Pull request pour adapter les classes Geolocation et Vehicle à nos besoins, et qu'elles restent toutefois assez génériques ;
- Relever à quelle fréquence une analyse du site est pertinente (1 semaine semble bien), et trouver un compromis si on souhaite analyser qu'une partie des pages ;
