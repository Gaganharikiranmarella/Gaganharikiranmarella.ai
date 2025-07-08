def assign_ids(t_frame, tacticam_feats, matches):
    for tac_idx, brd_idx in matches:
        player_id = f"player_{brd_idx}"
        tacticam_feats[tac_idx]["player_id"] = player_id
    return t_frame
