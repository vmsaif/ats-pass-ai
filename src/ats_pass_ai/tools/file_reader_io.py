
class FileReaderIO:
    """Class to read content from a file."""

    def _read_text_file(self, file_path):
        """Read and return content from a file specified by its path."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()