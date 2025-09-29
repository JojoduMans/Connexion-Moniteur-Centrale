#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guide de Diagnostic Réseau pour Central d'Interphonie (CI) - Port 24005
Classe de diagnostic pour utilisation en ligne de commande ou avec Streamlit
"""

import json
from datetime import datetime

class GuideDiagnosticCI:
    """Classe principale pour le diagnostic réseau CI."""
    
    def __init__(self):
        self.historique_parcours = []
        self.recommandations_finales = []
        self.CI_PORT = 24005
        
    def log_etape(self, etape, reponse, action_recommandee=""):
        """Enregistre chaque étape du parcours diagnostic."""
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "etape": etape,
            "reponse": reponse,
            "action": action_recommandee
        }
        self.historique_parcours.append(entry)
    
    def afficher_titre(self, titre):
        """Affiche un titre formaté."""
        print("\n" + "="*70)
        print(f"🔍 {titre}")
        print("="*70)
    
    def afficher_action(self, action, details="", urgent=False):
        """Affiche une action recommandée."""
        icone = "🚨" if urgent else "👉"
        print(f"\n{icone} ACTION RECOMMANDÉE:")
        print(f"   {action}")
        if details:
            print(f"   📋 Détails: {details}")
    
    def afficher_wireshark_guide(self, contexte):
        """Affiche les filtres Wireshark selon le contexte."""
        guides = {
            "connexion_tcp": {
                "titre": "ANALYSE CONNEXION TCP CI",
                "filtres": [
                    ("Connexions CI", f"tcp.port == {self.CI_PORT}"),
                    ("Handshake TCP", f"tcp.port == {self.CI_PORT} and (tcp.flags.syn == 1 or tcp.flags.ack == 1)"),
                    ("Connexions refusées", f"tcp.port == {self.CI_PORT} and tcp.flags.reset == 1"),
                    ("Timeouts", "tcp.analysis.retransmission or tcp.analysis.fast_retransmission")
                ]
            },
            "multicast": {
                "titre": "ANALYSE TRAFIC MULTICAST",
                "filtres": [
                    ("Multicast général", "ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255"),
                    ("IGMP", "igmp"),
                    ("Découverte CI", "udp and ip.dst >= 224.0.0.0"),
                    ("Annonces périodiques", "udp.srcport == 67 or udp.dstport == 67")
                ]
            },
            "qos": {
                "titre": "ANALYSE QoS ET DSCP",
                "filtres": [
                    ("Marquage DSCP", "ip.dsfield.dscp != 0"),
                    ("Trafic prioritaire", "ip.dsfield.dscp >= 32"),
                    ("Paquets droppés", "icmp.type == 11 or icmp.type == 3"),
                    ("Congestion", "tcp.analysis.window_full")
                ]
            }
        }
        
        if contexte in guides:
            guide = guides[contexte]
            print(f"\n🔬 {guide['titre']}")
            print("-" * 50)
            for nom, filtre in guide['filtres']:
                print(f"📌 {nom}:")
                print(f"   {filtre}")
    
    def poser_question(self, question, options=None):
        """Pose une question avec validation de réponse."""
        if options is None:
            options = ["OUI", "NON"]
        
        while True:
            reponse = input(f"\n❓ {question} ({'/'.join(options)}): ").upper().strip()
            if reponse in options:
                return reponse
            print(f"⚠️  Réponse invalide. Choisissez parmi: {', '.join(options)}")
    
    def get_ci_port(self):
        """Retourne le numéro de port CI."""
        return self.CI_PORT
    
    def get_historique(self):
        """Retourne l'historique du parcours diagnostic."""
        return self.historique_parcours
    
    def exporter_rapport(self, filename=None):
        """Exporte le rapport de diagnostic en JSON."""
        if filename is None:
            filename = f"diagnostic_ci_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            rapport = {
                "diagnostic_ci": {
                    "port": self.CI_PORT,
                    "timestamp": datetime.now().isoformat(),
                    "parcours": self.historique_parcours,
                    "recommandations": self.recommandations_finales
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Rapport sauvegardé: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return None


def main():
    """Fonction principale pour utilisation en ligne de commande."""
    print("🔧 GUIDE DE DIAGNOSTIC RÉSEAU - CENTRAL D'INTERPHONIE (CI)")
    print("="*70)
    print("Cette classe est conçue pour être utilisée avec l'interface Streamlit")
    print("Lancez 'streamlit run app.py' pour l'interface graphique")
    print("="*70)

if __name__ == "__main__":
    main()
