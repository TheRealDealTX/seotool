<?php
/**
 * Blog post registry. Each post lives at /{slug}/ (the same root-level
 * permalinks the WordPress site used) and its body is content/posts/{slug}.html.
 * Newest first.
 */

const POSTS = [
    [
        'slug' => 'hurricane-insurance-claim-guide-sugar-land',
        'title' => 'Hurricane Insurance Claims in Sugar Land: A Step-by-Step Guide',
        'seo_title' => 'Hurricane Insurance Claim Guide for Sugar Land Homeowners',
        'description' => 'A Sugar Land public adjuster explains how to file a hurricane insurance claim in Fort Bend County: deductibles, wind vs. flood, documentation and deadlines.',
        'excerpt' => 'Beryl, Ike and Harvey taught Fort Bend County hard lessons. Here is how to protect a hurricane claim from the first hour after the storm to the final payment.',
        'date' => '2026-10-13T09:00:00-05:00',
        'modified' => '2026-10-13T09:00:00-05:00',
        'image' => '/wp-content/uploads/2026/02/Sugar-Land-Public-Adjusting-BG-1.webp',
        'thumb' => '/wp-content/uploads/2026/02/Property-Inspection.webp',
    ],
    [
        'slug' => 'how-much-does-a-public-adjuster-cost-in-texas',
        'title' => 'How Much Does a Public Adjuster Cost in Texas?',
        'seo_title' => 'How Much Does a Public Adjuster Cost in Texas? (Fee Cap Explained)',
        'description' => 'Texas caps public adjuster fees at 10% of the settlement. A Sugar Land public adjuster explains how fees work, what you pay, and when hiring one pays off.',
        'excerpt' => 'Texas law caps what a public adjuster can charge. Here is exactly how the fee works, with real math, so you can decide whether representation pays for itself.',
        'date' => '2026-10-10T09:00:00-05:00',
        'modified' => '2026-10-10T09:00:00-05:00',
        'image' => '/wp-content/uploads/2026/02/Negotiation.webp',
        'thumb' => '/wp-content/uploads/2026/02/Negotiation.webp',
    ],
    [
        'slug' => 'hail-damage-insurance-claims-sugar-land',
        'title' => 'Hail Damage Insurance Claims in Sugar Land & Fort Bend County',
        'seo_title' => 'Hail Damage Insurance Claims in Sugar Land, TX | Public Adjuster Guide',
        'description' => 'How to spot hail damage, document it, and push back on a low hail claim offer in Sugar Land, TX—written by a licensed Sugar Land public adjuster.',
        'excerpt' => 'Hail damage hides in plain sight. Learn what insurers look for, what they tend to miss, and how Sugar Land homeowners can get a hail claim paid correctly.',
        'date' => '2026-10-07T09:00:00-05:00',
        'modified' => '2026-10-07T09:00:00-05:00',
        'image' => '/wp-content/uploads/2026/02/Claim-Preparation.webp',
        'thumb' => '/wp-content/uploads/2026/02/Claim-Preparation.webp',
    ],
    [
        'slug' => 'fire-insurance-adjuster-secrets',
        'title' => 'Fire Insurance Adjuster Secrets: How to Maximize Your Claim',
        'seo_title' => 'Fire Insurance Adjuster Secrets: How to Maximize Your Claim',
        'description' => 'Learn fire insurance adjuster secrets to maximize your claim. Discover tips, mistakes to avoid, and how to get a fair payout fast.',
        'excerpt' => 'A house fire changes everything in minutes. Learn how fire insurance adjusters evaluate claims, the mistakes that shrink payouts, and how to recover what you are owed.',
        'date' => '2026-03-25T02:08:10+00:00',
        'modified' => '2026-10-13T09:00:00-05:00',
        'image' => '/wp-content/uploads/2026/03/Fire-Insurance-Adjuster-Secrets.webp',
        'thumb' => '/wp-content/uploads/2026/03/Fire-Insurance-Adjuster-Secrets-300x200.webp',
    ],
    [
        'slug' => 'the-smart-homeowners-guide-to-finding-the-right-public-adjuster',
        'title' => 'The Smart Homeowner’s Guide to Finding the Right Public Adjuster',
        'seo_title' => 'The Smart Homeowner’s Guide to Finding the Right Public Adjuster',
        'description' => 'Learn how to find a public adjuster you can trust. Discover tips, red flags, and steps to secure a fair insurance settlement.',
        'excerpt' => 'How to find a public adjuster you can trust: the questions to ask, the red flags to avoid, and what Sugar Land homeowners should know before signing.',
        'date' => '2026-03-14T01:30:00+00:00',
        'modified' => '2026-10-13T09:00:00-05:00',
        'image' => '/wp-content/uploads/2026/03/The-Smart-Homeowners-Guide-to-Finding-the-Right-Public-Adjuster.webp',
        'thumb' => '/wp-content/uploads/2026/03/The-Smart-Homeowners-Guide-to-Finding-the-Right-Public-Adjuster-300x200.webp',
    ],
    [
        'slug' => 'why-use-a-public-adjuster',
        'title' => 'Why Use a Public Adjuster?',
        'seo_title' => 'Why Use a Public Adjuster? | Sugar Land Public Adjuster',
        'description' => 'Why use a public adjuster? Learn how they protect your interests, uncover hidden value, and help secure a fair insurance settlement.',
        'excerpt' => 'Claims are often slow, stressful and quietly underpaid. Here is what a public adjuster actually does—and when hiring one makes the most sense.',
        'date' => '2026-02-07T10:32:21+00:00',
        'modified' => '2026-10-13T09:00:00-05:00',
        'image' => '/wp-content/uploads/2026/02/Why-Use-a-Public-Adjuster.webp',
        'thumb' => '/wp-content/uploads/2026/02/Why-Use-a-Public-Adjuster-300x200.webp',
    ],
];

function find_post(string $slug): ?array
{
    foreach (POSTS as $p) {
        if ($p['slug'] === $slug) {
            return $p;
        }
    }
    return null;
}
