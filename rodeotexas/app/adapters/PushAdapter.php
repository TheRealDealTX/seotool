<?php
declare(strict_types=1);

namespace RT\Adapters;

/**
 * Source whose records are delivered by the external weekly routine
 * (POST /api/import/) rather than fetched by this server — for example events
 * found by researching official organizer websites. The server never fetches
 * anything for it; see RT\Importer::runPushed().
 */
final class PushAdapter extends Adapter
{
    public static function describe(): string
    {
        return 'Pushed by the external weekly routine (POST /api/import/)';
    }

    public function fetch(): array
    {
        throw new \RuntimeException('Records for this source are pushed by the external routine; there is nothing to fetch here.');
    }
}
