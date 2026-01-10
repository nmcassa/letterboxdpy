"""
Letterboxd Follow Statistics Analyzer

Analyzes follow relationships (followers/following) and identifies:
- Mutual follows (Friends)
- Fans (They follow you, you don't follow back)
- Not Following Back (You follow them, they don't follow back)

Generates interactive HTML report and JSON data.
"""

import os
import argparse
from datetime import datetime
from json import dumps as json_dumps

from letterboxdpy import user
from pykit.terminal_utils import get_input
from letterboxdpy.utils.utils_file import build_path
from letterboxdpy.utils.utils_directory import Directory


class FollowStatsHtmlRenderer:
    """Handles HTML report generation for follow statistics."""
    
    CSS = """
        :root { 
            --bg-color: #0d1117; 
            --text-primary: #c9d1d9; 
            --text-secondary: #8b949e; 
            --accent-color: #238636; 
            --border-color: #30363d; 
            --card-bg: #161b22; 
            --hover-bg: #21262d;
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
            background-color: var(--bg-color); color: var(--text-primary); margin: 0; padding: 20px; 
            line-height: 1.5; cursor: default;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        
        .header { 
            display: flex; justify-content: space-between; align-items: flex-start;
            margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--border-color);
        }
        h1 { margin: 0; font-size: 24px; color: var(--text-primary); font-weight: 600; }
        
        /* Stats Grid */
        .stats-grid { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
            gap: 16px; margin-bottom: 30px; 
        }
        .stat-card { 
            background: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 16px; text-align: center;
        }
        .stat-val { font-size: 28px; font-weight: 700; color: #ffffff; display: block; margin-bottom: 4px; }
        .stat-label { font-size: 13px; color: var(--text-secondary); }
        
        /* Tabs - Segmented Control */
        .tabs { 
            display: inline-flex; background: rgba(110, 118, 129, 0.1); 
            border-radius: 6px; padding: 4px; margin-bottom: 20px; 
            border: 1px solid var(--border-color);
        }
        .tab-btn { 
            background: none; border: none; color: var(--text-secondary); 
            padding: 6px 16px; font-size: 13px; cursor: pointer; 
            border-radius: 5px; font-weight: 500; transition: all 0.2s; 
        }
        .tab-btn:hover { color: var(--text-primary); background: rgba(177, 186, 196, 0.08); }
        .tab-btn.active { 
            background: rgba(110, 118, 129, 0.3); color: var(--text-primary); 
            font-weight: 600; box-shadow: none;
        }
        
        /* Content Grid */
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .sort-info { margin-bottom: 12px; color: var(--text-secondary); font-size: 11px; font-style: italic; opacity: 0.7; }
        
        .user-grid { 
            display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; 
        }
        .user-card { 
            background: var(--card-bg); border: 1px solid var(--border-color); 
            border-radius: 8px; padding: 16px; display: flex; align-items: center; gap: 12px;
            transition: transform 0.2s, border-color 0.2s; text-decoration: none;
        }
        .user-card:hover { 
            transform: translateY(-2px); border-color: var(--text-secondary); background: var(--hover-bg);
        }
        .avatar-placeholder {
            width: 40px; height: 40px; border-radius: 50%; background: #2b3137;
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; color: var(--text-secondary); font-weight: bold;
        }
        .user-info { display: flex; flex-direction: column; overflow: hidden; }
        .user-name { color: var(--text-primary); font-weight: 600; font-size: 14px; }
        .user-meta { color: var(--text-secondary); font-size: 12px; margin-top: 2px; }
        
        /* Footer */
        .footer { text-align: center; margin-top: 40px; color: var(--text-secondary); font-size: 12px; border-top: 1px solid var(--border-color); padding-top: 20px;}
    """
    
    SCRIPT = """
        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        }
        
        // Search functionality
        function filterUsers(query) {
            query = query.toLowerCase();
            const activeTab = document.querySelector('.tab-content.active');
            const cards = activeTab.querySelectorAll('.user-card');
            
            cards.forEach(card => {
                const name = card.querySelector('.user-name').textContent.toLowerCase();
                if (name.includes(query)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    """

    def __init__(self, username):
        self.username = username

    def _calculate_ratio_info(self, section_id, count, stats):
        total_following = len(stats['details']['all_following'])
        total_followers = len(stats['details']['all_followers'])
        
        if section_id in ['mutual', 'notback']:
            pct = round(count / total_following * 100, 1) if total_following else 0
            return f" · <strong>{pct}%</strong> of Following"
        elif section_id == 'fans':
            pct = round(count / total_followers * 100, 1) if total_followers else 0
            return f" · <strong>{pct}%</strong> of Followers"
        return ""

    def _generate_user_cards(self, users):
        cards = []
        for u in users:
            initial = u[0].upper() if u else "?"
            cards.append(f"""
            <a href="https://letterboxd.com/{u}/" target="_blank" class="user-card">
                <div class="avatar-placeholder">{initial}</div>
                <div class="user-info">
                    <span class="user-name">@{u}</span>
                    <span class="user-meta">View Profile</span>
                </div>
            </a>
            """)
        return "".join(cards)

    def render(self, filepath, stats):
        sections = [
            {'id': 'mutual', 'title': 'Mutual Follows', 'data': stats['details']['followback']},
            {'id': 'fans', 'title': 'Fans (Reviewers)', 'data': stats['details']['fans']},
            {'id': 'notback', 'title': 'Not Following Back', 'data': stats['details']['not_followback']},
            {'id': 'all_following', 'title': 'Following', 'data': stats['details']['all_following']},
            {'id': 'all_followers', 'title': 'Followers', 'data': stats['details']['all_followers']}
        ]
        
        tabs_html = ""
        contents_html = ""
        
        for i, section in enumerate(sections):
            is_active = "active" if i == 0 else ""
            count = len(section['data'])
            
            # Logic extracted to helper
            ratio_info = self._calculate_ratio_info(section['id'], count, stats)
            cards_html = self._generate_user_cards(section['data'])
            
            # Tab Button
            tabs_html += f"""
                <button class="tab-btn {is_active}" onclick="switchTab('{section['id']}')">
                    {section['title']} <span style="opacity: 0.6; margin-left: 4px;">{count}</span>
                </button>
            """
            
            # Tab Content
            contents_html += f"""
            <div id="{section['id']}" class="tab-content {is_active}">
                <div class="sort-info">Ordered by Letterboxd default{ratio_info}</div>
                <div class="user-grid">
                    {cards_html if cards_html else '<div style="color:var(--text-secondary); padding:20px;">No users found in this category.</div>'}
                </div>
            </div>
            """
            
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Follow Stats - {self.username}</title>
            <style>{self.CSS}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div>
                        <h1>Follow Statistics</h1>
                        <div style="color: var(--text-secondary); margin-top: 5px;">for <span style="color: var(--text-primary); font-weight:600">@{self.username}</span></div>
                    </div>
                    <div>
                        <input type="text" placeholder="Filter users..." 
                            style="background:var(--card-bg); border:1px solid var(--border-color); padding:8px 12px; border-radius:6px; color:var(--text-primary);"
                            onkeyup="filterUsers(this.value)">
                    </div>
                </div>
                
                <div class="tabs">
                    {tabs_html}
                </div>
                
                {contents_html}
                
                <div class="footer">
                    Generated with letterboxdpy · {datetime.now().strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            <script>{self.SCRIPT}</script>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
            
class FollowStatsAnalyzer:
    """Analyze follow statistics for Letterboxd users."""
    
    EXPORTS_DIR = build_path(os.path.dirname(__file__), 'exports', 'users')
    
    def __init__(self, username: str):
        self.username = username
        self.user_instance = user.User(username)
        
        # Setup directories
        self.user_dir = build_path(self.EXPORTS_DIR, self.username)
        Directory.create(self.user_dir)
    
    def analyze(self):
        """Analyze follow statistics for the user."""
        print(f"Fetching followers and following for {self.username}...")
        followers = self.user_instance.get_followers()
        following = self.user_instance.get_following()
        
        stats = self._calculate_stats(following, followers)
        self._save(stats)
        return stats
    
    def _calculate_stats(self, following: dict, followers: dict) -> dict:
        """Calculate follow statistics preserving original order."""
        following_list = list(following.keys())
        followers_list = list(followers.keys())
        
        following_set = set(following_list)
        followers_set = set(followers_list)
        
        # Lists preserving order
        not_followback = [u for u in following_list if u not in followers_set]
        followback = [u for u in following_list if u in followers_set]
        fans = [u for u in followers_list if u not in following_set]
        
        return {
            'summary': {
                'total_following': len(following_list),
                'total_followers': len(followers_list),
                'mutual_follows': len(followback),
                'not_followback_count': len(not_followback),
                'fans_count': len(fans),
                'followback_ratio': round(len(followback) / len(following_list) * 100, 2) if following_list else 0
            },
            'details': {
                'not_followback': not_followback,
                'followback': followback,
                'fans': fans,
                'all_following': following_list,
                'all_followers': followers_list
            }
        }

    def _save(self, stats: dict):
        # Save JSON
        json_path = os.path.join(self.user_dir, 'follow_stats.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_dumps(stats, indent=4))
        print(f"Saved JSON: {json_path}")
        
        # Save HTML
        html_path = os.path.join(self.user_dir, 'follow_stats.html')
        renderer = FollowStatsHtmlRenderer(self.username)
        renderer.render(html_path, stats)
        print(f"Saved HTML: {html_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze follow stats and generate interactive HTML report")
    parser.add_argument("--user", '-u', help="Letterboxd username")
    args = parser.parse_args()

    if args.user:
        username = args.user
    else:
        username = get_input("Enter username: ", index=1)
        
    analyzer = FollowStatsAnalyzer(username)
    analyzer.analyze()