# Reisekrankenversicherung – Prozessautomatisierung

Dieses Projekt wurde als Teamprojekt an der TU Dortmund entwickelt und automatisiert den Antragsprozess für eine Reisekrankenversicherung. Eine Java-Webanwendung stellt das Antragsformular bereit und startet den Prozess in Camunda 8.

Der Ablauf wird mit BPMN modelliert. DMN-Entscheidungstabellen prüfen unter anderem Alter, Wohnort und versicherte Personen und bestimmen den Selbstbehalt. Python-Worker übernehmen die Validierung der Reisedaten sowie die Anbindung von REST-APIs zur Partnersuche, Neuanlage von Kunden und Speicherung von Versicherungsverträgen.

Zusätzlich umfasst der Prozess Währungsumrechnung, Telefonnummernprüfung, Reisewarnungen, E-Mail-Benachrichtigungen und die Beauftragung des Dokumentendrucks. Fälle, die eine manuelle Prüfung benötigen, werden über Camunda Forms bearbeitet.

**Technologien:** Camunda 8, BPMN, DMN, Python, Zeebe, REST-APIs, Java, Spring Boot und Thymeleaf.

Die Java-Webanwendung basiert auf der viadee-Fallstudie „Reisekrankenversicherung“.
