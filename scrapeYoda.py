import requests
from bs4 import BeautifulSoup
import re

prefix = "https://imsdb.com/scripts/"
urls = ["Star-Wars-The-Phantom-Menace", "Star-Wars-Revenge-of-the-Sith", "Star-Wars-The-Empire-Strikes-Back", "Star-Wars-Return-of-the-Jedi"]
end = ".html"
attack_clones_alt = "http://sellascript.com/Source/resources/screenplays/attackoftheclones.htm"

def clean_yoda_line(line):
    # Remove "YODA:" or "YODA :" prefix
    cleaned = re.sub(r'^YODA\s*:?\s*', '', line)
    # Remove text in parentheses
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    # Clean up extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

with open("yoda_lines.txt", "w", encoding="utf-8") as output_file:
    for url in urls:
        response = requests.get(prefix + url + end)
        
        soup = BeautifulSoup(response.content, "html.parser")
        script_content = soup.find('pre')
        
        if not script_content:
            script_content = soup.find('td', class_='scrtext')
            if script_content:
                script_text = script_content.get_text()
            else:
                error_msg = f"No script content found for {url}"
                output_file.write(f"{error_msg}\n\n")
                print(error_msg)
                continue
        else:
            script_text = script_content.get_text()
            
        yoda_text = script_text.splitlines()
        yoda_lines = []
        direct_yoda_lines = [line for line in yoda_text if "YODA:" in line or "YODA :" in line]
        yoda_lines.extend(direct_yoda_lines)
        
        i = 0
        while i < len(yoda_text):
            line = yoda_text[i].strip()
            if line == "YODA":
                yoda_dialog = line
                
                j = i + 1
                while j < len(yoda_text):
                    next_line = yoda_text[j].strip()
                    if next_line.isupper() and len(next_line) > 0 and "(" not in next_line or next_line == "":
                        break
                    yoda_dialog += " " + next_line
                    j += 1
                
                yoda_lines.append(yoda_dialog)
                i = j
            else:
                i += 1
        
        for line in yoda_lines:
            cleaned_line = clean_yoda_line(line)
            if cleaned_line:
                output_file.write(f"{cleaned_line}\n")
                print(cleaned_line)
        output_file.write("\n\n")
        print("\n")

print("All Yoda lines have been saved to yoda_lines.txt")


