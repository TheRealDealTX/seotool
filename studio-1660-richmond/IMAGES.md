# Image inventory: Studio at 1660 Richmond concept site

Every image is stored as WebP at three widths in `src/img/`: `KEY-500.webp`, `KEY-900.webp` and `KEY-1600.webp`. When the original is narrower than 1,600 px (three of the property photos are 1,024 px wide), the `-1600` file keeps the original width and the `srcset` lists its real width. Source images were never upscaled.

**Property photos** come from the property's own listing materials: the photos on Fat Property's building page and Unit 01 listing (fatproperty.com), and the photo the property submitted to its Rise Apartments listing (same image as `court-screen`). The property submitted them, so they're fine for this pitch.

**Stock photos** are from Pexels under the Pexels License (free to use, no attribution required). They are used only for neighborhood atmosphere and are labeled "representative photo" in the gallery. No images from Zillow, Apartments.com or Google were used. Unsplash wasn't used: it served an automated-access challenge, so the build didn't try to get around it.

| Key | Category | Source | Where it appears | Alt text |
|---|---|---|---|---|
| `court-deck` | community | Fat Property listing, 1660 Richmond Ave #01 (fatproperty.com/listings/1660-richmond-avenue-01/) (original file `fp-a212ce03f371.jpg`) | Home, Amenities, Gallery | Courtyard at Studio at 1660 Richmond with a curved wood deck, palms and tropical plantings between two-story buildings |
| `court-screen` | community | Fat Property building page (fatproperty.com/properties/1660-richmond/); same photo submitted to the Rise Apartments listing (original file `fp-building.jpg`) | Home, Gallery, Apply | Central courtyard with a mid-century brick screen wall, palms and open-air stairs |
| `court-lawn` | community | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-a6a683df2156.jpg`) | Home, Amenities, Gallery | Garden courtyard lawn framed by brick edging, shrubs and second-floor walkways |
| `walkway` | community | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-ddf0fe2e62f7.jpg`) | Home, Gallery, Residents | Wood boardwalk through the landscaped courtyard toward the blue front doors |
| `studio-living` | interiors | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-3aac8f6c815c.jpg`) | Home, The Studios, Gallery | Studio living area with dark plank-tile floors, ceiling fan and an open kitchen by the front door |
| `studio-room` | interiors | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-3d128f00cc47.jpg`) | Gallery | Bright main room of a studio with ceiling fan and wall A/C unit |
| `studio-window` | interiors | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-65dc21c60790.jpg`) | The Studios, Gallery | Studio main room with window, ceiling fan and doorway to the bath |
| `studio-closet` | interiors | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-e4e7b7f8b79a.jpg`) | Home, The Studios, Gallery | Studio interior with a large open closet, front door and kitchen beyond |
| `studio-bar` | interiors | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-fd970d1aeced.jpg`) | Home, The Studios, Gallery | Studio with a breakfast-bar counter, built-in cabinets and natural light |
| `kitchen-galley` | kitchens | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-989e0ea97ef8.jpg`) | Home, The Studios, Gallery | Galley kitchen with white cabinetry, electric range and double sink |
| `kitchen-counter` | kitchens | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-d41509e86fef.jpg`) | The Studios, Gallery | Kitchen with tile counters, cooktop, pantry cabinets and refrigerator |
| `kitchen-upgraded` | kitchens | Fat Property listing, 1660 Richmond Ave #01 (likely an upgraded-unit example; confirm which unit) (original file `fp-08c941420f98.jpg`) | Home, Amenities, Gallery | Upgraded kitchen finish with painted cabinets, granite counters and stainless appliances |
| `bath` | interiors | Fat Property listing, 1660 Richmond Ave #01 (original file `fp-a947c7e62409.jpg`) | The Studios, Gallery | Full bathroom with tub and shower combination and vanity window |
| `skyline` | neighborhood | Pexels photo 18441167 (Erik Mclean), Pexels License (original file `px-18441167.jpg`) | Home, Gallery, Neighborhood | Downtown Houston skyline lit up at night |
| `mural` | neighborhood | Pexels photo 1253951, Pexels License (generic, not a specific Montrose location) (original file `px-1253951.jpg`) | Gallery | Colorful hand-painted mural above café stools |
| `coffee` | neighborhood | Pexels photo 38702181 (Eddie O), Pexels License (original file `px-38702181.jpg`) | Gallery, Neighborhood | Warm coffee bar counter in a Houston café |
| `museum` | neighborhood | Pexels photo 26424659, Pexels License (generic museum, not the Menil) (original file `px-26424659.jpg`) | Home, Gallery, Neighborhood | Visitors exploring paintings in a bright white art museum gallery |
| `bartender` | neighborhood | Pexels photo 10375843, Pexels License (original file `px-10375843.jpg`) | Home, Gallery | Bartender serving a guest at a lively neighborhood bar |
| `cocktail-bar` | neighborhood | Pexels photo 5490965 (Rachel Claire), Pexels License (original file `px-5490965.jpg`) | Gallery | Moody cocktail bar with pendant lights and backlit shelves |
| `dog-walk` | neighborhood | Pexels photo 18565007 (Sofía Marquet), Pexels License (original file `px-18565007.jpg`) | Home, Gallery | Resident walking a dog past a storefront on a sunny sidewalk |

Hero slides on the homepage: `court-deck` (slide 1, preloaded LCP image), `court-screen` (slide 2) and `court-lawn` (slide 3).
Open Graph images: each page's `og:image` uses the hero photo for that page (default `court-deck`).

## Replacing photos

When the owner sends new photos, add them to `images.json` and run:

```bash
python3 -c "from PIL import Image; im=Image.open('photo.jpg').convert('RGB'); [ (im if w>=im.width else im.resize((w,round(im.height*w/im.width)))).save(f'src/img/KEY-{w}.webp',quality=64) for w in (500,900,1600)]"
```

Use a new key (file name) for a replaced photo so the CDN serves it right away; images are cached for a long time.
