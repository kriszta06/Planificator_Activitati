import numpy as np
from planner_m1 import ActivityModel
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json 
import os

class Activitate:
    def __init__(self, nume, durata, prioritate, este_fixa=False, ora_fixa=None):
        self.nume = nume
        self.durata = int(durata)
        self.prioritate = int(prioritate)
        self.este_fixa = este_fixa
        
        if ora_fixa:
            if isinstance(ora_fixa, datetime):
                self.ora_fixa = ora_fixa
            else:
                try:
                    time_part = datetime.strptime(ora_fixa, "%H:%M").time()
                    self.ora_fixa = datetime.combine(datetime.now().date(), time_part)
                except ValueError:
                    raise ValueError("Format orei invalid! Te rog folosește HH:MM")
        else:
            self.ora_fixa = None

#pt sortare activitati
def planifica_simpla(activitati):
    activitati.sort(key=lambda a: (-a.prioritate, a.durata)) #sortez desc dupa prioritate, cresc dupa durata
    ora_start = datetime.strptime("08:00", "%H:%M")
    ora_limita = datetime.strptime("23:59", "%H:%M")
    rezultat = []
    depasire = False
    
    for act in activitati:
        start = ora_start
        stop = start + timedelta(minutes=act.durata)
        if stop > ora_limita:
            depasire = True
            messagebox.showwarning(
                "Depășire program",
                "Unele activități nu încap în intervalul 08:00-00:00!\n"
                f"Ultima activitate planificată se termină la {stop.strftime('%H:%M')}."
            )
            break 
        rezultat.append(f"{start.strftime('%H:%M')} - {stop.strftime('%H:%M')} | {act.nume}")
        ora_start = stop
    
    return rezultat

#pt gestionare fisiere
def salveaza_activitati(lista, cale="data/activitati.json"):
    os.makedirs("data", exist_ok=True)
    
    def activitate_to_dict(a):
        return {
            "nume": a.nume,
            "durata": a.durata,
            "prioritate": a.prioritate,
            "ora_fixa": a.ora_fixa.strftime("%H:%M") if a.ora_fixa else None
        }
        
    with open(cale, "w", encoding='utf-8') as f:
        json.dump([activitate_to_dict(a) for a in lista], f, indent=2, ensure_ascii=False)

#pt gestionare fisiere
def incarca_activitati(cale="data/activitati.json"):
    try:
        with open(cale, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            date = json.loads(content)
            return [Activitate(**a) for a in date]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Eroare", "Fișierul de activități este corupt!")
        return []

#alg AStar
class PlanificatorAStar:
    def __init__(self, activitati, start_time="08:00"):

        if not activitati:
            raise ValueError("Nu există activități de planificat! Adaugă activități înainte de a genera programul.")

        #impart in doua liste activitatile
        self.activitati_fixe = [a for a in activitati if a.ora_fixa is not None]
        self.activitati_flex = [a for a in activitati if a.ora_fixa is None]

        #salvez ora de start
        self.start_time = datetime.strptime(start_time, "%H:%M")

        #obiect de tip ActivityModel
        self.model = ActivityModel()

        #salvez scorurile generate
        self._pred_cache = {}
        
        if not self.model.load_training_data():
            self._train_initial_model()
        
        self._valideaza_activitati_fixe()

    #validare
    def _valideaza_activitati_fixe(self):
        
        #sortez activitati in functie de ora fixa
        self.activitati_fixe.sort(key=lambda x: x.ora_fixa)
        
        #le parcurg in perechi
        for i in range(len(self.activitati_fixe)-1):

            current_end = self.activitati_fixe[i].ora_fixa + timedelta(minutes=self.activitati_fixe[i].durata)
            next_start = self.activitati_fixe[i+1].ora_fixa
            
            
            if current_end > next_start:
                raise ValueError(
                    f"Activitațile fixe se suprapun:\n"
                    f"• {self.activitati_fixe[i].nume} ({self.activitati_fixe[i].ora_fixa.strftime('%H:%M')}-{current_end.strftime('%H:%M')})\n"
                    f"• {self.activitati_fixe[i+1].nume} ({next_start.strftime('%H:%M')}-{(next_start + timedelta(minutes=self.activitati_fixe[i+1].durata)).strftime('%H:%M')})"
                )     
    
    #pt antrenare model cu date initiale
    def _train_initial_model(self):
        initial_data = [
            (30, 5, 3, 0.8),
            (60, 3, 2, 0.6),
            (15, 8, 1, 0.9),
            (45, 6, 4, 0.7)
        ]
        for durata, prioritate, nr_ramase, scor in initial_data:
            self.model.add_training_data(durata, prioritate, nr_ramase, scor)

    #pt euristica ac. flexibile
    def _compute_ml_heuristic(self, activitate, remaining_acts):

        #generez o cheie pt a nu repeta calculele 
        #calculeaza scoruri
        cache_key = (activitate.durata, activitate.prioritate, len(remaining_acts))
        
        if cache_key in self._pred_cache:
            return self._pred_cache[cache_key]
        
        durata = activitate.durata
        prioritate = activitate.prioritate
        nr_ramase = len(remaining_acts)
        #apelez ML pt a genera scorul
        scor = self.model.predict(durata, prioritate, nr_ramase)
        #pun accent pe prioritate
        self._pred_cache[cache_key] = scor * (1 + (prioritate/10))
        return self._pred_cache[cache_key]

    #pt activitati fixe
    def _planifica_activitati_fixe(self, today, end_time):

        #sortez activitatile fixe
        self.activitati_fixe.sort(key=lambda x: x.ora_fixa)
        fixed_activities = []
        
        for act in self.activitati_fixe:
            act.ora_fixa = datetime.combine(today, act.ora_fixa.time())
            start = act.ora_fixa
            end = start + timedelta(minutes=act.durata)
            
            if end > end_time:
                raise ValueError(f"Activitatea fixă '{act.nume}' depășește ora limită!")
                
            fixed_activities.append((act.nume, start, end))
        
        return fixed_activities

    #pt a cauta intervale de timp libere
    def _gaseste_intervale_libere(self, fixed_activities, start_time, end_time):
        free_intervals = []
        current_time = start_time
        buffer = timedelta(minutes=10) #pt a nu supraaglomera

        #verific daca exista timp liber inainte de prima activitate
        if fixed_activities and current_time < fixed_activities[0][1]:
            free_intervals.append((current_time, fixed_activities[0][1]))
        
        #parcurg ac. in perechi
        for i in range(len(fixed_activities)-1):
            current_end = fixed_activities[i][2] + buffer
            next_start = fixed_activities[i+1][1]
            
            #daca gasesc timp liber, il salvez in lista
            if current_end < next_start:
                free_intervals.append((current_end, next_start))
        
        #verific daca e timp liber dupa ultima activitate
        if fixed_activities:
            last_end = fixed_activities[-1][2] + buffer
            if last_end < end_time:
                free_intervals.append((last_end, end_time))
        elif current_time < end_time:  
            free_intervals.append((current_time, end_time))
        
        return free_intervals
    
    #pt a planifica ac. flexibile
    def _planifica_activitati_flexibile(self, flex_activities, free_intervals, end_time):
        flexible_schedule = []
        remaining_flex = flex_activities.copy()  #creez o copie pt a putea elimina ac.
        
        #sortez intervalele libere desc
        free_intervals.sort(key=lambda x: x[1] - x[0], reverse=True)
        
        #sortez ac. descresc dupa scor
        remaining_flex.sort(key=lambda a: -self._compute_ml_heuristic(a, remaining_flex))
        
        for interval_start, interval_end in free_intervals:
            interval_duration = (interval_end - interval_start).total_seconds() / 60 #tr in minute
            scheduled_in_interval = []
            
            for act in remaining_flex[:]:  
                act_duration = act.durata
                
                if act_duration <= interval_duration:
                    end_time_act = interval_start + timedelta(minutes=act_duration)
                    
                    #daca ac. incape in intervalul liber, il salvez 
                    scheduled_in_interval.append((act, interval_start, end_time_act))
                    
                    #calculez durata ramasa in interval
                    interval_start = end_time_act + timedelta(minutes=10)
                    interval_duration = (interval_end - interval_start).total_seconds() / 60
                    
                    remaining_flex.remove(act)
            
            #adaug ac. la lista finala
            flexible_schedule.extend([(a[0].nume, a[1], a[2]) for a in scheduled_in_interval])
        
        return flexible_schedule, remaining_flex

    #pt a coordona procesul
    def planifica(self):
        try:

            #salvez start si end
            today = datetime.now().date()
            self.start_time = datetime.combine(today, self.start_time.time())
            end_time = datetime.combine(today, datetime.strptime("23:59", "%H:%M").time())
            
            #salvez ac. fixe
            fixed_activities = self._planifica_activitati_fixe(today, end_time)
            
            #salvez intervale libere
            free_intervals = self._gaseste_intervale_libere(fixed_activities, self.start_time, end_time)
            
            #salvez ac. flexibile sortate dupa scor
            flex_activities = sorted(
                self.activitati_flex,
                key=lambda a: -self._compute_ml_heuristic(a, self.activitati_flex)
            )
            
            #salvez lista finala de ac. flexibile
            flexible_schedule, remaining_flex = self._planifica_activitati_flexibile(
                flex_activities, free_intervals, end_time)
            
            #imbin cele doua liste
            full_schedule = fixed_activities + flexible_schedule
            #sortez tot dupa ora de inceputr
            full_schedule.sort(key=lambda x: x[1])
            
            result = []
            #formatare
            for act in full_schedule:
                result.append(f"{act[1].strftime('%H:%M')} - {act[2].strftime('%H:%M')} | {act[0]}")
            
            if remaining_flex:
                result.append("\n⚠️ ACTIVITĂȚI NEPLANIFICATE:")
                for act in remaining_flex:
                    result.append(f"- {act.nume} (durata: {act.durata} min, prioritate: {act.prioritate})")
            
            return result if result else ["Nu există activități planificate."]
            
        except Exception as e:
            error_msg = f"Eroare la planificare: {str(e)}"
            messagebox.showerror("Eroare", error_msg)
            return [error_msg]