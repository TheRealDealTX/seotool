-- Reference data. Safe to re-run (INSERT IGNORE on unique slugs).

INSERT IGNORE INTO regions (slug, name, sort) VALUES
 ('panhandle-plains', 'Panhandle & Plains', 1),
 ('west-texas',       'West Texas & Big Bend', 2),
 ('north-texas',      'North Texas & Prairies', 3),
 ('east-texas',       'East Texas Piney Woods', 4),
 ('gulf-coast',       'Gulf Coast', 5),
 ('hill-country',     'Hill Country & Central Texas', 6),
 ('south-texas',      'South Texas & Rio Grande Valley', 7);

INSERT IGNORE INTO event_types (slug, name, sort) VALUES
 ('rodeo',            'Rodeo', 1),
 ('bull-riding',      'Bull riding', 2),
 ('roughstock',       'Bronc & roughstock', 3),
 ('barrel-racing',    'Barrel racing', 4),
 ('breakaway-roping', 'Breakaway roping', 5),
 ('steer-roping',     'Steer roping', 6),
 ('roping',           'Roping & timed events', 7),
 ('ranch-rodeo',      'Ranch rodeo', 8),
 ('finals',           'Finals & championships', 9),
 ('related',          'Related competition', 10);

INSERT IGNORE INTO associations (slug, abbr, name, level, website, sort) VALUES
 ('prca',  'PRCA',  'Professional Rodeo Cowboys Association', 'professional', 'https://www.prorodeo.com/', 1),
 ('wpra',  'WPRA',  'Women''s Professional Rodeo Association', 'professional', 'https://www.wpra.com/', 2),
 ('pbr',   'PBR',   'Professional Bull Riders', 'professional', 'https://pbr.com/', 3),
 ('ipra',  'IPRA',  'International Professional Rodeo Association', 'professional', 'https://www.ipra-rodeo.com/', 4),
 ('upra',  'UPRA',  'United Professional Rodeo Association', 'amateur', 'https://www.upra.org/', 5),
 ('cpra',  'CPRA',  'Cowboys Professional Rodeo Association', 'amateur', NULL, 6),
 ('acra',  'ACRA',  'American Cowboys Rodeo Association', 'amateur', NULL, 7),
 ('igra',  'IGRA',  'International Gay Rodeo Association', 'amateur', NULL, 8),
 ('wrca',  'WRCA',  'Working Ranch Cowboys Association', 'amateur', NULL, 9),
 ('thsra', 'THSRA', 'Texas High School Rodeo Association', 'high_school', 'https://www.thsra.org/', 10),
 ('tyra',  'TYRA',  'Texas Youth Rodeo Association', 'youth', NULL, 11),
 ('ajra',  'AJRA',  'American Junior Rodeo Association', 'youth', NULL, 12),
 ('nlbra', 'NLBRA', 'National Little Britches Rodeo Association', 'youth', 'https://www.nlbra.com/', 13),
 ('nira',  'NIRA',  'National Intercollegiate Rodeo Association', 'college', NULL, 14);
