# 🚀 Moderný GitHub Stats Dashboard s GitHub Logom

## 📋 Čo je nové

### ✨ Nové funkcie
- **GitHub Logo** - Oficiálne GitHub logo v header-i
- **Moderný dizajn** - Gradientné pozadia a lepšie farby
- **Animácie** - Plynulé slide-in animácie
- **Dark/Light mode** - Automatické prepínanie podľa GitHub témy
- **Lepšie rozloženie** - Optimalizované pre čitateľnosť

### 📁 Nové súbory
```
templates/
├── modern-overview.svg      # Moderný dark mode template
├── modern-overview-light.svg # Moderný light mode template  
├── modern-languages.svg     # Moderný jazyky template

scripts/
├── generate_modern_images.py # Generátor moderných štatistík
├── test_modern_stats.py     # Test skript
└── Makefile                 # Príkazy pre ľahšie spúšťanie

.github/workflows/
└── generate-modern-stats.yml # Automatické generovanie
```

## 🛠️ Ako používať

### 1. Lokálne testovanie
```bash
# Nastavte GitHub token
export ACCESS_TOKEN="your_github_token"

# Spustite test
python test_modern_stats.py

# Alebo použite Makefile
make test
```

### 2. Generovanie štatistík
```bash
# Moderné štatistiky s logom
make modern

# Klasické štatistiky  
make classic

# Všetky štatistiky
make all
```

### 3. Automatické generovanie
- GitHub Action sa spustí každých 6 hodín
- Môžete ho spustiť manuálne v GitHub Actions tab
- Automaticky commitne nové štatistiky

## 📊 Aktualizovaný README

Váš hlavný README (`uldyssian-sh/README.md`) teraz používa:
- Moderné štatistiky pre dark mode
- Klasické štatistiky pre light mode
- Automatické prepínanie podľa GitHub témy

## 🎨 Dizajn features

### Moderný Overview
- GitHub logo v header-i
- Gradientné pozadie (modrá → fialová)
- Animované štatistiky
- Profesionálny vzhľad

### Moderné Jazyky
- Top 8 jazykov v grid layout-e
- Farebné indikátory pre každý jazyk
- Progress bar s plynulými prechodmi
- Lepšie využitie priestoru

## 🔧 Konfigurácia

### Environment variables
```bash
ACCESS_TOKEN=your_github_token    # Povinné
GITHUB_ACTOR=uldyssian-sh        # Automaticky nastavené
EXCLUDED=""                      # Vylúčené repozitáre
EXCLUDED_LANGS=""               # Vylúčené jazyky
EXCLUDE_FORKED_REPOS=false      # Zahrnúť forked repos
```

### Prispôsobenie farieb
Môžete upraviť farby v template súboroch:
- `#58a6ff` - Hlavná modrá
- `#7c3aed` - Fialová pre gradienty  
- `#0d1117` - Dark pozadie
- `#f0f6fc` - Svetlý text

## 📈 Výhody nového dashboardu

1. **Profesionálny vzhľad** - GitHub logo a moderný dizajn
2. **Lepšia čitateľnosť** - Optimalizované fonty a spacing
3. **Responzívnosť** - Funguje v dark aj light mode
4. **Automatizácia** - Pravidelné aktualizácie cez GitHub Actions
5. **Flexibilita** - Ľahko prispôsobiteľné templaty

## 🚀 Ďalšie kroky

1. **Commit a push** všetky nové súbory do GitHub
2. **Spustite GitHub Action** pre prvé generovanie
3. **Skontrolujte výsledok** v vašom profile README
4. **Prispôsobte farby** podľa vašich preferencií

## 💡 Tipy

- Štatistiky sa aktualizujú každých 6 hodín
- Môžete manuálne spustiť aktualizáciu v GitHub Actions
- Pre rýchle testovanie použite `make test`
- Pre lokálne generovanie použite `make modern`

---

**Vytvoril:** Amazon Q Developer  
**Pre:** LT (uldyssian-sh)  
**Dátum:** $(date +'%Y-%m-%d')