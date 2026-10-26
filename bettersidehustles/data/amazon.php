<?php
// Amazon Associates catalog. Every link is built by amazon_url() with the
// AMAZON_TAG (bettersidehustles-20, set in inc/config.php). Links are Amazon search URLs rather than single
// ASINs so they never point at a discontinued listing.
//
// key => [title, search query, one-line reason, icon]
// Icons are names from icon() in inc/functions.php.

return [
    // Driving & delivery
    'phone-mount'    => ['Magnetic Car Phone Mount', 'magnetic car phone mount dashboard', 'Keeps navigation and ride requests in view without fumbling at red lights.', 'car'],
    'dash-cam'       => ['Front & Cabin Dash Cam', 'dual dash cam front and inside for rideshare', 'Records the road and the cabin, which protects you if a passenger dispute or accident comes up.', 'camera'],
    'insulated-bag'  => ['Insulated Delivery Bag', 'insulated food delivery bag large', 'Hot food arrives hot, which is how you keep ratings and tips up.', 'bag'],
    'car-charger'    => ['Fast Dual-Port Car Charger', 'fast usb c car charger dual port', 'Gig apps drain batteries fast; a 40W+ charger keeps your phone alive all shift.', 'bolt'],
    'power-bank'     => ['Portable Power Bank (20,000 mAh)', 'portable charger power bank 20000mah', 'Backup power for long delivery runs, events and days away from an outlet.', 'bolt'],
    'mileage-log'    => ['Mileage & Expense Log Book', 'vehicle mileage log book for taxes', 'Every business mile you log is worth a deduction at tax time.', 'book'],
    'seat-covers'    => ['Waterproof Car Seat Covers', 'waterproof car seat covers universal', 'Protects your upholstery from spills, pets and rainy-day passengers.', 'car'],
    'hand-cart'      => ['Folding Hand Truck', 'folding hand truck dolly', 'Makes courier, grocery and moving gigs faster and easier on your back.', 'box'],

    // Content creation & teaching
    'ring-light'     => ['Ring Light with Tripod Stand', 'ring light with tripod stand and phone holder', 'Even, flattering light for course videos, product photos and short-form content.', 'sun'],
    'usb-mic'        => ['USB Condenser Microphone', 'usb condenser microphone for podcast and recording', 'Clear audio matters more than video quality — students and viewers leave over bad sound.', 'mic'],
    'lav-mic'        => ['Wireless Lavalier Mic for Phones', 'wireless lavalier microphone for iphone android', 'Turns your phone into a pro recording setup for under the price of a dinner out.', 'mic'],
    'webcam'         => ['1080p HD Webcam', '1080p webcam with microphone', 'A sharp camera for tutoring, coaching calls and talking-head course lessons.', 'camera'],
    'gimbal'         => ['Smartphone Gimbal Stabilizer', 'smartphone gimbal stabilizer', 'Smooth, steady phone footage for UGC, real estate videos and social clips.', 'camera'],
    'tripod'         => ['Phone & Camera Tripod', 'phone tripod with remote extendable', 'Hands-free filming and photos from any angle.', 'camera'],
    'headset'        => ['Noise-Cancelling Headset', 'noise cancelling headset with microphone usb', 'Essential for remote support, virtual assistant and tutoring calls.', 'headphones'],
    'drawing-tablet' => ['Drawing Tablet', 'drawing tablet for beginners', 'For designers, illustrators and anyone selling digital art or templates.', 'pen'],
    'laptop-stand'   => ['Adjustable Laptop Stand', 'adjustable laptop stand aluminum', 'Better posture and a better camera angle for long freelance sessions.', 'laptop'],
    'camera'         => ['Beginner Mirrorless Camera', 'mirrorless camera for beginners with lens', 'A step up for real estate, event and product photography gigs.', 'camera'],
    'light-box'      => ['Product Photo Light Box', 'photo light box for product photography', 'Clean white-background product photos that make listings sell.', 'sun'],

    // E-commerce & reselling
    'label-printer'  => ['Thermal Shipping Label Printer', 'thermal shipping label printer 4x6', 'Print USPS, UPS and FedEx labels in seconds instead of fighting with an inkjet.', 'printer'],
    'shipping-scale' => ['Digital Shipping Scale', 'digital postal shipping scale', 'Weigh packages at home so you never overpay — or underpay — postage.', 'box'],
    'poly-mailers'   => ['Poly Mailer Shipping Bags', 'poly mailers shipping bags', 'Cheap, light packaging for clothing and soft goods.', 'box'],
    'cutting-machine'=> ['Cricut-Style Cutting Machine', 'cricut cutting machine', 'Custom shirts, decals and signage — a proven Etsy and craft-fair earner.', 'scissors'],
    'heat-press'     => ['Heat Press Machine', 'heat press machine for t shirts', 'Turns blank tees, totes and hats into products you can sell locally or online.', 'shirt'],

    // Home & local services
    'cleaning-kit'   => ['Professional Cleaning Caddy & Supplies', 'professional cleaning caddy supplies kit', 'Show up organized and finish rental turnovers faster.', 'sparkle'],
    'pressure-washer'=> ['Electric Pressure Washer', 'electric pressure washer', 'Driveways, decks and siding — one of the best-paying weekend hustles per hour.', 'drop'],
    'tool-kit'       => ['Home Repair Tool Kit', 'home repair tool kit with case', 'Covers most handyman calls: furniture assembly, fixtures, small repairs.', 'wrench'],
    'cordless-drill' => ['Cordless Drill/Driver Kit', 'cordless drill driver kit', 'The single tool that pays for itself fastest in handyman and assembly work.', 'wrench'],
    'leaf-blower'    => ['Cordless Leaf Blower', 'cordless leaf blower battery', 'Quick, quiet yard cleanups for lawn care clients.', 'leaf'],
    'snow-shovel'    => ['Ergonomic Snow Shovel', 'ergonomic snow shovel', 'Cold-city winters turn into paydays for anyone willing to clear driveways.', 'snow'],
    'dog-leash'      => ['Hands-Free Dog Walking Leash', 'hands free dog leash waist', 'Walk multiple dogs safely and keep your hands free for your phone and bags.', 'paw'],
    'poker-set'      => ['Casino Poker Chip & Card Set', 'casino poker chip set with cards', 'Practice dealing and chip handling at home before a dealer audition.', 'cards'],
    'snorkel-set'    => ['Snorkel Gear Set', 'snorkel set adult', 'Rent-out or tour-guide gear for visitors in beach and island towns.', 'wave'],
    'reef-sunscreen' => ['Reef-Safe Sunscreen', 'reef safe mineral sunscreen', 'Required in Hawaii and smart for anyone working outdoors all day.', 'sun'],
    'whiteboard'     => ['Desktop Whiteboard', 'desktop whiteboard easel', 'Makes online tutoring sessions clearer and more interactive.', 'pen'],

    // Planning & money
    'planner'        => ['Side Hustle Planner', 'business planner for entrepreneurs', 'Plan weekly hours, goals and income so your side hustle grows on purpose.', 'calendar'],
    'receipt-scanner'=> ['Portable Receipt Scanner', 'portable receipt scanner', 'Digitize receipts the day you get them — your tax preparer will thank you.', 'printer'],

    // Books
    'book-100-startup'    => ['The $100 Startup — Chris Guillebeau', 'The $100 Startup Chris Guillebeau', 'Real case studies of people who built income from small, cheap ideas.', 'book'],
    'book-side-hustle'    => ['Side Hustle: From Idea to Income in 27 Days', 'Side Hustle From Idea to Income in 27 Days Guillebeau', 'A day-by-day plan to launch a side hustle in under a month.', 'book'],
    'book-4-hour'         => ['The 4-Hour Workweek — Tim Ferriss', 'The 4-Hour Workweek Tim Ferriss', 'The classic on automation, outsourcing and buying back your time.', 'book'],
    'book-psych-money'    => ['The Psychology of Money — Morgan Housel', 'The Psychology of Money Morgan Housel', 'How to keep and grow the money your side hustle earns.', 'book'],
    'book-rich-dad'       => ['Rich Dad Poor Dad — Robert Kiyosaki', 'Rich Dad Poor Dad Robert Kiyosaki', 'The mindset shift from earning income to building assets.', 'book'],
    'book-profit-first'   => ['Profit First — Mike Michalowicz', 'Profit First Mike Michalowicz', 'A simple cash system that makes every side business profitable from day one.', 'book'],
    'book-company-of-one' => ['Company of One — Paul Jarvis', 'Company of One Paul Jarvis', 'Why staying small and solo can be the smartest business strategy.', 'book'],
    'book-this-is-mkt'    => ['This Is Marketing — Seth Godin', 'This Is Marketing Seth Godin', 'The best plain-English primer on marketing anything to anyone.', 'book'],
    'book-show-your-work' => ['Show Your Work! — Austin Kleon', 'Show Your Work Austin Kleon', 'How to get discovered by sharing what you make — ideal for creators.', 'book'],
    'book-dotcom'         => ['DotCom Secrets — Russell Brunson', 'DotCom Secrets Russell Brunson', 'Funnels and offers for anyone selling courses or digital products online.', 'book'],
    'book-taxes'          => ['J.K. Lasser\'s Small Business Taxes', 'J.K. Lasser Small Business Taxes', 'Deductions and rules every self-employed earner should know.', 'book'],
    'book-millionaire-nd' => ['The Millionaire Next Door', 'The Millionaire Next Door Stanley', 'What wealth actually looks like — and how ordinary earners build it.', 'book'],
];
