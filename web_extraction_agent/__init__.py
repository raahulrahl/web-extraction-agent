# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""web-extraction-agent - A Bindu Agent for web content extraction and structuring."""

from web_extraction_agent.__version__ import __version__
from web_extraction_agent.main import (
    handler,
    initialize_agent,
    main,
    run_agent,
    cleanup,
    APIKeyError,
    ContentSection,
    PageInformation,
)

__all__ = [
    "__version__",
    "handler",
    "initialize_agent",
    "run_agent",
    "cleanup",
    "main",
    "APIKeyError",
    "ContentSection",
    "PageInformation",
]