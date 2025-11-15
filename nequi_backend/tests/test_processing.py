from app.services.processing import filter_inappropriate, build_metadata

#Censura palabras prohibidas.
def test_filter_inappropriate_masks_banned_words():
    is_clean, filtered = filter_inappropriate("hola insulto mundo")
    assert is_clean is False
    assert "insulto" not in filtered
    assert "*****" in filtered  # masked length equals


#Genera estadísticas correctas.
def test_build_metadata_counts_words_and_chars():
    md = build_metadata("Hola mundo bonito")
    assert md["word_count"] == 3
    assert md["character_count"] == len("Hola mundo bonito")
    assert "processed_at" in md
