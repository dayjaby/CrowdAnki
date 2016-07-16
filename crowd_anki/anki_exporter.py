import json
import os
import shutil

from crowd_anki.utils.constants import DECK_FILE_EXTENSION, MEDIA_SUBDIRECTORY_NAME
from crowd_anki.representation.deck import Deck


class AnkiJsonExporter(object):
    def __init__(self, collection):
        self.collection = collection

    def export_deck(self, deck_name, output_dir="./", copy_media=True):
        deck = Deck.from_collection(self.collection, deck_name)

        deck_directory = os.path.join(output_dir, deck_name)
        if not os.path.exists(deck_directory):
            os.makedirs(deck_directory)

        deck_filename = os.path.join(deck_directory, deck_name + DECK_FILE_EXTENSION)
        with open(deck_filename, mode='w') as deck_file:
            deck_file.write(json.dumps(deck, default=Deck.default_json, sort_keys=True, indent=4))

        self._save_changes()

        if copy_media:
            self._copy_media(deck, deck_directory)

    def _save_changes(self):
        """Save updates that were maid during the export. E.g. UUID fields"""
        # This saves decks and deck configurations
        self.collection.decks.save()
        self.collection.decks.flush()

        self.collection.models.save()
        self.collection.models.flush()

        # Notes?

    def _copy_media(self, deck, deck_directory):
        new_media_directory = os.path.join(deck_directory, MEDIA_SUBDIRECTORY_NAME)

        if not os.path.exists(new_media_directory):
            os.makedirs(new_media_directory)

        for file_src in deck.get_media_file_list():
            shutil.copy(os.path.join(self.collection.media.dir(), file_src), new_media_directory)
