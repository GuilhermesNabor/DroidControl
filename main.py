from src.ui.menu import Menu
from src.utils.logger import logger

def main():
    """Application entry point."""
    try:
        menu = Menu()
        menu.display_main_menu()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye!")
    except Exception as e:
        logger.critical(f"Unhandled exception in main loop: {e}")

if __name__ == "__main__":
    main()
