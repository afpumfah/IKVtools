### V3.0.03 - November 2020

[ ] DAS MUSS ICH NOCHMAL GENAUER ÜBERPRÜFEN. Wenn Ende Buchhaltung in Industrieprojekten erreicht wird, muss die Projektgelder gesperrt werden und die Werte auf Null gesetzt werden.
Das muss auch noch in der save() Funktion berücksichtigt werden. Andernfalls kann man durch ändern an irgendeiner Stelle hervorrufen, dass die Werte wieder eingeblendet ehe man nicht wieder auf die Liste geht.

[ ] Fokus auf Fehlermanagement im nächsten Update

##### Dashboard

- Die Klammern entfernt, die bei auslaufenden Projekten fälschlicherweise angezeigt wurden
- Auslaufende Projekten wurden immer unabhängig vom Jahr aufgelistet. Der Fehler wurde behoben.
- (Über)fällige Anträge und VÖs werden jetzt durchweg grau hinterlegt. Dies war vorher nur für den aktuellen Monat der Fall.

##### Assistenten

- Detailansicht
    - HiWis werden jetzt nach Namen sortiert

##### Industrie
- TODO:
    - Projekte, die abgelaufen sind, müssen wieder gesperrt werden, bzw. die verfügbaren Gelder müssen auf 0 gesetzt werden.

- Allgemein
    - Wenn ein Projekt beauftragt wird, wurden alle Arbeitspakete in der Summe für AL und A Gelder freigegeben. Der Fehler wurde behoben.
    - Falls Industrieprojekte über mehrer Jahre laufen (beauftragt sind), wurde diese nicht mit in der beauftragten Summe des Vorjahres berücksichtigt. Der Fehler wurde nun behoben

- Listenansicht
    - Wenn Ende Buchhaltung in Industrieprojekten erreicht wird, werden die Werte für die verbleibenden Projektgelder jetzt auf null gesetzt, da die Gelder nicht mehr zur Verfügung stehen. Dieser Fehler hat dazu geführt, dass man in der Liste Gelder sehen konnte die gar nicht zur Verfügung standen.

- Detailansicht
    - Nachdem die Projektgelder einmal freigegeben wurden, wurden die Werte nicht mehr zurückgesetzt, sobald man die Freigabe wieder rückgängig gemacht hat. Der Fehler wurde jetzt behoben.

##### Veröffentlichungen

- Allgemein
    - Eingabefeld für Journal enthielt einen formalen Fehler. Der Fehler wurde behoben

##### Einstellungen

- Journal
    - Beim erstellen eines Journals wurde eine falsche Erfolgsmeldung erzeugt. Der Fehler wurde behoben.
