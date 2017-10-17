/** fr localization */
define({
    // ----------------------------------------------------------------------------- masthead
    "Analyze Data": "Analyse de données",
    Workflow: "Workflow",
    "Shared Data": "Données partagées",
    "Data Libraries": "Bibliothèque de données",
    Histories: "Historiques",
    Workflows: "Workflows",
    Visualizations: "Visualisations",
    Pages: "Pages",
    Visualization: "Visualisation",
    "New Track Browser": "Nouveau Navigateur de Tracks/Pistes",
    "Saved Visualizations": "Visualisations sauvegardées",
    "Interactive Environments": "Environnements interactifs",
    Admin: "Admin",
    Help: "Aide",
    Support: "Assistance",
    Search: "Recherche",
    "Mailing Lists": "Liste de diffusion",
    Videos: "Vidéos",
    Wiki: "Documentations",
    "How to Cite Galaxy": "Comment citer Galaxy",
    "Interactive Tours": "Guides interactifs",
    User: "Utilisateur",
    Login: "Authentification",
    Register: "Enregistrement",
    "Login or Register": "Authentification et Enregistrement",
    "Logged in as": "Authentifié en tant que",
    Preferences: "Préférences",
    "Custom Builds": "Mes génomes Builds de référence",
    Logout: "Déconnexion",
    "Saved Histories": "Historiques sauvegardés",
    "Saved Datasets": "Jeux de données sauvegardés",
    "Saved Pages": "Pages sauvegardées",
    //Tooltip
    "Account and saved data": "Compte et données sauvegardées",
    "Account registration or login": "Enregistrement ou authentification",
    "Support, contact, and community": "Support,contact et communauté",
    "Administer this Galaxy": "Outils Admin",
    "Visualize datasets": "Visualiser les jeux de données",
    "Access published resources": "Accéder aux données partagées",
    "Chain tools into workflows": "Relier outils dans un workflow",
    "Analysis home view": "Accueil analyse de données",
    // ---------------------------------------------------------------------------- histories
    // ---- history/options-menu
    "History Lists": "Tableaux des historiques",
    // Saved histories is defined above.
    // "Saved Histories":
    //     false,
    "Histories Shared with Me": "Historiques partagés avec moi",
    "Current History": "Cet Historique",
    "Create New": "Créer un nouveau",
    "Copy History": "Copier l'Historique",
    "Share or Publish": "Partager et publier",
    "Show Structure": "Montrer la structure",
    "Extract Workflow": "Extraire un Workflow",
    // Delete is defined elsewhere, but is also in this menu.
    // "Delete":
    //     false,
    "Delete Permanently": "Supprimer définitivement",
    "Dataset Actions": "Actions sur les jeux de données",
    "Copy Datasets": "Copier des jeux de données",
    "Dataset Security": "Permissions/Sécurité",
    "Resume Paused Jobs": "Reprendre les processus en pause",
    "Collapse Expanded Datasets": "Réduire les données étendues",
    "Unhide Hidden Datasets": "Afficher les données cachées",
    "Delete Hidden Datasets": "Supprimer les données cachées",
    "Purge Deleted Datasets": "Purger les données supprimées",
    Downloads: "Télécharger",
    "Export Tool Citations": "Exporter les citations des outils",
    "Export History to File": "Exporter l'Historique dans un fichier",
    "Other Actions": "Autres actions",
    "Import from File": "Importer depuis un fichier",
    Webhooks: "Webhooks",

    // ---- history-model
    // ---- history-view
    "This history is empty": "Cet historique est vide",
    "No matching datasets found":
        "Aucunes données correspondantes n'ont été trouvées",
    "An error occurred while getting updates from the server":
        "Une erreur s'est produite lors de la réception des données depuis le serveur",
    "Please contact a Galaxy administrator if the problem persists":
        "Veuillez contacter un administrateur de l'instance Galaxy si ce problème persiste",
    //TODO:
    //"An error was encountered while <% where %>" :
    //false,
    "search datasets": "Rechercher des données",
    "You are currently viewing a deleted history!":
        "Vous consultez actuellement un historique supprimé!",
    "You are over your disk quota":
        "Vous avez dépassé votre quota d'espace disque",
    "Tool execution is on hold until your disk usage drops below your allocated quota":
        "L'exécution de l'outil est en attente tant que votre utilisation d'espace disque dépasse le quota attribué",
    All: "Tout",
    None: "Aucun",
    "For all selected": "Pour toute la sélection",

    // // ---- history-view-edit
    "Edit history tags": "Editer les mots-clés de l'historique",
    "Edit history Annotation": "Editer l'annotation de l'historique",
    "Click to rename history": "Cliquer pour renommer l'historique",
    // multi operations
    "Operations on multiple datasets":
        "Opérer sur plusieurs jeux de données en même temps",
    "Hide datasets": "Cacher les jeux de données",
    "Unhide datasets": "Afficher les jeux de données cachés",
    "Delete datasets": "Supprimer les jeux de données",
    "Undelete datasets": "Restaurer les jeux de données supprimés",
    "Permanently delete datasets":
        "Supprimer définitivement les jeux de données",
    "This will permanently remove the data in your datasets. Are you sure?":
        "Cela supprimera de manière permanente les données de votre historique. Êtes-vous certain?",

    // menu operations

    // // ---- history-view-annotated
    Dataset: "Jeu de données",
    Annotation: "Annotation",

    // ---- history-view-edit-current
    "This history is empty. Click 'Get Data' on the left tool menu to start":
        "Cet historique est vide. Cliquer sur 'Get Data' au niveau du menu d'outils à gauche pour démarrer",
    "You must be logged in to create histories":
        "Vous devez être connecté pour créer un historique",
    //TODO:
    //"You can <% loadYourOwn %> or <% externalSource %>" :
    //"Vous pouvez <% loadYourOwn %> ou <% externalSource %>",
    "load your own data": "Charger vos propres données",
    "get data from an external source":
        "Charger des données depuis une source externe",

    // these aren't in zh/ginga.po and the template doesn't localize
    "Include Deleted Datasets": "Inclure les jeux de données supprimés",
    "Include Hidden Datasets": "Inclure les jeux de données cachés",

    // ---------------------------------------------------------------------------- datasets
    // ---- hda-model
    "Unable to purge dataset": "Impossible de purger le jeu de données",

    // ---- hda-base
    // display button
    "Cannot display datasets removed from disk":
        "Impossible de visualiser les jeux de données supprimés du disque",
    "This dataset must finish uploading before it can be viewed":
        "Le jeu de données doit être totalement téléversé avant de pouvoir être visualiser",
    "This dataset is not yet viewable":
        "Ce jeu de données n'est pas visualisable",
    "View data": "Voir les données",
    // download button
    Download: "Télécharger",
    "Download dataset": "Télécharger le jeu de données",
    "Additional files": "Fichiers additionnels",
    // info/show_params
    "View details": "Voir les détails",

    // dataset states
    // state: new
    "This is a new dataset and not all of its data are available yet":
        "Il s'agit d'un nouveau jeu de données et seule une partie des données est accessible pour le moment",
    // state: noPermission
    "You do not have permission to view this dataset":
        "Vous n'avez pas la permission de voir ce jeu de données",
    // state: discarded
    "The job creating this dataset was cancelled before completion":
        "Le processus à l'origine de ce jeu de données a été annulé prématurément",
    // state: queued
    "This job is waiting to run": "Ce calcul est en attente de traitement",
    // state: upload
    "This dataset is currently uploading":
        "Ce jeu de données est en cours de téléversement",
    // state: setting_metadata
    "Metadata is being auto-detected": "Les métadonnées sont auto-détectées",
    // state: running
    "This job is currently running": "Le traitement est en cours",
    // state: paused
    'This job is paused. Use the "Resume Paused Jobs" in the history menu to resume':
        'Ce traitement est en pause. Utilisez le "Relancer les traitements en pause" dans le menu d\'historique pour le relancer',
    // state: error
    "An error occurred with this dataset":
        "Une erreur est survenue avec ce jeu de données",
    // state: empty
    "No data": "Aucune donnée",
    // state: failed_metadata
    "An error occurred setting the metadata for this dataset":
        "Une erreur est survenue pendant la récupération des métadonnées de ce jeu de données",

    // ajax error prefix
    "There was an error getting the data for this dataset":
        "Il est survenu une erreur durant la récupération du contenu de ce jeu de données",

    // purged'd/del'd msg
    "This dataset has been deleted and removed from disk":
        "Ce jeu de données a été supprimé et effacé du disque",
    "This dataset has been deleted": "Ce jeu de données a été supprimé",
    "This dataset has been hidden": "Ce jeu de données a été caché",

    format: "format",
    database: "génome de référence",

    // ---- hda-edit
    "Edit attributes": "Editer les attributs",
    "Cannot edit attributes of datasets removed from disk":
        "Impossible d'éditer les attributs de jeux de données effacés du disque",
    "Undelete dataset to edit attributes":
        "Restaurer le jeu de données pour en éditer les attributs",
    "This dataset must finish uploading before it can be edited":
        "Ce jeu de données doit être entièrement téléversé avant toute modification",
    "This dataset is not yet editable":
        "Ce jeu de données n'est pas encore éditable",

    Delete: "Supprimer",
    "Dataset is already deleted": "Le jeu de données est déjà supprimé",

    "View or report this error": "Voir ou remonter cette erreur",

    "Run this job again": "Exécuter ce traitement à nouveau",

    Visualize: "Visualiser",
    "Visualize in": "Visualiser via",

    "Undelete it": "Restaurer",
    "Permanently remove it from disk": "Supprimer définitivement du disque",
    "Unhide it": "Rendre visible",

    "You may be able to": "Vous devriez être en mesure de",
    "set it manually or retry auto-detection":
        "Traitez le manuellement ou retenter la détection automatique",

    "Edit dataset tags": "Editer les mots-clés du jeu de données",
    "Edit dataset annotation": "Editer les annotations du jeu de données",

    // ---------------------------------------------------------------------------- misc. MVC
    Tags: "Mots-clés",
    "Edit annotation": "Editer les annotations"
});
