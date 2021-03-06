from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
SECRET_KEY = env.str("SECRET_KEY")

DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
