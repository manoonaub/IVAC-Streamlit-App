# 🎥 Script de Démonstration Vidéo (2-4 minutes)

## 🎯 Objectif de la vidéo
Présenter le **narrative** de l'application IVAC en montrant comment les données racontent une histoire cohérente sur les inégalités éducatives en France.

---

## ⏱️ Structure Chronologique (4 minutes)

### **[0:00-0:30] Introduction & Contexte (30 sec)**

**À DIRE :**
> "Bonjour ! Je vous présente mon tableau de bord IVAC — une application Streamlit qui analyse les indicateurs de valeur ajoutée des collèges français. La question centrale : **certains établissements font-ils mieux que prévu en tenant compte du profil de leurs élèves ?**"

**À MONTRER :**
- Lancer l'app (page Introduction)
- Montrer le titre et la source des données (data.gouv.fr)
- Expliquer brièvement la valeur ajoutée : VA > 0 = meilleur que prévu, VA < 0 = en-dessous

**ASTUCE :** Switcher la langue FR → EN pour montrer le support bilingue

---

### **[0:30-1:30] Data Quality & Profiling (1 min)**

**À DIRE :**
> "Avant d'analyser, je vérifie la qualité des données. Voici la page Profiling qui montre les valeurs manquantes, les statistiques descriptives, et les distributions."

**À MONTRER :**
- Aller sur "Data Quality & Profiling"
- Montrer la table des valeurs manquantes
- Scroll rapide vers les histogrammes
- Mentionner : "J'ai détecté X colonnes avec des NaN, mais les colonnes clés (valeur_ajoutee, taux_reussite_g) sont fiables."

**KEY MESSAGE :**
> "La transparence sur les limites est essentielle en data storytelling."

---

### **[1:30-2:45] Overview & Analysis — Le cœur de l'histoire (1 min 15)**

**À DIRE :**
> "Passons à l'analyse. Cette page combine tendances nationales, disparités territoriales, et comparaisons sectorielles."

**À MONTRER (séquence rapide) :**

1. **KPIs (10 sec)**
   - "Voici les 4 métriques clés : taux moyen, valeur ajoutée moyenne, dispersion, nombre d'établissements."
   - Pointer le delta (flèche verte/rouge)

2. **Tendances temporelles (15 sec)**
   - "L'évolution conjointe montre que la VA reste stable autour de 0 sur plusieurs sessions."
   - Montrer les 2 axes (VA à gauche, taux à droite)

3. **Carte choroplèthe (20 sec)**
   - "Les couleurs révèlent des disparités géographiques : les départements en vert performent mieux."
   - Hover sur 2-3 départements pour montrer les détails

4. **Distribution (15 sec)**
   - "L'histogramme montre une distribution centrée autour de 0, avec quelques établissements exceptionnels (zones vertes) et fragiles (zones rouges)."

5. **Public vs Privé (15 sec)**
   - "Le test statistique confirme un écart significatif (p < 0.05), mais attention : différence ≠ causalité."
   - Montrer le box plot et le résultat du t-test

**KEY MESSAGE :**
> "Les données révèlent des inégalités territoriales et sectorielles persistantes."

---

### **[2:45-3:30] Deep Dives — Analyses approfondies (45 sec)**

**À DIRE :**
> "Pour aller plus loin, la page Deep Dives permet d'explorer établissement par établissement."

**À MONTRER :**
1. **Sélection des filtres (15 sec)**
   - Choisir une académie (ex: Paris)
   - Choisir une session (ex: 2024)
   - Montrer la liste déroulante des établissements

2. **Graphiques détaillés (20 sec)**
   - Montrer le graphique d'évolution d'un établissement sur plusieurs sessions
   - Montrer le Top 10 / Bottom 10 dans l'académie
   - Montrer une analyse par taille d'établissement (petit/moyen/grand)

3. **Export CSV (10 sec)**
   - Cliquer sur le bouton de téléchargement
   - "Les données filtrées peuvent être exportées pour des analyses complémentaires."

**KEY MESSAGE :**
> "Cette page permet d'identifier les outliers et de comprendre les facteurs contextuels."

---

### **[3:30-4:00] Conclusions & Recommandations (30 sec)**

**À DIRE :**
> "Enfin, la page Conclusions synthétise les 4 enseignements clés et propose 6 recommandations politiques."

**À MONTRER :**
- Scroll rapide sur les findings (disparités territoriales, écart public/privé, faible corrélation taux/VA)
- Montrer les recommandations (programmes de soutien territorial, évaluation contextualisée, partage des bonnes pratiques)
- Montrer la section "Limitations & Caveats" pour insister sur l'éthique

**À DIRE :**
> "**L'objectif n'est pas de classer, mais de soutenir.** Les données doivent guider l'action, pas stigmatiser."

---

### **[Optionnel] Closing (10 sec)**

**À DIRE :**
> "Merci d'avoir suivi cette démo ! Cette app transforme des données brutes en insights actionnables. Le code est reproductible, bilingue, et respecte les bonnes pratiques WCAG. Questions ?"

**À MONTRER :**
- Retour à la page d'accueil
- Montrer le footer avec les crédits (data.gouv.fr, Streamlit)

---

## 🎬 Conseils Techniques pour l'Enregistrement

### Préparation
1. **Tester l'app avant** : Vérifier que tous les graphiques s'affichent correctement
2. **Préparer les filtres** : Pré-sélectionner session 2024, région Île-de-France, etc.
3. **Nettoyer l'écran** : Fermer les onglets inutiles, désactiver notifications

### Logiciels recommandés
- **macOS** : QuickTime Player (Fichier → Nouvel enregistrement de l'écran)
- **Windows** : OBS Studio (gratuit, open source)
- **En ligne** : Loom (limité à 5 min gratuit)

### Paramètres
- **Résolution** : 1920x1080 (Full HD)
- **FPS** : 30 (suffisant pour une démo)
- **Audio** : Microphone de qualité (casque avec micro si possible)
- **Durée cible** : 3-4 minutes MAX

### Montage (optionnel)
- **Ajouter une intro** (5 sec) : Titre du projet + votre nom
- **Ajouter des sous-titres** : Pour l'accessibilité
- **Musique de fond** : Très subtile (ou pas du tout)

---

## 📝 Script Version Française (Alternative)

Si vous préférez faire la vidéo en français uniquement :

**[0:00-0:30] Intro**
> "Bonjour, je vous présente mon tableau de bord IVAC sur les performances des collèges français..."

**[0:30-1:30] Data Quality**
> "D'abord, je vérifie la qualité : voici les statistiques, les valeurs manquantes..."

**[1:30-2:45] Overview**
> "Ensuite, l'analyse révèle des disparités territoriales marquées — regardez cette carte..."

**[2:45-3:30] Deep Dives**
> "Puis je zoome sur Paris : certains établissements excellent malgré des contextes difficiles..."

**[3:30-4:00] Conclusions**
> "Enfin, 4 enseignements et 6 recommandations pour les politiques éducatives. Merci !"

---

## ✅ Checklist Avant Enregistrement

- [ ] App lancée et fonctionnelle sur localhost:8501
- [ ] Langue sélectionnée (FR ou EN)
- [ ] Filtres pré-configurés pour gagner du temps
- [ ] Script répété 2-3 fois à voix haute
- [ ] Microphone testé (pas de bruit de fond)
- [ ] Écran propre (pas de notifications, emails, etc.)
- [ ] Timer prêt (viser 3:30-3:50, pas plus de 4:00)

---

## 🎯 Messages Clés à Faire Passer

1. **Storytelling data-driven** : Les données racontent une histoire cohérente
2. **Transparence** : Je montre les limites (data quality, caveats)
3. **Interactivité** : L'utilisateur peut explorer avec les filtres
4. **Insights actionnables** : Pas juste des graphiques, mais des recommandations
5. **Design soigné** : Bilingue, accessible, cohérent visuellement

---

## 📤 Export & Soumission

**Format de sortie :**
- **Vidéo** : MP4 (H.264, 1920x1080)
- **Taille cible** : < 50 MB (compresser si nécessaire)
- **Nom du fichier** : `StreamlitApp25_20221191_AUBEL_DEMO.mp4`

**Où héberger :**
- YouTube (non listé)
- Google Drive (accessible via lien)
- OneDrive (si déjà utilisé pour le projet)

**Lien à inclure dans le README :**
```markdown
## 🎥 Demo Video

Watch the full walkthrough: [YouTube Link](https://youtu.be/YOUR_VIDEO_ID)
```

---

**Bonne chance pour votre enregistrement ! 🎬✨**

