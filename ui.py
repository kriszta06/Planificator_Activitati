from datetime import datetime
import tkinter as tk
from planner import Activitate, PlanificatorAStar, incarca_activitati, salveaza_activitati
import os
import tkinter.messagebox as messagebox
from planner_m1 import ActivityModel 

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificator Avansat")

        os.makedirs("data", exist_ok=True)

        self.activitati = incarca_activitati()
        print(f"Activități încărcate: {[a.nume for a in self.activitati]}")
        self.model = ActivityModel() 

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        labels = ["Nume", "Durată (min)", "Prioritate (1-mică, 10-mare)", "Oră fixă (HH:MM)"]
        self.entries = []
        
        for i, label in enumerate(labels):
            tk.Label(self.main_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(self.main_frame)
            entry.grid(row=i, column=1, pady=2)
            self.entries.append(entry)

        self.is_fixed_var = tk.BooleanVar()
        self.fixed_check = tk.Checkbutton(
            self.main_frame, 
            text="Activitate cu oră fixă",
            variable=self.is_fixed_var,
            command=self.toggle_fixed_time
        )
        self.fixed_check.grid(row=len(labels), column=0, columnspan=2, pady=5)
 
        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="Adaugă", command=self.adauga).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Planifică", command=self.afiseaza).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Șterge tot", command=self.sterge_tot).pack(side=tk.LEFT, padx=5)

        self.lista_activitati = tk.Listbox(self.root, width=50, height=10)
        self.lista_activitati.pack(pady=10)

        btn_sterge = tk.Button(self.root, text="Șterge activitatea selectată", command=self.sterge_activitate)
        btn_sterge.pack(pady=5)

        self.output = tk.Text(self.main_frame, height=15, width=50, wrap=tk.WORD)
        self.output.grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

        self.entries[3].config(state=tk.DISABLED)
        
        self.actualizeaza_lista_activitati()

        self.feedback_frame = tk.Frame(self.root)
        self.feedback_frame.pack(pady=5)
        
        tk.Label(self.feedback_frame, text="Cât de bună e planificarea?").pack(side=tk.LEFT)
        self.rating_var = tk.IntVar(value=3)  
        for i in range(1, 6):
            tk.Radiobutton(self.feedback_frame, text=str(i), variable=self.rating_var, value=i).pack(side=tk.LEFT)  # .pack() corectat
        
        tk.Button(self.feedback_frame, text="Trimite feedback", command=self.salveaza_feedback).pack(side=tk.LEFT, padx=5)

    #camp pt activare/dezactivare ora fixa
    def toggle_fixed_time(self):
        if self.is_fixed_var.get():
            self.entries[3].config(state=tk.NORMAL)
        else:
            self.entries[3].config(state=tk.DISABLED)
            self.entries[3].delete(0, tk.END)

    #preluare date din campuri
    def adauga(self):
        nume = self.entries[0].get()
        durata = self.entries[1].get()
        prioritate = self.entries[2].get()
        ora_fixa_str = self.entries[3].get() if self.is_fixed_var.get() else None
        
        #verificare corectitudine date
        if not nume:
            messagebox.showerror("Eroare", "Te rog completează numele activității!")
            return
        
        if not durata.isdigit() or int(durata) <= 0:
            messagebox.showerror("Eroare", "Durata trebuie să fie un număr întreg pozitiv (minute)!")
            return
        
        if not prioritate.isdigit() or int(prioritate) <= 0:
            messagebox.showerror("Eroare", "Prioritatea trebuie să fie un număr întreg pozitiv!")
            return
        
        ora_fixa = None
        if ora_fixa_str:
            try:
                ora_fixa = datetime.strptime(ora_fixa_str, "%H:%M")
            except ValueError:
                messagebox.showerror("Eroare", "Format orei invalid! Te rog folosește HH:MM")
                return
        
        #se creaza obiect
        act = Activitate(
            nume=nume,
            durata=int(durata),
            prioritate=int(prioritate),
            ora_fixa=ora_fixa
        )
        #se adauga la lista activitatilor
        self.activitati.append(act)
        salveaza_activitati(self.activitati)

        #resetare campuri
        for e in self.entries:
            e.delete(0, tk.END)
        self.is_fixed_var.set(False)
        self.entries[3].config(state=tk.DISABLED)

        #se actualizeaza lista afisata
        self.actualizeaza_lista_activitati()

    #afisare activitati
    def afiseaza(self):
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)

        if not self.activitati:
            self.output.insert(tk.END, "Nu există activități de planificat!")
            self.output.config(state='disabled')
            return

        try:
            #se creaza obiect PlanificatorAStar cu lista de activitati
            planificator = PlanificatorAStar(self.activitati)
            #obtinere ordine optima
            program = planificator.planifica()
            #afisare lista
            if program is None:
                raise ValueError("Planificatorul a returnat None")
            self.output.insert(tk.END, "PROGRAMUL ZILEI:\n\n")
            for linie in program:
                self.output.insert(tk.END, linie + "\n")

        except Exception as e:
            messagebox.showerror("Eroare de planificare", str(e))
            self.output.insert(tk.END, f"Eroare: {str(e)}")

        self.output.config(state='disabled')

    #stergere activitati
    def sterge_tot(self):
        
        #fereastra de confirmare
        if messagebox.askyesno("Confirmare", "Sigur vrei să ștergi toate activitățile?"):
            self.activitati.clear()
            salveaza_activitati(self.activitati)
            self.output.delete(1.0, tk.END)
            self.actualizeaza_lista_activitati()

    #actualizare lista
    def actualizeaza_lista_activitati(self):
        self.lista_activitati.delete(0, tk.END)
        for act in self.activitati:
            text = f"{act.nume} | Durata: {act.durata} min | Prioritate: {act.prioritate}"
            if act.ora_fixa:
                text += f" | Ora fixă: {act.ora_fixa.strftime('%H:%M')}"
            self.lista_activitati.insert(tk.END, text)

    #stergere o singura activitate
    def sterge_activitate(self):
        selectie = self.lista_activitati.curselection()
        if not selectie:
            messagebox.showwarning("Avertisment", "Selectează o activitate pentru a o șterge.")
            return

        index = selectie[0]
        activitate_stearsa = self.activitati.pop(index)
        salveaza_activitati(self.activitati)
        self.actualizeaza_lista_activitati()

        messagebox.showinfo("Șters", f"Activitatea '{activitate_stearsa.nume}' a fost ștearsă.")

    #trimitere feedback
    def salveaza_feedback(self):
        rating = self.rating_var.get()
        if not rating: 
            messagebox.showwarning("Avertisment", "Vă rugăm să selectați un rating!")
            return
 
        normalized_score = (rating - 1) / 4.0

        #extragere nume activitati
        planned_activities = [linie.split("|")[1].strip() 
                            for linie in self.output.get("1.0", tk.END).strip().split("\n") 
                            if "|" in linie]
        
        #se calculeaza cate activitati au ramas neplanificate si se trimit datele spre antrenare
        for act in self.activitati:
            if act.nume in planned_activities:
                remaining = len([a for a in self.activitati if a.nume not in planned_activities])
                self.model.add_training_data(
                    durata=act.durata,
                    prioritate=act.prioritate,
                    nr_ramase=remaining,
                    scor=normalized_score
                )
            else:
                pass
        
        messagebox.showinfo("Mulțumim", "Feedback-ul a fost înregistrat!")