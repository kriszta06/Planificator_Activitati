Planificator Avansat de Activități: Stare de Artă și Descrierea Modelului 

 

Lucrare scrisă de Soos Kriszta 

 

 

Cuprins 

​​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​​ 

 

Introducere 

 

	În era modernă, gestionarea eficientă a timpului a devenit o provocare majoră atât pentru persoanele fizice, cât și pentru organizații. Cu numeroase activități și responsabilități, de la întâlniri de lucru și studiu până la activități personale, este esențial să dispunem de un instrument inteligent care să ne ajute să optimizăm programul zilnic. În acest context, aplicația noastră, Planificatorul Avansat de Activități, vine cu o abordare inovatoare, combinând algoritmi clasici de planificare cu metode moderne de învățare automată pentru a oferi soluții personalizate și eficiente. 

Motivație 

Deși există numeroase aplicații de calendar și planificare, precum Google Calendar sau TimeHero, acestea au limitări semnificative în ceea ce privește optimizarea automată a activităților. Aceste limitări stau la baza scopului acestui proiect. 

Aplicația are ca scop principal să ofere un instrument flexibil, inteligent și ușor de utilizat pentru: 

Persoane fizice care doresc să-și gestioneze timpul eficient. 

Studenți care necesită o balanță între învățat, proiecte și timp liber. 

Profesioniști care au nevoie să-și planifice întâlniri și sarcini într-un mod optim. 

 

Stare de Artă 

 

Soluții Existente în Domeniu 

 

Google Calendar + Google Assistant 

Funcționalități principale: 

Sugerează automat ore pentru întâlniri pe baza programului utilizatorului. 

Folosește procesare de limbaj natural (NLP) pentru a interpreta comenzile vocale (ex: "Planifică o întâlnire la 15:00"). 

Învață preferințele utilizatorului pe baza istoricului (ex: evită orele de vârf dacă utilizatorul respinge în mod repetat întâlniri dimineața). 

Limitări: 

Nu optimizează automat ordinea activităților – utilizatorul trebuie să plaseze manual activitățile flexibile. 

Lipsa priorităților dinamice – nu ia în calcul durata sau importanța activităților pentru a le reordona. 

 

TimeHero 

Funcționalități principale: 

Automatizează programarea sarcinilor pe baza deadline-urilor și a estimărilor de timp. 

Se integrează cu tool-uri precum Slack, Trello, sau Google Workspace. 

Folosește ML pentru a prezice durata sarcinilor pe baza datelor istorice. 

Limitări: 

Se bazează pe deadline-uri, nu pe prioritate sau durată – nu optimizează ordinea activităților pentru eficiență maximă. 

Nu gestionează activități fixe vs. flexibile într-un mod inteligent. 

 

 

Analiză Comparativă 

 

Criteriu 

Planificatorul nostru 

Google Calendar 

TimeHero 

Algoritm de planificare 

A* + RandomForestRegressor 

Sugestii bazate pe NLP 

Bazat pe deadline-uri 

Optimizare automată 

✅ (prioritate + durată) 

❌ (necesită input manual) 

⚠️ (doar pe baza deadline) 

Feedback adaptiv 

✅ (reantrenare ML pe rating) 

✅ (învățare preferințe) 

❌ 

Gestionare flexibilitate 

✅ (fixe + flexibile) 

❌ 

⚠️ (doar sarcini) 

Planificare vocală 

❌ 

✅ (Google Assistant) 

❌ 

 

Puncte de Inovație 

 

Algoritm hibrid (A + ML)* 

Combină căutarea euristică (A*) cu predicții bazate pe învățare automată pentru o ordonare optimă. 

Scorul de prioritate este ajustat dinamic pe baza feedback-ului utilizatorului. 

Gestionare separată a activităților fixe și flexibile 

Activitatea fixă (ex: "Întâlnire la 14:00") este respectată, iar cele flexibile (ex: "Plimbare - 30 min") sunt plasate automat în intervalele libere. 

Îmbunătățire continuă prin feedback 

Rating-ul utilizatorului (1-5) este transformat într-un scor normalizat și folosit pentru reantrenarea modelului. 

 

Limitări și Dezvoltare Viitoare 

 

Limitări Curente 

Lipsa integării cu calendare externe (Google Calendar, Outlook). 

Interfața grafică simplistă (Tkinter are limite vizuale). 

Antrenament ML pe set mic de date (dacă training_data.csv este gol). 

 

Îmbunătățiri Planificate 

API pentru sincronizare calendar (folosind OAuth). 

Interfață web modernă (cu Flask/Django). 

Export PDF pentru programul generat. 

Regăndire din punct de vedere CSP (Constraint satisfaction problem) 

 

Descrierea Modelului 

 

Arhitectura Sistemului 

 

Sistemul are trei componente principale: 

Interfața Utilizator (UI) – realizată în Tkinter pentru: 

Adăugarea activităților (nume, durată, prioritate, oră fixă). 

Afișarea programului generat. 

Colectarea feedback-ului. 

Motorul de Planificare – implementat în planner.py: 

PlanificatorAStar: gestionează activitățile fixe și flexibile folosind A*. 

Activitate: clasă care stochează detalii despre fiecare activitate. 

Modelul de Machine Learning (planner_m1.py) – RandomForestRegressor pentru: 

Calcularea scorurilor de prioritate. 

Antrenare pe date istorice (training_data.csv). 

 

Detalii de Implementare 

 

Algoritmul A* 

Euristica: Scorul ML + prioritate + durată. 

Pași principali: 

Validare activități fixe: Verifică suprapuneri. 

Calcul scoruri ML: Folosește RandomForestRegressor pentru a estima prioritatea. 

Planificare: 

Plasare activități fixe. 

Umplere goluri cu activități flexibile (sortate după scor). 

 

RandomForestRegressor 

Antrenat pe: durată, prioritate, nr. activități rămase. 

Scop: Prezice un scor între 0-1 pentru a decide ordinea optimă. 

 

Modelul de ML (planner_m1.py) 

Antrenare: 

Date inițiale: durată, prioritate, nr. activități rămase, scor. 

Actualizare: La fiecare feedback, se adaugă date noi în training_data.csv. 

Predictie: 

def predict(self, durata, prioritate, nr_ramase): 
    return scor_între_0_și_1 

 

Rezultate și Validare 

 

Activitate 

Durată (min) 

Prioritate 

Ora fixă 

Poziția în planificare 

"Învățat Python" 

60 

8 

- 

09:00 - 10:00 

"Plimbare" 

30 

5 

- 

10:10 - 10:40 

"Întâlnire" 

45 

3 

11:00 

11:00 - 11:45 

 

Observații: 

Activitatea cu prioritate mare ("Învățat Python") este planificată prima. 

Buffer-ul de 10 minute este respectat între activități. 

Limitări și Îmbunătățiri Viitoare 

Integrare cu Google Calendar (folosind API). 

Asistent vocal pentru adăugarea rapidă a activităților. 

Extindere pentru echipe (repartizare sarcini între membri). 

 

Fluxul de Date (Workflow) 

 

Adăugare activități: 

Utilizatorul completează nume, durată, prioritate, oră fixă (opțional). 

Datele sunt salvate în activitati.json. 

Generare program: 

PlanificatorAStar rulează algoritmul și afișează rezultatul în UI. 

Feedback: 

Utilizatorul dă un rating (1-5) → scor normalizat → antrenare ML. 

 

Diagramă de secvențe 

Picture 

 

Detalii Tehnice Complete 

 

Cerințe Sistem 

 

Limbaje și versiuni: Python 3.8+, biblioteci necesare (scikit-learn, numpy, pandas, tkinter). 

Sistem de operare: Windows/Linux/macOS. 

Resurse hardware: CPU minim, RAM recomandat (ex: 4GB+ pentru seturi mari de date). 

 

Structura Fișierelor 

 

├── data/   
│   ├── activitati.json          # Lista activităților salvate   
│   └── training_data.csv       # Datele de antrenament pentru ML   
├── planner.py                  # Motorul de planificare (A*)   
├── planner_m1.py               # Modelul de ML (RandomForest)   
├── ui.py                       # Interfața grafică (Tkinter)   
└── main.py                     # Punctul de intrare al programului 

 

Instalare și Configurare 

 

Instalare dependențe: 

Bash - pip install scikit-learn numpy pandas 

Rulare program: 

Bash - python main.py 

Link repository:  https://github.com/kriszta06/Planificator_Activitati  

 

Concluzie 

 

 	Proiectul Planificator Avansat de Activități reprezintă o soluție inovatoare în domeniul managementului timpului, combinând tehnologii clasice (algoritmul A*) cu metode moderne de învățare automată (RandomForestRegressor). Prin această abordare, aplicația depășește limitările unor tool-uri populare precum Google Calendar sau TimeHero, oferind: 

Optimizare inteligentă a activităților pe baza: 

Priorității (definite de utilizator). 

Duratei (estimări automate). 

Feedback-ului (adaptare continuă prin ML). 

Flexibilitate ridicată: 

Gestionarea separată a activităților fixe (ex: întâlniri la ore specifice) și flexibile (plasate automat în intervale libere). 

Respectarea unui buffer de timp (10 minute) între activități. 

Îmbunătățire continuă: 

Modelul de ML se reantrenează pe baza rating-ului utilizatorului, devenind mai precis în timp. 

 
