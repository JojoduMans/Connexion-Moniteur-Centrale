#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Streamlit pour le Guide de Diagnostic Réseau CI
"""

import streamlit as st
import json
from datetime import datetime
from diagnostic_ci import GuideDiagnosticCI

# Configuration de la page
st.set_page_config(
    page_title="Diagnostic Réseau CI",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .stAlert > div {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialiser_session():
    """Initialise les variables de session."""
    if 'diagnostic' not in st.session_state:
        st.session_state.diagnostic = GuideDiagnosticCI()
    if 'etape_actuelle' not in st.session_state:
        st.session_state.etape_actuelle = 0
    if 'donnees_collectees' not in st.session_state:
        st.session_state.donnees_collectees = {}

def afficher_entete():
    """Affiche l'en-tête de l'application."""
    st.title("🔧 Guide de Diagnostic Réseau - Centrale d'Interphonie (CI)")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Port CI", "24005", "TCP")
    with col2:
        st.metric("Étape actuelle", f"{st.session_state.etape_actuelle}/9")
    with col3:
        st.metric("Données collectées", len(st.session_state.donnees_collectees))
    
    st.markdown("---")
    
    # Avertissement important
    st.warning("⚠️ **LIMITATION IMPORTANTE** : Les moniteurs ne permettent PAS l'exécution de commandes réseau. Toutes les commandes sont à exécuter depuis la **centrale de surveillance**.")

def afficher_sidebar():
    """Affiche la barre latérale avec navigation."""
    with st.sidebar:
        st.header("📋 Navigation")
        
        etapes = [
            "0️⃣ Configuration Initiale",
            "1️⃣ Découverte LLDP",
            "2️⃣ Couche Physique",
            "3️⃣ Couche IP",
            "4️⃣ Connectivité",
            "5️⃣ Port CI (24005)",
            "6️⃣ Couche Applicative",
            "7️⃣ Trafic Multicast",
            "8️⃣ QoS et Priorisation"
        ]
        
        etape_selectionnee = st.radio(
            "Sélectionner une étape",
            range(len(etapes)),
            format_func=lambda x: etapes[x],
            key='etape_navigation'
        )
        
        st.session_state.etape_actuelle = etape_selectionnee
        
        st.markdown("---")
        
        # Résumé des données collectées
        if st.session_state.donnees_collectees:
            st.subheader("📊 Données collectées")
            for cle, valeur in st.session_state.donnees_collectees.items():
                st.text(f"{cle}: {valeur}")
        
        st.markdown("---")
        
        # Boutons d'action
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        if st.button("💾 Exporter rapport", use_container_width=True):
            exporter_rapport()

def etape_configuration_initiale():
    """Étape 0: Configuration initiale."""
    st.header("0️⃣ Configuration Initiale du Moniteur")
    
    st.info("Cette étape vérifie la configuration de base du moniteur avant le diagnostic réseau.")
    
    with st.expander("📋 Informations sur cette étape", expanded=True):
        st.markdown("""
        **Points vérifiés :**
        - Configuration du label ou port mapping
        - Assignation dans la centrale
        - Activation des fonctionnalités
        """)
    
    # Question 1: Label/Port mapping
    col1, col2 = st.columns(2)
    with col1:
        label_config = st.radio(
            "Avez-vous configuré un label sur le moniteur ou utilisez-vous le port mapping ?",
            ["Oui", "Non"],
            key="q_label_config"
        )
    
    if label_config == "Non":
        st.error("⚠️ **ACTION REQUISE:** Configuration du label nécessaire")
        with st.expander("📝 Détails de la correction"):
            st.markdown("""
            1. Configurer un label unique sur le moniteur
            2. OU activer le port mapping automatique
            3. Vérifier que le label ne conflit pas avec un autre équipement
            """)
        
        with col2:
            auto_mapping = st.radio(
                "Le port mapping automatique est-il activé sur la centrale ?",
                ["Oui", "Non"],
                key="q_auto_mapping"
            )
        
        if auto_mapping == "Non":
            st.error("Configuration nécessaire côté centrale pour la découverte automatique")
    
    # Question 2: Assignation
    assignation = st.radio(
        "Le moniteur est-il correctement assigné/déclaré dans l'application centrale ?",
        ["Oui", "Non"],
        key="q_assignation"
    )
    
    if assignation == "Non":
        st.error("⚠️ **ACTION REQUISE:** Assignation du moniteur dans la centrale")
        with st.expander("📝 Détails de la correction"):
            st.markdown("""
            1. Ajouter le moniteur dans l'interface de gestion
            2. Associer le bon label/adresse au moniteur
            3. Vérifier les droits/autorisations du moniteur
            4. Sauvegarder et appliquer la configuration
            """)
        
        statut = st.radio(
            "Le moniteur apparaît-il comme 'En ligne' dans l'interface de la centrale ?",
            ["Oui", "Non"],
            key="q_statut_interface"
        )
    
    # Question 3: Fonctionnalités
    fonctionnalites = st.radio(
        "Toutes les fonctionnalités du moniteur sont-elles activées (appel, diffusion, etc.) ?",
        ["Oui", "Non"],
        key="q_fonctionnalites"
    )
    
    if fonctionnalites == "Non":
        st.warning("Vérifier la configuration des fonctionnalités - Activer les services nécessaires")
    
    # Navigation
    if st.button("➡️ Étape suivante : Découverte LLDP", use_container_width=True):
        st.session_state.etape_actuelle = 1
        st.rerun()

def etape_lldp():
    """Étape 1: Découverte LLDP."""
    st.header("1️⃣ Découverte LLDP - Topologie Réseau")
    
    st.info("LLDP permet d'identifier la topologie réseau et la configuration du port switch.")
    
    with st.expander("🔍 Commandes LLDP utiles", expanded=False):
        st.code("""
# Vérifier LLDP sur le switch
show lldp neighbors
show lldp neighbors detail

# Activer LLDP (Cisco)
lldp run

# Informations du port
show lldp interface <interface>
        """, language="bash")
    
    # Question LLDP activé
    lldp_active = st.radio(
        "LLDP est-il activé sur le switch connecté au moniteur ?",
        ["Oui", "Non"],
        key="q_lldp_active"
    )
    
    if lldp_active == "Non":
        st.warning("⚠️ Activer LLDP sur le switch : `lldp run`")
    else:
        # Moniteur visible
        lldp_visible = st.radio(
            "Le moniteur est-il visible dans 'show lldp neighbors' sur le switch ?",
            ["Oui", "Non"],
            key="q_lldp_visible"
        )
        
        if lldp_visible == "Non":
            st.error("⚠️ Moniteur non découvert par LLDP")
            with st.expander("📝 Actions correctives"):
                st.markdown("""
                1. Vérifier que LLDP est activé sur le moniteur
                2. Contrôler la connectivité physique
                3. Attendre la synchronisation LLDP (30s-2min)
                4. Vérifier avec: `show lldp neighbors detail`
                """)
        else:
            # Collecte d'informations LLDP
            st.subheader("📋 Informations LLDP collectées")
            
            col1, col2 = st.columns(2)
            with col1:
                device_name = st.text_input("Nom/Hostname du moniteur", key="lldp_device")
                port_switch = st.text_input("Port switch connecté (ex: Gi0/1)", key="lldp_port")
            
            with col2:
                vlan_natif = st.text_input("VLAN natif du port", key="lldp_vlan")
                capabilities = st.text_input("Capabilities LLDP", key="lldp_cap")
            
            if device_name:
                st.session_state.donnees_collectees['LLDP Device'] = device_name
            if port_switch:
                st.session_state.donnees_collectees['Port Switch'] = port_switch
            if vlan_natif:
                st.session_state.donnees_collectees['VLAN'] = vlan_natif
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 0
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : Couche Physique", use_container_width=True):
            st.session_state.etape_actuelle = 2
            st.rerun()

def etape_physique():
    """Étape 2: Couche Physique."""
    st.header("2️⃣ Couche Physique - Connectivité de base")
    
    with st.expander("🔍 Commandes de vérification", expanded=False):
        st.code("""
# État de l'interface
show interface <interface> status
show interface <interface>

# Erreurs d'interface
show interface <interface> | include error

# Nettoyer les compteurs
clear counters <interface>
        """, language="bash")
    
    # Question Link
    link_up = st.radio(
        "Le moniteur est-il alimenté et le voyant Link est-il vert/actif ?",
        ["Oui", "Non"],
        key="q_link_up"
    )
    
    if link_up == "Non":
        st.error("⚠️ **PROBLÈME PHYSIQUE DÉTECTÉ**")
        with st.expander("📝 Actions correctives urgentes"):
            st.markdown("""
            1. Tester un autre câble réseau
            2. Changer de port sur le switch
            3. Vérifier l'alimentation du moniteur
            4. Contrôler les LEDs du switch
            5. Vérifier les informations LLDP si disponibles
            """)
    else:
        # Erreurs d'interface
        erreurs = st.radio(
            "Le device status du port switch indique-t-il des erreurs ?",
            ["Oui", "Non"],
            key="q_erreurs_interface"
        )
        
        if erreurs == "Oui":
            st.warning("Analyser les erreurs d'interface (CRC, collisions, runts)")
        
        # Vitesse du lien
        vitesse = st.radio(
            "Le link est-il à la bonne vitesse (100M/1G) ?",
            ["Oui", "Non"],
            key="q_vitesse"
        )
        
        if vitesse == "Non":
            st.warning("Problème de négociation de vitesse - Forcer speed/duplex si nécessaire")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 1
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : Couche IP", use_container_width=True):
            st.session_state.etape_actuelle = 3
            st.rerun()

def etape_ip():
    """Étape 3: Couche IP."""
    st.header("3️⃣ Couche Réseau (IP) - Configuration réseau")
    
    with st.expander("🔍 Commandes réseau", expanded=False):
        st.code("""
# DHCP
show ip dhcp binding
show ip dhcp lease

# ARP
show ip arp
arp -a

# Routing
show ip route
        """, language="bash")
    
    # Collecte IP moniteur
    st.subheader("📋 Informations réseau du moniteur")
    col1, col2 = st.columns(2)
    
    with col1:
        ip_moniteur = st.text_input("Adresse IP du moniteur", key="ip_moniteur")
        subnet = st.text_input("Sous-réseau (ex: 192.168.1.0/24)", key="subnet")
    
    with col2:
        gateway = st.text_input("Passerelle par défaut", key="gateway")
    
    if ip_moniteur:
        st.session_state.donnees_collectees['IP Moniteur'] = ip_moniteur
    if gateway:
        st.session_state.donnees_collectees['Gateway'] = gateway
    
    # Question IP valide
    ip_valide = st.radio(
        "Le moniteur a-t-il une adresse IP valide (pas 169.254.x.x) ?",
        ["Oui", "Non"],
        key="q_ip_valide"
    )
    
    if ip_valide == "Non":
        st.error("⚠️ **PROBLÈME D'ATTRIBUTION IP**")
        with st.expander("📝 Actions correctives"):
            st.markdown("""
            1. Vérifier le serveur DHCP: `show ip dhcp binding`
            2. Contrôler la configuration IP statique du moniteur
            3. Vérifier les VLANs: `show vlan brief`
            4. Tester depuis un autre device sur le même segment
            """)
    else:
        # Test passerelle
        ping_gw = st.radio(
            "Le moniteur peut-il pinger sa passerelle par défaut ?",
            ["Oui", "Non"],
            key="q_ping_gw"
        )
        
        if ping_gw == "Non":
            st.error("⚠️ **PROBLÈME DE PASSERELLE**")
            with st.expander("📝 Diagnostic passerelle"):
                st.markdown("""
                1. Vérifier la table de routage: `show ip route`
                2. Contrôler les VLANs: `show vlan id <vlan>`
                3. Tester depuis un autre équipement du même VLAN
                4. Vérifier l'interface SVI: `show ip interface vlan<X>`
                """)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 2
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : Connectivité", use_container_width=True):
            st.session_state.etape_actuelle = 4
            st.rerun()

def etape_connectivite():
    """Étape 4: Connectivité."""
    st.header("4️⃣ Connectivité Moniteur ↔ Centrale")
    
    # Collecte IP centrale
    ip_centrale = st.text_input("Adresse IP de la centrale CI", key="ip_centrale")
    if ip_centrale:
        st.session_state.donnees_collectees['IP Centrale'] = ip_centrale
    
    with st.expander("🔍 Tests de connectivité", expanded=False):
        if ip_centrale:
            st.code(f"""
# Test ping
ping {ip_centrale}
ping {ip_centrale} -t

# Traceroute
tracert {ip_centrale}

# Test MTU
ping {ip_centrale} -f -l 1472
            """, language="bash")
    
    # Question ping centrale
    ping_centrale = st.radio(
        "Le moniteur peut-il pinger l'IP de la centrale ?",
        ["Oui", "Non"],
        key="q_ping_centrale"
    )
    
    if ping_centrale == "Non":
        st.error("⚠️ **PROBLÈME DE CONNECTIVITÉ**")
        with st.expander("📝 Diagnostic approfondi"):
            st.markdown(f"""
            1. Traceroute: `tracert {ip_centrale or 'IP_CENTRALE'}`
            2. Vérifier les ACLs: `show ip access-list`
            3. Contrôler les firewalls intermédiaires
            4. Vérifier les routes: `show ip route`
            """)
    else:
        # Test latence
        latence_ok = st.radio(
            "La latence ping est-elle correcte (<10ms en LAN, <50ms en WAN) ?",
            ["Oui", "Non"],
            key="q_latence"
        )
        
        if latence_ok == "Non":
            st.warning("⚠️ Latence élevée détectée")
            
            pertes = st.radio(
                "Y a-t-il des pertes de paquets dans le ping ?",
                ["Oui", "Non"],
                key="q_pertes"
            )
            
            if pertes == "Oui":
                st.error("Pertes de paquets - Vérifier la charge réseau et les erreurs d'interface")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 3
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : Port CI", use_container_width=True):
            st.session_state.etape_actuelle = 5
            st.rerun()

def etape_port_ci():
    """Étape 5: Port CI 24005."""
    st.header("5️⃣ Port CI 24005 - Service et Connexion TCP")
    
    st.warning("⚠️ **TESTS DEPUIS LA CENTRALE UNIQUEMENT** - Le moniteur ne permet pas l'exécution de commandes")
    
    with st.expander("🔍 Commandes de test (depuis la centrale)", expanded=False):
        st.code("""
# Vérifier écoute du service
netstat -an | grep 24005
ss -tlnp | grep 24005

# Test local
telnet localhost 24005

# PowerShell
Get-NetTCPConnection -LocalPort 24005
        """, language="bash")
    
    # Service écoute
    service_ecoute = st.radio(
        "Le service CI écoute-t-il sur le port 24005 sur la centrale ?",
        ["Oui", "Non"],
        key="q_service_ecoute"
    )
    
    if service_ecoute == "Non":
        st.error("⚠️ **SERVICE CI NON ACTIF**")
        with st.expander("📝 Actions correctives urgentes"):
            st.markdown("""
            1. Vérifier service: `systemctl status <service_ci>`
            2. Contrôler config port dans fichier conf
            3. Examiner logs: `journalctl -u <service>`
            4. Redémarrer si nécessaire
            5. Vérifier bind address (0.0.0.0 vs IP spécifique)
            """)
    else:
        # Analyse Wireshark
        st.subheader("🔬 Analyse Wireshark")
        
        with st.expander("Filtres Wireshark recommandés"):
            st.code("""
# Filtre de base
tcp.port == 24005

# Handshake TCP
tcp.port == 24005 and (tcp.flags.syn == 1 or tcp.flags.reset == 1)

# Connexions refusées
tcp.port == 24005 and tcp.flags.reset == 1

# Retransmissions
tcp.analysis.retransmission
            """)
        
        tentatives = st.radio(
            "Une capture Wireshark montre-t-elle des tentatives de connexion du moniteur ?",
            ["Oui", "Non"],
            key="q_tentatives_wireshark"
        )
        
        if tentatives == "Non":
            st.error("⚠️ Moniteur ne tente pas de connexion")
            st.markdown("""
            **Causes possibles:**
            - Moniteur hors tension
            - Problème réseau en amont
            - Configuration moniteur incorrecte
            - IP centrale mal configurée
            """)
        else:
            handshake_ok = st.radio(
                "Le handshake TCP s'établit-il correctement (SYN → SYN-ACK → ACK) ?",
                ["Oui", "Non"],
                key="q_handshake"
            )
            
            if handshake_ok == "Non":
                rst_packets = st.radio(
                    "Y a-t-il des paquets TCP RST (reset) ?",
                    ["Oui", "Non"],
                    key="q_rst"
                )
                
                if rst_packets == "Oui":
                    st.error("Connexion activement refusée - Vérifier firewall/ACL")
                else:
                    st.error("Pas de SYN-ACK - Le paquet SYN n'arrive pas ou pas de réponse")
            else:
                comm_app = st.radio(
                    "La communication applicative s'établit-elle après le TCP ?",
                    ["Oui", "Non"],
                    key="q_comm_app"
                )
                
                if comm_app == "Non":
                    st.warning("Problème couche applicative - Vérifier authentification")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 4
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : Couche Applicative", use_container_width=True):
            st.session_state.etape_actuelle = 6
            st.rerun()

def etape_applicative():
    """Étape 6: Couche Applicative."""
    st.header("6️⃣ Couche Applicative - Service CI")
    
    with st.expander("🔍 Commandes de vérification service", expanded=False):
        st.code("""
# État du service
systemctl status <service_ci>
journalctl -u <service_ci> -f

# Processus
ps aux | grep ci

# Ports écoutés
netstat -tlnp | grep 24005

# Ressources
top
df -h
        """, language="bash")
    
    service_repond = st.radio(
        "Le service CI répond-il aux requêtes applicatives ?",
        ["Oui", "Non"],
        key="q_service_repond"
    )
    
    if service_repond == "Non":
        st.error("⚠️ **PROBLÈME APPLICATIF DÉTECTÉ**")
        
        logs_erreur = st.radio(
            "Y a-t-il des erreurs dans les logs de l'application CI ?",
            ["Oui", "Non"],
            key="q_logs_erreur"
        )
        
        if logs_erreur == "Oui":
            type_erreur = st.text_input("Type d'erreur observé dans les logs", key="type_erreur")
            if type_erreur:
                st.session_state.donnees_collectees['Type erreur'] = type_erreur
        
        ressources_ok = st.radio(
            "Les ressources système sont-elles suffisantes (CPU < 80%, RAM libre) ?",
            ["Oui", "Non"],
            key="q_ressources"
        )
        
        if ressources_ok == "Non":
            st.error("⚠️ Ressources système insuffisantes")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 5
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : Trafic Multicast", use_container_width=True):
            st.session_state.etape_actuelle = 7
            st.rerun()

def etape_multicast():
    """Étape 7: Trafic Multicast."""
    st.header("7️⃣ Trafic Multicast - Découverte Automatique")
    
    st.info("Le multicast est souvent utilisé pour la découverte automatique des moniteurs")
    
    with st.expander("🔬 Filtres Wireshark Multicast", expanded=False):
        st.code("""
# Multicast général
ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255

# IGMP
igmp

# Découverte CI
udp and ip.dst >= 224.0.0.0
        """)
    
    with st.expander("🔍 Commandes réseau multicast", expanded=False):
        st.code("""
# IGMP Snooping
show ip igmp snooping
show ip igmp snooping groups

# IGMP Querier
show ip igmp snooping querier

# Table multicast
show mac address-table multicast

# PIM (si routage)
show ip pim neighbor
show ip mroute
        """, language="bash")
    
    multicast_visible = st.radio(
        "Du trafic multicast est-il visible en Wireshark ?",
        ["Oui", "Non"],
        key="q_multicast_visible"
    )
    
    if multicast_visible == "Non":
        st.error("⚠️ **PROBLÈME MULTICAST**")
        
        igmp_snooping = st.radio(
            "IGMP Snooping est-il activé sur les switches ?",
            ["Oui", "Non"],
            key="q_igmp_snooping"
        )
        
        if igmp_snooping == "Oui":
            querier_ok = st.radio(
                "Un IGMP Querier est-il présent et actif ?",
                ["Oui", "Non"],
                key="q_querier"
            )
            
            if querier_ok == "Non":
                st.error("⚠️ Configurer un Querier IGMP")
    else:
        groupes = st.text_input("Groupes multicast observés (ex: 224.1.1.1)", key="groupes_multicast")
        if groupes:
            st.session_state.donnees_collectees['Groupes multicast'] = groupes
        
        contenu_ok = st.radio(
            "Le contenu des paquets multicast semble-t-il correct ?",
            ["Oui", "Non"],
            key="q_contenu_multicast"
        )
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 6
            st.rerun()
    with col2:
        if st.button("➡️ Étape suivante : QoS", use_container_width=True):
            st.session_state.etape_actuelle = 8
            st.rerun()

def etape_qos():
    """Étape 8: QoS."""
    st.header("8️⃣ QoS et Priorisation - Qualité de Service")
    
    with st.expander("🔍 Commandes QoS", expanded=False):
        st.code("""
# Configuration QoS
show policy-map
show class-map

# Par interface
show policy-map interface <int>

# Statistiques
show policy-map interface <int> statistics
show interface <int> | include drops

# Utilisation
show interface | include load
        """, language="bash")
    
    with st.expander("🔬 Filtres Wireshark QoS", expanded=False):
        st.code("""
# Marquage DSCP
ip.dsfield.dscp != 0

# Trafic prioritaire
ip.dsfield.dscp >= 32

# Congestion
tcp.analysis.window_full
        """)
    
    qos_active = st.radio(
        "Des politiques QoS sont-elles configurées sur le réseau ?",
        ["Oui", "Non"],
        key="q_qos_active"
    )
    
    if qos_active == "Oui":
        dscp_ok = st.radio(
            "Le marquage DSCP est-il correct sur les paquets CI ?",
            ["Oui", "Non"],
            key="q_dscp"
        )
        
        if dscp_ok == "Non":
            st.warning("⚠️ Problème de marquage QoS")
        
        congestion = st.radio(
            "Y a-t-il des signes de congestion réseau ?",
            ["Oui", "Non"],
            key="q_congestion"
        )
        
        if congestion == "Oui":
            st.error("⚠️ Congestion détectée")
            
            perf_ci = st.radio(
                "Les performances du CI sont-elles dégradées pendant les pics ?",
                ["Oui", "Non"],
                key="q_perf_ci"
            )
    else:
        problemes_perf = st.radio(
            "Y a-t-il des problèmes de performance ou de latence ?",
            ["Oui", "Non"],
            key="q_problemes_perf"
        )
        
        if problemes_perf == "Oui":
            st.warning("💡 Considérer l'implémentation de la QoS pour le trafic CI")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Étape précédente", use_container_width=True):
            st.session_state.etape_actuelle = 7
            st.rerun()
    with col2:
        if st.button("✅ Voir la synthèse", use_container_width=True):
            st.session_state.etape_actuelle = 9
            st.rerun()

def afficher_synthese():
    """Affiche la synthèse du diagnostic."""
    st.header("📊 Synthèse du Diagnostic")
    
    st.success("Diagnostic terminé - Voici le récapitulatif")
    
    # Données collectées
    if st.session_state.donnees_collectees:
        st.subheader("📋 Informations collectées")
        
        col1, col2 = st.columns(2)
        items = list(st.session_state.donnees_collectees.items())
        mid = len(items) // 2
        
        with col1:
            for cle, valeur in items[:mid]:
                st.metric(cle, valeur)
        
        with col2:
            for cle, valeur in items[mid:]:
                st.metric(cle, valeur)
    
    # Points clés Wireshark
    st.subheader("🔬 Points clés pour l'analyse Wireshark")
    st.markdown("""
    - **Interface à surveiller**: Celle connectée au segment du moniteur
    - **Filtre de base**: `tcp.port == 24005`
    - **Durée recommandée**: 5-10 minutes pendant un test
    - **Séquence à vérifier**: SYN → SYN-ACK → ACK puis échanges applicatifs
    """)
    
    # Recommandations
    st.subheader("🎯 Recommandations")
    st.info("""
    1. Sauvegarder ce diagnostic pour référence future
    2. Documenter les corrections appliquées
    3. Tester la solution après chaque modification
    4. Surveiller la stabilité sur 24-48h
    """)
    
    # Export
    st.subheader("💾 Export du rapport")
    if st.button("📥 Télécharger le rapport JSON", use_container_width=True):
        exporter_rapport()

def exporter_rapport():
    """Exporte le rapport de diagnostic en JSON."""
    rapport = {
        "diagnostic_ci": {
            "port": 24005,
            "timestamp": datetime.now().isoformat(),
            "donnees_collectees": st.session_state.donnees_collectees,
            "etape_finale": st.session_state.etape_actuelle
        }
    }
    
    json_str = json.dumps(rapport, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Télécharger le rapport",
        data=json_str,
        file_name=f"diagnostic_ci_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def main():
    """Fonction principale de l'application."""
    initialiser_session()
    afficher_entete()
    afficher_sidebar()
    
    # Routage des étapes
    etapes_fonctions = {
        0: etape_configuration_initiale,
        1: etape_lldp,
        2: etape_physique,
        3: etape_ip,
        4: etape_connectivite,
        5: etape_port_ci,
        6: etape_applicative,
        7: etape_multicast,
        8: etape_qos,
        9: afficher_synthese
    }
    
    # Affichage de l'étape actuelle
    etape_fonction = etapes_fonctions.get(st.session_state.etape_actuelle, afficher_synthese)
    etape_fonction()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🔧 Guide de Diagnostic Réseau CI - Version 1.0.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
