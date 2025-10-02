import atexit
import streamlit as st
from sshtunnel import SSHTunnelForwarder


# =============================================================================
# Fonctions de gestion de la connexion SSH et base de données
# =============================================================================

@st.cache_resource
def init_tunnel():
    """
    Initialise le tunnel SSH une seule fois pour sécuriser la connexion à la base de données.
    
    Returns:
        SSHTunnelForwarder: L'objet tunnel SSH ou None en cas d'erreur
    """
    try:
        tunnel = SSHTunnelForwarder(
            (st.secrets.SSH_HOST, st.secrets.SSH_PORT),
            ssh_username=st.secrets.SSH_USER,
            ssh_password=st.secrets.SSH_PASSWORD,
            remote_bind_address=(st.secrets.REMOTE_HOST, st.secrets.REMOTE_PORT),
            local_bind_address=('localhost', st.secrets.LOCAL_PORT)
        )
        tunnel.start()
        
        # Fonction de nettoyage automatique du tunnel à la fermeture de l'application
        def cleanup_tunnel():
            if tunnel.is_active:
                tunnel.stop()
        
        atexit.register(cleanup_tunnel)

        # st.success(f"✅ Tunnel SSH établi : localhost:{st.secrets.LOCAL_PORT} -> {st.secrets.SSH_HOST}:{st.secrets.REMOTE_PORT}")
        return tunnel
    except Exception as e:
        st.error(f"❌ Erreur lors de la création du tunnel SSH : {e}")
        return None


@st.cache_resource
def init_database_connection(_tunnel):
    """
    Initialise la connexion à la base de données MySQL via st.connection.
    
    Args:
        _tunnel: L'objet SSHTunnelForwarder actif
        
    Returns:
        Connection: L'objet de connexion à la base de données ou None en cas d'erreur
    """
    if _tunnel and _tunnel.is_active:
        try:
            # Construction de l'URL de connexion pour st.connection
            connection_url = (
                f"mysql+pymysql://{st.secrets.DB_USER}:{st.secrets.DB_PASSWORD}"
                f"@localhost:{st.secrets.LOCAL_PORT}/{st.secrets.DB_NAME}"
            )
            
            # Création de la connexion avec st.connection
            conn = st.connection(
                name="mysql_db",
                type="sql",
                url=connection_url
            )
            
            # st.success("✅ Connexion à la base de données établie avec st.connection")
            return conn
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la connexion à la base de données : {e}")
            return None
    else:
        # st.error("❌ Le tunnel SSH n'est pas actif")
        return None


# =============================================================================
# Initialisation des connexions avec st.session_state
# =============================================================================

def initialize_connections():
    """
    Initialise le tunnel SSH et la connexion à la base de données,
    et les stocke dans st.session_state pour les partager entre les pages.
    """
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = None

    if 'tunnel' not in st.session_state:
        st.session_state.tunnel = None

    # Initialisation du tunnel SSH si pas encore fait
    if st.session_state.tunnel is None:
        st.session_state.tunnel = init_tunnel()

    # Initialisation de la connexion à la base de données si pas encore fait
    if st.session_state.db_connection is None and st.session_state.tunnel is not None:
        st.session_state.db_connection = init_database_connection(st.session_state.tunnel)
