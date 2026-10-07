"""301 map for legacy cebudavao.com URLs that are NOT recreated.

Default target is the homepage (keeps backlink equity, per the brief). Where a
retired URL is a near-duplicate of a recreated page, it points there instead
(SPECIFIC), and old category archives point at the matching new hub (CATEGORY).
build.py merges this with every URL in the Semrush export and writes
redirects.php; recreated paths (plan.LEGACY) are never redirected.
"""

SPECIFIC = {
 # festivals & events
 "/events/edsa-30th-anniversary/": "/events/what-is-edsa-revolution/",
 "/festivals/watch-sinulog-2016-live-stream/": "/festivals/what-makes-the-sinulog-2012-festival-the-number-one-festival-in-the-philippines/",
 # food near-duplicates
 "/food/kinilaw-na-malasugi-broadbill-swordfish-ceviche/": "/food/kinilaw-na-malasugi-davao-style/",
 "/food/tombo-tuna-kinilaw-for-breakfast/": "/food/kinilaw-na-malasugi-davao-style/",
 "/food/grilled-tuna-belly-and-tuna-kinilaw-with-coconut-milk/": "/food/kinilaw-na-malasugi-davao-style/",
 "/food/fried-bangus-milkfish-with-tomato-sauce-and-eggplant/": "/food/inihaw-na-bangus-or-sinugbang-bangus-grilled-milkfish/",
 "/food/planting-thai-basil-in-philippines/": "/food/how-to-grow-basil-in-the-philippines/",
 "/food/planting-habanero-chili-peppers-davao-2/": "/food/how-to-grow-basil-in-the-philippines/",
 "/food/greet-and-taste-davao-delicacies-the-durian-style/": "/food/davao-durian-guide/",
 "/food/top-5-popular-foods-cebu/": "/food/the-cheapest-and-most-delicious-food-in-cebu/",
 "/food/how-to-make-cebu-inasal-de-talisay/": "/food/secret-ingredients-of-cebu-lechon-revealed/",
 "/food/andoks-litson-in-cebu/": "/food/secret-ingredients-of-cebu-lechon-revealed/",
 "/food/eat-food-in-cebu-with-a-cellophane-glove/": "/food/the-cheapest-and-most-delicious-food-in-cebu/",
 "/food/maya-maya-red-snapper-with-tomato-sauce/": "/culture/cebus-and-davaos-different-fish/",
 "/food/sabaw-na-ulo-ng-maya-maya-plain-red-snapper-head-soup/": "/food/5-best-filipino-soups-to-eat-on-rainy-days/",
 "/food/tahong-soup-and-pritong-kitang/": "/food/5-best-filipino-soups-to-eat-on-rainy-days/",
 "/food/matangbaka-or-tamarong/": "/culture/cebus-and-davaos-different-fish/",
 "/food/streets-of-davao-and-greenwich-lasagna-supreme/": "/food/the-delectable-food-in-davao/",
 "/delicacies/": "/food/filipino-pasalubong-guide-cebu-davao/",
 "/restaurants-2/list-korean-restaurants-davao/": "/restaurants-2/top-ten-restaurants-in-davao/",
 "/restaurants-2/mandarin-tea-garden-at-sm-davao/": "/restaurants-2/top-ten-restaurants-in-davao/",
 "/restaurants-2/satisfying-night-at-casa-verde-restaurant/": "/restaurants-2/top-ten-restaurants-in-davao/",
 "/restaurants-2/taste-zubuchon-review/": "/food/secret-ingredients-of-cebu-lechon-revealed/",
 # language & culture
 "/culture/meaning-hanep-english/": "/tools/bisaya-dictionary/",
 "/culture/meaning-hinuktok-english/": "/tools/bisaya-dictionary/",
 "/culture/meaning-of-purbida-or-porbida/": "/tools/bisaya-dictionary/",
 "/word-meanings/meaning-of-sago-in-english/": "/tools/bisaya-dictionary/",
 "/culture/decoding-the-dude-the-davao-guy-versus-the-cebu-city-guy/": "/travel/destinations/cebu-and-davao-their-differences/",
 "/culture/interesting-abaca-for-an-old-lady/": "/culture/indigenous-tribes-of-davao/",
 # music
 "/music/list-pinoy-new-wave-bands/": "/music/complete-list-of-rock-bands-and-pop-bands-in-the-philippines-from-the-60s-to-present/",
 "/music/list-of-filipino-rock-songs-you-think-are-original/": "/music/complete-list-of-rock-bands-and-pop-bands-in-the-philippines-from-the-60s-to-present/",
 "/personal/the-music-of-the-80s-nostalgia-of-new-wave-era/": "/music/complete-list-of-rock-bands-and-pop-bands-in-the-philippines-from-the-60s-to-present/",
 "/music/blitzkrieg-reunion-generation-x-makes-davao-rock-scene-original/": "/music/complete-list-of-bisrock-bands/",
 "/music/pinatikay-sa-kugsik-with-ian-tayao-of-queso/": "/music/complete-list-of-rock-bands-and-pop-bands-in-the-philippines-from-the-60s-to-present/",
 "/davao-and-cebu-music/": "/music/complete-list-of-bisrock-bands/",
 "/events/a-great-night-at-mts-with-urbandub-and-powerspoonz/": "/music/complete-list-of-bisrock-bands/",
 # travel near-duplicates
 "/beach/rosal-beach/": "/beach/en-route-to-the-real-beaches-of-davao-3/",
 "/beach/trip-to-samal-highlands-garden-resort/": "/beach/list-of-resort-destinations-in-davao/",
 "/photo-gallery-samal-highlands-garden-resort/": "/beach/list-of-resort-destinations-in-davao/",
 "/resorts/davao-resorts/": "/beach/list-of-resort-destinations-in-davao/",
 "/beach-resorts/": "/beach/list-of-resort-destinations-in-davao/",
 "/beach-resorts/paradise-island-resort-davao-complete-information/": "/beach/paradise-resort/",
 "/photo-albums/paradise-island-resort-pictures/": "/beach/paradise-resort/",
 "/travel/tips/how-to-reach-pearl-farm-beach-resort/": "/beach/pearl-farm-davao/",
 "/resorts/paradisiacal-isla-reta-beach-resort/": "/travel/tips/how-to-go-to-isla-reta-beach-resort/",
 "/travel/destinations/wind-and-wave-davao-brought-us-to-talikud-island/": "/travel/tips/how-to-go-to-isla-reta-beach-resort/",
 "/travel/tips/how-to-get-to-buenavista-island/": "/beach/list-of-resort-destinations-in-davao/",
 "/travel/davao-tourists-spots/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/davao-tourism-places-you-want-to-go/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/destinations/attractions-davao-less-visited/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/destinations/garden-of-eden-in-davao/": "/travel/tips/how-to-get-to-eden-nature-park/",
 "/travel/tips/how-to-get-to-japanese-tunnel/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/tips/how-to-get-to-abreeza-mall/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/destinations/turning-back-the-clock-at-st-francis-xavier-seminary-and-catalunan-grande-river/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/hilltop-site-of-catalunan-grande-seminary-is-now-privately-owned/": "/travel/destinations/top-ten-summer-destinations-in-davao/",
 "/travel/black-taxis-in-davao/": "/travel/taxi-procedure-davao-international-airport/",
 "/hotels/davao-hotels/": "/hotels/hotels-in-davao-under-1000-pesos-a-night/",
 "/hotels/insular-hotel-davao/": "/hotels/hotels-in-davao-under-1000-pesos-a-night/",
 "/travel/destinations/top-ten-summer-destinations-in-cebu/": "/travel/destinations/cebu-tourist-spots/",
 "/travel/tips/how-to-reach-tops-in-cebu-without-paying-a-hundred-peso-bill/": "/travel/destinations/cebu-tourist-spots/",
 "/travel/tips/how-to-get-to-crown-regency-hotel-cebu-to-experience-skywalk-adventure/": "/travel/destinations/cebu-tourist-spots/",
 "/travel/tips/five-things-you-should-know-before-roaming-the-streets-of-cebu/": "/travel/destinations/cebu-tourist-spots/",
 "/travel/tips/how-to-reach-fort-san-pedro/": "/travel/tips/how-to-get-to-magellans-cross/",
 "/travel/destinations/cebu-church-invasion/": "/travel/tips/how-to-get-to-magellans-cross/",
 "/beach/vano-beach-in-mactan/": "/travel/tips/how-to-get-to-plantation-bay-in-mactan/",
 "/resorts/imperial-palace-cebu/": "/travel/tips/how-to-get-to-plantation-bay-in-mactan/",
 "/travel/tips/how-to-get-to-boracay-island-from-bantayan-island/": "/travel/tips/sea-travel-from-cebu-to-boracay/",
 "/travel/tips/travel-from-butuan-to-cebu-by-land-sea-and-air/": "/travel/tips/how-to-reach-cebu-from-davao-by-land/",
 "/travel/tips/how-to-get-to-cebu-from-iligan-city/": "/travel/tips/how-to-reach-cebu-from-davao-by-land/",
 "/travel/anti-tanim-bala-luggage-can-now-be-bought-in-malls/": "/travel/baggage-items-allowed-and-prohibited-on-a-flight-by-the-tsa/",
 "/cebu-pacific-promos/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/airphil-express-latest-promo-888-pesos/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/cebu-pacific-cheap-flights-promo-eighto-na/amp/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/cebu-pacific-new-promo-pinyakamura/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/cebu-pacifics-288-pesos-for-domestic-flights-and-888-pesos-for-international-flights/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/cebu-pacifics-flight-promo-from-mindanao-to-manila-only-1299-pesos/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/cheap-flights-cebu-pacific-latest-promo-only-199-pesos-flight-from-cebu-to-davao/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/cebu-pacific-flights-change-terminals-at-naia/": "/travel/flights-travel/cheap-flights-in-the-philippines/",
 "/travel/flights-travel/touchdown-davao-from-airphil-express/": "/travel/flights-travel/philippine-airlines-history/",
 # money & work
 "/real-estate/cebu-pension-house/": "/real-estate/apartments-for-rent-in-cebu/",
 "/travel/tips/how-to-land-a-job-in-cebu/amp/": "/jobs/updated-list-of-call-centers-in-cebu/",
 "/jobs/job-vacancies-and-openings-at-nccc-davao/": "/travel/tips/find-jobs-in-davao/",
 "/finance/bpi-not-affiliated-with-paypal/": "/finance/bpi-atm-card-blocked-after-entering-correct-pin-three-times/",
 "/technology/smart-bro-internet-is-it-really-smarter/": "/tech/best-internet-providers-cebu-davao/",
 "/technology/smart-bro-unlisurf-50-is-now-unlisurf-60/": "/tech/best-internet-providers-cebu-davao/",
 "/technology/how-installers-set-up-smart-bro-canopy-wireless-broadband-internet/": "/tech/best-internet-providers-cebu-davao/",
 "/technology/smart-bro-gets-into-my-nerves/": "/tech/best-internet-providers-cebu-davao/",
 # news sources
 "/news/cebu-daily-news/": "/news/superbalita-cebu/",
 "/news-updates/": "/news/",
 "/news/is-cebu-island-vulnerable-to-tsunami-shame-on-phivolcs/": "/news/pagasa-typhoon-signals-explained/",
 "/world-news/huge-cyclone-hits-tacloban-city-leytehuge-tornado-hits-tacloban-city-leyte/": "/news/pagasa-typhoon-signals-explained/",
 # sports
 "/sports/did-mayweather-illegally-take-an-iv-injection-before-the-pacquiao-fight/": "/sports/cebu-davao-boxing-legends/",
 "/sports/manny-pacquiao-wins-unanimous-decision-versus-bradley/": "/sports/cebu-davao-boxing-legends/",
 "/sports/filipino-boxer-knocks-pakistani-one-championship-champion/": "/sports/cebu-davao-boxing-legends/",
 "/sports/gilas-pilipinas-vs-lebanon-live-streaming/": "/sports/basketball-in-the-philippines-pba-uaap-mpbl/",
 "/sports/ginebra-vs-san-miguel-game-5-live-streaming/": "/sports/basketball-in-the-philippines-pba-uaap-mpbl/",
 "/technology/duterte-plays-basketball-for-gilas-pilipinas-in-video-game-simulation/": "/sports/basketball-in-the-philippines-pba-uaap-mpbl/",
 # quizzes & misc
 "/fun-quizzes/fun-quiz-who-are-the-beautiful-women-in-the-philippines/": "/fun-quizzes/name-these-philippine-travel-destinations/",
 "/movies/look-could-she-be-the-next-darna/": "/category/entertainment/",
 "/contact/": None,          # recreated as a page (never redirected)
 "/2-the-chameleons-tears/": "/",
 # old WordPress (2023-2025 install) archive URLs
 "/home/": "/",
 "/category/articles/": "/category/expat-living/",
 "/category/popular/": "/category/expat-living/",
 "/author/brandy/": "/category/expat-living/",
 "/comments/feed/": "/feed/",
}

# Old category archives (2017 site) -> new hubs. Paginated variants follow the base.
CATEGORY = {
 "books": "/category/lifestyle/", "business": "/category/money/", "culture": "/category/culture/",
 "entertainment": "/category/entertainment/", "festivals": "/tools/festival-calendar/",
 "hotels": "/category/travel/", "movies": "/category/entertainment/", "resorts": "/category/travel/",
 "sports": None,  # same URL exists in the new site
 "pcso-lotto-results": "/",
}

# First path segments of the 2017 site; a bare "/food/" etc. goes to the hub.
SECTION_HUB = {
 "food": "/category/food/", "travel": "/category/travel/", "culture": "/category/culture/",
 "music": "/category/entertainment/", "movies": "/category/entertainment/", "entertainment": "/category/entertainment/",
 "sports": "/category/sports/", "news": "/news/", "technology": "/category/tech/", "tech": "/category/tech/",
 "beach": "/category/travel/", "hotels": "/category/travel/", "events": "/category/culture/",
 "festivals": "/category/culture/", "finance": "/category/money/", "real-estate": "/category/money/",
 "jobs": "/category/money/", "word-meanings": "/tools/bisaya-dictionary/", "lifestyle": "/category/lifestyle/",
 "health": "/category/lifestyle/", "books": "/category/lifestyle/",
}
