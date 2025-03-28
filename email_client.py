import poplib
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import getpass
import sys

class EmailClient:
    def __init__(self):
        self.email = None
        self.password = None
        self.pop_connection = None
        self.imap_connection = None
        
    def login(self):
        """Cere utilizatorului să introducă credențialele de Gmail"""
        print("\n==== Autentificare Gmail ====")
        self.email = input("Adresa de Gmail: ")
        self.password = getpass.getpass("Parola: ")
        print()
        
    def menu(self):
        """Afișează meniul principal"""
        while True:
            print("\n==== Client Email Gmail ====")
            print("1. Listare email-uri prin POP3")
            print("2. Listare email-uri prin IMAP")
            print("3. Trimite email text simplu")
            print("4. Trimite email cu atașament")
            print("5. Ieșire")
            
            choice = input("\nAlegeți o opțiune (1-5): ")
            
            if choice == '1':
                self.list_emails_pop3()
            elif choice == '2':
                self.list_emails_imap()
            elif choice == '3':
                self.send_text_email()
            elif choice == '4':
                self.send_email_with_attachment()
            elif choice == '5':
                print("La revedere!")
                sys.exit(0)
            else:
                print("Opțiune invalidă. Încercați din nou.")
    
    def list_emails_pop3(self):
        """Listează email-urile folosind protocolul POP3"""
        try:
            print("\n==== Listare email-uri prin POP3 ====")
            print("Conectare la serverul POP3...")
            
            # Conectare la Gmail POP3
            self.pop_connection = poplib.POP3_SSL('pop.gmail.com', 995)
            self.pop_connection.user(self.email)
            self.pop_connection.pass_(self.password)
            
            # Obține statistici
            num_messages, total_size = self.pop_connection.stat()
            print(f"Conectat cu succes. {num_messages} email-uri în inbox.")
            
            # Listare ultimele 10 email-uri (sau toate dacă sunt mai puține)
            num_to_show = min(num_messages, 10)
            emails = []
            
            for i in range(num_messages, num_messages - num_to_show, -1):
                try:
                    resp, lines, octets = self.pop_connection.retr(i)
                    msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                    msg = email.message_from_string(msg_content)
                    
                    from_addr = self.decode_header_text(msg['From'])
                    subject = self.decode_header_text(msg['Subject'])
                    date = msg['Date']
                    
                    emails.append({
                        'id': i,
                        'from': from_addr,
                        'subject': subject,
                        'date': date
                    })
                except Exception as e:
                    print(f"Eroare la citirea email-ului {i}: {e}")
            
            # Afișare email-uri
            if emails:
                print("\nEmail-uri recente:")
                print(f"{'ID':<5}{'De la':<40}{'Subiect':<40}{'Data':<20}")
                print('-' * 100)
                
                for email_item in emails:
                    print(f"{email_item['id']:<5}{email_item['from'][:38]:<40}{email_item['subject'][:38]:<40}{email_item['date'][:18]:<20}")
                
                # Opțiuni suplimentare
                while True:
                    choice = input("\nIntroduceți ID-ul pentru a vedea email-ul sau 'q' pentru a reveni la meniu: ")
                    if choice.lower() == 'q':
                        break
                    
                    try:
                        email_id = int(choice)
                        self.view_pop3_email(email_id)
                    except ValueError:
                        print("Introduceți un ID valid sau 'q'.")
            else:
                print("Nu există email-uri de afișat.")
                
            # Închidere conexiune
            self.pop_connection.quit()
            
        except Exception as e:
            print(f"Eroare la conexiunea POP3: {e}")
    
    def list_emails_imap(self):
        """Listează email-urile folosind protocolul IMAP"""
        try:
            print("\n==== Listare email-uri prin IMAP ====")
            print("Conectare la serverul IMAP...")
            
            # Conectare la Gmail IMAP
            self.imap_connection = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            self.imap_connection.login(self.email, self.password)
            
            # Selectare inbox
            self.imap_connection.select('INBOX')
            
            # Căutare email-uri
            status, message_ids = self.imap_connection.search(None, 'ALL')
            email_ids = message_ids[0].split()
            
            # Numărul de email-uri
            num_messages = len(email_ids)
            print(f"Conectat cu succes. {num_messages} email-uri în inbox.")
            
            # Listare ultimele 10 email-uri (sau toate dacă sunt mai puține)
            num_to_show = min(num_messages, 10)
            emails = []
            
            for i in range(num_messages - 1, num_messages - num_to_show - 1, -1):
                if i < 0:
                    break
                    
                email_id = email_ids[i]
                
                try:
                    status, msg_data = self.imap_connection.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    from_addr = self.decode_header_text(msg['From'])
                    subject = self.decode_header_text(msg['Subject'])
                    date = msg['Date']
                    
                    emails.append({
                        'id': email_id.decode(),
                        'from': from_addr,
                        'subject': subject,
                        'date': date,
                        'msg': msg
                    })
                except Exception as e:
                    print(f"Eroare la citirea email-ului {email_id}: {e}")
            
            # Afișare email-uri
            if emails:
                print("\nEmail-uri recente:")
                print(f"{'ID':<5}{'De la':<40}{'Subiect':<40}{'Data':<20}")
                print('-' * 100)
                
                for i, email_item in enumerate(emails, 1):
                    print(f"{i:<5}{email_item['from'][:38]:<40}{email_item['subject'][:38]:<40}{email_item['date'][:18]:<20}")
                
                # Opțiuni suplimentare
                while True:
                    choice = input("\nIntroduceți numărul pentru a vedea email-ul sau 'q' pentru a reveni la meniu: ")
                    if choice.lower() == 'q':
                        break
                    
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(emails):
                            self.view_imap_email(emails[idx]['msg'])
                        else:
                            print("Număr invalid.")
                    except ValueError:
                        print("Introduceți un număr valid sau 'q'.")
            else:
                print("Nu există email-uri de afișat.")
            
            # Închidere conexiune
            self.imap_connection.close()
            self.imap_connection.logout()
            
        except Exception as e:
            print(f"Eroare la conexiunea IMAP: {e}")
    
    def view_pop3_email(self, msg_num):
        """Vizualizează conținutul unui email prin POP3"""
        try:
            # Obține email-ul
            resp, lines, octets = self.pop_connection.retr(msg_num)
            msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
            msg = email.message_from_string(msg_content)
            
            # Afișare email
            self.display_email(msg)
            
        except Exception as e:
            print(f"Eroare la citirea email-ului: {e}")
    
    def view_imap_email(self, msg):
        """Vizualizează conținutul unui email prin IMAP"""
        try:
            # Afișare email
            self.display_email(msg)
            
        except Exception as e:
            print(f"Eroare la afișarea email-ului: {e}")
    
    def display_email(self, msg):
        """Afișează conținutul unui email"""
        print("\n" + "=" * 80)
        print(f"De la:    {self.decode_header_text(msg['From'])}")
        print(f"Către:    {self.decode_header_text(msg['To'])}")
        print(f"Subiect:  {self.decode_header_text(msg['Subject'])}")
        print(f"Data:     {msg['Date']}")
        print("=" * 80)
        
        # Obține corpul email-ului
        body = ""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Conținut text
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode(errors="replace")
                    except:
                        body = "Nu se poate decoda corpul mesajului"
                
                # Atașamente
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append((filename, part))
        else:
            # Dacă nu este multipart
            try:
                body = msg.get_payload(decode=True).decode(errors="replace")
            except:
                body = "Nu se poate decoda corpul mesajului"
        
        # Afișare corp email
        print("\nConținut email:")
        print("-" * 80)
        print(body)
        print("-" * 80)
        
        # Afișare atașamente
        if attachments:
            print(f"\nAtașamente ({len(attachments)}):")
            for i, (filename, _) in enumerate(attachments, 1):
                print(f"{i}. {filename}")
            
            # Opțiune pentru descărcare atașamente
            save_option = input("\nDoriți să salvați atașamentele? (d/n): ")
            if save_option.lower() == 'd':
                save_dir = input("Introduceți calea directorului de salvare (sau apăsați Enter pentru directorul curent): ")
                if not save_dir:
                    save_dir = os.getcwd()
                
                for filename, part in attachments:
                    filepath = os.path.join(save_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                print(f"Atașamentele au fost salvate în {save_dir}")
        
        input("\nApăsați Enter pentru a continua...")
    
    def send_text_email(self):
        """Trimite un email doar cu text"""
        print("\n==== Trimitere email text ====")
        
        to_address = input("Către: ")
        subject = input("Subiect: ")
        
        print("Introduceți corpul email-ului (terminați cu o linie care conține doar '.'): ")
        body_lines = []
        while True:
            line = input()
            if line == '.':
                break
            body_lines.append(line)
        
        body = "\n".join(body_lines)
        
        try:
            # Creare mesaj
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_address
            msg['Subject'] = subject
            
            # Adăugare corp text
            msg.attach(MIMEText(body, 'plain'))
            
            # Conectare la serverul SMTP
            print("Trimitere email...")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print("Email-ul a fost trimis cu succes!")
            
        except Exception as e:
            print(f"Eroare la trimiterea email-ului: {e}")
    
    def send_email_with_attachment(self):
        """Trimite un email cu atașamente"""
        print("\n==== Trimitere email cu atașament ====")
        
        to_address = input("Către: ")
        subject = input("Subiect: ")
        
        print("Introduceți corpul email-ului (terminați cu o linie care conține doar '.'): ")
        body_lines = []
        while True:
            line = input()
            if line == '.':
                break
            body_lines.append(line)
        
        body = "\n".join(body_lines)
        
        # Solicitare atașamente
        attachments = []
        print("\nAdăugare atașamente (introduceți calea completă a fișierului sau 'gata' pentru a termina):")
        
        while True:
            filepath = input("Calea fișierului: ")
            if filepath.lower() == 'gata':
                break
            
            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                attachments.append((filename, filepath))
                print(f"Adăugat: {filename}")
            else:
                print("Fișierul nu există. Încercați din nou.")
        
        try:
            # Creare mesaj
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_address
            msg['Subject'] = subject
            
            # Adăugare corp text
            msg.attach(MIMEText(body, 'plain'))
            
            # Adăugare atașamente
            for filename, filepath in attachments:
                with open(filepath, 'rb') as f:
                    attachment = MIMEApplication(f.read(), Name=filename)
                attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(attachment)
            
            # Conectare la serverul SMTP
            print("Trimitere email...")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print("Email-ul a fost trimis cu succes!")
            
        except Exception as e:
            print(f"Eroare la trimiterea email-ului: {e}")
    
    def decode_header_text(self, header):
        """Decodifică headerele email pentru a gestiona diferite codificări"""
        if header is None:
            return ""
        
        decoded_header = email.header.decode_header(header)
        header_parts = []
        
        for part, encoding in decoded_header:
            if isinstance(part, bytes):
                # Încearcă să decodifice cu codificarea furnizată
                if encoding:
                    try:
                        header_parts.append(part.decode(encoding))
                    except:
                        header_parts.append(part.decode('utf-8', errors='replace'))
                else:
                    header_parts.append(part.decode('utf-8', errors='replace'))
            else:
                header_parts.append(part)
        
        return ' '.join(header_parts)

def main():
    print("=== Client Email Gmail ===")
    print("Notă: Pentru Gmail, trebuie să activați 'Less secure app access' în setările contului")
    print("sau să folosiți o parolă de aplicație dacă aveți activată verificarea în 2 pași.")
    
    client = EmailClient()
    client.login()
    client.menu()

if __name__ == "__main__":
    main()