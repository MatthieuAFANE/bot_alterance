import smtplib
import csv
import time
import random
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURATION DES COMPTES ---
ACCOUNTS = [
    {
        "email": "matthieuafane@gmail.com",
        "password": "yzaalcundihumnuo"
    },
    {
        "email": "matthieu.afane1@gmail.com",
        "password": "gbgvalygvmwcywvj"
    }
]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CSV_FILE = "candidatures_propres.csv"
CV_FILE = "CV Matthieu AFANE.pdf"

def send_email(row, account):
    sender_email = account["email"]
    password = account["password"]
    
    try:
        entreprise = row['Nom entreprise']
        tuteur = row['Tuteur'].strip() if row['Tuteur'].strip() else "Madame, Monsieur"
        destinataire = row['Mail']
        sujet_ancien_stage = row['Sujet du stage']

        if not destinataire or "@" not in destinataire:
            return False

        # Création du message
        msg = MIMEMultipart()
        msg['From'] = f"Matthieu Afane <{sender_email}>"
        msg['To'] = destinataire
        msg['Subject'] = f"Candidature Alternance IT (BUT 3) - {entreprise}"

        # Ton texte personnalisé
        body = f"""Bonjour {tuteur},

Je me permets de vous adresser ma candidature spontanée en vue d'intégrer {entreprise} dans le cadre d'une alternance pour l'année scolaire 2026-2027, avec une prise de poste commençant entre septembre et début octobre 2026.

Actuellement étudiant en 2e année de BUT Informatique à l'IUT de Reims, je prépare désormais l'obtention de mon diplôme de 3e année.

Pour vous donner un aperçu de mon profil, je viens de terminer mon stage à la Direction des Systèmes d'Information (DSI) de Châlons-en-Champagne. J'ai eu l'opportunité d'y concevoir de A à Z un outil d'audit web basé sur les normes d'accessibilité (RGAA 4.1), en implémentant notamment des modèles d'Intelligence Artificielle pour automatiser les analyses.

Sachant que vous faites régulièrement confiance aux étudiants de notre IUT (notamment récemment sur des missions portant sur : {sujet_ancien_stage}), je suis convaincu que mes compétences techniques et mon autonomie pourraient vous intéresser.

Vous trouverez ci-joint mon CV détaillant mes premières expériences. Pour un aperçu plus visuel de mes projets scolaires et personnels, je vous invite également à consulter mon portfolio.

Je reste à votre entière disposition pour convenir d'un entretien afin d'échanger sur mes motivations.

Dans l'attente de votre retour, je vous prie d'agréer l'expression de mes salutations distinguées.

Cordialement,

Matthieu Afane
=> Portfolio : https://matthieuafane.free.nf/
07 71 83 21 41
{sender_email}"""

        msg.attach(MIMEText(body, 'plain'))

        # Pièce jointe CV
        with open(CV_FILE, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=\"{CV_FILE}\"")
            msg.attach(part)

        # Envoi
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, destinataire, msg.as_string())
        server.quit()

        print(f"✅ Envoyé via {sender_email} -> {entreprise}")
        return True

    except Exception as e:
        print(f"❌ Erreur avec {sender_email} pour {entreprise} : {e}")
        return False
# --- LANCEMENT DU SCRIPT ---
print("🚀 Démarrage de la campagne de candidatures...\n")

MAX_ENVOIS_JOUR = 40 # Sécurité anti-spam Google
compteur_envois = 0

with open(CSV_FILE, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    account_index = 0
    
    for row in reader:
        # COUPE-CIRCUIT DE SÉCURITÉ
        if compteur_envois >= MAX_ENVOIS_JOUR:
            print("\n🛑 LIMITE QUOTIDIENNE ATTEINTE ! Le script s'arrête pour protéger tes comptes Google.")
            print("Pense à supprimer les lignes déjà envoyées de ton CSV pour demain.")
            break

        current_account = ACCOUNTS[account_index % len(ACCOUNTS)]
        success = send_email(row, current_account)
        
        if success:
            account_index += 1
            compteur_envois += 1 # On ajoute +1 au compteur
            
            wait_time = random.randint(60, 150)
            
            for remaining in range(wait_time, 0, -1):
                print(f"\r⏳ Prochain envoi dans : {remaining:02d} secondes... (Envois aujourd'hui : {compteur_envois}/{MAX_ENVOIS_JOUR})", end="", flush=True)
                time.sleep(1)
            
            print("\r" + " " * 80 + "\r", end="")

print("\n✨ Fin du programme.")