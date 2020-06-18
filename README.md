# Capitalizing on a TREC Track to Build a Tweet Summarization Dataset

Ce github contient le code du papier [Capitalizing on a TREC Track to Build a Tweet Summarization Dataset](https://www.irit.fr/CIRCLE/wp-content/uploads/2020/06/CIRCLE20_20.pdf).

## Différentes parties de ce répertoire

* [Annotations](/Annotations): Annotations que nous fournissons
* [Résultats](/Résultats): Résultats ROUGE
* [Données](/Données): Répertoire pour les textes des tweets et les résumés de chaque évènement
* [TREC IS annotations](/TREC%20IS%20annotations): TREC IS annotations
* [Tweets](/Tweets): Tweets bruts

## Package Requirements

Python 3.7

```
numpy==1.17.2
pandas==0.23.4
tqdm==4.28.1
```

## Données requises

Téléchargez les tweets et les annotations sur le site de la tâche TREC IS:
* [Annotations](http://dcs.gla.ac.uk/~richardm/TREC_IS/2020/TRECIS_2018_2019-labels.json "TREC IS Annotations 2018-2019")
* [Tweets](http://dcs.gla.ac.uk/~richardm/TREC_IS/2020/data.html "TREC IS Tweets 2018-2019"): Suivez les instructions et téléchargez les annotations **trecis2018-test**, **trecis2018-train**, **trecis2019-A-test** et **trecis2019-B-test**

* Placez les fichiers json d'annotations dans le répertoire [TREC IS annotations](/TREC%20IS%20annotations)
* Placez les fichiers json des tweets (dézippez les fichiers IS) dans le répertoire [Tweets](/Tweets)

## Générer les résumés

Exécutez le fichier python :

```
python initialization.py [-remove_coverage=False]
```

* Les résumés sont générés et placés dans le répertoire [Résumés](/Résumés)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

