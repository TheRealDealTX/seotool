<?php
defined('INC') || exit;
/**
 * Vintique Flea — site configuration.
 * Edit this file to change business details, event dates and the affiliate tag.
 */

const SITE_NAME   = 'Vintique Flea';
const SITE_URL    = 'https://vintiqueflea.com';
const SITE_TAGLINE = "Houston's Curated Indoor Marketplace of Interesting Things";
const AMAZON_TAG  = 'josephrayditt-20';

/** Where contact / vendor form messages are emailed. Must be a mailbox that exists. */
const CONTACT_TO   = 'info@vintiqueflea.com';
/** The From: address for outgoing form mail — must be on the vintiqueflea.com domain. */
const CONTACT_FROM = 'no-reply@vintiqueflea.com';

const VENUE = [
    'name'     => 'Silver Street Studios',
    'street'   => '2000 Edwards Street',
    'city'     => 'Houston',
    'region'   => 'TX',
    'postal'   => '77007',
    'country'  => 'US',
    'district' => 'Washington Avenue Arts District',
];

const SOCIAL = [
    // 'Facebook'  => 'https://www.facebook.com/…',
    // 'Instagram' => 'https://www.instagram.com/…',
];

/**
 * Upcoming market dates. Leave empty to show "dates announced soon".
 * Each entry produces an Event schema block and a card on /events/.
 * Example:
 * ['name' => 'Vintique Flea: Spring Edition', 'season' => 'spring',
 *  'start' => '2027-03-20T10:00', 'end' => '2027-03-21T17:00',
 *  'hours' => ['Sat, Mar 20: 10am–6pm', 'Sun, Mar 21: 10am–5pm'],
 *  'price_online' => 7, 'price_door' => 10, 'tickets_url' => ''],
 */
const UPCOMING_EVENTS = [];
