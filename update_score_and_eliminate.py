def update_score_and_eliminate(scores, players_missed):
    """Updates the letter totals of players and eliminates any player who 
    reaches all five letters.
    
    Parameters: 
        scores (dict): maps the player names to how many letters they currently 
        have. (ex. {"Danny": 3, "Ava": 5})
        
        players_missed (str): name of the player who missed the spoon each round.
        
    Returns:
        tuple: (updated_scores, eliminated_players)
        
            updated_scores (dict): the remaining players with their updated
            letter counts.
            
            eliminated_players (list): the list of players who were removed each
            round.
    """
    
    scores[players_missed] += 1
    eliminated_players = []
    
    for player, letters in list(scores.items()):
        if letters >= 5:
            eliminated_players.append(player)
            del scores[player]
            
    return scores, eliminated_players




# test
if __name__ == "__main__":
    test_scores = {"P1": 0, "P2": 3, "P3": 4}
    updated, eliminated = update_score_and_eliminate(test_scores, "P3")
    
    print("Updated:", updated)
    print("Eliminated:", eliminated)
    

    