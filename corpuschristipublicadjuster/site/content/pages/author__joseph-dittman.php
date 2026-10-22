<?php
defined('CCPA_ROOT') || exit;
return [
    'template'          => 'author',
    'person_schema'     => true,
    'title'             => 'Joseph Dittman, Licensed Public Adjuster',
    'crumb'             => 'Joseph Dittman',
    'breadcrumb_parent' => ['About Us', '/about-us/'],
    'seo_title'         => 'Joseph Dittman, Licensed Texas Public Adjuster | Author',
    'description'       => 'Joseph Dittman is a licensed Texas public adjuster, certified insurance appraiser, and insurance umpire who writes and reviews the articles on this site.',
    'lead'              => 'Licensed Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness. Author and reviewer of the articles on Corpus Christi Public Adjuster.',
    'kicker'            => 'Author',
    'image'             => '/assets/img/featured/page-author-joseph-dittman.webp',
    'image_alt'         => 'Joseph Dittman, Texas public adjuster',
    'faqs' => [
        ['q' => 'Is Joseph Dittman a licensed public adjuster?', 'a' => '<p>Yes. Joseph Dittman is a Texas public adjuster. Corpus Christi Public Adjuster is a public adjusting service of Rise Public Adjusting LLC, licensed by the Texas Department of Insurance (license #3356839). You can verify licenses through TDI\'s online license lookup.</p>'],
        ['q' => 'How can I contact Joseph directly?', 'a' => '<p>Email Joseph at [[author-email]]. For a claim review, you can also use the <a href="/free-claim-review/">Free Claim Review</a> form, which goes to [[email]], or call or text [[phone]].</p>'],
        ['q' => 'What is the difference between his appraiser and umpire work?', 'a' => '<p>In the appraisal process found in many property policies, each side selects an appraiser to evaluate the amount of loss, and the appraisers select an umpire to resolve differences between them. Joseph has served in both roles, which gives him a view of how disputed claims are evaluated from more than one side.</p>'],
        ['q' => 'Can I ask Joseph to review my claim?', 'a' => '<p>Yes. Request a Free Claim Review and your information will be reviewed by a licensed Texas public adjuster. There is no cost and no obligation.</p>'],
    ],
    'body' => <<<'HTML'
<p>Joseph Dittman is a Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness. He writes and reviews the articles on Corpus Christi Public Adjuster to give homeowners and business owners in Corpus Christi, Nueces County, and the Coastal Bend clear, accurate information about property insurance claims, from hurricane and TWIA windstorm losses to hail, water, and fire damage.</p>
<p>Want to reach him directly? Email Joseph at [[author-email]].</p>

<h2>Professional background</h2>
<p>Joseph's experience covers several sides of the property claims process, which shapes how he explains claims to policyholders:</p>
<ul>
<li><strong>Carrier-side adjusting.</strong> Adjusting claims on behalf of insurers, including how claims are evaluated and estimated from the insurance company's side.</li>
<li><strong>Public adjusting.</strong> Representing policyholders in preparing, documenting, and negotiating their claims.</li>
<li><strong>Appraisal.</strong> Serving as an appraiser in the process used to resolve disagreements over the amount of a loss.</li>
<li><strong>Umpire work.</strong> Serving as an insurance umpire, the neutral party who helps resolve differences between appraisers.</li>
<li><strong>Expert witness support.</strong> Providing support on property insurance disputes.</li>
<li><strong>Construction.</strong> Hands-on construction experience, which helps in reading damage, scoping repairs, and reviewing estimates.</li>
</ul>

<h2>Areas of focus</h2>
<p>Joseph has experience across a broad range of property losses, including:</p>
<ul>
<li>Residential and commercial property claims</li>
<li>Hurricane and catastrophe losses</li>
<li>Wind and storm damage, including TWIA windstorm claims</li>
<li>Hail damage</li>
<li>Water damage</li>
<li>Fire damage</li>
<li>Insurance appraisal and umpire matters</li>
</ul>
<p>Read more about how these claims work on our <a href="/services/">services page</a>, including <a href="/services/hurricane-damage-claims/">hurricane damage claims</a>, <a href="/services/twia-windstorm-claims/">TWIA windstorm claims</a>, and <a href="/services/insurance-appraisal/">insurance appraisal</a>.</p>

<h2>Company association</h2>
<p>Corpus Christi Public Adjuster is a public adjusting service of [[company]], licensed by the Texas Department of Insurance (license #[[license]]). As a public adjuster, Joseph represents the insured only. He is not an attorney and does not give legal advice; readers with legal questions should consult a Texas attorney.</p>

<h2>How articles are written and reviewed</h2>
<p>Articles on this site are meant to help property owners understand their claims, not to promise outcomes. Joseph's standards for this site:</p>
<ul>
<li><strong>Checked against Texas law.</strong> Statements about deadlines, fees, and claim rules are checked against the Texas Insurance Code, including Chapters 542, 542A, 2210, and 4102, and against Texas Department of Insurance and TWIA guidance, with links to official sources.</li>
<li><strong>Real weather data.</strong> Local storm references are checked against the NOAA NCEI Storm Events Database, National Hurricane Center reports, and National Weather Service records rather than anecdotes.</li>
<li><strong>Local building context.</strong> Code and permit references are checked against the City of Corpus Christi's published requirements and the TDI windstorm program.</li>
<li><strong>Careful framing.</strong> Coverage always depends on the policy and the facts, so articles use careful language and avoid guarantees.</li>
<li><strong>Visible dates.</strong> Each article shows its published and updated dates so readers know how current it is.</li>
</ul>
<p>If you spot something that needs correcting, email [[author-email]] or [[email]]. Have a question about your own claim? Request a <a href="/free-claim-review/">Free Claim Review</a>, browse the <a href="/blog/">claim guides</a>, or read more <a href="/about-us/">about Corpus Christi Public Adjuster</a>.</p>
HTML,
];
