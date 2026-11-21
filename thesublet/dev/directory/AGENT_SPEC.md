# Directory data collection spec

For EACH city in your list, call the MCP tool `mcp__Data_for_seo__business_data_business_listings_search` (load it first with ToolSearch query "select:mcp__Data_for_seo__business_data_business_listings_search") with EXACTLY these params (no `description`, no `title`, no `filters`):

  categories: ["extended_stay_hotel","furnished_apartment_building","corporate_housing","short_term_apartment_rental_agency","serviced_apartment","student_housing_center"]
  location_coordinate: "<lat>,<lng>,<radius>"   (given in your list)
  limit: 100

Each call returns up to 10 businesses. Two possible outcomes:

A) The tool says the output was too large and saved it to a file (a path under /root/.claude/projects/.../tool-results/). Then just append ONE line to your paths file:
   echo "<city-key> <full path>" >> /home/user/seotool/thesublet/dev/directory/paths-<BATCH>.txt
   Do NOT read the file.

B) The JSON is returned inline. Then transcribe every item EXACTLY (copy values verbatim, never guess or invent; omit a field if missing) into JSON lines appended to
   /home/user/seotool/thesublet/dev/directory/raw-<BATCH>.jsonl
   using a small python3 script (json.dumps per line, ensure_ascii=False). Fields per item:
   key (the city key), cid, place_id, title, category, category_ids (list), description (first 500 chars), address, city (address_info.city), zip, region, borough (address_info.borough), lat (latitude), lng (longitude), phone, url, domain, rating (rating.value), votes (rating.votes_count), status (work_time.work_hours.current_status if present), is_claimed

Process cities one at a time; after each, write the data before moving on. Do not create or edit any other files. When done, reply with one line: how many cities went to paths vs raw, and any errors.
