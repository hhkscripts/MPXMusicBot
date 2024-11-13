from MPXMusic.core.bot import MPXBot
from MPXMusic.core.dir import dirr
from MPXMusic.core.git import git
from MPXMusic.core.userbot import Userbot
from MPXMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()
# Bot Client
app = MPXBot()

# Assistant Client
userbot = Userbot()

from .platforms import PlaTForms

Platform = PlaTForms()

HELPABLE = {}
