import csv
import re
import dns.resolver

CSV_ENTREE = "test_candidatures.csv"
CSV_SORTIE = "candidatures_propres.csv"

def verifier_email(email):
    email = email.strip()
    
    # 1. Vérification de la syntaxe de base
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(regex, email):
        return False, "Syntaxe invalide"
    
    # 2. Vérification du nom de domaine (Enregistrement MX)
    domaine = email.split('@')[1]
    try:
        # On demande au réseau si ce domaine peut recevoir des mails
        dns.resolver.resolve(domaine, 'MX')
        return True, "OK"
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False, "Domaine mort ou invalide"
    except Exception as e:
        return False, f"Erreur: {e}"

print("🔍 Début du nettoyage du fichier CSV...\n")

mails_valides = 0
mails_invalides = 0

# On ouvre le fichier d'origine en lecture, et le nouveau en écriture
with open(CSV_ENTREE, mode='r', encoding='utf-8') as f_in, \
     open(CSV_SORTIE, mode='w', encoding='utf-8', newline='') as f_out:
    
    reader = csv.DictReader(f_in, delimiter=';')
    
    # On prépare le nouveau fichier avec une colonne supplémentaire "Statut"
    champs = reader.fieldnames + ["Statut_Verification"]
    writer = csv.DictWriter(f_out, fieldnames=champs, delimiter=';')
    writer.writeheader()
    
    for row in reader:
        email = row['Mail']
        
        # Si la case mail est vide
        if not email:
            row['Statut_Verification'] = "Vide"
            mails_invalides += 1
            writer.writerow(row)
            continue
            
        # Test de l'email
        est_valide, message = verifier_email(email)
        row['Statut_Verification'] = message
        
        if est_valide:
            print(f"✅ {email} -> {message}")
            mails_valides += 1
            writer.writerow(row) # On garde cette ligne
        else:
            print(f"❌ {email} -> {message} (RETIRÉ)")
            mails_invalides += 1
            # Tu peux choisir de l'écrire ou non dans le fichier final.
            # Là, on l'écrit avec le message d'erreur pour que tu puisses vérifier.
            writer.writerow(row)

print("\n📊 Bilan du nettoyage :")
print(f"Emails valides (Domaine OK) : {mails_valides}")
print(f"Emails invalides/morts : {mails_invalides}")
print(f"\n✅ Le nouveau fichier nettoyé a été créé sous le nom : {CSV_SORTIE}")