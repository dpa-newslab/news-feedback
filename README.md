# news-feedback

news-feedback ist eine Web-Oberfläche, mit der Nutzerfeedback zu automatisch erstellten Nachrichtenpaketen eingesammelt werden kann. Die Software ist Teil des Projektes [News-Stream](http://newsstreamproject.org/).

## Aufruf

https://dpa-newslab.github.io/news-feedback/#(xxxxxxxx)


Statt des (xxxxxx) muss die öffentlich zugängliche URL eines Nachrichtenpaket-Bündels angegeben werden. Solche Nachrichtenpaket-Bündel lassen sich zum Beispiel mit dem Script im Verzeichnis `newsbundle-generator` erstellen.

### Beispiele

Diese Beispiele sind Passwortgeschützt. Das Passwort ist über die üblichen Wege verfügbar.


  - Aktuelle Branchennews aus der dpa-Berichterstattung:
    https://werkzeugkasten.dpa-newslab.com/newsstream-branchen/#werkzeugkasten.dpa-newslab.com/newsstream-branchen/data/demo-dpa/
  
  
  - Aktuelle Branchennews aus dem Neofonie Newscrawl:
    https://werkzeugkasten.dpa-newslab.com/newsstream-branchen/#werkzeugkasten.dpa-newslab.com/newsstream-branchen/data/demo-newscrawl/


## newsbundle-generator

--- tbd ---

## Datenstruktur der Nachrichtenbündel

### 1. Datenebene

**index.json**

  - wird als erstes aufgerufen
  - beinhaltet unter „chapters“ die Dateinamen der nächste Datenebene, mit der die Navigation aufgebaut wird
  - außerdem sind hier Allgemeines zur App zu finden wie Titel, Beschreibung und Email-Angaben

```json
{
  "chapters": {
    "31. 10. 2016": "20161031-index.json",
    "30. 10. 2016": "20161030-index.json",
    "29. 10. 2016": "20161029-index.json",
….
  },
  "placeholder": "Anmerkung",
  "subject": "Branchendienst - Feedback",
  "email": "mvirtel@dpa-newslab.com",
  "description": "<h2>Anleitung</h2><p>Unser Algorithmus... <a href='#'>Mehr Informationen</a></p>",
  "title": "Branchendienst"
}
```


### 2. Datenebene

Beispiel für einen Dateinamen: 20161030-index.json

   - enthält die Angaben zur Navigation pro „chapter“
   - außerdem enthält sie unter „docs“ alle Angaben der Teaser, die im Hauptbereich bei Klick auf die Navigation angezeigt werden
   - unter „docs.dokument“ gibt es die Dateinamen der 3. Datenebene

unter docs: Angaben zu den Teasern

Beispiel für ein Teaser Element:

```json

        {
            "sourcelink": "javascript:alert('Link für ex neoApplication')",
            "id": "2c992bf793469764dd50f225a0448905",
            "subtitle": "Untertitel zu Zeitung",
            "createdAt": "2016-10-25T22:05:09Z",
            "section": "FIN",
            "title": "Regierung ...",
            "source": "ex neoApplication",
            "externalId": "urn:newsml:dpa.com:20090101:161025-99-939150/2",
            "sections": [
              "FIN"
            ],
            "document": "20161025/2c992bf793469764dd50f225a0448905.json"
          }
```

### 3. Datenebene

Beispiel für einen Dateinamen: 
`20161030/2e6a9a1492abdaad827658546298fd29.json`

  - enthält den Content, der bei Klick auf einen Teaser angezeigt wird
  - enthält außerdem Angaben, die zur Auswertung der Daten sinnvoll sind

```json
{
  "sourcelink": "javascript:alert('Link für ex neoApplication')",
  "id": "2c992bf793469764dd50f225a0448905",
  "subtitle": "Untertitel zu Zeitung: Regierung rät in Rentenbericht zur privaten Vorsorge",
  "createdAt": "2016-10-25T22:05:09Z",
  "index": "../20161025-index.json",
  "text": "Berlin (dpa) - Die Bundesregierung...",
  "section": "FIN",
  "root": "../index.json",
  "title": "Zeitung: Regierung rät in Rentenbericht zur privaten Vorsorge",
  "source": "ex neoApplication",
  "externalId": "urn:newsml:dpa.com:20090101:161025-99-939150/2",
  "sections": [
    "FIN"
  ],
  "document": "20161025/2c992bf793469764dd50f225a0448905.json"
}
```




