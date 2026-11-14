import sqlite3
import zipfile
import io
import re
from pathlib import Path
import pandas as pd

class Subtitles_DB_Service:
    def __init__(self, database_file_path: str):
        self.database_file_path = database_file_path
        self.db_connection = sqlite3.connect(self.database_file_path)
        self.data_frame = pd.read_sql_query("SELECT * FROM zipfiles", self.db_connection)

    def get_cleaned_subtitles(self, startRow: int, endRow: int) -> list[str]:
        cleaned_contents = []

        for index in range(startRow -1, endRow):
            subtitle_number = self.data_frame.iloc[index, 0]
            subtitle_name = self.data_frame.iloc[index, 1]
            binary_data = self.data_frame.iloc[index, 2]

            decoded_subtitle_content = ""

            with io.BytesIO(binary_data) as f:
                with zipfile.ZipFile(f, 'r') as zip_file_content_list:
                    for zip_file_content in zip_file_content_list.namelist():
                        subtitle_content = zip_file_content_list.read(zip_file_content)

                        if decoded_subtitle_content == "":
                            decoded_subtitle_content = subtitle_content.decode('latin-1')
                        else:
                            decoded_subtitle_content = f"{decoded_subtitle_content} {subtitle_content.decode('latin-1')}"

            cleaned_subtitle_content = self.clean_subtitle_content(decoded_subtitle_content)
            cleaned_contents.append((subtitle_number, subtitle_name, cleaned_subtitle_content))

        return cleaned_contents
    
    @staticmethod
    def clean_subtitle_content(raw_content: str) -> str:
        if not raw_content or not raw_content.strip():
            return ""

        cleaned_lines = []
        
        # 1. Pre-compile Regex Patterns for Performance
        # Matches SRT/VTT timestamps: e.g., 00:00:02,160 --> 00:00:04.400 or 00:02.000
        timestamp_pattern = re.compile(
            r'(\d{1,2}:)?\d{2}:\d{2}[,.]\d{3}\s*-->\s*(\d{1,2}:)?\d{2}:\d{2}[,.]\d{3}'
        )
        # Matches standalone sequence numbers (SRT index lines)
        sequence_pattern = re.compile(r'^\d+$')
        # Matches any formatting tags inside brackets: e.g., {\an4}, <i>, <font...>, <b>
        tag_pattern = re.compile(r'<[^>]*>|\{[^}]*\}')
        # Matches VTT style blocks or headers
        vtt_header_pattern = re.compile(r'^(WEBVTT|STYLE|REGION|NOTE).*$', re.IGNORECASE)

        # 2. Process Line by Line
        for line in raw_content.splitlines():
            line = line.strip()
            if not line:
                continue

            # --- STRATEGY A: Handle ASS/SSA Dialogue Lines ---
            if line.startswith("Dialogue:"):
                # ASS format hides text behind the 9th comma
                parts = line.split(",", 9)
                if len(parts) >= 10:
                    line = parts[9]
                else:
                    continue # Malformed dialogue line

            # --- STRATEGY B: Filter out SRT/VTT Metadata & Timelines ---
            if timestamp_pattern.search(line):
                continue
            if sequence_pattern.match(line):
                continue
            if vtt_header_pattern.match(line):
                continue

            # --- STRATEGY C: Clean Up Text Tags & Encoding ---
            # Strip HTML/ASS formatting tags
            line = tag_pattern.sub('', line)
            
            # Resolve common broken UTF-8 encoding artifacts
            line = line.replace("â€”", "—").replace("â€", "'")
            
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        # 3. Final Normalization for Vectorization/DB storage
        # Joins lines with spaces, then collapses any accidental double spaces
        full_text = " ".join(cleaned_lines)
        return re.sub(r'\s+', ' ', full_text).strip()    