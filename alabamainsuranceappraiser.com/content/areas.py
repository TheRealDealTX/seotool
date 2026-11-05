"""/service-areas/ hub and one page per city. Keyword: "insurance appraiser <city> AL"."""

from components import (BIZ, CITIES, SERVICES, btn, callout, card, checklist, fig, faq_html, faq_schema, grid,
                        icon, related_links, section_head, service_schema, url)

A = {
    "birmingham-al": dict(
        county="Jefferson County", region="Central Alabama", img="storm",
        communities=["Homewood", "Mountain Brook", "Vestavia Hills", "Hoover", "Trussville", "Bessemer", "Center Point", "Irondale", "Pelham", "Gardendale"],
        hoods=["Southside", "Forest Park", "Crestwood", "Avondale", "Highland Park", "Redmont", "Roebuck", "Pratt City"],
        risks=[("hail", "Hail", "Spring hailstorms regularly push across the metro, damaging shingles, gutters and soft metals from Bessemer to Trussville."),
               ("storm", "Tornadoes", "The April 27, 2011 outbreak tore through Pratt City and Pleasant Grove, and spring and fall tornado watches are routine."),
               ("droplets", "Water losses", "Older housing stock means aging supply lines, cast-iron drains and roof leaks behind many interior claims."),
               ("building", "Commercial", "Downtown, Southside and the US-280 corridor carry office, medical, retail and multi-family risk.")],
        intro="Birmingham is the state's largest metro and one of its busiest claim markets. Hail, tornadoes and severe thunderstorms hit the Magic City and its suburbs every year, and the mix of century-old homes, mid-century neighborhoods and new construction means no two roof or interior losses price the same way.",
        local="Many Birmingham neighborhoods &mdash; Forest Park, Crestwood, Highland Park &mdash; are full of older homes with plaster walls, original hardwood, steep roofs and architectural details that standard estimates often under-scope. Steep-slope and two-story charges, plaster repair, matching of discontinued materials and the cost of working on hillside lots are recurring points of disagreement.",
        faqs=[("Do you inspect properties inside Birmingham city limits and the suburbs?", "<p>Yes. We cover all of Jefferson County and the surrounding metro, including Shelby, St. Clair and Walker county communities.</p>"),
              ("Are older Birmingham homes harder to appraise?", "<p>They take more care. Plaster, old-growth wood trim, slate or older shingles and steep roofs need line items many estimates leave out.</p>")]),
    "huntsville-al": dict(
        county="Madison County", region="North Alabama / Tennessee Valley", img="roof",
        communities=["Madison", "Harvest", "Meridianville", "Hazel Green", "Owens Cross Roads", "New Market", "Toney", "Gurley"],
        hoods=["Hampton Cove", "Jones Valley", "Five Points", "Twickenham", "Blossomwood", "Providence", "Monte Sano", "South Huntsville"],
        risks=[("hail", "Hail", "The Tennessee Valley is one of Alabama's most active hail areas, and large-hail days can damage thousands of roofs in an afternoon."),
               ("storm", "Tornadoes", "Supercells crossing North Alabama in spring and late fall bring tornado and straight-line wind damage."),
               ("home", "New construction", "Rapid growth means many newer homes with architectural shingles, vinyl siding and open floor plans."),
               ("building", "Commercial &amp; tech", "Research Park, the Redstone corridor and new retail and multi-family developments.")],
        intro="Huntsville and Madison County are growing faster than almost anywhere in the Southeast, and the Tennessee Valley's hail and tornado season makes for a steady stream of property claims. A single spring storm can leave entire subdivisions waiting on roof claims.",
        local="Newer Huntsville subdivisions often share the same builder-grade shingle line and siding color. After a hailstorm, that helps establish damage patterns &mdash; but it also creates matching disputes when a product has been discontinued. Open floor plans also make continuous-flooring and paint-scope questions common on interior claims.",
        faqs=[("Do you cover Madison, Harvest and Hampton Cove?", "<p>Yes, along with the rest of Madison County and nearby Limestone and Marshall county communities.</p>"),
              ("Is hail damage on a newer roof still worth disputing?", "<p>Yes. Newer roofs carry less depreciation, so a properly scoped replacement can be worth significantly more than a repair estimate.</p>")]),
    "montgomery-al": dict(
        county="Montgomery County", region="Central Alabama / River Region", img="residential",
        communities=["Prattville", "Millbrook", "Pike Road", "Wetumpka", "Deatsville", "Hope Hull", "Elmore", "Tallassee"],
        hoods=["Old Cloverdale", "Cloverdale", "Garden District", "Dalraida", "Halcyon", "Vaughn Meadows", "Arrowhead", "Capitol Heights"],
        risks=[("storm", "Severe storms &amp; tornadoes", "The River Region sits in the heart of Dixie Alley's spring and fall severe-weather season."),
               ("wind", "Tropical remnants", "Hurricanes weakening inland can still bring damaging gusts and heavy rain to the capital."),
               ("home", "Historic homes", "Old Cloverdale and the Garden District have older homes with materials that are costly to match."),
               ("building", "Government &amp; commercial", "Downtown offices, churches, schools and retail across the River Region.")],
        intro="Montgomery and the River Region see the full range of Alabama weather: spring tornado outbreaks, summer thunderstorms with straight-line winds, and the inland remains of Gulf hurricanes. The capital's housing stock runs from historic Old Cloverdale homes to new construction in Pike Road and Prattville.",
        local="Historic homes in the Garden District and Cloverdale often have wood siding, original windows, plaster and specialty roofing that carry higher repair costs and specific methods. Matching and code requirements frequently come up when only part of an older building is damaged.",
        faqs=[("Do you cover Prattville and Millbrook?", "<p>Yes &mdash; all of Montgomery, Autauga and Elmore counties, and the rest of Central Alabama.</p>"),
              ("Can tropical storm damage in Montgomery trigger a hurricane deductible?", "<p>It depends on the policy definition. Some hurricane deductibles apply to any damage during a named storm, even inland. Check your declarations page.</p>")]),
    "mobile-al": dict(
        county="Mobile County", region="Gulf Coast", img="flood",
        communities=["Daphne", "Spanish Fort", "Fairhope", "Saraland", "Satsuma", "Semmes", "Theodore", "Tillmans Corner", "Grand Bay", "Dauphin Island"],
        hoods=["Midtown", "Oakleigh Garden District", "De Tonti Square", "Spring Hill", "West Mobile", "Leinkauf", "Ashland Place", "Downtown"],
        risks=[("umbrella", "Hurricanes", "Frederic, Ivan, Katrina and Sally all left their mark on Mobile and Baldwin counties."),
               ("wind", "Wind &amp; named-storm deductibles", "Percentage deductibles and separate wind policies complicate coastal claims."),
               ("droplets", "Wind-driven rain", "Storm-created openings lead to interior water damage that's often disputed as flood."),
               ("building", "Commercial &amp; port", "Port, industrial, hospitality and multi-family property along the Bay.")],
        intro="Mobile and the Alabama Gulf Coast face the state's highest hurricane exposure. Coastal policies are more complicated, too: percentage named-storm deductibles, separate wind coverage through the Alabama Insurance Underwriting Association (the coastal wind pool) for some properties, and flood coverage under yet another policy.",
        local="On Gulf Coast claims, sorting wind damage from flood damage is often the central fight. So is the size of the named-storm deductible, which is measured against the dwelling limit rather than the loss. Historic homes in Oakleigh, De Tonti Square and Midtown add slate, wood windows and plaster to the scope. Getting the wind portion of the loss fully documented is essential.",
        faqs=[("Do you work with Alabama wind pool (AIUA) claims?", "<p>Yes. If your wind coverage is through the Alabama Insurance Underwriting Association, appraisal rights and procedures come from that policy, and we work within them.</p>"),
              ("Do you cover Baldwin County?", "<p>Yes &mdash; Daphne, Spanish Fort, Fairhope, Foley, Gulf Shores, Orange Beach and the rest of the Eastern Shore and coast.</p>")]),
    "tuscaloosa-al": dict(
        county="Tuscaloosa County", region="West Alabama", img="storm",
        communities=["Northport", "Cottondale", "Coaling", "Brookwood", "Vance", "Lake View", "Moundville", "Duncanville"],
        hoods=["Alberta City", "Forest Lake", "Downtown", "Holt", "Glendale Gardens", "Woodland Forrest", "Lake Tuscaloosa"],
        risks=[("storm", "Tornadoes", "The April 27, 2011 EF4 tornado carved a path through Alberta City and Holt; the area remains tornado-prone."),
               ("users", "Student &amp; rental housing", "The University of Alabama drives a large stock of rentals, duplexes and apartment complexes."),
               ("hail", "Hail &amp; wind", "Spring storms bring hail and damaging wind across West Alabama."),
               ("droplets", "Water losses", "Lake and river properties and older homes see water and plumbing claims.")],
        intro="Tuscaloosa knows severe weather. The 2011 tornado reshaped whole neighborhoods, and spring storms still bring tornado warnings, hail and damaging wind to the city and its neighbors. With the University of Alabama in town, a large share of claims involve rental homes and multi-family property.",
        local="Investment and rental properties raise their own issues: landlord policies, loss of rents coverage, multiple units with the same damage, and tenants who need access coordinated. For apartment complexes and student housing, documenting each unit and building separately keeps the appraisal organized.",
        faqs=[("Do you handle claims for rental and student housing?", "<p>Yes. We work with individual landlords, property managers and apartment owners across Tuscaloosa and Northport.</p>"),
              ("Can appraisal include loss of rents?", "<p>Some policies allow appraisal of any amount-of-loss dispute, including loss of rents. It depends on the policy wording.</p>")]),
    "hoover-al": dict(
        county="Jefferson and Shelby counties", region="Birmingham metro", img="home",
        communities=["Vestavia Hills", "Pelham", "Helena", "Alabaster", "Bessemer", "Homewood", "Chelsea", "Indian Springs"],
        hoods=["Ross Bridge", "Riverchase", "Greystone", "Trace Crossings", "Bluff Park", "Lake Cyrus", "Inverness", "Brock's Gap"],
        risks=[("hail", "Hail", "Hoover's location on the southern edge of the metro puts it in the path of frequent spring hail."),
               ("home", "Larger homes", "Large two-story homes with complex roof lines raise steep, high and waste-factor questions."),
               ("storm", "Wind &amp; tornadoes", "Severe thunderstorms and tornadoes cross the Cahaba valley each year."),
               ("building", "Retail &amp; office", "Riverchase Galleria, US-31 and the I-459 corridor carry major commercial exposure.")],
        intro="Hoover straddles Jefferson and Shelby counties and is home to some of the Birmingham area's largest residential neighborhoods. Bigger homes with complex roof designs mean bigger roof claims &mdash; and more places for an estimate to go wrong.",
        local="Neighborhoods such as Ross Bridge, Greystone and Lake Cyrus feature steep, cut-up roofs with many hips, valleys and dormers. Those features raise the waste factor and add flashing, ridge and valley materials that quick estimates often leave out. Two-story elevations also carry access and high-roof charges.",
        faqs=[("Do you cover both the Jefferson and Shelby county sides of Hoover?", "<p>Yes, and the rest of Shelby County including Pelham, Helena, Alabaster and Chelsea.</p>"),
              ("Why does roof complexity matter so much?", "<p>Hips, valleys and dormers increase waste, labor and accessory materials. Try our <a href='/tools/roof-square-calculator/'>Roof Square Calculator</a> to see the effect.</p>")]),
    "auburn-al": dict(
        county="Lee County", region="East Alabama", img="storm",
        communities=["Opelika", "Smiths Station", "Beauregard", "Loachapoka", "Notasulga", "Waverly", "Salem", "Phenix City"],
        hoods=["Downtown Auburn", "Moores Mill", "Cary Woods", "Asheton Lakes", "Yarbrough Farms", "Grove Hill", "Camden Ridge"],
        risks=[("storm", "Tornadoes", "The March 3, 2019 EF4 tornado in Beauregard was a reminder of Lee County's tornado risk."),
               ("users", "Student housing", "Auburn University brings a large stock of rentals, condos and apartment complexes."),
               ("wind", "Tropical remnants", "Hurricanes moving north from the Gulf can bring strong wind and heavy rain to East Alabama."),
               ("hail", "Hail", "Spring hail affects roofs, gutters and vehicles across Auburn and Opelika.")],
        intro="Auburn and Opelika form one of Alabama's fastest-growing areas, and Lee County sees its share of severe weather &mdash; including the deadly 2019 Beauregard tornado. Between Auburn University rentals, new subdivisions and historic homes in Opelika, the claim mix is varied.",
        local="Rentals and condominiums near campus raise questions about which policy pays for what &mdash; the association's master policy or the unit owner's HO-6. Newer subdivisions around Auburn and Opelika often face matching problems after partial roof or siding damage.",
        faqs=[("Do you handle condo claims near campus?", "<p>Yes, for both unit owners and associations. We identify which items fall under the master policy and which under the unit owner's policy.</p>"),
              ("Do you cover Opelika and Phenix City?", "<p>Yes, along with all of Lee and Russell counties and the rest of East Alabama.</p>")]),
    "dothan-al": dict(
        county="Houston County", region="Wiregrass / Southeast Alabama", img="storm",
        communities=["Enterprise", "Ozark", "Headland", "Taylor", "Kinsey", "Cowarts", "Ashford", "Daleville"],
        hoods=["Downtown Dothan", "Westgate", "Honeysuckle Road", "Brannon Stand", "Kinsey Road", "the Ross Clark Circle corridor"],
        risks=[("umbrella", "Hurricanes", "Hurricane Michael in 2018 brought damaging wind deep into the Wiregrass."),
               ("storm", "Severe storms", "Tornadoes and straight-line wind accompany spring and tropical-season storms."),
               ("home", "Rural property", "Farm buildings, barns and outbuildings add other-structures coverage questions."),
               ("building", "Commercial &amp; agricultural", "Retail, medical and agricultural facilities across Southeast Alabama.")],
        intro="Dothan and the Wiregrass sit close enough to the Gulf that hurricanes remain a real threat &mdash; Hurricane Michael's 2018 wind damage across Houston County proved it. Add spring tornadoes and summer thunderstorms, and Southeast Alabama sees a wide variety of wind claims.",
        local="Rural properties around Dothan often include barns, shops, pole buildings and fencing, which may fall under other-structures coverage with its own limit. Metal roofing is common on these buildings, so functional-versus-cosmetic damage questions come up regularly after hail or wind.",
        faqs=[("Do you appraise farm buildings and outbuildings?", "<p>Yes, including metal shops, barns and pole buildings. Coverage limits for other structures vary, so we start with the policy.</p>"),
              ("Do you cover Enterprise and Ozark?", "<p>Yes &mdash; the whole Wiregrass, including Coffee, Dale, Henry and Geneva counties.</p>")]),
    "decatur-al": dict(
        county="Morgan County", region="North Alabama / Tennessee Valley", img="roof",
        communities=["Hartselle", "Priceville", "Trinity", "Somerville", "Falkville", "Athens", "Moulton", "Courtland"],
        hoods=["Old Decatur", "Albany Historic District", "Burningtree", "Point Mallard", "Southwest Decatur", "Westmeade", "Austinville"],
        risks=[("hail", "Hail", "Decatur sits in the Tennessee Valley hail corridor that runs from the Shoals to Huntsville."),
               ("storm", "Tornadoes", "North Alabama's spring and late-fall tornado season affects Morgan County every year."),
               ("home", "Historic districts", "Old Decatur and Albany have Victorian and early-1900s homes with specialty materials."),
               ("layers", "Industrial", "River-front manufacturing and industrial plants carry large commercial exposure.")],
        intro="Decatur, on the Tennessee River, shares North Alabama's busy hail and tornado season. Its two historic districts, Old Decatur and Albany, hold some of the state's best-preserved Victorian homes, while industrial plants along the river add large commercial risks.",
        local="Victorian homes in Albany and Old Decatur have wood siding, decorative trim, tall ceilings and older roofing that cost more to repair correctly than standard line items assume. On the industrial side, metal buildings and large low-slope roofs bring their own scope questions.",
        faqs=[("Do you cover Hartselle and Athens?", "<p>Yes, all of Morgan, Limestone and Lawrence counties.</p>"),
              ("Can you appraise historic homes?", "<p>Yes. We document and price the specialty materials and methods historic homes require.</p>")]),
    "florence-al": dict(
        county="Lauderdale County", region="The Shoals / Northwest Alabama", img="residential",
        communities=["Muscle Shoals", "Sheffield", "Tuscumbia", "Killen", "Rogersville", "Lexington", "Cherokee", "Russellville"],
        hoods=["Downtown Florence", "Sweetwater", "Forest Hills", "Wildwood Park", "Seven Points", "Mars Hill", "Patton Island"],
        risks=[("hail", "Hail", "The western end of the Tennessee Valley hail corridor regularly sees damaging hail."),
               ("storm", "Severe storms", "Tornadoes and straight-line wind sweep through the Shoals with spring systems."),
               ("droplets", "River &amp; lake property", "Homes along the Tennessee River and Wilson Lake bring water-exposure questions."),
               ("users", "Rental housing", "The University of North Alabama supports rental and multi-family property.")],
        intro="Florence and the Shoals &mdash; Muscle Shoals, Sheffield and Tuscumbia &mdash; anchor Northwest Alabama. The area shares the Tennessee Valley's hail and tornado exposure, and its riverfront and lake homes add their own claim considerations.",
        local="Lake and riverfront homes along Wilson Lake and the Tennessee River often have boathouses, docks and retaining walls, each with different coverage. Understanding which damage falls under the homeowner policy and which may not is part of preparing a clean appraisal.",
        faqs=[("Do you cover Muscle Shoals, Sheffield and Tuscumbia?", "<p>Yes &mdash; all of Lauderdale, Colbert and Franklin counties.</p>"),
              ("Are docks and boathouses covered?", "<p>It depends on the policy. Some homeowner policies limit or exclude docks; check yours before an appraisal.</p>")]),
    "gadsden-al": dict(
        county="Etowah County", region="Northeast Alabama", img="storm",
        communities=["Rainbow City", "Southside", "Attalla", "Glencoe", "Boaz", "Hokes Bluff", "Reece City", "Altoona"],
        hoods=["Downtown Gadsden", "Alabama City", "East Gadsden", "Noccalula Falls", "Lookout Mountain"],
        risks=[("storm", "Tornadoes", "Northeast Alabama's ridges and valleys see frequent tornado warnings and wind damage."),
               ("hail", "Hail", "Spring storms bring hail to Etowah County and the Sand Mountain area."),
               ("home", "Older homes", "Many homes date to Gadsden's industrial era, with older roofs and systems."),
               ("droplets", "Coosa River", "Riverfront property and heavy rain bring water-intrusion claims.")],
        intro="Gadsden and Etowah County sit where the Appalachian foothills meet the Coosa River. Severe storms and tornadoes cross Northeast Alabama every spring, and much of the city's housing dates to its steel-making era.",
        local="Older homes in Alabama City and East Gadsden often have multiple roof layers, older electrical and plumbing, and materials that are hard to match. Tear-off of additional layers, decking replacement and code items are frequent sources of estimate gaps.",
        faqs=[("Do you cover Rainbow City and Boaz?", "<p>Yes &mdash; all of Etowah County plus Marshall, DeKalb, Cherokee and Calhoun county communities.</p>"),
              ("Why do multiple roof layers matter?", "<p>Each extra layer adds tear-off labor and disposal. Missing layers is one of the most common roof-estimate errors.</p>")]),
}


def area_page(city, slug):
    d = A[slug]
    path = f"/service-areas/{slug}/"
    p = {
        "path": path,
        "title": f"Insurance Appraiser in {city}, AL | Claim Appraisal",
        "description": f"Insurance appraiser in {city}, AL ({d['county']}): independent claim appraisal and estimates for hail, wind, water and fire losses.",
        "h1": f"Insurance Appraiser in {city}, AL",
        "lead": f"Independent property claim appraisal and estimating for homeowners and businesses in {city} and across {d['county']}.",
        "kicker": f"{d['region']} &middot; {d['county']}", "hero_img": d["img"], "nav_active": "/service-areas/",
        "crumbs": [("Home", "/"), ("Service Areas", "/service-areas/"), (f"{city}, AL", path)],
        "sidebar_links": [(f"{c}, AL", f"/service-areas/{s}/") for c, s in CITIES if s != slug][:8],
        "sidebar_title": "Other service areas", "priority": "0.7",
    }
    risk_cards = [card(t, b, None, i) for i, t, b in d["risks"]]
    svc_links = "".join(f'<li><a href="/services/{s}/">{n}</a></li>' for s, n, _, _ in SERVICES)
    others = [(f"Insurance appraiser {c}, AL", f"/service-areas/{s}/") for c, s in CITIES if s != slug][:4]
    p["body"] = f'''
<p class="lead-p">{d["intro"]}</p>
<p>Alabama Insurance Appraiser works with {city} homeowners, commercial owners, property managers, contractors and attorneys when a claim comes down to a disagreement over the amount of loss. We inspect, measure and estimate the damage, compare it with the carrier's numbers and build a documented appraisal position.</p>
<h2>Property risks we see in {city}</h2>
{grid(risk_cards, 2)}
<h2>What makes {city} claims different</h2>
<p>{d["local"]}</p>
{callout(f"<p>Your appraisal rights, deadlines and procedures come from your policy, not from where you live. Read the appraisal provision before you send a written demand.</p>", "info", "Check the policy first")}
<h2>Insurance appraisal services in {city}</h2>
<ul class="tags">{"".join(f'<li><a href="/services/{s}/">{n}</a></li>' for s, n, _, _ in SERVICES)}</ul>
<h2>Neighborhoods and nearby communities</h2>
<p>We take assignments throughout {city}, including {", ".join(d["hoods"][:-1])} and {d["hoods"][-1]}, and in nearby {", ".join(d["communities"][:-1])} and {d["communities"][-1]}.</p>
{checklist([f"Residential claims in every {city} neighborhood", f"Commercial and multi-family property across {d['county']}", "Rural and small-town property in the surrounding counties", "On-site inspections, Matterport capture and desk reviews"], "checklist two-col")}
<h2>How to get started</h2>
<p>Call {BIZ["phone_short"]} or <a href="/contact/">send your claim details</a>. Have your carrier's estimate, any contractor estimate and your policy handy. We'll talk through the gap and tell you whether appraisal, an estimate review or a supplement makes the most sense.</p>
<h2>{city} insurance appraisal FAQ</h2>
{faq_html(d["faqs"])}
{related_links("Other Alabama service areas", others + [("All service areas", "/service-areas/")])}
'''
    p["schema"] = [service_schema(p, f"Insurance appraisal in {city}, AL", "Property insurance appraisal",
                                  area={"@type": "City", "name": f"{city}, Alabama",
                                        "containedInPlace": {"@type": "AdministrativeArea", "name": f"{d['county']}, Alabama"}}),
                   faq_schema(p, d["faqs"])]
    return p


def hub():
    p = {
        "path": "/service-areas/",
        "title": "Alabama Insurance Appraiser Service Areas | Statewide",
        "description": "Alabama Insurance Appraiser serves all 67 counties, including Birmingham, Huntsville, Montgomery, Mobile, Tuscaloosa, Hoover, Auburn and Dothan.",
        "h1": "Insurance Appraisal Service Areas Across Alabama",
        "lead": "From the Tennessee Valley to the Gulf Coast, we take residential and commercial appraisal assignments in all 67 Alabama counties.",
        "kicker": "Statewide coverage", "hero_img": "home", "nav_active": "/service-areas/",
        "crumbs": [("Home", "/"), ("Service Areas", "/service-areas/")], "layout": "wide", "priority": "0.8",
        "schema_type": "CollectionPage",
    }
    cities = "".join(f'<a class="city" href="/service-areas/{s}/"><span>{c}<small>{A[s]["county"]}</small></span>{icon("arrow", "ico ico-sm")}</a>'
                     for c, s in CITIES)
    regions = [
        ("North Alabama &amp; Tennessee Valley", "Huntsville, Decatur, Florence, Athens, Madison and the Shoals. Frequent hail and spring tornadoes.", "hail"),
        ("Central Alabama", "Birmingham, Hoover, Tuscaloosa, Montgomery and the River Region. Dixie Alley severe weather and dense suburbs.", "storm"),
        ("East Alabama", "Auburn, Opelika, Gadsden, Anniston and the foothills. Tornado and hail exposure plus university housing.", "map"),
        ("South Alabama &amp; Gulf Coast", "Mobile, Baldwin County, Dothan and the Wiregrass. Hurricane wind, named-storm deductibles and wind-pool policies.", "umbrella"),
    ]
    p["body"] = f'''
<section class="section section-white"><div class="container">
  {section_head("Featured cities", "Choose your area", "Local pages cover the property risks, neighborhoods and claim issues specific to each city.", True)}
  <div class="city-grid">{cities}<a class="city city-statewide" href="/contact/"><span>Anywhere else in Alabama<small>Ask about your location</small></span>{icon("arrow", "ico ico-sm")}</a></div>
</div></section>
<section class="section section-aqua"><div class="container">
  {section_head("By region", "Alabama's weather changes the claim", "", True)}
  {grid([card(t, b, None, i) for t, b, i in regions], 4)}
</div></section>
<section class="section section-white"><div class="container split">
  <div class="reveal">
    {section_head("Rural &amp; small-town property", "Not near a big city? We still come to you")}
    <p>Many of our assignments are in small towns and rural counties: farmhouses, metal shops, churches, small-town commercial buildings and lake homes. Where travel is long, we combine Matterport capture, detailed photo documentation and desk review to keep costs reasonable.</p>
    {btn("Talk about your location", "/contact/", "primary", "pin")}
  </div>
  <div class="frame reveal"><div class="img-zoom"><img src="/assets/img/storm-damage-alabama-homes-720.webp" width="720" height="480" alt="Storm clouds over a row of homes in Alabama" loading="lazy"></div></div>
</div></section>'''
    p["schema"] = [{"@type": "ItemList", "@id": url("/service-areas/#list"), "name": "Alabama Insurance Appraiser service areas",
                    "itemListElement": [{"@type": "ListItem", "position": n, "url": url(f"/service-areas/{s}/"), "name": f"{c}, AL"}
                                        for n, (c, s) in enumerate(CITIES, 1)]}]
    return p


def pages():
    return [hub()] + [area_page(c, s) for c, s in CITIES]
