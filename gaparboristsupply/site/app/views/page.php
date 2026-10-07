<?php
defined('GAP') || exit;
/** @var string $slug */
$n = $CFG['name']; $mail = $CFG['email'];
$pages = [
 'about' => ['About Gap Arborist Supply', 'Gap Arborist Supply is an independent arborist gear store and buying guide for tree climbers, crews and serious homeowners.', [
   ['What we are', ["$n is an independent store and buying guide for the people who climb, rig, cut and clean up trees for a living, and for the homeowners and hobby climbers who take the work just as seriously. We pick the gear, explain what it is for and who it suits, and send you to a trusted retailer to buy it."]],
   ['How we pick gear', ['We look for gear that solves a real problem on a tree job: getting into the canopy, moving through it safely, bringing wood down under control, cutting cleanly and keeping a crew protected. We favour proven designs from makers with a track record in tree care, and we say plainly who a product is not right for.', 'Prices shown are typical street prices. Retail prices move, so every product links to the retailer for the current price.']],
   ['Safety first, always', ['Climbing and rigging gear is life-support equipment. Nothing on this site replaces proper training, the manufacturer\'s instructions, or the ANSI Z133 safety standard. If you are new to tree work, get trained before you buy and before you climb.']],
 ]],
 'contact' => ['Contact', 'Questions about gear, a product page, or working with us? Get in touch with Gap Arborist Supply.', [
   ['Get in touch', ["Email <a href=\"mailto:$mail\">$mail</a> with gear questions, corrections to a product page, or partnership enquiries. We read everything and reply as quickly as we can.", 'For orders, shipping and returns, contact the retailer you bought from: they handle payment and delivery.']],
 ]],
 'affiliate-disclosure' => ['Affiliate Disclosure', 'How Gap Arborist Supply earns money: some links are affiliate links, which pay us a commission at no extra cost to you.', [
   ['How this site makes money', ["$n is supported by its readers. When you click a \"Check price\" link and buy from the retailer, we may earn a commission. You pay the same price either way.", "$n is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate we earn from qualifying purchases.", 'Commissions never decide what we list or how we describe it. If a product is not right for a job, we say so.']],
   ['Prices', ['The prices on this site are typical street prices for reference. The retailer\'s price at checkout is the one that counts.']],
 ]],
 'privacy-policy' => ['Privacy Policy', 'How Gap Arborist Supply handles your information.', [
   ['What we collect', ['This site does not ask you to create an account. Your cart, saved items and compare list are stored only in your own browser (local storage) and are never sent to us. You can clear them at any time by clearing your browser data.', 'Our hosting provider keeps standard server logs (such as IP address, browser type and pages requested) for security and performance.']],
   ['Links to retailers', ['When you follow a link to a retailer, that retailer\'s privacy policy applies, and they may use cookies to credit the referral to us.']],
   ['Contact', ["Questions about privacy: <a href=\"mailto:$mail\">$mail</a>."]],
 ]],
 'terms-of-use' => ['Terms of Use', 'The terms for using the Gap Arborist Supply website.', [
   ['Using this site', ['The content on this site is general information about tree care equipment. It is not professional training or safety advice for your specific situation. Working at height, rigging and operating chainsaws are dangerous: always follow the manufacturer\'s instructions, applicable standards such as ANSI Z133, and your training.']],
   ['Product information', ['We work to keep product details accurate, but specifications, availability and prices change. Confirm details with the retailer and the manufacturer before you buy or use any product. Calculators and tools on this site give estimates only.']],
   ['Purchases', ['Purchases are made with third-party retailers, under their terms. We are not a party to that sale.']],
 ]],
];
[$h1, $desc, $sections] = $pages[$slug];
$meta = ['title' => $h1, 'desc' => $desc, 'canonical' => "/$slug/"];
?>
<section class="cat-hero"><div class="wrap narrow"><?= crumbs([[$h1, "/$slug/"]]) ?><h1><?= e($h1) ?></h1><p class="lede"><?= e($desc) ?></p></div></section>
<section class="wrap narrow prose page-body">
<?php foreach ($sections as [$h, $ps]): ?>
  <h2><?= e($h) ?></h2>
<?php foreach ($ps as $para): ?>  <p><?= preg_replace('#&lt;a href=&quot;(mailto:[^&]+)&quot;&gt;(.*?)&lt;/a&gt;#', '<a href="$1">$2</a>', e($para)) ?></p>
<?php endforeach; endforeach; ?>
</section>
