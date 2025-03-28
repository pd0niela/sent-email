# Aplicație Client Email în Terminal

## Descriere
Această aplicație permite gestionarea email-urilor Gmail prin intermediul unei interfețe simple în terminal. Aplicația implementează protocoalele POP3, IMAP și SMTP pentru a permite:
- Afișarea email-urilor din cutia poștală
- Vizualizarea conținutului email-urilor
- Descărcarea atașamentelor
- Trimiterea email-urilor cu și fără atașamente


## Instalare
1. Asigurați-vă că aveți Python instalat pe computerul dvs.
2. Salvați codul sursă într-un fișier numit `email_client.py`
3. Nu este nevoie de instalarea unor biblioteci suplimentare deoarece aplicația folosește doar biblioteci standard Python.

## Configurare Gmail

### Activarea accesului POP3 în Gmail
1. Conectați-vă la contul dvs. Gmail în browser
2. Accesați setările Gmail (pictograma ⚙️ din colțul din dreapta sus)
3. Selectați "Vezi toate setările"
4. Accesați tab-ul "Redirecționare și POP/IMAP"
5. Găsiți secțiunea "Descărcare POP" și selectați "Activează POP pentru toate mesajele" sau "Activează POP pentru mesajele care sosesc de acum înainte"
6. Salvați modificările

### Crearea unei parole de aplicație (necesar pentru autentificare)
1. Activați verificarea în doi pași pentru contul dvs. Gmail:
   - Accesați https://myaccount.google.com/security
   - Găsiți secțiunea "Verificare în 2 pași" și activați-o
2. Generați o parolă de aplicație:
   - Accesați https://myaccount.google.com/apppasswords
   - Selectați aplicația: "Alt" (sau "Other") și denumiți-o (ex. "Client Email Python")
   - Apăsați "Generare"
   - Google va afișa o parolă de 16 caractere - copiați această parolă
3. Folosiți această parolă de aplicație când vă conectați prin aplicația client email

## Utilizare

### Rulare aplicație
```
python email_client.py
```

### Meniu principal
Aplicația prezintă un meniu cu următoarele opțiuni:
1. Listare email-uri prin POP3
2. Listare email-uri prin IMAP
3. Trimite email text simplu
4. Trimite email cu atașament
5. Ieșire

### 1. Listarea email-urilor prin POP3
- Afișează ultimele 10 email-uri din cutia poștală
- Puteți selecta un email pentru vizualizare prin introducerea ID-ului acestuia
- Pentru a reveni la meniu, introduceți 'q'

### 2. Listarea email-urilor prin IMAP
- Afișează ultimele 10 email-uri din inbox
- Puteți selecta un email pentru vizualizare prin introducerea numărului acestuia
- Pentru a reveni la meniu, introduceți 'q'

### 3. Trimiterea unui email text simplu
- Introduceți adresa destinatarului și subiectul
- Introduceți corpul email-ului (terminați cu o linie care conține doar '.')
- Email-ul va fi trimis automat

### 4. Trimiterea unui email cu atașament
- Introduceți adresa destinatarului și subiectul
- Introduceți corpul email-ului (terminați cu o linie care conține doar '.')
- Adăugați unul sau mai multe atașamente prin introducerea căii fișierului
- Pentru a termina adăugarea atașamentelor, introduceți 'gata'
- Email-ul va fi trimis automat
