Planificator Avansat de Activități

Introducere

În era modernă, gestionarea eficientă a timpului a devenit o provocare majoră atât pentru persoanele fizice, cât și pentru organizații. Cu numeroase activități și responsabilități, de la întâlniri de lucru și studiu până la activități personale, este esențial să dispunem de un instrument inteligent care să ne ajute să optimizăm programul zilnic. În acest context, aplicația noastră, Planificatorul Avansat de Activități, vine cu o abordare inovatoare, combinând algoritmi clasici de planificare cu metode moderne de învățare automată pentru a oferi soluții personalizate și eficiente.

Motivație

Deși există numeroase aplicații de calendar și planificare, precum Google Calendar sau TimeHero, acestea au limitări semnificative în ceea ce privește optimizarea automată a activităților. Aceste limitări stau la baza scopului acestui proiect.
Aplicația are ca scop principal să ofere un instrument flexibil, inteligent și ușor de utilizat pentru:

•Persoane fizice care doresc să-și gestioneze timpul eficient.

•Studenți care necesită o balanță între învățat, proiecte și timp liber.

•Profesioniști care au nevoie să-și planifice întâlniri și sarcini într-un mod optim.

Stare de Artă

Soluții Existente în Domeniu

1.Google Calendar + Google Assistant

Funcționalități principale:

•Sugerează automat ore pentru întâlniri pe baza programului utilizatorului.

•Folosește procesare de limbaj natural (NLP) pentru a interpreta comenzile vocale (ex: "Planifică o întâlnire la 15:00").

•Învață preferințele utilizatorului pe baza istoricului (ex: evită orele de vârf dacă utilizatorul respinge în mod repetat întâlniri dimineața).

Limitări:

•Nu optimizează automat ordinea activităților – utilizatorul trebuie să plaseze manual activitățile flexibile.

•Lipsa priorităților dinamice – nu ia în calcul durata sau importanța activităților pentru a le reordona.

2.TimeHero

Funcționalități principale:

•Automatizează programarea sarcinilor pe baza deadline-urilor și a estimărilor de timp.

•Se integrează cu tool-uri precum Slack, Trello, sau Google Workspace.

•Folosește ML pentru a prezice durata sarcinilor pe baza datelor istorice.

Limitări:

•Se bazează pe deadline-uri, nu pe prioritate sau durată – nu optimizează ordinea activităților pentru eficiență maximă.

•Nu gestionează activități fixe vs. flexibile într-un mod inteligent

Puncte de Inovație

Algoritm hibrid (A + ML)*

•Combină căutarea euristică (A*) cu predicții bazate pe învățare automată pentru o ordonare optimă.

•Scorul de prioritate este ajustat dinamic pe baza feedback-ului utilizatorului.

•Gestionare separată a activităților fixe și flexibile

•Activitatea fixă (ex: "Întâlnire la 14:00") este respectată, iar cele flexibile (ex: "Plimbare - 30 min") sunt plasate automat în intervalele libere.

•Îmbunătățire continuă prin feedback

•Rating-ul utilizatorului (1-5) este transformat într-un scor normalizat și folosit pentru reantrenarea modelului.

Limitări și Dezvoltare Viitoare

Limitări Curente

•Lipsa integării cu calendare externe (Google Calendar, Outlook).

•Interfața grafică simplistă (Tkinter are limite vizuale).

•Antrenament ML pe set mic de date (dacă training_data.csv este gol).

Îmbunătățiri Planificate

•API pentru sincronizare calendar (folosind OAuth).

•Interfață web modernă (cu Flask/Django).

•Export PDF pentru programul generat.

•Regăndire din punct de vedere CSP (Constraint satisfaction problem)

Descrierea Modelului

Arhitectura Sistemului

Sistemul are trei componente principale:

1.Interfața Utilizator (UI) – realizată în Tkinter pentru:

•Adăugarea activităților (nume, durată, prioritate, oră fixă).

•Afișarea programului generat.

•Colectarea feedback-ului.

2.Motorul de Planificare – implementat în planner.py:

•PlanificatorAStar: gestionează activitățile fixe și flexibile folosind A*.

•Activitate: clasă care stochează detalii despre fiecare activitate.

3.Modelul de Machine Learning (planner_m1.py) – RandomForestRegressor pentru:

•Calcularea scorurilor de prioritate.

•Antrenare pe date istorice (training_data.csv).

Detalii de Implementare

Algoritmul A*

Euristica: Scorul ML + prioritate + durată.

Pași principali:

•Validare activități fixe: Verifică suprapuneri.

•Calcul scoruri ML: Folosește RandomForestRegressor pentru a estima prioritatea.

Planificare:

•Plasare activități fixe.

•Umplere goluri cu activități flexibile (sortate după scor).

RandomForestRegressor

Antrenat pe: durată, prioritate, nr. activități rămase.

Scop: Prezice un scor între 0-1 pentru a decide ordinea optimă.

Modelul de ML (planner_m1.py)

Antrenare:

•Date inițiale: durată, prioritate, nr. activități rămase, scor.

•Actualizare: La fiecare feedback, se adaugă date noi în training_data.csv.

Predictie:

def predict(self, durata, prioritate, nr_ramase): return scor_între_0_și_1

Fluxul de Date (Workflow)

Adăugare activități:

•Utilizatorul completează nume, durată, prioritate, oră fixă (opțional).

•Datele sunt salvate în activitati.json.

Generare program:

•PlanificatorAStar rulează algoritmul și afișează rezultatul în UI.

Feedback:

•Utilizatorul dă un rating (1-5) → scor normalizat → antrenare ML.

Diagramă de secvențe

![DS_AI](https://github.com/user-attachments/assets/a2afff1f-0963-4d9a-862f-06f0e2b5d5ff)

Detalii Tehnice Complete

Cerințe Sistem

Limbaje și versiuni: Python 3.8+, biblioteci necesare (scikit-learn, numpy, pandas, tkinter).

Sistem de operare: Windows/Linux/macOS.

Resurse hardware: CPU minim, RAM recomandat (ex: 4GB+ pentru seturi mari de date).

Structura Fișierelor
![image](https://github.com/user-attachments/assets/94c9f54d-8959-4682-9366-6fbe8ad34e9d)

Instalare și Configurare

Instalare dependențe:

Bash - pip install scikit-learn numpy pandas

Rulare program:

Bash - python main.py

Concluzie

Proiectul Planificator Avansat de Activități reprezintă o soluție inovatoare în domeniul managementului timpului, combinând tehnologii clasice (algoritmul A*) cu metode moderne de învățare automată (RandomForestRegressor). Prin această abordare, aplicația depășește limitările unor tool-uri populare precum Google Calendar sau TimeHero, oferind:

1.Optimizare inteligentă a activităților pe baza:

•Priorității (definite de utilizator).

•Duratei (estimări automate).

•Feedback-ului (adaptare continuă prin ML).

2.Flexibilitate ridicată:

•Gestionarea separată a activităților fixe (ex: întâlniri la ore specifice) și flexibile (plasate automat în intervale libere).

•Respectarea unui buffer de timp (10 minute) între activități.

3.Îmbunătățire continuă:

•Modelul de ML se reantrenează pe baza rating-ului utilizatorului, devenind mai precis în timp.
