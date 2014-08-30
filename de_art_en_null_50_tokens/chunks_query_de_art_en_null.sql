SELECT range_de, string_before_de, my_chunk_de::text, tags_de, string_after_de, range_en, string_before_en, my_chunk_en::text, tags_en, string_after_en  FROM
(
SELECT *, rtrim(split_part(s_de::text ,my_chunk_de::text ,1))AS string_before_de, ltrim(split_part(s_de::text ,my_chunk_de::text ,2)) AS string_after_de, rtrim(split_part(s_en::text ,my_chunk_en::text ,1))AS string_before_en, ltrim(split_part(s_en::text ,my_chunk_en::text ,2)) AS string_after_en
FROM
       
(
SELECT *, array_length((europarl2.get_sentence_by_range_id3(range_de)).token_ids, 1) as len_sent_de, array_length((europarl2.get_sentence_by_range_id3(range_en)).token_ids, 1) as len_sent_en,
  (europarl2.get_sentence_by_range_id3(range_en)).s as s_en, (europarl2.get_sentence_by_range_id3(range_de)).s as s_de
FROM
(
SELECT * FROM
(
       SELECT 
               europarl2.get_range_id_by_token(c_en.token_ids[1]) range_en,
               europarl2.get_range_id_by_token(c_de.token_ids[1]) range_de,
               chunk_en,
               chunk_de,
               europarl2.token_ids_to_string(c_en.token_ids) my_chunk_en,
               europarl2.token_ids_to_tags(c_en.token_ids) tags_en,
               europarl2.token_ids_to_string(c_de.token_ids) my_chunk_de,
               europarl2.token_ids_to_tags(c_de.token_ids) tags_de
       FROM europarl2.aligned_np_chunks_ende
       LEFT JOIN europarl2.chunk c_en ON c_en.chunk_id = chunk_en
       LEFT JOIN europarl2.chunk c_de ON c_de.chunk_id = chunk_de
 ) z
       
WHERE tags_de @> ARRAY['ART']::varchar[]
AND NOT tags_en @> ARRAY['DT']::varchar[]
LIMIT 500

) x
--AND tags_en[1] != 'DT'
--AND LOWER(substring(my_chunk_de from 1 for 3)) IN('die', 'der', 'das', 'dem', 'den', 'des')
WHERE range_en IS NOT NULL
AND range_de IS NOT NULL
-- ### ignore genitiv:
--AND NOT my_chunk_en LIKE E'% ''s'
---### ignore possesiv pronouns:
--AND NOT LOWER(substring(my_chunk_en from 1 for 3)) IN('our', 'its')
limit 400)
AS my_table
WHERE len_sent_en <=50
AND len_sent_de <=50
AND NOT (abs(range_en - range_de))  > 20
-- ### If we want to be more sure of the alignment:
AND NOT len_sent_en > len_sent_de *2
AND NOT len_sent_de > len_sent_en *2
AND split_part(s_de::text ,chunk_de::text ,3) = ''
AND split_part(s_en::text ,chunk_en::text ,3) = ''
LIMIT 10)
AS chunks_in_s
ORDER BY my_chunk_de