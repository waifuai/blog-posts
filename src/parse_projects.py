
from bs4 import BeautifulSoup
import re

def parse_projects(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    projects = []
    cards = soup.find_all('div', class_='project-card')

    for card in cards:
        title_elem = card.find('h3', class_='project-title')
        title = title_elem.get_text(strip=True) if title_elem else "Unknown"
        
        link_elem = card.find('a', class_='project-link')
        link = link_elem['href'] if link_elem else "#"
        
        desc_elem = card.find('p', class_='project-description')
        desc = desc_elem.get_text(strip=True) if desc_elem else ""
        
        stats_div = card.find('div', class_='project-stats')
        views = 0
        likes = 0
        date = ""
        
        if stats_div:
            stats = stats_div.find_all('span', class_='stat')
            for stat in stats:
                text = stat.get_text(strip=True)
                if 'views' in text:
                    try:
                        views = int(re.search(r'(\d+)', text).group(1))
                    except:
                        pass
                elif 'likes' in text:
                    try:
                        likes = int(re.search(r'(\d+)', text).group(1))
                    except:
                        pass
                elif '📅' in text:
                    date = text.replace('📅', '').strip()

        projects.append({
            'title': title.replace('\n', ' ').replace('\r', ''),
            'description': desc,
            'link': link,
            'views': views,
            'likes': likes,
            'date': date
        })

    return projects

def generate_markdown(projects):
    # Sort by likes descending
    sorted_projects = sorted(projects, key=lambda x: x['likes'], reverse=True)
    
    print("## Top Featured Projects (by Likes)")
    print("| Project | Description | Views | Likes |")
    print("|---------|-------------|-------|-------|")
    
    # Top 25
    for p in sorted_projects[:25]:
        # Escape pipes in description and remove newlines
        desc = p['description'].replace('|', '\|').replace('\n', ' ').replace('\r', '')
        # Truncate description if too long
        if len(desc) > 100:
            desc = desc[:97] + "..."
        print(f"| [{p['title']}]({p['link']}) | {desc} | {p['views']} | {p['likes']} |")

    print("\n\n## All Projects List (for manual categorization checks)")
    for p in sorted_projects:
        print(f"- {p['title']} (Likes: {p['likes']}, Views: {p['views']})")

if __name__ == "__main__":
    file_path = "html/06-websim-projects.html"
    output_path = "src/project_data.md"
    try:
        projects = parse_projects(file_path)
        # Capture output to file
        import sys
        with open(output_path, 'w', encoding='utf-8') as f:
            sys.stdout = f
            generate_markdown(projects)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
