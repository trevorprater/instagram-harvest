INSERT INTO photo
    (id, pcode, owner_id, location_id, caption, likes, comments, created, updated, is_vid, url)
    VALUES
        (554387665870799357, 'exlKUUFkH9', 332896423, -1, 'Wedding planning in Wine Country calls for... Starbucks!!! #weddingplanning #ilovestarbucks #mmmsooogood #coffee', 9, 3, 1380308181, 1470193990, False, 'https://scontent-lga3-1.cdninstagram.com/t51.2885-15/e15/11313436_1609740032645028_1415927269_n.jpg?ig_cache_key=NTU0Mzg3NjY1ODcwNzk5MzU3.2')
        ON
            CONFLICT (id)
            DO UPDATE SET
                pcode = EXCLUDED.pcode,
                location_id = EXCLUDED.location_id,
                caption = EXCLUDED.caption,
                likes = EXCLUDED.likes,
                comments = EXCLUDED.comments,
                created = EXCLUDED.created,
                updated = EXCLUDED.updated,
                is_vid = EXCLUDED.is_vid,
                url = EXCLUDED.URL;

