<?php
/**
 * Plugin Name: SYL Ad Placement
 * Description: Places AdSense units in high-earning spots on shineyourlightblog.com while keeping them away from affiliate links.
 * Version:     1.0.0
 * Author:      Shine Your Light
 *
 * Installed as a must-use plugin (wp-content/mu-plugins/), so it is always on.
 *
 * Placement strategy
 * ------------------
 * Single posts (via the_content, which Elementor's Post Content widget uses):
 *   1. "Top" display unit after the intro (~first 50+ words) - highest viewability.
 *   2. In-article units every ~350 words further down, at most 4.
 *   3. Multiplex ("autorelaxed") unit after the post body - readers who finish
 *      a post click through to more content, and this format earns well there.
 * Archives / home / search:
 *   4. In-feed unit inside the post grid after the 3rd post (and the 9th on
 *      long lists), spanning the full grid row.
 *
 * Affiliate safety
 * ----------------
 * Content is split into top-level blocks (paragraphs, images, lists...). An ad
 * may only go in a gap when neither of the AFFILIATE_BUFFER blocks before it nor
 * the AFFILIATE_BUFFER blocks after it contain an affiliate/shopping link, an
 * affiliate disclosure, or an embed/widget. Ads also never go directly under a
 * heading, and two ads are never closer than MIN_WORDS_BETWEEN words.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

final class SYL_Ad_Placement {

	const CLIENT = 'ca-pub-3886800648957674';

	const SLOT_TOP        = '8096221599'; // display, responsive
	const SLOT_IN_ARTICLE = '1960371044'; // in-article fluid
	const SLOT_MULTIPLEX  = '8746967795'; // autorelaxed
	const SLOT_IN_FEED    = '5524169668'; // in-feed fluid
	const IN_FEED_LAYOUT  = '-gd+y-52-bo+14o';

	const FIRST_AD_MIN_WORDS = 50;   // words of intro before the top ad
	const MIN_WORDS_BETWEEN  = 350;  // spacing between in-content ads
	const MAX_IN_CONTENT     = 5;    // top ad + in-article ads
	const AFFILIATE_BUFFER   = 2;    // clean blocks required on each side of an ad
	const TAIL_BLOCKS        = 2;    // keep the last blocks ad-free (multiplex follows)

	/** Hosts (or host suffixes) treated as affiliate / shopping links. */
	const AFFILIATE_HOSTS = array(
		'amzn.to', 'amzn.com', 'amazon.com', 'amazon.ca', 'amazon.co.uk', 'a.co',
		'rstyle.me', 'shopstyle.it', 'shopstyle.com', 'liketk.it', 'shopltk.com', 'liketoknow.it',
		'howl.me', 'shop-links.co', 'go.skimresources.com', 'skimlinks.com', 'go.redirectingat.com',
		'shareasale.com', 'shareasale-analytics.com', 'awin1.com', 'linksynergy.com', 'click.linksynergy.com',
		'anrdoezrs.net', 'jdoqocy.com', 'tkqlhce.com', 'dpbolvw.net', 'kqzyfj.com', 'emjcd.com',
		'sjv.io', 'pxf.io', 'ojrq.net', 'impact.com', 'avantlink.com', 'pntra.com', 'pntrs.com',
		'gopjn.com', 'pjtra.com', 'pjatr.com', 'rakuten.com', 'flexoffers.com', 'partnerize.com',
		'prf.hn', 'mavely.app', 'mavely.app.link', 'shopmy.us', 'joinsubtext.com', 'bit.ly',
		'wayfair.com', 'potterybarn.com', 'westelm.com', 'crateandbarrel.com', 'cb2.com',
		'restorationhardware.com', 'rh.com', 'target.com', 'walmart.com', 'homedepot.com',
		'lowes.com', 'etsy.com', 'serenaandlily.com', 'anthropologie.com', 'overstock.com',
		'kirklands.com', 'worldmarket.com', 'wisteria.com', 'ballarddesigns.com', 'joss.com',
		'jossandmain.com', 'birchlane.com', 'allmodern.com', 'mcgeeandco.com', 'arhaus.com',
		'containerstore.com', 'bedbathandbeyond.com', 'hm.com', 'nordstrom.com', 'zgallerie.com',
		'gumroad.com',
	);

	public static function init() {
		add_filter( 'the_content', array( __CLASS__, 'filter_content' ), 50 );
		add_action( 'wp_head', array( __CLASS__, 'print_styles' ), 99 );
		add_action( 'wp_footer', array( __CLASS__, 'print_footer_script' ), 99 );
	}

	/** Pages where we must not output ads at all. */
	private static function disabled() {
		if ( is_admin() || is_feed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
			return true;
		}
		if ( is_preview() || is_customize_preview() ) {
			return true;
		}
		if ( isset( $_GET['elementor-preview'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
			return true;
		}
		if ( function_exists( 'amp_is_request' ) && amp_is_request() ) {
			return true;
		}
		/** Allow turning ads off per post with the custom field `syl_no_ads` = 1. */
		if ( is_singular() && get_post_meta( get_queried_object_id(), 'syl_no_ads', true ) ) {
			return true;
		}
		return (bool) apply_filters( 'syl_ads_disabled', false );
	}

	/* ------------------------------------------------------------------ */
	/* Ad markup                                                          */
	/* ------------------------------------------------------------------ */

	private static function unit( $slot, $attrs, $style, $wrapper_class ) {
		return "\n" . '<div class="syl-ad ' . esc_attr( $wrapper_class ) . '">'
			. '<span class="syl-ad__label">Advertisement</span>'
			. '<ins class="adsbygoogle" style="' . esc_attr( $style ) . '"'
			. ' data-ad-client="' . self::CLIENT . '" data-ad-slot="' . $slot . '"' . $attrs . '></ins>'
			. '<script data-no-optimize="1" data-no-defer="1" data-cfasync="false">(adsbygoogle = window.adsbygoogle || []).push({});</script>'
			. '</div>' . "\n";
	}

	private static function ad_top() {
		return self::unit( self::SLOT_TOP, ' data-ad-format="auto" data-full-width-responsive="true"', 'display:block', 'syl-ad--top' );
	}

	private static function ad_in_article() {
		return self::unit( self::SLOT_IN_ARTICLE, ' data-ad-layout="in-article" data-ad-format="fluid"', 'display:block; text-align:center;', 'syl-ad--in-article' );
	}

	private static function ad_multiplex() {
		return self::unit( self::SLOT_MULTIPLEX, ' data-ad-format="autorelaxed"', 'display:block', 'syl-ad--multiplex' );
	}

	/* ------------------------------------------------------------------ */
	/* Single posts                                                       */
	/* ------------------------------------------------------------------ */

	public static function filter_content( $content ) {
		static $done = false;

		if ( $done || self::disabled() || ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		if ( get_the_ID() !== get_queried_object_id() ) {
			return $content; // e.g. a related-posts widget rendering another post
		}
		$done = true;

		$blocks = self::split_blocks( $content );
		$count  = count( $blocks );

		if ( $count < 3 ) {
			return $content . self::ad_multiplex();
		}

		$info = array();
		foreach ( $blocks as $i => $html ) {
			$info[ $i ] = array(
				'words'     => str_word_count( wp_strip_all_tags( $html ) ),
				'risky'     => self::is_risky( $html ),
				'heading'   => (bool) preg_match( '/^\s*<h[1-6]\b/i', $html ),
				'ends_colon' => (bool) preg_match( '/:\s*(<\/[a-z]+>\s*)*$/i', $html ),
			);
		}

		// Gap $g sits after block $g. Pick gaps greedily, top to bottom.
		$insert_after = array();
		$words_so_far = 0;
		$words_since  = 0;
		$last_gap     = $count - 1 - self::TAIL_BLOCKS;

		for ( $g = 0; $g < $count - 1; $g++ ) {
			$words_so_far += $info[ $g ]['words'];
			$words_since  += $info[ $g ]['words'];

			if ( count( $insert_after ) >= self::MAX_IN_CONTENT || $g > $last_gap ) {
				break;
			}

			$is_first = empty( $insert_after );
			if ( $is_first && $words_so_far < self::FIRST_AD_MIN_WORDS ) {
				continue;
			}
			if ( ! $is_first && $words_since < self::MIN_WORDS_BETWEEN ) {
				continue;
			}
			if ( ! self::gap_is_clean( $g, $info, $count ) ) {
				continue;
			}

			$insert_after[ $g ] = $is_first ? 'top' : 'in-article';
			$words_since        = 0;
		}

		$out = '';
		foreach ( $blocks as $i => $html ) {
			$out .= $html;
			if ( isset( $insert_after[ $i ] ) ) {
				$out .= 'top' === $insert_after[ $i ] ? self::ad_top() : self::ad_in_article();
			}
		}

		return $out . self::ad_multiplex();
	}

	/** True when an ad may go between block $g and block $g + 1. */
	private static function gap_is_clean( $g, $info, $count ) {
		if ( $info[ $g ]['heading'] || $info[ $g ]['ends_colon'] ) {
			return false; // keep headings / lead-ins attached to what follows
		}
		$from = max( 0, $g - self::AFFILIATE_BUFFER + 1 );
		$to   = min( $count - 1, $g + self::AFFILIATE_BUFFER );
		for ( $i = $from; $i <= $to; $i++ ) {
			if ( $info[ $i ]['risky'] ) {
				return false;
			}
		}
		return true;
	}

	/** Does this block contain something an ad must not sit next to? */
	private static function is_risky( $html ) {
		if ( preg_match( '/<(iframe|script|form|ins|embed|object)\b/i', $html ) ) {
			return true; // embeds, shop widgets, existing ads
		}
		if ( preg_match( '/rel=["\'][^"\']*sponsored/i', $html ) ) {
			return true;
		}
		if ( preg_match( '/affiliate|commission|disclosure|shop the (look|post)|shop this|shop my|#ad\b|sponsored/i', wp_strip_all_tags( $html ) ) ) {
			return true;
		}
		if ( preg_match( '/class=["\'][^"\']*(affiliate|shop|product|wp-block-button|buy)/i', $html ) ) {
			return true;
		}
		if ( preg_match_all( '/<a\b[^>]*href=["\']([^"\']+)["\']/i', $html, $m ) ) {
			foreach ( $m[1] as $href ) {
				if ( self::is_affiliate_url( html_entity_decode( $href ) ) ) {
					return true;
				}
			}
		}
		return false;
	}

	private static function is_affiliate_url( $url ) {
		$host = wp_parse_url( $url, PHP_URL_HOST );
		if ( ! $host ) {
			return false; // relative / internal link
		}
		$host = strtolower( preg_replace( '/^www\./i', '', $host ) );
		$own  = strtolower( preg_replace( '/^www\./i', '', (string) wp_parse_url( home_url(), PHP_URL_HOST ) ) );
		if ( $host === $own ) {
			return false;
		}
		foreach ( self::AFFILIATE_HOSTS as $aff ) {
			if ( $host === $aff || substr( $host, -strlen( '.' . $aff ) ) === '.' . $aff ) {
				return true;
			}
		}
		// Tracking parameters typical of affiliate programs.
		return (bool) preg_match( '/[?&](tag|aff|affid|aff_id|affiliate|ref|irclickid|clickid|subid|u1|utm_medium=affiliate)=/i', $url );
	}

	/**
	 * Split post HTML into top-level blocks without re-serialising it, so the
	 * original markup is preserved byte for byte.
	 */
	private static function split_blocks( $html ) {
		$void   = array( 'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr' );
		$blocks = array();
		$depth  = 0;
		$start  = 0;
		$len    = strlen( $html );
		$pos    = 0;

		while ( $pos < $len && preg_match( '/<!--.*?-->|<(\/?)([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*?(\/?)>/s', $html, $m, PREG_OFFSET_CAPTURE, $pos ) ) {
			$tag_start = $m[0][1];
			$tag_end   = $tag_start + strlen( $m[0][0] );
			$pos       = $tag_end;

			if ( ! isset( $m[2] ) || '' === $m[2][0] ) {
				continue; // comment
			}
			$name    = strtolower( $m[2][0] );
			$closing = '/' === $m[1][0];

			if ( ! $closing && in_array( $name, array( 'script', 'style' ), true ) ) {
				$close = stripos( $html, '</' . $name, $tag_end );
				if ( false === $close ) {
					break;
				}
				$pos = strpos( $html, '>', $close );
				$pos = false === $pos ? $len : $pos + 1;
				if ( 0 === $depth ) {
					$blocks[] = substr( $html, $start, $pos - $start );
					$start    = $pos;
				}
				continue;
			}

			if ( in_array( $name, $void, true ) || '/' === $m[3][0] ) {
				if ( 0 === $depth && in_array( $name, array( 'hr', 'img' ), true ) ) {
					$blocks[] = substr( $html, $start, $tag_end - $start );
					$start    = $tag_end;
				}
				continue;
			}

			if ( $closing ) {
				$depth = max( 0, $depth - 1 );
				if ( 0 === $depth ) {
					$blocks[] = substr( $html, $start, $tag_end - $start );
					$start    = $tag_end;
				}
			} else {
				$depth++;
			}
		}

		if ( $start < $len ) {
			$rest = substr( $html, $start );
			if ( '' !== trim( $rest ) || empty( $blocks ) ) {
				$blocks[] = $rest;
			} else {
				$blocks[ count( $blocks ) - 1 ] .= $rest;
			}
		}

		// Merge blocks that are only whitespace into their predecessor.
		$merged = array();
		foreach ( $blocks as $b ) {
			if ( '' === trim( $b ) && ! empty( $merged ) ) {
				$merged[ count( $merged ) - 1 ] .= $b;
			} else {
				$merged[] = $b;
			}
		}
		return $merged;
	}

	/* ------------------------------------------------------------------ */
	/* Shared assets                                                      */
	/* ------------------------------------------------------------------ */

	public static function print_styles() {
		if ( self::disabled() ) {
			return;
		}
		?>
<style id="syl-ad-placement">
.syl-ad{clear:both;margin:32px auto;text-align:center;min-height:120px}
.syl-ad__label{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#999;margin-bottom:6px}
.syl-ad--multiplex{margin-top:48px}
.syl-ad--in-feed{grid-column:1/-1;margin:8px 0}
</style>
		<?php
	}

	public static function print_footer_script() {
		if ( self::disabled() ) {
			return;
		}
		$show_feed = ! is_singular() && ( is_home() || is_front_page() || is_archive() || is_search() );
		?>
<script data-no-optimize="1" data-no-defer="1" data-cfasync="false">
(function () {
	var client = <?php echo wp_json_encode( self::CLIENT ); ?>;
	// Site Kit normally loads adsbygoogle.js; load it ourselves only if it is missing.
	if (!document.querySelector('script[src*="adsbygoogle.js"]')) {
		var s = document.createElement('script');
		s.async = true;
		s.crossOrigin = 'anonymous';
		s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + client;
		document.head.appendChild(s);
	}
	<?php if ( $show_feed ) : ?>
	// In-feed ad inside the main post grid: after post 3, and after post 9 on long lists.
	var grids = document.querySelectorAll('.elementor-loop-container'), grid = null;
	for (var i = 0; i < grids.length; i++) {
		if (grids[i].children.length >= 6) { grid = grids[i]; break; }
	}
	if (!grid) { return; }
	var items = grid.querySelectorAll(':scope > .e-loop-item');
	[3, 9].forEach(function (n) {
		if (items.length <= n) { return; }
		var wrap = document.createElement('div');
		wrap.className = 'syl-ad syl-ad--in-feed';
		wrap.innerHTML = '<span class="syl-ad__label">Advertisement</span>' +
			'<ins class="adsbygoogle" style="display:block" data-ad-format="fluid"' +
			' data-ad-layout-key="<?php echo esc_js( self::IN_FEED_LAYOUT ); ?>"' +
			' data-ad-client="' + client + '" data-ad-slot="<?php echo esc_js( self::SLOT_IN_FEED ); ?>"></ins>';
		items[n - 1].after(wrap);
		(window.adsbygoogle = window.adsbygoogle || []).push({});
	});
	<?php endif; ?>
})();
</script>
		<?php
	}
}

SYL_Ad_Placement::init();
