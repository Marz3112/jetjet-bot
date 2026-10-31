# Lucky Jet Telegram – prototype d'analyse statistique

Ce projet est un prototype de bot Telegram. Il propose un menu et analyse les multiplicateurs que l'utilisateur colle depuis l'historique.

## Limites importantes
- Il ne se connecte pas à 1win.
- Il ne prédit pas le prochain multiplicateur.
- Il ne place aucun pari.
- Les fréquences passées ne prédisent pas les résultats futurs.
- Les cibles 200× à 1 200× sont affichées comme seuils d'analyse, pas comme signaux garantis.

## Mise en service (nécessite un hébergement Python)
1. Créer un bot avec `@BotFather` dans Telegram et récupérer le token.
2. Installer les dépendances : `pip install -r requirements.txt`
3. Définir la variable d'environnement `TELEGRAM_BOT_TOKEN` avec le token.
4. Lancer : `python bot.py`

Ne partage jamais le token du bot dans une conversation publique.
