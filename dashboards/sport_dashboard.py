import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="SFG Men's Sports Dashboard", layout="wide")
st.title("SFG Men's Sports Dashboard")

BOSTON_TEAMS = {
    "Boston Celtics",
    "Boston Bruins",
    "New England Patriots",
    "Boston Red Sox"
}

OTHER_FAVORITE_TEAMS = {
    # "New York Rangers",
    "Minnesota Wild",
    "Buffalo Bills",
    "Minnesota Vikings",
    # "Detroit Lions"
}

ENDPOINTS = {
    # "WNBA": "http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/standings",
    "NHL": "https://site.web.api.espn.com/apis/v2/sports/hockey/nhl/standings",
    "NFL": "https://site.web.api.espn.com/apis/v2/sports/football/nfl/standings",
    "NBA": "https://site.web.api.espn.com/apis/v2/sports/basketball/nba/standings",
    # "MLB": "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/standings",
}

def get_standings(league_name, url):
    try:
        data = requests.get(url, timeout=10).json()
        teams = []
        for conference in data["children"]:
            for entry in conference["standings"]["entries"]:
                team = entry["team"]["displayName"]
                stats = {s["name"]: s["value"] for s in entry["stats"] if "value" in s}
                if league_name == 'NBA' or league_name == 'WNBA':
                    teams.append({
                        "Team": team,
                        "Wins": stats.get("wins"),
                        "Losses": stats.get("losses"),
                        "Win %": f"{round(100*(stats.get("wins")/(stats.get("wins")+stats.get("losses"))),0)}%"
                    })
                elif league_name == 'NHL':
                    teams.append({
                        "Team": team,
                        "Wins": stats.get("wins"),
                        "Losses": stats.get("losses"),
                        "OTL": stats.get("otLosses"),
                        "Points": stats.get("points")
                    })
                elif league_name == 'NFL':
                    teams.append({
                        "Team": team,
                        "Wins": stats.get("wins"),
                        "Losses": stats.get("losses"),
                        "Ties": stats.get("ties"),
                        "Win %": f"{round(100*(stats.get("wins")/(stats.get("wins")+stats.get("losses")+stats.get("ties"))),0)}%"
                    })
            if league_name == 'NHL':
                df = pd.DataFrame(teams).sort_values(by="Points", ascending=False)
            else:
                df = pd.DataFrame(teams).sort_values(by="Wins", ascending=False)
     
        df["Highlight"] = df["Team"].apply(lambda t: "B" if t in BOSTON_TEAMS else ("X" if t in OTHER_FAVORITE_TEAMS else ""))
        df = df.applymap(lambda x: int(x) if isinstance(x, float) and x.is_integer() else x)
        return df

    except Exception as e:
        st.error(f"Error loading {league_name} standings: {e}")
        return pd.DataFrame()

# 🎨 Custom CSS for highlighting favorite teams
highlight_css = """
<style>/
table td {
    padding: 0.4em 1em;
}
.bosfavorite {
    background-color: #B80000 !important;
    font-weight: bold;
}
.othfavorite {
    background-color: #582380 !important;
    font-weight: bold;
}
</style>
"""

st.markdown(highlight_css, unsafe_allow_html=True)

# 🧱 Layout: one column per league
cols = st.columns(len(ENDPOINTS))

for i, (league, url) in enumerate(ENDPOINTS.items()):
    with cols[i]:
        st.subheader(f"{league} Standings")
        df = get_standings(league, url)
        if not df.empty:
            # Convert to HTML to apply highlighting
            def highlight_row(row):
                if row["Team"] in BOSTON_TEAMS:
                    css_class = "bosfavorite"
                elif row["Team"] in OTHER_FAVORITE_TEAMS:
                    css_class = "othfavorite"
                else:
                    css_class = ""
                return f'<tr class="{css_class}">' + "".join(
                    [f"<td>{row[c]}</td>" for c in df.columns if c != "Highlight"]
                ) + "</tr>"

            html_table = (
                "<table><tr>" +
                "".join(f"<th>{col}</th>" for col in df.columns if col != "Highlight") +
                "</tr>" +
                "".join(df.apply(highlight_row, axis=1)) +
                "</table>"
            )
            st.markdown(html_table, unsafe_allow_html=True)
