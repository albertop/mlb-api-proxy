"""
MLB Stats Translation Dictionary

Maps MLB Stats API field names to standard baseball abbreviations.
- All keys use camelCase (JSON convention)
- All values use standard baseball abbreviations
- No duplicate keys
- Corrected baseball accuracy (balks = BK, not WP)
- Consistent percentage/ratio formatting
- Organized by stat type
"""

STAT_TRANSLATIONS = {
    # ============================================================
    # HITTER STATS - Basic Batting Statistics
    # ============================================================
    # NOTE: bare "games" is NOT translated: it is the structural array key in the
    # schedule (dates[].games). The stat "games played" is covered by "gamesPlayed".
    "gamesPlayed": "G",
    "atBats": "AB",
    "runs": "R",
    "hits": "H",
    "singles": "X1B",
    "doubles": "X2B",
    "triples": "X3B",
    "homeRuns": "HR",
    "rbi": "RBI",
    "reachedOnError": "ROE",
    "runsBattedIn": "RBI",  # Full name variant
    "stolenBases": "SB",
    "caughtStealing": "CS",
    "strikeOuts": "K",
    "baseOnBalls": "BB",
    "walks": "BB",  # Alternate name
    "intentionalWalks": "IBB",
    "hitByPitch": "HBP",
    "hitByPitches": "HBP",  # Plural variant
    "hitBatsman": "HBP",
    "sacBunts": "SH",
    "sacrificeBunts": "SH",  # Full name
    "sacFlies": "SF",
    "sacrificeFlies": "SF",  # Full name
    "plateAppearances": "PA",
    "totalPlateAppearances": "PA",
    "totalBases": "TB",
    "leftOnBase": "LOB",
    "homeRunsPerPlateAppearance": "HRpPA",
    "groundIntoTriplePlay": "GITP",
    # ============================================================
    # HITTER STATS - Contact & Batting Quality
    # ============================================================
    "avg": "AVG",
    "battingAverage": "AVG",  # Full name
    "obp": "OBP",
    "onBasePercentage": "OBP",  # Full name
    "slg": "SLG",
    "sluggingPercentage": "SLG",  # Full name
    "ops": "OPS",
    "onBasePlusSlugging": "OPS",  # Full name
    "babip": "BABIP",
    "iso": "ISO",
    "groundOutsToAirouts": "GOtoAO",
    "stolenBasePercentage": "SBpct",
    "caughtStealingPercentage": "CSpct",
    "catchersInterference": "CI",
    "atBatsPerHomeRun": "ABpHR",
    "extraBaseHits": "XH",
    "strikeoutPercent": "Kpct",
    "walkPercent": "BBpct",
    # ============================================================
    # HITTER STATS - Batted Ball Distribution
    # ============================================================
    "groundOuts": "GOuts",
    "airOuts": "AOuts",
    "flyOuts": "FOuts",
    "popOuts": "POuts",
    "lineOuts": "LOuts",
    "groundHits": "GH",
    "flyHits": "FH",
    "popHits": "PH",
    "lineHits": "LH",
    "totalSwings": "Swings",
    "swingAndMisses": "SwingMiss",
    "ballsInPlay": "BIP",
    "gidp": "GIDP",
    "groundIntoDoublePlay": "GIDP",
    "groundIntoDoublePlays": "GIDP",  # Plural variant
    "groundOutsPerFlyOut": "GOpFO",
    "groundoutToFlyoutRatio": "GOtoFO",
    "numberOfPitches": "Pitches",
    # ============================================================
    # PITCHER STATS - Basic Pitching Statistics
    # ============================================================
    "wins": "W",
    "losses": "L",
    "gamesPitched": "GP",
    "gamesStarted": "GS",
    "gamesFinished": "GF",
    "completeGames": "CG",
    "shutouts": "SHO",
    "saves": "SV",
    "blownSaves": "BS",
    "holds": "HLD",
    "inningsPitched": "IP",
    "innings": "INN",  # Singular variant
    "earnedRuns": "ER",
    "earnedRun": "ER",  # Singular variant
    "era": "ERA",
    "earnedRunAverage": "ERA",  # Full name
    "wildPitches": "WP",
    "wildPitch": "WP",  # Singular variant
    "balks": "BK",
    "balk": "BK",  # Singular variant
    "battersFaced": "BF",
    "totalBattersFaced": "BF",
    "outs": "Outs",
    "strikes": "Strikes",
    "catcherEarnedRunAverage": "Catcher_ERA",
    "passedBalls": "PB",
    "lobPercent": "LOBpct",  # Left on Base Percentage
    "lobWins": "LOB_W",
    "bipWins": "BIP_W",  # Wins from balls in play
    "fdpWins": "FDP_W",  # Wins from fielding dependent pitching
    "gidpPercentage": "GIDPpct",
    "battersFacedPerGame": "BFpG",
    "buntsFailed": "SH_Fail",  # Failed bunts (not a standard stat, but added for completeness)
    "buntsMissedTipped": "SH_Missed",  # Missed or tipped bunts (added for completeness)
    "whiffPercentage": "SwingMisspct",  # Swinging strike percentage (whiff rate)
    "flyBallPercentage": "FBpct",  # Percentage of fly balls allowed (not in original, but added for completeness)
    # ============================================================
    # PITCHER STATS - Strikeouts, Walks, Control
    # ============================================================
    "strikeoutsPer9": "Kp9",
    "strikeoutsPer9Inn": "Kp9",  # Alternate notation
    "baseOnBallsPer9": "BBp9",
    "walksPer9Inn": "BBp9",  # Walks per 9 innings
    "hitsPer9": "Hp9",
    "hitsPer9Inn": "Hp9",  # Alternate notation
    "homeRunsPer9": "HRp9",
    "strikeoutsToWalks": "KpBB",
    "strikeoutWalkRatio": "KpBB",  # K/BB ratio
    "strikePercentage": "Strikepct",
    "swingingStrikePercentage": "Swstrpct",  # Swinging strike percentage
    "saveOpportunities": "SaveOpp",
    "savePercentage": "SVpct",
    "winPercentage": "Winpct",
    "winningPercentage": "Winpct",  # Alternate name
    "strikeoutsMinusWalksPercentage": "KpBBpct",  # (K-BB)/PA percentage
    "inningsPitchedPerGame": "IPpG",
    # ============================================================
    # CATCHER STATS - Inherited Runners, Pickoffs
    # ============================================================
    # NOTE: "passedBalls" is already defined above (→ PB); do not repeat here.
    "pickoffAttempts": "PKO_Att",
    # ============================================================
    # PITCHER STATS - Inherited Runners, Pickoffs
    # ============================================================
    "inheritedRunners": "InhR",
    "inheritedRunnersScored": "InhRS",
    "InheritedRunners": "InhR",  # Alternate name
    "InheritedRunnersScored": "InhRS",  # Alternate name
    "pickoffs": "PKO",
    "Pickoffs": "PKO",  # Alternate name
    "bequeathedRunners": "BqR",
    "bequeathedRunnersScored": "BqRS",
    "hitBatsmen": "HBP",  # Same as hitter stat
    # ============================================================
    # PITCHER STATS - Advanced Metrics
    # ============================================================
    "whip": "WHIP",
    "walksAndHitsPerInningPitched": "WHIP",  # Full name
    "pitchesPerInning": "PpInn",
    "pitchesPerPlateAppearance": "PpPA",
    "walksPerPlateAppearance": "BBpPA",
    "strikeoutsPerPlateAppearance": "KPpA",
    "walksPerStrikeout": "BBpK",
    "ratioBBSO": "BBpK",
    "runsScoredPer9": "Rp9",
    "qualityStarts": "QS",
    "gidpOpp": "GIDP_Opp",
    # ============================================================
    # PITCHER STATS - FIP & Advanced Pitching Stats
    # ============================================================
    "fip": "FIP",
    "fipMinus": "FIPminus",
    "xfip": "xFIP",
    "ra9War": "RA9WAR",
    "eraMinus": "ERAminus",
    "fmli": "fmLI",  # Final Mound Leverage Index
    # ============================================================
    # ADVANCED STATS - WAR Components (Removed duplicates)
    # ============================================================
    "war": "WAR",  # Single entry for both hitter and pitcher context
    "rar": "RAR",  # Single entry for Runs Above Replacement
    "ubr": "UBR",  # Ultra Base Running
    # ============================================================
    # ADVANCED STATS - Weighted Stats (Offensive)
    # ============================================================
    "woba": "wOBA",
    "xWoba": "xwOBA",  # Expected wOBA
    "xWobacon": "xwOBACON",  # Expected wOBA on contact
    "xAvg": "xAVG",  # Expected batting average
    "xSlg": "xSLG",  # Expected slugging percentage
    "wRaa": "wRAA",
    "wRc": "wRC",
    "wRcPlus": "wRCPlus",
    "wGdp": "wGDP",
    "wSb": "wSB",
    "spd": "SPD",
    # ============================================================
    # ADVANCED STATS - Positional & Component Analysis
    # ============================================================
    # NOTE: generic WAR-component words (positional, batting, fielding, baseRunning,
    # replacement) were removed: as bare keys they collide with structural sections
    # in MLB responses (e.g. boxscore team.batting / team.fielding) and would rename
    # them globally. Re-add only if a specific WAR-component endpoint needs them.
    "wLeague": "wLeague",
    "sd": "SD",
    "md": "MD",
    "pli": "pLI",
    "inli": "inLI",
    "gmli": "gmLI",
    "exli": "exLI",
    # ============================================================
    # ADVANCED STATS - Fielding & Defensive Metrics
    # ============================================================
    "UZR": "UZR",  # Ultimate Zone Rating
    "outsAboveAverage": "OAA",  # Outs Above Average
    "fieldingRunsPrevented": "FRP",  # Fielding Runs Prevented
    "doublePlays": "DP",  # Double plays
    "chances": "TC",  # Total chances (fielding stat)
    # NOTE: "streak" removed: it collides with the standings "streak" object.
    "walkOffs": "WO",
    "assists": "A",
    "errors": "E",
    "putOuts": "PO",
    "rangeFactorPer9Inn": "RFp9",
    "rangeFactorPerGame": "RFpG",
    "fieldingPercentage": "Fldpct",
    "throwingErrors": "ThrE",
    "triplePlays": "TP",
    # ============================================================
    # GAME STATS - RISP & Streaks
    # ============================================================
    "hitsRisp": "H_RISP",  # Hits with Runners In Scoring Position
    "leftOnBaseRisp": "LOB_RISP",  # Left on base in RISP situations
    "winStreak": "WStrk",  # Consecutive wins
    "lossStreak": "LStrk",  # Consecutive losses
    # ============================================================
    # ROSTER & TEAM STATS
    # ============================================================
    "runSupport": "RS",
}

# ============================================================
# SPANISH TRANSLATIONS DICTIONARY
# Maps each unique abbreviation from STAT_TRANSLATIONS to its Spanish equivalent
# ============================================================
STAT_SPANISH = {
    "A": "Asistencias",
    "ABpHR": "AB por HR",
    "AOuts": "Outs Aéreos",
    "AVG": "Promedio",
    "AB": "Turnos al Bate",
    "BABIP": "Promedio en Juego",
    "BB": "Bases por Bolas",
    "BBp9": "BB por 9 Innings",
    "BBpK": "BB por K",
    "BBpPA": "BB por PA",
    "BBpct": "% de BB",
    "Kpct": "% de Ponches",
    "BF": "Bateadores Enfrentados",
    "BFpG": "Bateadores Enfrentados por Juego",
    "BIP": "Bolas en Juego",
    "BIP_W": "Victorias por Bolas en Juego",
    "BK": "Balks",
    "BqR": "Corredores Legados",
    "BqRS": "Carreras de Corredores Legados",
    "BS": "Saves Perdidos",
    "Catcher_ERA": "ERA del Receptor",
    "CG": "Juegos Completos",
    "CI": "Interferencia de Receptor",
    "CS": "Robos Fallidos",
    "CSpct": "% Robos Fallidos",
    "DP": "Dobles Plays",
    "E": "Errores",
    "ER": "Carreras Limpias",
    "ERA": "Promedio de Carreras Limpias",
    "ERAminus": "ERA-",
    "FH": "Hits Elevados",
    "FIP": "Pitcheo Independiente",
    "FDP_W": "Victorias por Pitcheo Dependiente de la Defensa",
    "FIPminus": "FIP-",
    "Fldpct": "% de Defensa",
    "FOuts": "Outs Elevados",
    "FRP": "Carreras Prevenidas",
    "FBpct": "% de Fly Balls Permitidos",
    "G": "Juegos",
    "GF": "Juegos Terminados",
    "GH": "Hits Rodados",
    "GIDP": "Rodados de Doble Play",
    "GIDP_Opp": "Oportunidades GIDP",
    "GIDPpct": "% de GIDP",
    "GITP": "Rodados de Triple Play",
    "GOuts": "Outs Rodados",
    "GOtoAO": "Outs Rodados / Outs Aéreos",
    "GOtoFO": "Outs Rodados / Outs Elevados",
    "GOpFO": "Outs Rodados por Outs Elevados",
    "GP": "Juegos Lanzados",
    "GS": "Juegos Iniciados",
    "H": "Hits",
    "H_RISP": "Hits con Corredores en Posición de Anotar",
    "HBP": "Golpeado por Lanzamiento",
    "HLD": "Holds",
    "Hp9": "Hits por 9 Innings",
    "HR": "Jonrones",
    "HRp9": "HR por 9 Innings",
    "HRpPA": "HR por PA",
    "IBB": "Bases por Bolas Intencionales",
    "INN": "Innings",
    "InhR": "Corredores Heredados",
    "InhRS": "Carreras de Corredores Heredados",
    "IP": "Innings Lanzados",
    "IPpG": "Innings por Juego",
    "ISO": "Poder Aislado",
    "K": "Ponches",
    "KpBBpct": "% de (K-BB) por PA",
    "KPpA": "K por PA",
    "KpBB": "K / BB",
    "Kp9": "Ponches por 9 Innings",
    "L": "Derrotas",
    "LH": "Hits Lineales",
    "LOB": "Corredores Dejados",
    "LOB_RISP": "Corredores Dejados en Posición de Anotar",
    "LOBpct": "% de Corredores Dejados",
    "LOB_W": "Victorias por Corredores Dejados",
    "LOuts": "Outs Lineales",
    "LStrk": "Racha de Derrotas",
    "MD": "Desviación Media",
    "Outs": "Outs",
    "OAA": "Outs Sobre Promedio",
    "OBP": "Porcentaje de Embase",
    "OPS": "Embase más Slugging",
    "PA": "Apariciones al Bate",
    "PB": "Pasadas",
    "PH": "Hits Pop",
    "PKO": "Pickoffs",
    "PKO_Att": "Intentos de Pickoff",
    "Pitches": "Lanzamientos",
    "POuts": "Outs Pop",
    "PpInn": "Lanzamientos por Inning",
    "PpPA": "Lanzamientos por Aparición al Bate",
    "PO": "Outs Registrados",
    "QS": "Quality Starts",
    "R": "Carreras",
    "RA9WAR": "RA9 WAR",
    "RAR": "Carreras Sobre Reemplazo",
    "RBI": "Carreras Impulsadas",
    "ROE": "Embasarse por Error",
    "RFpG": "Factor de Rango por Juego",
    "RFp9": "Factor de Rango por 9 Innings",
    "RS": "Apoyo de Carreras",
    "Rp9": "Carreras por 9 Innings",
    "SB": "Bases Robadas",
    "SBpct": "% Bases Robadas",
    "SD": "Desviación Estándar",
    "SH": "Sacrificios de Toque",
    "SH_Fail": "Toques Fallidos",
    "SH_Missed": "Toques Perdidos",
    "SHO": "Blanqueadas",
    "SF": "Sacrificios de Vuelo",
    "SLG": "Porcentaje de Slugging",
    "SPD": "Velocidad",
    "Strikepct": "% de Strikes",
    "Strikes": "Strikes",
    "SaveOpp": "Oportunidades de Salvamento",
    "SV": "Saves",
    "SVpct": "% de Saves",
    "Swings": "Swings Totales",
    "SwingMiss": "Swings y Misses",
    "SwingMisspct": "% de Swing y Falla",
    "Swstrpct": "% de Swinging Strikes",
    "TB": "Bases Totales",
    "TC": "Oportunidades Totales",
    "ThrE": "Errores de Lanzamiento",
    "TP": "Triples Plays",
    "UBR": "Ultra Base Running",
    "UZR": "Calificación de Zona Definitiva",
    "W": "Victorias",
    "WAR": "Victorias Sobre Reemplazo",
    "WHIP": "Caminantes e Hits por Inning",
    "WO": "Walk Offs",
    "WP": "Lanzamiento Descontrolado",
    "WStrk": "Racha de Victorias",
    "Winpct": "% de Victorias",
    "XH": "Extra bases",
    "X1B": "Sencillos",
    "X2B": "Dobles",
    "X3B": "Triples",
    "exLI": "Índice de Apalancamiento Esperado",
    "fmLI": "Índice de Apalancamiento del Lanzador Final",
    "gmLI": "Índice de Apalancamiento del Juego",
    "inLI": "Índice de Apalancamiento del Inning",
    "pLI": "Índice de Apalancamiento de Presión",
    "wGDP": "Bolas Dobles Ponderadas",
    "wLeague": "Liga Ponderada",
    "wOBA": "Embase Ponderado",
    "wRAA": "Carreras Ponderadas Sobre Promedio",
    "wRC": "Carreras Creadas Ponderadas",
    "wRCPlus": "Carreras Creadas Ponderadas Plus",
    "wSb": "Bases Robadas Ponderadas",
    "xAVG": "Promedio Esperado",
    "xFIP": "FIP Esperado",
    "xSLG": "Slugging Esperado",
    "xwOBA": "Embase Ponderado Esperado",
    "xwOBACON": "Embase Ponderado Esperado en Contacto",
}


def metric_abbreviation(metric: str) -> str:
    """
    Look up a metric name in STAT_TRANSLATIONS and return its abbreviation.
    Search is case-insensitive.

    Args:
        metric (str): The metric name to look up (camelCase format or any case)

    Returns:
        str: The abbreviation if found, otherwise returns the original metric string

    Example:
        metric_abbreviation("battingAverage") -> "AVG"
        metric_abbreviation("BattingAverage") -> "AVG"
        metric_abbreviation("unknownMetric") -> "unknownMetric"
    """
    # First try exact match
    if metric in STAT_TRANSLATIONS:
        return STAT_TRANSLATIONS[metric]

    # Then try case-insensitive match
    for key in STAT_TRANSLATIONS:
        if key.lower() == metric.lower():
            return STAT_TRANSLATIONS[key]

    # Return original if not found
    return metric


def abbrev_description_spanish(abbreviation: str) -> str:
    """
    Look up an abbreviation in STAT_SPANISH and return its Spanish description.
    Search is case-insensitive.

    Args:
        abbreviation (str): The abbreviation to look up

    Returns:
        str: The Spanish description if found, otherwise returns the original abbreviation

    Example:
        abbrev_description_spanish("AVG") -> "Promedio"
        abbrev_description_spanish("avg") -> "Promedio"
        abbrev_description_spanish("unknownAbbrev") -> "unknownAbbrev"
    """
    # First try exact match
    if abbreviation in STAT_SPANISH:
        return STAT_SPANISH[abbreviation]

    # Then try case-insensitive match
    for key in STAT_SPANISH:
        if key.lower() == abbreviation.lower():
            return STAT_SPANISH[key]

    # Return original if not found
    return abbreviation


def validate_translations() -> bool:
    """Validate abbreviation <-> Spanish consistency.

    Note: multiple field names intentionally map to the same abbreviation (aliases,
    e.g. ``avg``/``battingAverage`` -> ``AVG``), so duplicate abbreviations are NOT an
    error. What we actually guard against is drift between the two dictionaries:
      1. every produced abbreviation must have a Spanish description, and
      2. STAT_SPANISH must not contain orphan keys (typos) that match no abbreviation.
    Lookups are case-insensitive, so comparisons here are too.
    """
    abbrevs = {v.lower() for v in STAT_TRANSLATIONS.values()}
    spanish = {k.lower() for k in STAT_SPANISH}

    missing_spanish = sorted({v for v in STAT_TRANSLATIONS.values() if v.lower() not in spanish})
    orphan_spanish = sorted({k for k in STAT_SPANISH if k.lower() not in abbrevs})

    problems = []
    if missing_spanish:
        problems.append(f"Abbreviations without Spanish: {missing_spanish}")
    if orphan_spanish:
        problems.append(f"Orphan Spanish keys (no matching abbreviation): {orphan_spanish}")
    if problems:
        raise ValueError("; ".join(problems))
    return True


if __name__ == "__main__":
    validate_translations()
    print(f"[OK] Stats translation dictionary loaded: {len(STAT_TRANSLATIONS)} mappings")
    print(f"[OK] Spanish descriptions: {len(STAT_SPANISH)}")
    print("[OK] Abbreviation <-> Spanish consistency validated")
